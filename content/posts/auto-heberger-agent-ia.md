---
title: "Auto-héberger son agent IA : par où commencer (checklist souveraine)"
description: "Une feuille de route concrète pour lancer un agent IA sous son contrôle — sans dépendre d'un cloud tiers ni facturer chaque pensée."
date: 2026-08-09
draft: false
tags: ["Hermes Agent", "auto-hébergement", "souveraineté", "LM Studio", "tutoriel"]
categories: ["Tutoriel"]
cover:
  image: "images/auto-heberger-agent-ia.png"
---

Beaucoup d'assistants restent prisonniers d'un navigateur et d'un abonnement. Reprendre la main ne demande pas d'être ingénieur : quelques choix structurants suffisent. Voici la checklist que j'applique pour démarrer un agent **souverain** — celui qui tourne sur ma machine, avec mes données, et qui ne s'éteint pas si le cloud tombe.

## 1. Choisir une machine qui reste la sienne

Inutile d'un serveur distant pour commencer. Un **Mac Apple Silicon** (M1 et au-delà) ou n'importe quel poste avec 16 Go de RAM fait l'affaire pour un modèle local de 7 à 12 Go. La contrainte n'est pas la puissance, c'est la **mémoire unifiée** : tout ce qui dépasse ~12 Go de modèle déclenche du swap et l'expérience s'effondre.

> Règle d'or : un modèle de 7 Go + l'agent + le système ≈ 14-15 Go. Sur 16 Go, ça passe, mais gardez une marge pour le reste.

## 2. Prendre un agent qui sait se passer du cloud

L'agent doit pouvoir exécuter des tâches réelles — lire un fichier, lancer une commande, naviguer, planifier. C'est là que le **local-first** prend tout son sens : Hermes Agent, par exemple, se configure pour pointer vers un modèle qui réside sur votre machine via un provider `custom` (LM Studio, Ollama…). Le modèle par défaut devient le vôtre ; le cloud reste disponible pour les tâches ponctuelles.

## 3. Faire tourner le modèle en local

Deux options dominantes sur Mac :

- **LM Studio** — serveur compatible OpenAI sur `localhost:1234`. Idéal quand on veut un agent *fonctionnel* (avec outils), car les modèles récents (Gemma 4, Qwen 3.5) supportent l'appel d'outils à 16 Go.
- **Ollama** — plus léger à installer, mais les modèles conseillés pour 16 Go ne font pas d'appel d'outils. Parfait pour le chat pur, moins pour un agent autonome.

Pour un agent qui *fait* des choses, LM Studio + **Gemma 4 12B QAT** (≈ 7 Go) est mon point de départ.

## 4. Vérifier avant de publier

Une fois l'agent en place, trois réflexes :

- **Confidentialité** : aucune donnée sensible ne quitte la machine (sauf si vous le demandez).
- **Coût** : l'inférence est à coût marginal nul une fois le matériel payé.
- **Résilience** : l'agent répond même sans réseau.

## 5. Publier ses résultats, souverainement

Le site que vous lisez est lui-même un exemple : généré en local (Hugo), versionné sur Git, déployé automatiquement à chaque `git push`. Pas d'éditeur tiers, pas de dépendance cachée. Le même principe s'applique à l'agent : maîtrisez la chaîne, de la génération à la diffusion.

---

**En résumé** : une machine à soi, un agent qui sait s'en passer du cloud, un modèle local fonctionnel, et une chaîne de publication maîtrisée. La souveraineté n'est pas un luxe de geek — c'est un choix d'architecture.
