---
title: "Quel backend LLM local pour Hermes sur Mac M4 : LM Studio vs Ollama vs MLX (benchmarks réels)"
date: 2026-08-15
draft: false
tags: ["hermes-agent", "souveraineté", "ollama", "lm-studio", "mlx", "benchmark", "m4", "llama"]
cover:
  image: "images/backend-llm-local-m4-comparatif.png"
---

## Résumé

On partait d'un problème : Ollama qui « hallucine complètement ». Après avoir
mesuré trois backends locaux (LM Studio, Ollama, MLX) sur un Mac M4 17 Go avec
Hermes Agent, le verdict est clair : **Ollama + `llama3.1:8b` est le meilleur
choix local**. Ce qui causait l'hallucination n'était pas Ollama, mais le
mauvais modèle qu'on lui donnait.

## Le piège de l'hallucination

Ollama n'hallucine pas « tout seul ». Il exécute le modèle qu'on lui donne. Les
causes d'hallucination avec Hermes :

1. **Mauvais modèle** : trop petit (`llama3.2:1b`, `qwen2.5:0.5b`) ou base
   non-instruct → réponses absurdes.
2. **Modèle reasoning** (Qwen3, Gemma2 thinking) → sortie vide dans Hermes.
3. **Contexte trop court** par défaut → le modèle oublie et invente.

Le remède : un modèle **instruct, non-reasoning, 8B+** — exactement
`llama3.1:8b`.

## Méthodologie

Pour chaque backend, sur le même Mac M4 17 Go :

1. **Inférence** : sortie propre ou vide ?
2. **Tool-calling** : `tool_calls` structuré (indispensable pour un agent) ?
3. **Contexte réel** : 1K → 64K tokens, seuil de rupture ?
4. **Vitesse** : temps de réponse mesuré.

Tests via API (`/v1/chat/completions`) et CLI Hermes réel.

## Résultats mesurés

| Backend | Modèle | Inférence | Tool-calling | Contexte réel | Vitesse |
|---|---|---|---|---|---|
| **LM Studio** | hermes-3-llama-3.1-8b | ✅ | ✅ standard | 8K (refuse 16K) | ~22s |
| **Ollama** | llama3.1:8b | ✅ | ✅ standard | **32K** | 21-111s |
| **MLX** | Llama-3.1-8B-4bit | ✅ | ⚠️ format `<|python_tag|>` | 8K (32K timeout) | 200s (lent) |

### Détail

**LM Studio** : tool-calling OK, mais RoPE scaling absent → contexte bloqué à
8K natif. Refuse 16K+ (HTTP 400).

**Ollama** : applique le RoPE scaling → **tient 32K réellement** (3x LM
Studio). Tool-calling standard, inférence propre. C'est le gagnant.

**MLX** : utilise le GPU Apple M4 (`applegpu_g16g`), mais le quant 4bit est
**lent** (200s pour une réponse courte, timeout à 32K). Le tool-calling sort
dans un format non-standard (`<|python_tag|>`) que Hermes ne parse pas. Malgré
l'optimisation M4, le quant 4bit + template Llama posent problème.

## Pourquoi Ollama gagne

- ✅ **Contexte 32K réel** (LM Studio plafonne à 8K)
- ✅ **Tool-calling standard** (agent opérationnel)
- ✅ **Inférence propre** (non-reasoning)
- ✅ ~4.7 Go RAM (coexiste avec ComfyUI)
- ✅ 100% local (souveraineté préservée)

MLX aurait dû être le plus rapide (GPU M4 natif), mais le quant 4bit + template
cassé le rend plus lent et moins fiable que Ollama.

## Configuration retenue

```yaml
# ~/.hermes/config.yaml
model:
  default: llama3.1:8b
  provider: ollama
  context_length: 32768   # realiste (64K declaratif depasse les capacites M4)
```

Alias utiles (`~/.zshrc`) :

```bash
alias hermes-ollama='hermes chat --provider ollama -m llama3.1:8b'
alias hermes-local='hermes chat --provider lmstudio -m hermes-3-llama-3.1-8b'
```

L'app Desktop Hermes reste sur le cloud Nous Portal (dualité souveraine).

## L'install MLX (pour mémoire)

MLX demande un venv isolé (`env -u PYTHONPATH` obligatoire pour ne pas
contaminer l'env Hermes) et un jumelage de versions précis :
`mlx-lm==0.21.3` + `transformers==4.44.2`. Sans ça, crash
`BatchEncoding` au tokenizer. Serveur : `mlx_lm.server --port 8080`.

## Conclusion

La souveraineté numérique exige de **mesurer**, pas d'affirmer. Sur M4 17 Go,
**Ollama + llama3.1:8b** est le backend local le plus fiable pour Hermes : 32K
de contexte réel, tool-calling fonctionnel, zéro hallucination (avec le bon
modèle). L'hallucination de départ n'était pas un bug Ollama — c'était un
mauvais modèle.

L'infrastructure Fabrica Miracula est désormais documentée de bout en bout :
audit de souveraineté, config duale, benchmark LLM, vérité du contexte 64K, et
choix du backend local.
