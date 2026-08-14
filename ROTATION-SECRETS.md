# Procédure de ROTATION des clés API compromises (Fabrica Miracula)

⚠️ **Contexte** : le fichier `.env` contenait toutes les clés API et a été
commité dans le dépôt **public** du 12 août au 13 août 2026. Ces clés sont
donc considérées comme **publiques** et doivent être révoquées immédiatement,
même si l'historique git a depuis été purgé.

L'ordre de priorité : X (credentials complets → un tiers peut tweeter en votre nom)
> LinkedIn (token = accès au profil) > Meta (page + IG).

---

## 1. X / Twitter (OAuth 1.0a) — CRITIQUE

Aller sur https://developer.twitter.com/en/portal/dashboard
1. **Project & App** → votre application Fabrica Miracula.
2. Onglet **Keys and tokens**.
3. `Consumer Keys` → **Regenerate** (révoque `X_API_KEY` + `X_API_KEY_SECRET`).
4. `Authentication Tokens` (Access Token & Secret) → **Regenerate** (révoque
   `X_ACCESS_TOKEN` + `X_ACCESS_TOKEN_SECRET`).
5. Notez les 4 nouvelles valeurs.

## 2. Meta (Facebook + Instagram) — Graph API

Aller sur https://developers.facebook.com/tools/explorer
1. En haut, sélectionnez votre application, puis dans le sélecteur de token
   cliquez sur **"Get User Access Token"** pour générer un nouveau
   `META_ACCESS_TOKEN` (valide ~60 jours).
2. `META_FB_PAGE_ID` : ID numérique de la page (inchangé, à vérifier dans
   Paramètres → Page → À propos → ID de la page).
3. `META_IG_USER_ID` : ID du compte Instagram Business (inchangé ; à récupérer
   via `GET /{page-id}?fields=instagram_business_account`).
4. `META_IG_DEFAULT_IMAGE` : URL d'une image hébergée (ex. logo FABRICA
   MIRACULA sur le site) — inchangée.

## 3. LinkedIn — UGC Posts API

1. https://www.linkedin.com/developers/apps → votre app.
2. Onglet **Auth** → **Generate new access token** (révoque l'ancien
   `LINKEDIN_ACCESS_TOKEN`, ~60 jours).
3. `LINKEDIN_USER_ID` : URN `urn:li:person:XXXX` (inchangé).

---

## 4. Saisir les 10 secrets dans GitHub

Aller sur : https://github.com/voisin71-sys/fabrica-miracula/settings/secrets/actions

Cliquer **New repository secret** pour CHACUN (nom exact, sensible à la casse) :

| Nom du secret | Valeur |
|---|---|
| `X_API_KEY` | (nouveau consumer key) |
| `X_API_KEY_SECRET` | (nouveau consumer secret) |
| `X_ACCESS_TOKEN` | (nouveau access token) |
| `X_ACCESS_TOKEN_SECRET` | (nouveau access token secret) |
| `META_ACCESS_TOKEN` | (nouveau token Graph) |
| `META_FB_PAGE_ID` | (ID page FB) |
| `META_IG_USER_ID` | (ID IG Business) |
| `META_IG_DEFAULT_IMAGE` | (URL image par défaut IG) |
| `LINKEDIN_ACCESS_TOKEN` | (nouveau token LinkedIn) |
| `LINKEDIN_USER_ID` | (URN personne LinkedIn) |

> Ne commencez PAS le nom par `GITHUB_` (réservé).

---

## 5. Vérification (sans spammer)

Une fois les 10 secrets saisis, lancez un test **dry-run** depuis votre machine :

```bash
cd /Users/masterai/sites/fabrica-miracula
DISTRIBUTE_DRY_RUN=1 python3 scripts/distribute.py
```

Cela affiche les 4 messages SANS les poster. Pour un vrai test de connexion
sans risque de double-poste, vous pouvez aussi utiliser le déclenchement
manuel GitHub : onglet **Actions** → *Distribute to social* → **Run workflow**.

⚠️ **Règle** : un run vert sur GitHub ne prouve PAS que les posts sont partis.
Le script ignore silencieusement un réseau si sa clé manque. Après un run,
vérifiez bien la sortie du job : elle doit afficher « publication OK (id=…) »
pour chaque réseau, et vous verrez les posts apparaître sur vos comptes.
