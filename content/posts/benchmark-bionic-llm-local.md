---
title: "Benchmark de ma bibliothèque LLM locale (BIONIC) sur Mac M4 : 5 modèles testés via Ollama"
date: 2026-08-15
draft: false
tags: ["hermes-agent", "souveraineté", "ollama", "benchmark", "gemma", "llama", "qwen", "phi", "m4", "bionic"]
cover:
  image: "images/benchmark-bionic-llm-local.png"
---

## Résumé

On a testé **5 modèles de ma bibliothèque locale** (`/Volumes/DATA_CENTER/BIONIC LLM MODELS`)
directement dans Ollama sur un Mac M4 17 Go, sans aucun téléchargement réseau.
Résultat : **Gemma 4 4B est le plus rapide** (0.6s), **Llama 3.1 8B le plus
polyvalent** (contexte 16K). Tous deux sont 100% souverains.

## Pourquoi tester sa propre bibliothèque

Les modèles ne viennent pas que d'Ollama Hub. Ma bibliothèque BIONIC contient
des GGUF locaux (Qwen, Phi, Gemma, Llama) que j'utilise sans dépendre du
réseau. Ollama permet de les charger via un **Modelfile** :

```
FROM /Volumes/DATA_CENTER/BIONIC LLM MODELS/lmstudio-community/gemma-4-E4B-it-GGUF/gemma-4-E4B-it-Q4_K_M.gguf
```

Puis `ollama create <nom> -f Modelfile`. **Zéro téléchargement** = souveraineté
totale.

## Méthodologie

Même Mac M4 17 Go, Ollama comme backend (il gère le RoPE scaling et le
tool-calling proprement — contrairement à LM Studio qui renvoyait du vide sur
les modèles reasoning). Pour chaque modèle :

1. **Inférence** : sortie propre ou vide ?
2. **Tool-calling** : `tool_calls` structuré (indispensable pour Hermes) ?
3. **Contexte** : 8K / 16K, seuil de rupture ?
4. **Vitesse** : temps de réponse mesuré.

## Résultats mesurés

| Modèle (source BIONIC) | Inférence | Tool-calling | Contexte | Vitesse | RAM |
|---|---|---|---|---|---|
| **llama3.1:8b** (Ollama pull) | ✅ | ✅ | **16K+** | 4.3s | 4.9 Go |
| **gemma4-4b-local** (E4B GGUF Q4_K_M) | ✅ | ✅ | 8K | **0.6s** | 5.3 Go |
| qwen25-7b-local (bartowski Q4_K_S) | ✅ | ✅ | 8K | 3.3s | 4.5 Go |
| gemma4-local 12B (QAT Q4_0) | ✅ | ✅ | 8K | 72.7s | 7.0 Go |
| phi35-local (Q4_K_M) | ✅ | ❌ vide | refuse | 2.0s | 2.4 Go |

### Détail par modèle

**Llama 3.1 8B** : le seul à tenir 16K de contexte. Tool-calling standard,
inférence propre, rapide. Le plus polyvalent.

**Gemma 4 4B** : **la révélation du bench**. 0.6s de réponse (120x plus rapide
que le 12B !), tool-calling OK, qualité Gemma. Plafonne à 8K de contexte, mais
pour une session interactive c'est imbattable.

**Qwen 2.5 7B** : bon compromis (tool-calling OK, léger 4.5 Go), mais contexte
8K seulement via Ollama.

**Gemma 4 12B** : qualité supérieure mais **72.7s par réponse** sur M4 sans VRAM
dédiée. Inutilisable en interactif, sauf pour des tâches batch patience.

**Phi 3.5** : inférence OK mais tool-calling cassé (HTTP 400, format non
reconnu). Inutilisable comme agent.

### Note sur LM Studio vs Ollama
Testé plus tôt : LM Studio renvoyait du **vide** sur Gemma 4 (reasoning non
géré). Ollama gère le reasoning correctement → Gemma 4 fonctionne. Le backend
fait toute la différence.

## Verdict : quel modèle pour Hermes ?

- **Session interactive rapide** → **Gemma 4 4B** (0.6s, tool-calling OK)
- **Contexte long (16K+)** → **Llama 3.1 8B**
- **Léger/économique** → Qwen 2.5 7B
- **À éviter** → Phi 3.5 (tool-calling cassé), Gemma 4 12B (trop lent)

## Configuration retenue

```bash
# llama3.1:8b = defaut Hermes (16K, polyvalent)
alias hermes-local='hermes chat --provider ollama -m llama3.1:8b'
# gemma4-4b = option ultra-rapide
alias hermes-gemma4b='hermes chat --provider ollama -m gemma4-4b-local'
```

L'app Desktop Hermes reste sur le cloud Nous Portal (dualité souveraine).

## Conclusion

Ma bibliothèque BIONIC, chargée localement dans Ollama, couvre tous les cas
d'usage Hermes sans un octet réseau. **Gemma 4 4B** surprend par sa vitesse ;
**Llama 3.1 8B** reste le plus sûr (16K). La souveraineté, c'est mesurer — pas
croire les specs papier.
