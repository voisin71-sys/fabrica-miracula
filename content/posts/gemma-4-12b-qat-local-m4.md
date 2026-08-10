---
title: "Gemma 4 12B QAT en local : ce que donne un LLM de 7 Go sur Mac M4 16 Go"
description: "Retour mesuré sur l'usage d'un modèle de langage de 12 milliards de paramètres quantifié, exécuté entièrement en local sur un Mac Apple Silicon à 16 Go — sans cloud, sans abonnement."
date: 2026-08-09
draft: false
tags: ["Gemma 4", "LLM local", "Mac M4", "quantification", "souveraineté", "LM Studio"]
categories: ["Réflexion"]
cover:
  image: "images/gemma-4-12b-qat-local-m4.png"
---

On entend souvent que « louer un LLM dans le cloud, c'est plus simple ». C'est vrai pour le setup initial. Mais une fois le modèle installé, c'est l'inverse : plus de limite de requêtes, plus de facture au token, et surtout — plus rien ne quitte la machine. Voici ce que donne concrètement **Gemma 4 12B QAT**, exécuté en local sur un **Mac M4 à 16 Go de RAM unifiée**.

## Qu'est-ce que le QAT ?

Gemma 4 12B est un modèle de 12 milliards de paramètres. Dans sa version **QAT** (*Quantization-Aware Training*), il est comprimé à ~7 Go sur disque — contre 24+ Go pour une version non quantifiée. La quantification réduit la précision numérique des poids pour gagner en taille et en vitesse, sans que la qualité s'effondre.

> En clair : on fait tenir un modèle de taille « moyenne » dans la RAM d'un portable grand public.

## Pourquoi 12B sur 16 Go ?

C'est le compromis le plus intéressant pour une machine à 16 Go :

- **Assez de paramètres** pour raisonner, suivre des instructions complexes, et — point crucial — **appeler des outils** (lire un fichier, lancer une commande, naviguer).
- **Assez léger** (7 Go) pour laisser ~8 Go à l'agent, au système et au reste.

Les modèles au-delà (27B, 31B) exigent 20+ Go de RAM : hors limite sur 16 Go, ils déclenchent du swap mémoire et l'expérience devient inusable.

## L'infrastructure (toute locale)

- **Modèle** : `google/gemma-4-12b-qat` (7,15 Go), servi par **LM Studio** (serveur compatible OpenAI sur `localhost:1234`).
- **Agent** : Hermes Agent, configuré pour pointer vers ce endpoint local via un provider `custom`.
- **Matériel** : Mac M4, 16 Go unifiés, macOS 26.

Le résultat : un agent qui fonctionne, outils inclus, **sans aucune dépendance réseau** pour le raisonnement.

## Ce qui marche — et ce qui coince

**Côté qualité** : le modèle répond correctement aux tâches de raisonnement, de rédaction et de planification. Pour un usage personnel ou professionnel courant, c'est largement suffisant.

**Côté outils** : le *tool-calling* fonctionne — c'est ce qui distingue un vrai agent d'un simple chatbot. C'est aussi ce qui rend le local viable : l'agent *fait* des choses, il ne se contente pas de texte.

**Deux réserves honnêtes** :

1. **Le reasoning verbeux.** Gemma 4 est un modèle *reasoning* : il écrit son raisonnement intermédiaire avant la réponse. Avec un `max_tokens` trop court, la réponse finale apparaît vide. Il faut réserver de la marge (≥ 300 tokens) pour voir le contenu utile.
2. **La RAM serrée.** 7 Go de modèle + l'agent + macOS ≈ 14-15 Go. Aucune marge pour lancer autre chose de lourd (génération d'images, navigateur chargé) en parallèle. Garder un modèle plus léger (4B) en réserve reste la bonne pratique.

## En chiffres (vécus)

- Taille disque : **~7 Go**
- RAM occupée : **~9-10 Go** (modèle + overhead)
- Coût : **nul** après l'achat du matériel
- Dépendance réseau : **aucune** pour le raisonnement
- Tool-calling : **oui**

## Verdict

Gemma 4 12B QAT sur Mac M4 16 Go n'est pas le modèle le plus puissant du marché. C'est le **meilleur rapport capacité / contrainte** pour qui veut un agent local *fonctionnel* sans dépasser 16 Go. La souveraineté a un coût — la RAM — mais pas de facture.

Et si une tâche dépasse le modèle local ? L'agent peut basculer temporairement sur un LLM cloud, puis revenir en local. Le local n'est pas un dogme : c'est la base, le cloud reste l'appoint.
