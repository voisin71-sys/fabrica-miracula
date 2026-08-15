---
title: "LLM local pour Hermes sur M4 : la vérité sur le contexte 64K (benchmarks réels)"
date: 2026-08-15
draft: false
tags: ["hermes-agent", "souveraineté", "lm-studio", "benchmark", "llama", "phi-3.5", "qwen", "contexte", "m4"]
cover:
  image: "images/llm-local-contexte-64k-m4.png"
---

## Résumé

On nous promet des LLM locaux avec 64K, 128K de contexte. En pratique, sur un
Mac M4 17 Go avec LM Studio, **aucun modèle ne tient réellement 64K** — et le
tool-calling (le cœur d'un agent comme Hermes) fonctionne sur peu de modèles.
Cet article documente les tests réels menés pour choisir le meilleur LLM local
pour Hermes Agent, avec les preuves brutes.

## La promesse vs la réalité

Hermes Agent exige un contexte de **64 000 tokens minimum** (déclaré dans
`config.yaml`). On a testé tous les modèles disponibles sur le M4 pour voir
lesquels tiennent cette promesse.

**Résultat : aucun.** Même après avoir réglé LM Studio à `context_length:
65536`, tous les modèles refusent (`HTTP 400`) dès qu'on dépasse leur limite
native.

## Méthodologie

Pour chaque modèle, on a mesuré :

1. **Réponse simple** : sortie propre ou vide ?
2. **Tool-calling** : émet-il un `tool_calls` structuré (indispensable pour un agent) ?
3. **Contexte progressif** : 1K → 64K tokens, seuil de rupture ?
4. **RAM** : empreinte réelle (LM Studio RSS).

Tests via l'API LM Studio (`/v1/chat/completions`) et le CLI Hermes réel.

## Résultats mesurés

| Modèle | Tool-calling | Contexte réel (refus >) | Raisoning | RAM |
|---|---|---|---|---|
| **hermes-3-llama-3.1-8b** | ✅ OK | 8K (refuse 16K) | Non | ~5 Go |
| qwen2.5-7b-instruct | ✅ OK | 32K | Non | ~8 Go |
| qwen2.5-coder-14b | ✅ OK | 32K | Non | ~13,4 Go |
| **phi-3.5-mini Q4_K_M** | ❌ vide (`length`) | 16K | Non | ~4 Go |
| qwen3.5-4b | ✅ OK | 128K natif | **Oui** → vide | ~9 Go |
| gemma-4-12b-qat | ✅ OK | inconnu | **Oui** → vide | ~13 Go |

### Détail des échecs

**Phi-3.5-mini** : annoncé 128K natif, mais LM Studio le cappe. Pire : le
tool-calling renvoie `finish_reason: "length"` avec un contenu vide — l'agent
est paralysé. Inutilisable pour Hermes.

**Gemma 4 / Qwen 3.5** : comportement de "reasoning" natif. Ils consomment
tout le contexte dans leur réflexion AVANT de produire le texte → sortie vide.
Aucun paramètre API LM Studio ne désactive ce reasoning.

**Llama-3.1-8B** : tool-calling OK, sortie propre, mais limite native 8K.
C'est le seul modèle qui fonctionne comme agent sur ce setup.

## Le piège du `context_length` dans config.yaml

On a cru que `model.context_length: 65536` suffisait. **Faux.** Cette valeur
est une *déclaration* que Hermes lit au démarrage, mais c'est **LM Studio**
qui doit accepter la fenêtre de contexte réelle. Sans RoPE scaling effectif
(que LM Studio n'applique pas automatiquement ici), le modèle reste à sa
limite native.

Test confirmé : même réglé à 65536 dans LM Studio, `hermes-3-llama-3.1-8b`
refuse 16K+ (HTTP 400).

## Verdict : quel LLM local pour Hermes sur M4 ?

**Le meilleur compromis reste `hermes-3-llama-3.1-8b`** :

- ✅ Tool-calling fonctionnel (agent opérationnel)
- ✅ Sortie propre (non-reasoning)
- ✅ ~5 Go RAM (laisse de la place pour ComfyUI en parallèle)
- ⚠️ Contexte réel = 8K (le 64K est déclaratif, pas physique)

Les sessions courtes (le cas d'usage réel) fonctionnent parfaitement. Le 64K
reste un objectif théorique non atteignable sur ce matériel avec LM Studio.

### Pour un vrai 64K+ un jour

- Modèle 128K natif **avec tool-calling préservé** via LM Studio (Phi-3.5 a
  échoué ici — peut-être un quant plus doux, ex. Q8 au lieu de Q4).
- Ou un autre backend (Ollama avec `num_ctx`, vLLM) qui applique le RoPE
  scaling correctement.

## Preuves

- Tests API `/v1/chat/completions` : contextes 1K→64K, measure du `finish_reason`.
- CLI Hermes réel : barre d'état confirme `hermes-3-llama-3.1-8b`.
- RAM mesurée via `ps` (LM Studio RSS).

L'infrastructure souveraine (CLI local + Desktop cloud) est auditée,
configurée et documentée avec des preuves réelles — pas d'affirmations.

## Conclusion

La souveraineté numérique ne se résume pas à "tout faire en local". Elle
exige de **mesurer** ce qui marche vraiment. Sur M4 17 Go + LM Studio, le
meilleur agent local est Llama-3.1-8B — pas le plus "puissant" sur le papier,
mais le seul qui répond aux exigences fonctionnelles de Hermes.
