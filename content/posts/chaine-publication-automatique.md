---
title: "La chaîne de publication automatique de Fabrica Miracula"
description: "Comment un simple git push construit le site, le déploie, puis le diffuse sur X, Facebook et Instagram — sans dépendre d'un éditeur tiers."
date: 2026-08-09
draft: false
tags: ["automatisation", "GitHub Actions", "Hugo", "RSS", "souveraineté"]
categories: ["Réflexion"]
cover:
  image: "images/chaine-publication-automatique.png"
---

Écrire un article, puis le voir apparaître sur le site **et** être annoncé sur
trois réseaux sociaux — sans ouvrir un seul tableau de bord — c'est possible,
et c'est exactement ce que nous avons monté pour **Fabrica Miracula**. Cet
article explique la chaîne, en français, pour que vous puissiez la reproduire
ou l'adapter.

## Le principe : une seule action, tout le reste suit

Tout commence par un `git push`. Une fois ce geste fait, plus rien n'est
manuel :

```
Vous écrivez → git push → GitHub Actions (build + deploy) → RSS → X / Facebook / Instagram
```

Le site est la **source de vérité**. Les réseaux sociaux ne sont que des
vitrines : ils annoncent ce qui existe déjà, ils ne détiennent pas le contenu.

## Les maillons de la chaîne

### 1. Le site (Hugo + GitHub Pages)

Le site est un site statique généré par **Hugo** et hébergé gratuitement par
**GitHub Pages**. Aucune base de données, aucun serveur à gérer : un dossier de
fichiers texte, versionné avec Git.

### 2. Le déploiement automatique (`hugo.yaml`)

Un premier workflow GitHub Actions se déclenche à chaque `push` sur `main` :
il installe Hugo, reconstruit le site, et publie l'artefact sur GitHub Pages.
À la fin, le site est en ligne.

### 3. La diffusion (`distribute.yaml` + `scripts/distribute.py`)

Un **second** workflow se déclenche *après* le déploiement réussi. Il lance un
script Python (sans aucune dépendance externe — `stdlib` uniquement) qui :

1. Lit le **flux RSS** du site (`/index.xml`).
2. Prend le **dernier article**.
3. Formate un message adapté à chaque réseau.
4. Poste sur **X**, **Facebook** et **Instagram** — pour chaque réseau dont la
   clé API est configurée.

### 4. La sécurité et la sobriété du script

- **Aucune clé codée en dur.** Tout vient de *secrets* GitHub (variables
  d'environnement). Si une clé manque, le réseau est ignoré — pas d'échec
  global.
- **Idempotence.** Un fichier d'état mémorise le dernier article diffusé. Si le
  workflow est relancé, il ne spamme pas.
- **Mode simulation.** `DISTRIBUTE_DRY_RUN=1` affiche ce qui serait posté,
  sans aucun appel réseau — parfait pour tester.
- **Stdlib uniquement.** Pas de `pip install`, donc rien à casser dans le
  cloud.

## Les détails techniques (sans prétention)

### X (Twitter) : OAuth 1.0a

L'API X en mode « Bearer Token » est lecture seule. Pour **publier**, le script
signe chaque requête avec **OAuth 1.0a** (HMAC-SHA1) en utilisant quatre clés :
clé consommateur, secret consommateur, jeton d'accès, secret du jeton. Tout est
calculé en local avec `hmac` et `hashlib`.

### Meta (Facebook + Instagram) : Graph API

- **Facebook** : publication sur le fil de la page via un *Page Access Token*.
- **Instagram** : création d'un conteneur média (image + légende), puis
  publication. Instagram exige une image à chaque post.

## Pourquoi c'est souverain

1. **Le contenu reste à vous.** Il vit dans un dépôt Git et sur un site
   statique. Personne ne peut le modifier sans passer par votre historique.
2. **Aucun intermédiaire éditorial.** Pas de plateforme « tout-en-un » qui
   réécrit, monétise ou censure vos posts.
3. **Reproductible.** La chaîne tient dans des fichiers texte. Elle peut être
   réinstallée ailleurs demain.
4. **Gratuit** pour un site public et un usage modéré.

## Les limites à connaître (honnêteté oblige)

- **L'API X** a des quotas : le niveau gratuit permet ~1 500 posts/mois sur
  votre propre compte ; au-delà, c'est payant.
- **L'API Meta** : une app en mode « développement » n'agit que sur *vos*
  comptes (admin/testeur). Pour d'autres comptes, il faut soumettre l'app à la
  *revue Meta*.
- **Les clés restent à obtenir manuellement** (comptes X et Meta) et à déposer
  comme secrets GitHub — cette étape ne peut pas être automatisée à votre place.

## En résumé

Une ligne de commande (`git push`) déclenche : construction, mise en ligne, et
diffusion sur trois réseaux. C'est l'illustration concrète de Fabrica Miracula :
**fabriquer sa propre maîtrise**, un maillon à la fois.

> L'automatisation n'est pas un luxe. C'est ce qui transforme une intention en
> routine — sans renoncer à la souveraineté.
