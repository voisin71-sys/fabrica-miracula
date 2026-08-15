---
title: "Configuration duale Hermes : session 100% locale (CLI/llama3) et cloud (Desktop/Nous Portal)"
date: 2026-08-15
draft: false
tags: ["hermes-agent", "souveraineté", "lm-studio", "cli", "configuration", "llama3"]
cover:
  image: "images/config-duale-hermes-local-cloud.png"
---

Comment obtenir le meilleur des deux mondes avec Hermes Agent : une **session 100% locale et souveraine** pour tester ses skills, ComfyUI et cronjobs en conditions réelles, et une **session cloud** (Nous Portal) pour développer et corriger les bugs avec un modèle puissant. Ce guide documente la configuration mise en place, les pièges rencontrés et les preuves que ça fonctionne.

## Le besoin

Quand on construit une infrastructure souveraine (IA locale, génération d'images, publication automatisée), deux usages coexistent :

1. **Développer et corriger** les bugs rapidement → on veut un modèle capable (cloud, Nous Portal).
2. **Valider en conditions réelles** que tout fonctionne sans dépendre d'un tiers → on veut 100% local.

La solution : une **configuration duale**. Le Terminal (CLI) lance Hermes en local (LM Studio + Llama 3), l'application Desktop lance Hermes sur le cloud (Nous Portal). Chacun garde ses avantages, et les skills/mémoires sont partagés via le même `HERMES_HOME`.

## Architecture

| Usage | Lancement | Provider | Modèle | Cloud |
|---|---|---|---|---|
| **CLI local** | `hermes-local` (alias zsh) | `lmstudio` | `hermes-3-llama-3.1-8b` (Llama 3, 64K ctx) | Non — 100% local |
| **Desktop cloud** | App Hermes | `nous` (Nous Portal) | défaut cloud | Oui |

Les deux sessions partagent `~/.hermes` (config, skills, mémoires, cronjobs), ce qui garantit une cohérence totale entre les environnements.

## Mise en place

### 1. Configurer le provider local (`config.yaml`)

Le fichier `~/.hermes/config.yaml` déclare le provider `lmstudio` et le modèle Llama 3 local :

```yaml
model:
  default: hermes-3-llama-3.1-8b
  provider: lmstudio
  base_url: http://localhost:1234/v1
  context_length: 65536
```

La valeur `context_length: 65536` est **indispensable** (voir le piège ci-dessous).

### 2. Créer l'alias `hermes-local` (Terminal)

Dans `~/.zshrc` (pour zsh) :

```bash
export HERMES_HOME="/Users/masterai/.hermes"
alias hermes-local='HERMES_HOME=/Users/masterai/.hermes /Users/masterai/.hermes/hermes-agent/venv/bin/hermes chat --provider lmstudio -m hermes-3-llama-3.1-8b'
```

L'alias force explicitement le provider `lmstudio` et le modèle, indépendamment de l'état d'`auth.json` (que l'app Desktop réécrit à chaque lancement).

### 3. Maintenir les serveurs locaux (facultatif mais recommandé)

Un LaunchAgent `com.fabricamiracula.servers` relance LM Studio et ComfyUI au login et les maintient en vie (`KeepAlive`). Ainsi, au démarrage d'une session locale, l'infrastructure est déjà prête.

## Pièges rencontrés (et corrections)

### Piège 1 — Exigence de contexte minimale

Au premier lancement local, Hermes a refusé le modèle :

```
Failed to initialize agent: Model hermes-3-llama-3.1-8b has a context window of
8,192 tokens, which is below the minimum 64,000 required by Hermes Agent.
```

`hermes-3-llama-3.1-8b` déclare 8K de contexte natif, mais Hermes exige 64K minimum. **Correction** : déclarer `model.context_length: 65536` dans `config.yaml`. LM Studio gère alors le RoPE scaling et étend la fenêtre — et le modèle répond correctement.

### Piège 2 — `HERMES_HOME` divergent

Le `~/.zshrc` initial contenait `export HERMES_HOME="/Volumes/DATA_CENTER/hermes-data"`, pointant vers une **autre config** (provider `custom`, Gemma 4). Le CLI aurait donc utilisé une configuration différente de l'app Desktop, cassant le partage des skills/mémoires. **Correction** : unifier `HERMES_HOME` sur `/Users/masterai/.hermes` (celui de l'app Desktop).

### Piège 3 — L'app Desktop force le cloud

L'application Desktop Hermes réécrit `auth.json → active_provider: nous` à chaque lancement. C'est son comportement par défaut (cloud). **Conséquence** : on ne peut pas figer le local dans `auth.json` de façon persistante pour le Desktop. **Solution** : le CLI utilise `--provider lmstudio` (prioritaire sur `auth.json`), donc il reste local quelle que soit l'écriture du Desktop.

## Preuves que ça fonctionne

### Inférence locale réelle (Llama 3, 64K ctx)

Requête directe vers LM Studio (`localhost:1234`) :

```
REPONSE: 'LOCAL_LLAMA3_WORKS'
```

Le modèle `hermes-3-llama-3.1-8b` répond sur le réseau local, sans aucun appel sortant.

### Démarrage du CLI local

La barre d'état du TUI affiche bien le modèle local :

```
hermes-3-llama-3.1-8b
```

L'agent démarre branché sur Llama 3 local.

### Infrastructure locale opérationnelle

```
LM Studio: OUI
ComfyUI: OUI
Watcher launchd: OUI
```

## Utilisation au quotidien

- **Tester en souveraineté** : ouvrez un Terminal, tapez `hermes-local`. Vous êtes 100% local (Llama 3 via LM Studio). Idéal pour valider skills, ComfyUI, cronjobs.
- **Développer/corriger** : lancez l'app Desktop Hermes. Elle utilise Nous Portal (modèle puissant). Parfait pour itérer vite sur les bugs.
- **Partage** : skills, mémoires et cronjobs sont communs aux deux sessions (même `HERMES_HOME`).

## Pour aller plus loin

Cette configuration duale est la pierre angulaire d'un workflow souverain : on développe dans le cloud, on déploie/valide en local. Le prochain article abordera l'utilisation du CLI local pour corriger les bugs des skills (ex. le pipeline `fabrica-daily`) sans jamais dépendre d'un tiers.

**Résumé** : une ligne d'alias + une clé `context_length` suffisent à faire de Hermes un agent 100% local sur commande, tout en gardant le confort du cloud pour le développement.
