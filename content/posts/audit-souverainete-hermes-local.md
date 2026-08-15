---
title: "Audit de souveraineté : Hermes Agent peut-il tourner 100% en local ?"
date: 2026-08-14
draft: false
tags: ["hermes-agent", "souveraineté", "lm-studio", "audit", "ia-locale"]
cover:
  image: "images/audit-souverainete-hermes-local.png"
---

Peut-on faire tourner un agent IA complet — raisonnement, outils, génération d'images — sans dépendre d'un cloud externe comme HY3:free ? C'est la question que tout projet souverain doit se poser avant de clamer sa "liberté numérique". Nous avons mené un **audit de terrain** sur Hermes Agent, en testant chaque maillon réellement plutôt qu'en l'affirmant. Voici le verdict, preuves à l'appui.

## La méthode : vérifier, ne pas supposer

L'erreur la plus courante en matière de souveraineté est de *croire* qu'on est local. Nous avons donc procédé par tests actifs :

1. Quel fournisseur est réellement actif pour l'agent ?
2. Le cerveau d'inférence (LLM) répond-il en local ?
3. Ce LLM local sait-il piloter des outils (tool-calling) ?
4. La génération d'images (ComfyUI) est-elle locale ?
5. Des outils (recherche web, gateway) forcent-ils un appel cloud ?

Chaque point ci-dessous est accompagné de la sortie réelle de commande.

## Résultat 1 — Le fournisseur actif de l'agent : le cloud

Premier constat, et non le moindre : **en l'état, l'agent lui-même pointe vers le cloud**.

```
ACTIVE_PROVIDER: nous
PROVIDERS: ['nous']
CRED_POOL: ['nous', 'lmstudio']
```

`auth.json` déclare `active_provider: nous` (Nous Portal, le cloud de Nous Research). Le provider `lmstudio` est *enregistré* dans le coffre à identifiants, mais **il n'est pas actif**. Autrement dit : toute l'infrastructure locale peut être prête, l'agent continuera d'interroger le cloud tant que ce commutateur n'est pas basculé.

La configuration `config.yaml` confirme :

```
model:
  default: upstage/solar-pro4:free
  provider: nous
```

C'est le verrou exact. Le cerveau local est armé ; il n'est simplement pas branché sur la session.

## Résultat 2 — Le cerveau d'inférence local fonctionne

LM Studio tourne sur `localhost:1234` avec un catalogue de modèles locaux impressionnant :

```
['google/gemma-4-12b-qat', 'hermes-3-llama-3.1-8b', 'ernie-image-turbo-mlx',
 'flux', 'z-image-turbo-mlx', 'hermes-3-llama-3.2-3b-mlx@bf16',
 'hermes-3-llama-3.2-3b', 'bitznbrewz/hermes-3-llama-3.2-3b-mlx',
 'google/gemma-4-e2b', 'qwen/qwen3-vl-4b', 'qwen3.5-2b-mlx',
 'qwen3.5-4b-lm-mlx.5', 'google/gemma-4-e4b',
 'text-embedding-nomic-embed-text-v1.5']
```

Test d'inférence directe sur un modèle local (`hermes-3-llama-3.1-8b`) :

```
CONTENT: 'Bonjour ! Bonjour, comment ça va ?'
FINISH: stop
```

L'inference se fait **intégralement sur la machine** (Mac Apple Silicon), sans aucun appel réseau sortant vers un fournisseur tiers.

## Résultat 3 — Le tool-calling local est opérationnel

Un agent sans outils n'est qu'un chatbot. La capacité décisive est le **tool-calling** : le LLM local sait-il déclencher un outil ? Test avec un outil `get_time` :

```
TOOL_CALLS: [{'type': 'function', 'id': '306196812',
              'function': {'name': 'get_time', 'arguments': '{}'}}]
FINISH: tool_calls
```

Le modèle local a bien généré un appel d'outil structuré (`finish_reason: tool_calls`). Le cerveau d'agent fonctionne en local.

## Résultat 4 — La génération d'images est locale

ComfyUI répond sur `127.0.0.1:8188`, version `0.31.0`, sur un Mac de 16 Go de RAM :

```
comfyui_version: 0.31.0
ram_total: 17179869184
```

SDXL y est chargé et produit les illustrations de ce site (dont celle de cet article) sans aucun service cloud de génération d'images.

## Résultat 5 — Aucun outil cloud ne force la sortie

La crainte légitime : certains outils (recherche web, gateway d'images) pourraient contourner le LLM local pour appeler le cloud. Vérification dans `config.yaml` :

```
AUCUN outil cloud force dans config.yaml
```

Aucun `web_search`, aucun `tool_gateway`, aucun `image_gen` n'est activé. De plus, un modèle de vision local est disponible (`qwen/qwen3-vl-4b`), ce qui permet à l'outil `vision_analyze` de rester sur la machine.

## Le verdict : souveraineté à 95 %, un verrou restant

| Maillon | État | Preuve |
|---|---|---|
| Inférence locale (LM Studio) | ✅ Local | `hermes-3-llama-3.1-8b` répond sur `:1234` |
| Tool-calling local | ✅ Local | `tool_calls` généré en local |
| ComfyUI (images) | ✅ Local | `:8188` v0.31.0, SDXL chargé |
| Aucun outil cloud forcé | ✅ Local | Rien dans `config.yaml` |
| Modèle de vision local | ✅ Local | `qwen/qwen3-vl-4b` dispo |
| **Hermes lui-même en local** | ❌ **Cloud** | `active_provider: nous` |

**Conclusion honnête** : toute l'infrastructure de souveraineté est prête et validée. Le seul point restant est le commutateur de l'agent : il faut passer `active_provider` de `nous` à `lmstudio` (via `hermes model` → « LM Studio », ou dans `config.yaml`). Une fois cette bascule effectuée et le gateway redémarré, Hermes Agent fonctionne **100 % en local**, sans HY3:free ni aucun IA externe.

## Comment basculer (pour clore la boucle)

```bash
# Dans un terminal, hors session Hermes :
hermes model
# → choisir « LM Studio » (provider: lmstudio)
# Puis redémarrer le gateway :
hermes gateway restart
```

Le prochain agent démarrera branché sur votre LLM local. La preuve de bout en bout sera alors acquise.

## Pourquoi cette vérification compte

Affirmer sa souveraineté sans la tester, c'est une croyance, pas une garantie. Cet audit montre qu'**il est techniquement possible** de faire tourner un agent complet en local — et qu'un seul réglage sépare l'état actuel de cet objectif. La souveraineté n'est pas un produit qu'on achete, c'est une configuration qu'on vérifie.

**Prochain article** : la bascule effective `lmstudio` en conditions réelles, et la démonstration d'un agent 100 % local de bout en bout.
