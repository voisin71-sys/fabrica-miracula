---
title: "Benchmark LLM local pour Hermes Agent : Qwen2.5-Coder-14B vs 7B vs Llama-3.1-8B"
date: 2026-08-15
draft: false
tags: ["hermes-agent", "souveraineté", "lm-studio", "benchmark", "qwen", "llama", "gemma"]
cover:
  image: "images/benchmark-llm-local-hermes.png"
---

Quel est le meilleur LLM local pour faire tourner Hermes Agent en souveraineté totale ? Nous avons mesuré trois modèles chargés sur un Mac M4 (17 Go de RAM) via LM Studio : le plus puissant (Qwen2.5-Coder-14B), le compromis (Qwen2.5-7B), et la référence (Llama-3.1-8B). Résultats réels, pas de théorie.

## La contrainte Hermes

Hermes Agent n'est pas un simple chatbot : c'est un agent à outils (tool-calling), avec une **exigence de contexte minimale de 64 000 tokens**. Trois critères décisifs :

1. **Sortie propre** : pas de « reasoning » qui pollue le flux (Hermes attend du texte direct).
2. **Tool-calling fiable** : génération d'appels d'outils structurés.
3. **Contexte ≥ 64K** : le modèle doit accepter la fenêtre étendue (RoPE scaling).

Nous avons écarté d'emblée **Gemma 4** et **Qwen 3.5** : leurs comportements de reasoning renvoient du vide (`finish: length`, contenu vide) — incompatibles avec Hermes. Seuls les modèles **non-reasoning** restent.

## Les candidats testés

| Modèle | Taille | Type | RAM (LM Studio) |
|---|---|---|---|
| `qwen2.5-coder-14b-instruct` | 14B (Q4_K_M) | non-reasoning, coder | ~13.4 Go |
| `qwen2.5-7b-instruct` | 7B (Q4_K_S) | non-reasoning | ~8 Go |
| `hermes-3-llama-3.1-8b` | 8B | non-reasoning | ~8.5 Go |

## Méthodologie

Chaque modèle a été soumis à trois épreuves via l'API OpenAI de LM Studio (`localhost:1234`) :
- **Test 1** : réponse simple (expliquer la souveraineté numérique en 2 phrases).
- **Test 2** : tool-calling (`get_weather("Paris")`).
- **Test 3** : instruction complexe (plan de 3 points pour sécuriser un Mac).

Le contexte a été forcé à 64K via `model.context_length: 65536` dans `config.yaml`.

## Résultats

### Test 1 — Réponse simple (non-vide exigé)

| Modèle | Temps | Sortie |
|---|---|---|
| Qwen2.5-Coder-14B | 47.6 s | ✅ propre |
| Qwen2.5-7B | 20.5 s | ✅ propre |
| Llama-3.1-8B | 23.9 s | ✅ propre |

Les trois répondent correctement. Le 14B est 2× plus lent.

### Test 2 — Tool-calling

| Modèle | Résultat | Note |
|---|---|---|
| Qwen2.5-Coder-14B | `tool=True` (outil dans le texte, `finish: stop`) | ⚠️ format non structuré |
| Qwen2.5-7B | `tool_calls` structuré, 16.1 s | ✅ |
| Llama-3.1-8B | `tool_calls` structuré, 22.8 s | ✅ |

Tous déclenchent l'outil. Le 14B renvoie l'appel dans le texte plutôt qu'en `tool_calls` JSON — Hermes le parse généralement, mais c'est à surveiller en conditions réelles.

### Test 3 — Instruction complexe (qualité)

| Modèle | Temps | Qualité |
|---|---|---|
| **Qwen2.5-Coder-14B** | 64.1 s | ✅ **meilleure**, plan complet et structuré |
| Qwen2.5-7B | 38.5 s | ⚠️ tronqué (`length`) |
| Llama-3.1-8B | 44.0 s | ⚠️ tronqué (`length`) |

Ici le 14B montre sa supériorité : il produit un plan détaillé et complet, là où les modèles plus petits s'arrêtent par manque de contexte.

### Empreinte mémoire

LM Studio consomme **13.4 Go** avec le 14B chargé (sur 17.2 Go) — il ne reste que **3.8 Go** libres. Avec ComfyUI en parallèle (génération d'images, ~4-6 Go), le système entre en swap. Les modèles 7B/8B (~8 Go) gardent ~9 Go libres : **confortables pour un workflow souverain complet** (agent + images).

## Verdict

| Critère | Gagnant |
|---|---|
| Qualité brute | **Qwen2.5-Coder-14B** |
| Vitesse | Qwen2.5-7B / Llama-3.1-8B |
| Économie RAM (M4 + ComfyUI) | Qwen2.5-7B |
| Compatibilité Hermes (non-reasoning) | Qwen2.5 (les deux) |

**Le plus performant** est sans conteste Qwen2.5-Coder-14B — mais au prix d'une lenteur doublée et d'une empreinte mémoire qui interdit le parallélisme avec ComfyUI.

**Le meilleur compromis** pour une session Hermes locale quotidienne (rédaction + publication illustrée) est **Qwen2.5-7B-Instruct** : non-reasoning, tool-calling OK, 64K OK, léger (8 Go), qualité largement suffisante. C'est précisément le modèle retenu par défaut (`model.default` dans `config.yaml`).

Llama-3.1-8B, bien que fonctionnel, est désormais dépassé par les Qwen2.5 (même taille, meilleure qualité).

## Recommandation pratique

- **Par défaut** : `qwen2.5-7b-instruct` (alias `hermes-local`) — équilibré pour M4 17 Go + ComfyUI.
- **Puissance ponctuelle** : charger `qwen2.5-coder-14b-instruct` et lancer une session dédiée (`hermes chat -m qwen2.5-coder-14b-instruct`) quand ComfyUI est éteint.
- **À éviter pour Hermes** : Gemma 4, Qwen 3.5 (reasoning → sortie vide).

La souveraineté numérique, c'est aussi choisir son modèle en connaissance de cause — mesuré, pas supposé.
