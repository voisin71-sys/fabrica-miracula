---
title: "Zombie : un vieux PC ressuscité en serveur de rendu IA local"
date: 2026-08-28T09:00:00+02:00
draft: false
description: "Comment un PC Windows équipé d'une RTX 3060 est devenu le moteur de génération d'images 100 % local du projet Fabrica Miracula, piloté à distance par ComfyUI."
tags: ["comfyui", "flux", "ia-local", "souverainete", "rtx-3060", "zombie"]
cover:
  image: "images/zombie-pc-render-ia-local.png"
  alt: "Tour PC Zombie ressuscitée en serveur de rendu IA, panneau latéral glow vert-cyan"
  caption: "Généré avec Flux.1 dev sur Zombie (ComfyUI, 100 % local)"
---

On l'appelle **Zombie**. C'est un vieux PC Windows, relégué au fond d'un bureau, que l'on aurait pu jeter. Relifté d'un GPU et branché sur le réseau, il est devenu le bras armé de Fabrica Miracula : la machine qui *fabrique* les images, pendant que le Mac gère l'écriture, l'orchestration et la publication.

## Pourquoi un second PC ?

Générer des images localement coûte de la mémoire vidéo. Le Mac M4 (16 Go de RAM unifiée) est excellent pour faire tourner un LLM de rédaction, mais il n'a pas de carte graphique dédiée pour le rendu diffusion. Plutôt que de renvoyer le travail dans le cloud — et de perdre la main sur nos données —, nous avons préféré confier le rendu à une machine distincte, entièrement sous notre contrôle.

Zombie est un PC Windows (ComfyUI sur `192.168.1.100:8188`) équipé d'une **NVIDIA RTX 3060 12 Go**. Douze gigaoctets de VRAM suffisent largement pour un modèle comme **Flux.1 dev** enquantifié GGUF (Q4_K_S), sans dépendre d'un service tiers.

## Le workflow, de bout en bout

Tout part du Mac. Un script y poste un *workflow* ComfyUI vers Zombie, sans charger le moindre poids localement :

1. **UnetLoaderGGUF** charge `flux1-dev-Q4_K_S.gguf` (le cœur du modèle, ~6,5 Go).
2. **DualCLIPLoader** charge les deux encodeurs texte — `t5xxl_fp8` et `clip_l` — qui traduisent le prompt en conditionnement.
3. **VAELoader** charge `ae.safetensors`, le décodeur qui transforme le bruit latent en pixels.
4. Un **KSampler** Euler/simple (24 steps, guidance 3.5) échantillonne l'image.
5. **SaveImage** écrit le PNG côté Windows ; le script Mac le récupère via l'API `/view`.

Le résultat revient sur le Mac en quelques minutes. Le modèle ne quitte jamais le réseau local.

## Flux.1 dev, pas de SD1.5

Longtemps, Zombie n'a pu faire tourner que SD1.5 : la GTX 1650 d'origine (4 Go) était à la limite du supportable. L'arrivée de la RTX 3060 a changé la donne. SD1.5 reste utile pour des illustrations rapides, mais pour une vraie couverture d'article — détails, lumière, lisibilité du prompt — **Flux.1 dev** est d'une autre catégorie. C'est lui qui produit l'image de cet article.

## Souveraineté avant confort

Ce montage n'est pas le plus simple. On pourrait générer des visuels en deux clics chez un fournisseur cloud. Mais le projet Fabrica Miracula défend une idée précise : l'infrastructure de création doit rester à portée de main. Pas d'API facturée à la requête, pas d'image envoyée sur un serveur tiers, pas de dépendance qui s'éteint un jour.

Zombie n'est pas qu'un vieux PC recyclé. C'est une démonstration concrète : avec du matériel d'occasion et des outils libres (ComfyUI, les poids ouverts de Flux), on fabrique soi-même une usine à images locale et pérenne.

## Et demain ?

La prochaine étape est d'automatiser davantage : que le cron du matin rédige, demande sa couverture à Zombie, et publie — sans intervention. La machine est déjà prête. Il reste à peaufiner les chaînes. Zombie, lui, ne demande qu'à tourner.
