# EXPORT COMPLET — FABRICA MIRACULA & HERMES AGENT
# Date : 2026-08-28
# Usage : Reconstruire Hermes et reconnecter tous les services après wipe

---

## 1. FABRICA MIRACULA — SITE & DISTRIBUTION

### Dépôt Git (source Hugo)
- **URL** : https://github.com/voisin71-sys/fabrica-miracula.git
- **Clone local** : /Users/masterai/sites/fabrica-miracula
- **Branche source** : `main`
- **Branche déploiement** : `gh-pages` (HTML compilé par GitHub Actions)
- **Git user** : `Hermes Agent <hermes@fabrica-miracula.local>`
- **Site live** : https://voisin71-sys.github.io/fabrica-miracula/
- **Flux RSS** : https://voisin71-sys.github.io/fabrica-miracula/index.xml

### GitHub Secrets (Actions CI/CD)
> À re-saisir sur https://github.com/voisin71-sys/fabrica-miracula/settings/secrets/actions

| Secret | Description |
|---|---|
| `X_API_KEY` | Consumer Key X/Twitter |
| `X_API_KEY_SECRET` | Consumer Secret X/Twitter |
| `X_ACCESS_TOKEN` | Access Token X/Twitter |
| `X_ACCESS_TOKEN_SECRET` | Access Token Secret X/Twitter |
| `META_ACCESS_TOKEN` | Token Graph API Meta (FB + IG) |
| `META_FB_PAGE_ID` | ID numérique page Facebook |
| `META_IG_USER_ID` | ID compte Instagram Business |
| `META_IG_DEFAULT_IMAGE` | URL image par défaut IG |
| `LINKEDIN_ACCESS_TOKEN` | Token UGC Posts API LinkedIn |
| `LINKEDIN_USER_ID` | URN personne LinkedIn (urn:li:person:XXXX) |

### Réseaux Sociaux
- **X/Twitter** : https://x.com/ (handle à définir — hugo.toml a un placeholder)
- **Facebook Page** : via Meta Business
- **Instagram Business** : lié à la page FB
- **LinkedIn** : via UGC Posts API

### Variables d'Environnement (scripts/distribute.py)
```
X_API_KEY=
X_API_KEY_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=
META_ACCESS_TOKEN=
META_FB_PAGE_ID=
META_IG_USER_ID=
META_IG_DEFAULT_IMAGE=
LINKEDIN_ACCESS_TOKEN=
LINKEDIN_USER_ID=
DISTRIBUTE_DRY_RUN=1
SITE_URL=https://voisin71-sys.github.io/fabrica-miracula/
```

### Script Distribution
- **Fichier** : /Users/masterai/sites/fabrica-miracula/scripts/distribute.py
- **Test dry-run** : `cd /Users/masterai/sites/fabrica-miracula && DISTRIBUTE_DRY_RUN=1 python3 scripts/distribute.py`
- **Idempotence** : GUID du dernier article posté gardé en cache
- **Réseaux** : X (280 chars), FB (63206), IG (2200), LinkedIn (3000)

---

## 2. FABRICA DAILY — PUBLICATION AUTOMATIQUE (Skill Hermes)

### Localisation
- **Skill** : `software-development/fabrica-daily`
- **Profil actif** : pulitzer (version 2.2.0, la plus complète)
- **Archives** : apollon (2.0.0), HERMES_BACKUP_20260816 (1.x)

### Architecture
```
cron 08:00 (9eee3c941d09)
  └─► publish_article.py  (orchestre)
       ├─► llm_client.py    (rédaction LLM)
       ├─► comfy_cover_zombie.py  (couverture ComfyUI Zombie)
       └─► Git (add + commit + push) → GitHub Actions → site live

cron 09:00 (7995d49465db)
  └─► Vérification site live (curl + compteur articles)
```

### Variables d'Environnement Clés
```
FABRICA_LLM_PROVIDER=ollama
FABRICA_LLM_MODEL=gemma4:12b-it-qat
FABRICA_LLM_ENDPOINT=http://127.0.0.1:11434/v1/chat/completions
FABRICA_COMFY_URL=http://192.168.1.100:8188
FABRICA_COMFY_WORKFLOW=flux-art-deco.json
FABRICA_COMFY_ZOMBIE=1
FABRICA_COMFY_TIMEOUT=600
FABRICA_SITE_DIR=/Users/masterai/sites/fabrica-miracula
FABRICA_GIT_USER_NAME=Hermes Agent
FABRICA_GIT_USER_EMAIL=hermes@fabrica-miracula.local
```

### Zombie (PC Windows — ComfyUI)
- **Host** : 192.168.1.100:8188
- **Nom** : DESKTOP-9PD26FN
- **User SSH** : Stephane
- **Clé SSH** : ~/.ssh/id_ed25519_comfy
- **Modèle Flux** : flux1-dev-Q4_K_S.gguf
- **CLIP** : clip_l.safetensors + t5xxl_fp8_e4m3fn.safetensors
- **VAE** : ae.safetensors
- **Réveil auto** : SSH + start_comfy.ps1 (intégré à comfy_cover_zombie.py)
- **Workflow** : flux-art-deco.json (UnetLoaderGGUF + DualCLIPLoader + VAELoader)

### LLM de Rédaction
- **Par défaut actuel** : gemma4:12b-it-qat (Ollama)
- **Alternatives configurées** :
  - lmstudio/qwen3.5-2b-mlx
  - lmstudio/qwen2.5-coder-14b-instruct
  - lmstudio/qwen2.5-7b-instruct
  - ollama/gemma4:12b-it-qat
  - openrouter/anthropic/claude-sonnet-4

### Styles de Couverture (aléatoire, 8 styles)
`cartoon`, `photo-realiste`, `art-deco`, `art-nouveau`, `maitres-flamands`, `impressionniste`, `pointillisme`, `cubiste`

### Cron Jobs Hermes
| ID | Nom | Horaire | Livraison |
|---|---|---|---|
| `9eee3c941d09` | Fabrica Miracula - publication quotidienne | `0 8 * * *` | telegram |
| `7995d49465db` | Fabrica Miracula - verification site live | `0 9 * * *` | origin |

---

## 3. HERMES AGENT — INSTALLATION & PROFILS

### Installation Hermes
- **Version** : v0.20.5 (2026.8.19)
- **Source** : git clone → /Volumes/DATA_CENTER/HermesAgent-source
- **Méthode** : `hermes update` (git pull)
- **Python** : 3.11.16
- **OpenAI SDK** : 2.24.0
- **Symlink** : ~/.hermes/hermes-agent → /Volumes/DATA_CENTER/HermesAgent-source
- **Binaire venv** : /Users/masterai/.hermes/hermes-agent/venv/bin/hermes

### Symlinks (/Volumes/DATA_CENTER/)
```
~/.hermes/bin → HermesAgent-bin
~/.hermes/cache → HermesAgent-cache
~/.hermes/hermes-agent → HermesAgent-source
~/.hermes/logs → HermesAgent-logs
~/.hermes/lsp → HermesAgent-lsp
~/.hermes/node → HermesAgent-node
~/.hermes/sessions → HermesAgent-sessions
~/.hermes/skills → HermesAgent-skills
```

### Profils Hermes (8 profils)
| Profil | Modèle par défaut | Provider |
|---|---|---|
| **apollon** | gemma4:12b-it-qat | custom:ollama-local |
| **chandler** | tencent/hy3:free | nous |
| **gaston** | gemma4:12b-it-qat | custom:ollama-local |
| **pulitzer** | gemma4:12b-it-qat | custom:ollama-local |
| **regis** | gemma4:12b-it-qat | custom:ollama-local |
| **reparator** | gemma4:12b-it-qat | custom:ollama-local |
| **zeus** | meituan/longcat-2.0:free | nous |

> pulitzer est le profil avec le skill fabrica-daily (v2.2.0).
> zeus est le profil de cette session (actif).

---

## 4. AUTHENTIFICATIONS & PROVIDERS

### Nous Research (OAuth)
- **Portal** : https://portal.nousresearch.com
- **Inference** : https://inference-api.nousresearch.com/v1
- **Auth** : device_code OAuth (client_id: hermes-cli)
- **Token** : expirant toutes les ~1h, auto-refresh via refresh_token
- **Accès** : `hermes auth` pour ré-authentifier

### LM Studio (local)
- **Endpoint** : http://127.0.0.1:1234/v1
- **Modèles** : qwen3.5-2b-mlx, qwen2.5-coder-14b-instruct, qwen2.5-7b-instruct
- **Clé API** : via env `LM_API_KEY` (fingerprint: sha256:2ded0a9f931d9f76)

### Ollama (local)
- **Endpoint** : http://127.0.0.1:11434/v1
- **Modèle** : gemma4:12b-it-qat
- **Custom provider** : `ollama-local` dans config.yaml

### llama-server (LaunchAgent)
- **Binaire** : /opt/homebrew/bin/llama-server
- **Modèle** : gemma-4-12B-it-QAT-Q4_0.gguf
- **Port** : 127.0.0.1:1234
- **Context** : 65536
- **GPU layers** : 9999
- **LaunchAgent** : ai.hermes.llama-gemma4qat

### GitHub Copilot
- **Token** : via `gh auth login` (fingerprint: sha256:9b6d8a21514e0e80)
- **Endpoint** : https://api.githubcopilot.com

### Custom Providers configurés
| Nom | Base URL | Modèle par défaut |
|---|---|---|
| ollama-local | http://localhost:11434/v1 | gemma4:12b-it-qat |
| qwen354b | http://127.0.0.1:1234/V1 | qwen3.5-2b-mlx |
| xiaomi | http://127.0.0.1:1234/v1 | qwen3.5-2b-mlx |

---

## 5. TELEGRAM

### Bot Config
- **Activé** : true
- **Home channel** : Stef (chat_id: 6218415094)
- **User ID** : 6218415094
- **Token** : via `TELEGRAM_BOT_TOKEN` env ou config

### Env Vars Telegram (fix août 2025)
```
HERMES_TELEGRAM_DISABLE_FALLBACK_IPS=1
HERMES_TELEGRAM_HTTP_CONNECT_TIMEOUT=10
HERMES_TELEGRAM_INIT_TIMEOUT=20
```

---

## 6. LAUNCHAGENTS (Services SystemD/macOS)

### /Library/LaunchAgents/ (root)
- **ai.hermes.gateway.plist** — Gateway par défaut (non-profil)

### ~/Library/LaunchAgents/ (user)
- **ai.hermes.gateway-zeus.plist** — Gateway profil Zeus
- **ai.hermes.guard-gemma4qat.plist** — Guard llama-server (check 300s)
- **ai.hermes.llama-gemma4qat.plist** — llama-server gemma-4-12B
- **ai.hermes.monitor.plist** — Monitor serveur (port 8911)

### Fichiers de logs
- ~/.hermes/profiles/zeus/logs/gateway.log
- ~/.hermes/profiles/zeus/logs/gateway.error.log
- ~/.hermes/profiles/zeus/logs/guard-gemma4qat.log
- ~/.hermes/profiles/zeus/logs/llama-server.log

---

## 7. OUTILS & WRAPPERS

### comfy-py
- **Chemin** : /Users/masterai/.local/bin/comfy-py
- **Rôle** : wrapper Python venv pour scripts Fabrica (évite le python3 système 3.9)
- **Usage** : `comfy-py scripts/publish_article.py`

### uv (gestionnaire de paquets)
- **Chemin** : /Volumes/DATA_CENTER/HermesAgent-bin/uv
- **toolchain** : browser-use CLI

### tirith (security scanner)
- **Chemin** : /Volumes/DATA_CENTER/HermesAgent-bin/tirith
- **Rôle** : pre-exec scanning (bloqué par défaut en dev)

---

## 8. MODELS & DATA

### Chemins des Modèles
```
/Volumes/DATA_CENTER/BIONIC LLM MODELS/
  └─ lmstudio-community/gemma-4-12B-it-QAT-GGUF/gemma-4-12B-it-QAT-Q4_0.gguf

/Volumes/DATA_CENTER/OllamaModels/
/Volumes/DATA_CENTER/mlx_models/
```

### Bases de données
- **state.db** : état Hermes (sessions, mémoire, etc.)
- **kanban.db** : kanban board
- **projects.db** : projets
- **cron/executions.db** : historique jobs cron

---

## 9. PIPELINE DE DÉSINSTALLATION & RECONSTRUCTION

### Phase 1 : Sauvegarde (déjà faite)
- /Volumes/DATA_CENTER/HERMES_WIPE_BACKUP_20260828_183206/ (5.3 GB)
- /Volumes/DATA_CENTER/HERMES_BACKUP_20260816_2043/
- /Volumes/DATA_CENTER/HERMES_BACKUP_20260816_2224/

### Phase 2 : Désinstallation Hermes
```bash
# 1. Arrêter tous les services
launchctl unload ~/Library/LaunchAgents/ai.hermes.*.plist
launchctl unload /Library/LaunchAgents/ai.hermes.gateway.plist

# 2. Supprimer le gateway
kill $(cat ~/.hermes/gateway_state.json | jq -r .pid) 2>/dev/null

# 3. Supprimer le dossier ~/.hermes (TOUT)
rm -rf ~/.hermes

# 4. Supprimer les LaunchAgents
rm -f ~/Library/LaunchAgents/ai.hermes.*.plist
rm -f /Library/LaunchAgents/ai.hermes.gateway.plist

# 5. Supprimer les données globales (optionnel)
rm -rf /Volumes/DATA_CENTER/HermesAgent-*
```

### Phase 3 : Reinstallation propre
```bash
# 1. Télécharger la dernière version
curl -L -o /tmp/hermes-setup.dmg https://hermes-agent.nousresearch.com/download
hdiutil attach /tmp/hermes-setup.dmg
cp -R /Volumes/Hermes/Hermes.app /Applications/
hdiutil detach /Volumes/Hermes

# 2. Lancer une installation fraîche
open /Applications/Hermes.app
# Suivre l'assistant → profil par défaut

# 3. Ré-authentifier Nous
hermes auth

# 4. Ré-authentifier Telegram (si bot existant)
# → demander un nouveau token @BotFather si nécessaire

# 5. Recloner Fabrica Miracula
cd /Users/masterai/sites
git clone https://github.com/voisin71-sys/fabrica-miracula.git

# 6. Reconfigurer les secrets GitHub (section 1)
# 7. Reconfigurer les LaunchAgents (section 6)
# 8. Recréer les cron jobs (section 2)
```

### Phase 4 : Vérification
```bash
# Site live
curl -s -o /dev/null -w "%{http_code}" https://voisin71-sys.github.io/fabrica-miracula/

# Distribution dry-run
cd /Users/masterai/sites/fabrica-miracula
DISTRIBUTE_DRY_RUN=1 python3 scripts/distribute.py

# LLM local
curl -s http://127.0.0.1:1234/v1/models | jq

# ComfyUI Zombie
curl -s http://192.168.1.100:8188/system_stats | jq

# Cron jobs
hermes cron list
```

---

## 10. CONTACTS & RESSOURCES

- **Hermes Docs** : https://hermes-agent.nousresearch.com/docs
- **Nous Portal** : https://portal.nousresearch.com
- **GitHub Fabrica** : https://github.com/voisin71-sys/fabrica-miracula
- **Hugo PaperMod** : https://github.com/adityatelange/hugo-PaperMod
- **ComfyUI** : https://github.com/comfyanonymous/ComfyUI
- **Flux** : https://blackforestlabs.ai/

---

*Export généré automatiquement — 2026-08-28*
*Conserver ce fichier en SÉCURITÉ (contient des références de tokens et clés)*
