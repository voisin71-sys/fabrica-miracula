---
title: "Retour d'expérience : mon installation de Fabrica Miracula, des tâtonnements aux premiers résultats"
description: "Le récit sans filtre de la mise en place du site : modèles de langage testés, erreurs rencontrées et leçons tirées."
date: 2026-08-09
draft: false
tags: ["retour d'expérience", "installation", "LLM", "Hugo", "GitHub Pages"]
categories: ["Récit"]
cover:
  image: "images/retour-experience-installation.png"
---

Quand on décide de « fabriquer » son propre espace sur le web, rien ne se passe
comme dans un tutoriel bien lissé. Voici, sans retouche, le cheminement qui a
mené **Fabrica Miracula** de l'idée à la mise en ligne — et surtout les faux
pas qui nous ont fait avancer.

## Le point de départ

L'objectif était clair : un site **souverain**, gratuit, et alimenté
régulièrement. Le choix technique s'est porté sur **Hugo** (générateur de
sites statiques) couplé à **GitHub Pages** (hébergement gratuit). Pour m'aider
dans la mise en place, j'ai fait tourner plusieurs modèles de langage à tour de
rôle.

## Les LLM testés pour cette installation

| Modèle | Canal | Rôle pendant l'installation |
| --- | --- | --- |
| **Gemma 4 12B** (quantifié) | LM Studio local (`lmstudio`) | Tâches de recherche et de rédaction longue ; le « cerveau profond » du projet |
| **google/gemma-4-12b-qat** | Hermes (provider Nous) | Premières sessions de cadrage du site |
| **tencent/hy3:free** | Hermes (provider Nous) | Session de reprise et de déploiement final |

Le constat : un modèle **local** (Gemma 4 12B via LM Studio) est précieux
quand on manipule des données sensibles ou qu'on veut raisonner sans dépendre
d'un cloud. Un modèle **distribué** (Nous) est pratique pour les tâches
courantes et le débogage en direct.

## La chronologie des problèmes (et comment on les a résolus)

1. **Mauvaise référence du thème.** Au départ, le thème PaperMod était pointé
   vers un dépôt erroné (`admx/paper_theme`). Correction : utiliser le dépôt
   officiel `adityatelange/hugo-PaperMod`.
2. **Configuration TOML dépréciée.** `languageCode` était obsolète depuis
   Hugo v0.158 → remplacé par `locale`. Un autre bloc `server.port` était
   déclaré en double → corrigé.
3. **Icônes sociales au mauvais format.** PaperMod attend une *liste* de
   tables (`icon` + `url`), pas un dictionnaire plat. Le build plantait sur le
   template JSON-LD tant que ce n'était pas conforme.
4. **`enableGitInfo` exige un commit.** Le site refusait de construire tant que
   la branche `main` ne contenait aucun commit. Un commit initial a débloqué.
5. **Erreur de clé SSH (humaine).** L'assistant a d'abord communiqué
   l'**empreinte** de la clé au lieu de la **clé publique** elle-même. GitHub
   rejetait l'authentification. Régénérée depuis la clé privée, la bonne clé a
   fonctionné.
6. **Workflow GitHub Actions en échec.** Le tout premier run a échoué sur
   l'étape « Configurer GitHub Pages », car la fonctionnalité Pages n'était pas
   encore activée côté GitHub. Un commit vide a relancé le workflow **après**
   activation → succès.
7. **Chemin de service Hugo.** Le serveur de prévisualisation répondait sous
   `/fabrica-miracula/` (à cause du `baseURL`), d'où un 404 initial sur `/`.

## Ce que ça m'a appris

Un miracle, c'est une technique que l'on ne maîtrise pas encore. Chaque erreur
ci-dessus n'était qu'une étape vers la maîtrise : le déploiement automatique
fonctionne désormais à chaque `git push`, et le site est vivant.

> L'installation n'est pas un obstacle à la souveraineté. C'est l'entraînement
> qui la fabrique.
