# Distribution automatique — Fabrica Miracula

Le script `scripts/distribute.py` lit le flux RSS du site et publie un résumé
sur **X**, **Facebook** et **Instagram** après chaque déploiement.

> **Souveraineté réelle** : tout est déclenché par un `git push` et tourne dans
> GitHub Actions. Le site reste la source de vérité. Si une clé manque, le
> réseau est simplement ignoré (pas d'échec global).

## Comment ça marche

1. `hugo.yaml` reconstruit et déploie le site (GitHub Pages).
2. `distribute.yaml` se déclenche **après** le déploiement.
3. Il lit `index.xml`, prend le dernier article, formate un message et poste
   sur chaque réseau dont la clé est configurée.
4. Un fichier d'état empêche tout double-posting si le workflow est relancé.

---

## Obtenir les clés API (guide pas à pas)

Ces démarches exigent **vos** comptes (X, Facebook/Instagram) et ne peuvent pas
être automatisées à votre place. Une fois les clés obtenues, ajoutez-les comme
**secrets de dépôt** GitHub : *Settings → Secrets and variables → Actions →
New repository secret*.

### A. X (Twitter) — API v2 via OAuth 1.0a (user context, permet de poster)

> ⚠️ Le script utilise **OAuth 1.0a** (4 clés) car le Bearer Token app-only est
> lecture seule. Pour publier, il faut les 4 identifiants user context.

1. https://developer.x.com → connectez-vous avec votre compte X.
2. Créez un **Projet**, puis une **App** (`fabrica-miracula`).
3. Onglet *Keys and tokens* :
   - **API Key** (Consumer Key) → secret `X_API_KEY`
   - **API Key Secret** (Consumer Secret) → secret `X_API_KEY_SECRET`
   - **Access Token** (user context) → secret `X_ACCESS_TOKEN`
   - **Access Token Secret** → secret `X_ACCESS_TOKEN_SECRET`
4. *App permissions* → **Read and Write**.
5. Niveau d'accès : Free ≈ 1 500 posts/mois sur votre compte ; Basic ≈ 100 $/mois.
6. Déclarez les 4 secrets `X_*` dans GitHub (voir §C).

### C. LinkedIn — API UGC Posts (v2)

1. https://www.linkedin.com/developers/ → *Create app* (type « Share on LinkedIn »).
2. Onglet *Auth* : générez un **Access Token** avec la permission
   `w_member_social` (et `r_liteprofile` pour récupérer votre ID).
3. Votre **User ID** (URN) : `GET https://api.linkedin.com/v2/me` avec le token
   → `id` ; l'URN complet est `urn:li:person:{id}` (le script ajoute le préfixe
   si vous ne fournissez que l'id).
4. Secrets : `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_USER_ID`.
5. ⚠️ Le token LinkedIn est de **courte durée** (généralement 60 jours) : il
   faudra le renouveler manuellement, ou mettre en place un flux OAuth2 avec
   refresh token (hors périmètre de ce script stdlib).

### B. Meta — Facebook + Instagram (Graph API)

1. https://developers.facebook.com → connectez-vous.
2. *My Apps → Create App* → type **Business**. Nom : `fabrica-miracula`.
3. **Facebook (page)** :
   a. *Graph API Explorer* : générez un **User Access Token** avec la permission
      `pages_manage_posts` (et `pages_read_engagement`).
   b. Échangez-le contre un **Page Access Token** longue durée
      (`GET /{page-id}?fields=access_token` avec un user token longue durée).
   c. **ID de la page** : Page → *Paramètres → À propos → ID de la page*.
   d. Secrets : `META_ACCESS_TOKEN` (le page token), `META_FB_PAGE_ID`.
4. **Instagram (compte pro)** :
   a. Compte Insta **Professionnel** (Créateur/Entreprise) **relié à la page FB**
      (Insta → *Paramètres → Compte → Page liée*).
   b. ID du compte Insta pro via `GET /{page-id}?fields=instagram_business_account`.
   c. Une **image publique** sur le site (ex. `.../img/visuel-defaut.jpg`) —
      Instagram exige une image à chaque publication.
   d. Secrets : `META_IG_USER_ID`, `META_IG_DEFAULT_IMAGE`.
5. **Mode dev vs production** : en *dev*, l'app n'agit que sur les comptes des
   **administrateurs/testeurs** (vos propres pages/comptes sont couverts). Pour
   d'autres comptes, soumettez l'app à la **revue Meta** (*App Review*).

---

## Tester en local (sans poster)

```bash
DISTRIBUTE_DRY_RUN=1 python3 scripts/distribute.py
```

## Déclencher manuellement un post

GitHub : *Actions → Distribute to social → Run workflow*.
