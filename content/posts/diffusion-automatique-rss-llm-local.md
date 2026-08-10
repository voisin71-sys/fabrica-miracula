---
title: "Diffuser ses articles automatiquement en local : RSS, LLM et souveraineté"
description: "Comment j'ai construit une chaîne 100% locale qui lit le flux RSS de ce blog, génère un extrait via un LLM maison et diffuse sur les réseaux — sans dépendre d'un service tiers."
date: 2026-08-10
draft: false
tags: ["RSS", "automatisation", "LLM local", "souveraineté", "Python", "tutoriel"]
categories: ["Tutoriel"]
cover:
  image: "images/diffusion-automatique-rss-llm-local.png"
---

Publier un article, puis le partager à la main sur trois réseaux, c'est une routine qui s'oublie. L'idée n'était pas d'ajouter un outil SaaS de plus, mais de **fermer la boucle en restant sur ma machine** : lire ce que je viens d'écrire, en tirer un accroche, et le pousser là où le monde lit.

Voici la chaîne que je viens de monter pour *Fabrica Miracula*.

## Le point d'entrée : le flux RSS

Hugo génère déjà un flux RSS pour chaque section. Pas besoin d'API propriétaire pour savoir ce qui vient d'être publié — le flux `posts/index.xml` contient tout : titre, lien, description, date. C'est une source de vérité ouverte, standard, et **locale** (elle vit sur le même site que les articles).

> Le RSS n'est pas mort. C'est l'interface la plus souveraine qui existe : un fichier XML que n'importe qui peut lire, sans clé, sans quota.

## Le cerveau : un LLM qui tourne chez moi

Pour chaque nouvel article, un extrait doit être rédigé. Plutôt que d'appeler un service distant, j'utilise **Gemma 4 12B QAT**, servi en local par LM Studio sur `localhost:1234`. Le script lui demande trois variantes — une par plateforme — en respectant les contraintes de taille (280 caractères sur X, plus sur LinkedIn).

Une subtilité technique rencontrée : Gemma 4 est un modèle *reasoning*. Sans précaution, il noie sa réponse dans son propre raisonnement et renvoie un contenu vide. La solution : passer `reasoning_effort: "none"` pour récupérer directement l'accroche utile. Petit détail, mais sans lui, l'automatisation était muette.

## La diffusion : X, et les limites honnêtes

La sortie se fait via **`xurl`**, le CLI officiel de X, qui gère l'OAuth2 et son renouvellement. Pour LinkedIn et Meta, la réalité est moins confortable : **l'API n'autorise pas le posting sur un profil personnel**. Elle exige une page entreprise ou un compte business. Sur un profil perso, l'automatisation n'est pas une option propre — le script le sait et passe son chemin sans planter.

C'est une décision assumée : mieux vaut un *skip* transparent qu'une usine à bannir des comptes.

## L'orchestration : un script, une mémoire, un cron

Le script (`rss_poster.py`) fait trois choses :
1. Télécharge le flux et parse les items.
2. Compare avec un fichier `posted.json` — la mémoire des articles déjà traités.
3. Pour chaque nouveauté : génère les extraits, diffuse, puis coche la case.

Un cron (toutes les deux heures) relance la chaîne. Aucune intervention humaine. Si rien de neuf, silence.

## Pourquoi faire ça en local ?

- **Pas de dépendance à un service tiers** pour détecter ou rédiger.
- **Pas de facture au token** : l'inférence est déjà payée (le matériel).
- **Contrôle total** : le code est sur mon disque, je le modifie quand je veux.

La souveraineté, ce n'est pas seulement où vivent vos données. C'est aussi **qui déclenche vos automatisations**.

## Ce qu'il reste à faire

X est prêt dès que l'authentification est en place (une manipulation ponctuelle, côté utilisateur). LinkedIn et Meta attendront une page pro — ou une copie manuelle de l'extrait, ce qui reste trois secondes.

Le pipeline est en place. La prochaine fois que je publie un article ici, il se retrouvera tout seul sur X, avec une accroche que j'aurai écrite moi-même, sur ma machine.
