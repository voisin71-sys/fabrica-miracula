# Distribution automatique — Fabrica Miracula

Le script `scripts/distribute.py` lit le flux RSS du site et publie un résumé
sur **X**, **Facebook** et **Instagram** après chaque déploiement.

> **Souveraineté réelle** : tout est déclenché par un `git push` et tourne dans
> GitHub Actions. Aucune donnée n'est envoyée à un service tiers autre que les
> réseaux ciblés. Le site reste la source de vérité.

## Comment ça marche

1. Le workflow `hugo.yaml` reconstruit et déploie le site (GitHub Pages).
2. Le workflow `distribute.yaml` se déclenche **après** le déploiement.
3. Il lit `https://voisin71-sys.github.io/fabrica-miracula/index.xml`, prend le
   dernier article, formate un message et poste sur chaque réseau dont la clé
   est configurée.
4. Un fichier d'état (`last_guid`) empêche tout double-posting si le workflow
   est relancé.

Si une clé manque → le réseau est simplement ignoré (pas d'échec global).

## Obtenir les clés API (à faire une fois, manuellement)

Ces démarches exigent **vos** comptes et ne peuvent pas être automatisées à
votre place. Ajoutez chaque clé comme **secret de dépôt** GitHub :
*Settings → Secrets and variables → Actions → New repository secret*.

### X (Twitter) — API v2
- Créez un projet/app sur https://developer.x.com (portal développeur).
- Générez un **Bearer Token** (App-only, ou User context si vous postez en
  votre nom).
- Secret : `X_API_BEARER_TOKEN`

> ⚠️ **Réserve honnête** : l'API X est payante hors offre de base très limitée
> (500 posts/mois pour un compte éligible). Vérifiez votre niveau d'accès avant.
> Alternative souveraine : publier via l'app mobile plutôt que l'API.

### Facebook + Instagram — Meta Graph API
- Créez une **App** sur https://developers.facebook.com (type « Business » ou
  « Sans plateforme »).
- Pour **Facebook** : générez un **Page Access Token** longue durée pour votre
  page. Secrets : `META_ACCESS_TOKEN`, `META_FB_PAGE_ID`.
- Pour **Instagram** : reliez votre compte pro Insta à la page FB, récupérez
  l'`instagram_business_account` id. Secrets : `META_IG_USER_ID`,
  `META_IG_DEFAULT_IMAGE` (URL d'une image de votre site, obligatoire pour IG).

> ⚠️ **Réserve honnête** : une app Meta en mode « développement » ne peut poster
> que sur les comptes des administrateurs/testeurs. Pour poster en production,
> il faut soumettre l'app à **revue Meta** (délai, justifications). Prévoyez-le.

## Tester en local (sans poster)

```bash
DISTRIBUTE_DRY_RUN=1 python3 scripts/distribute.py
```

## Déclencher manuellement un post

Sur GitHub : *Actions → Distribute to social → Run workflow*.
