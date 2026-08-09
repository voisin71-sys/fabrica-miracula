---
title: "Ma configuration Hermes Agent en 2026 : pourquoi ce stack est le plus pertinent"
description: "Tour d'horizon de mon setup actuel — Mac Apple Silicon, Hermes Agent, LM Studio local, Hugo — et les raisons qui le rendent souverain."
date: 2026-08-09
draft: false
tags: ["configuration", "Hermes Agent", "LM Studio", "souveraineté", "Apple Silicon"]
categories: ["Réflexion"]
---

Beaucoup se contentent d'un assistant dans le navigateur. Moi, je voulais un
**atelier** : des outils qui reste sous mon contrôle, qui fonctionnent même si
le cloud tombe, et qui ne facturent pas chaque pensée. Voici la configuration
qui, en 2026, me semble la plus pertinente — et pourquoi.

## Les composants de mon setup

- **Machine** : Mac Apple Silicon sous macOS 26.5.2. Silencieux, puissant, et
  capable de faire tourner des modèles localement.
- **Hermes Agent** : utilisé à la fois depuis le **bureau** et **Telegram**
  (où certaines compétences comme ComfyUI s'activent automatiquement).
- **LM Studio en local** (provider `lmstudio`) : mes modèles de langage
  résident sur ma machine. **Gemma 4 12B** pour les tâches de recherche et de
  raisonnement profond ; des modèles **plus légers** pour les tâches rapides.
- **ComfyUI local** (`127.0.0.1:8188`) : génération d'images en local, sans
  envoyer mes prompts à un service tiers.
- **Site Hugo + GitHub Pages** : hébergement statique, gratuit, portable.
- **Clé SSH dédiée** pour les dépôts GitHub (isolée, sans phrase de passe pour
  l'automatisation des déploiements).
- **Réseaux ciblés** : X, Facebook, Instagram (distribution prévue par API).

## Pourquoi c'est le plus pertinent

### 1. La souveraineté avant tout
Mes données de raisonnement ne quittent pas mon réseau local. LM Studio et
ComfyUI tournent *sur ma machine*. Le site, lui, est un fichier statique —
personne ne peut le modifier sans passer par mon dépôt Git.

### 2. Le coût maîtrisé
GitHub Pages est gratuit pour un site public. Les modèles locaux ne coûtent
rien à l'usage une fois installés. Je ne paie pas à la requête.

### 3. La confidentialité par défaut
Rien de ce que j'écris ou génère n'est envoyé à un fournisseur cloud pour
« améliorer le service ». Le local est le défaut, pas l'option.

### 4. La résilience
Si un service en ligne tombe, mon atelier continue. Hugo rebuild en quelques
dizaines de millisecondes ; le déploiement est reproductible à l'identique.

### 5. La portabilité
Tout est décrit dans des fichiers texte (configuration, contenu, workflow).
Mon site tient dans un dossier Git et peut être republié n'importe où.

## Les limites assumées

La clé SSH sans phrase de passe est un choix de commodité pour l'automatisation
— moins sûr qu'une clé protégée. Et les modèles locaux demandent de la
mémoire vive ; un Mac entry-level aurait été à la peine.

## En résumé

Ce stack n'est pas le plus « simple » au premier abord. Mais il est le seul qui
transforme l'assistant en **outil que je possède**. C'est précisément ça,
Fabrica Miracula : fabriquer sa propre maîtrise, un composant à la fois.

> Le meilleur setup n'est pas le plus puissant. C'est celui qui vous rend
> autonome.
