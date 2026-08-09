#!/usr/bin/env python3
"""
Fabrica Miracula — Distribution automatique des articles vers X, Facebook, Instagram.

Stratégie souveraine & honnête :
- Le site est la source de vérité (flux RSS). On ne poste QUE ce qui vient du RSS.
- Idempotence : on garde en cache le GUID du dernier article posté pour ne jamais
  spammer en cas de relance du workflow.
- Sécurité : aucune clé n'est codée en dur ; tout vient des variables d'environnement
  (secrets GitHub). Si une clé manque, le réseau est simplement ignoré (pas d'échec
  global), et un message d'avertissement est émis.
- Dry-run : avec DISTRIBUTE_DRY_RUN=1, on affiche ce qui serait posté, sans appel réseau.

Usage local :
  python3 scripts/distribute.py --dry-run
"""

import os
import sys
import json
import time
import base64
import hmac
import hashlib
import html
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

SITE_URL = os.environ.get("SITE_URL", "https://voisin71-sys.github.io/fabrica-miracula/")
RSS_URL = SITE_URL.rstrip("/") + "/index.xml"
STATE_FILE = Path(os.environ.get("GITHUB_WORKSPACE", ".")) / ".distribute_state.json"

# Limites de caractères par réseau
LIMITS = {"x": 280, "facebook": 63206, "instagram": 2200}


def log(msg):
    print(f"[distribute] {msg}", flush=True)


def fetch_rss(url):
    req = urllib.request.Request(url, headers={"User-Agent": "FabricaMiraculaBot/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = r.read().decode("utf-8")
    return data


def parse_latest_item(rss_xml):
    """Retourne (guid, title, link, description) du dernier article du flux."""
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(rss_xml)
    # Hugo génère un flux RSS 2.0
    items = root.findall(".//item")
    if not items:
        return None
    item = items[0]  # le plus récent (Hugo trie par date décroissante)

    def text(tag):
        el = item.find(tag)
        return html.unescape(el.text.strip()) if el is not None and el.text else ""

    guid = text("guid") or text("link")
    title = text("title")
    link = text("link")
    desc = text("description")
    return guid, title, link, desc


def clean_text(s):
    # Supprime les balises HTML et normalise les espaces
    s = html.unescape(s or "")
    s = s.replace("<p>", " ").replace("</p>", " ")
    s = s.replace("<br>", " ").replace("<br/>", " ")
    import re
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def build_message(title, link, desc, network):
    limit = LIMITS.get(network, 280)
    base = clean_text(desc)
    # Résumé : premières phrases
    sentences = [s.strip() for s in base.split(". ") if s.strip()]
    summary = ""
    for s in sentences:
        cand = (summary + s + ". ").strip()
        if len(cand) > limit - 40:
            break
        summary = cand
    if not summary:
        summary = base[: limit - 40].strip()
    # Pour Instagram, pas de lien cliquable dans la légende (on le met en commentaire)
    if network == "instagram":
        msg = f"{title}\n\n{summary}\n\n#fabricamiracula #souverainete #hermesagent"
    else:
        msg = f"{title}\n\n{summary}\n\n{link}"
    # Troncature de sécurité
    if len(msg) > limit:
        msg = msg[: limit - 3].rstrip() + "..."
    return msg


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            return {}
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


# ----------------------------------------------------------------------------
# Posteurs par réseau (stdlib uniquement, via_url pour X ; Graph API pour Meta)
# ----------------------------------------------------------------------------

def post_x(message):
    """X (Twitter) via l'API v2 avec OAuth 1.0a (user context) — permet de poster.

    Nécessite 4 secrets :
      X_API_KEY, X_API_KEY_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
    """
    ck = os.environ.get("X_API_KEY")
    cs = os.environ.get("X_API_KEY_SECRET")
    at = os.environ.get("X_ACCESS_TOKEN")
    ats = os.environ.get("X_ACCESS_TOKEN_SECRET")
    missing = [n for n, v in (("X_API_KEY", ck), ("X_API_KEY_SECRET", cs),
                              ("X_ACCESS_TOKEN", at), ("X_ACCESS_TOKEN_SECRET", ats)) if not v]
    if missing:
        log(f"X : clés manquantes {missing} — réseau ignoré.")
        return False

    # Garanties non-None après le filtre ci-dessus
    ck_s: str = ck  # type: ignore[assignment]
    cs_s: str = cs  # type: ignore[assignment]
    at_s: str = at  # type: ignore[assignment]
    ats_s: str = ats  # type: ignore[assignment]

    url = "https://api.twitter.com/2/tweets"
    body = json.dumps({"text": message}).encode("utf-8")
    method = "POST"
    # Paramètres pour la signature OAuth 1.0a
    oauth_params = {
        "oauth_consumer_key": ck_s,
        "oauth_token": at_s,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_nonce": os.urandom(16).hex(),
        "oauth_version": "1.0",
    }
    # Base string = method & url & (paramètres triés urlencodés)
    param_str = "&".join(
        f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(v, safe='')}"
        for k, v in sorted(oauth_params.items())
    )
    base = "&".join([
        method,
        urllib.parse.quote(url, safe=""),
        urllib.parse.quote(param_str, safe=""),
    ])
    signing_key = f"{urllib.parse.quote(cs_s, safe='')}&{urllib.parse.quote(ats_s, safe='')}"
    sig = base64.b64encode(
        hmac.new(signing_key.encode(), base.encode(), hashlib.sha1).digest()
    ).decode()
    oauth_params["oauth_signature"] = sig
    auth_header = "OAuth " + ", ".join(
        f'{urllib.parse.quote(k, safe="")}="{urllib.parse.quote(v, safe="")}"'
        for k, v in sorted(oauth_params.items())
    )
    req = urllib.request.Request(
        url, data=body, headers={
            "Authorization": auth_header,
            "Content-Type": "application/json",
        }, method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
            log(f"X : tweet publié (id={data.get('data', {}).get('id')})")
            return True
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "ignore")[:200]
        log(f"X : erreur HTTP {e.code} — {detail}")
        return False


def post_meta(message, network):
    """Facebook/Instagram via Graph API — nécessite
    META_ACCESS_TOKEN + (META_FB_PAGE_ID | META_IG_USER_ID)."""
    token = os.environ.get("META_ACCESS_TOKEN")
    if not token:
        log(f"{network} : clé META_ACCESS_TOKEN absente — réseau ignoré.")
        return False
    if network == "facebook":
        node = os.environ.get("META_FB_PAGE_ID")
        if not node:
            log("Facebook : META_FB_PAGE_ID absent — réseau ignoré.")
            return False
        url = f"https://graph.facebook.com/v19.0/{node}/feed"
        data = urllib.parse.urlencode({"message": message, "access_token": token}).encode()
        req = urllib.request.Request(url, data=data, method="POST")
    else:  # instagram
        node = os.environ.get("META_IG_USER_ID")
        if not node:
            log("Instagram : META_IG_USER_ID absent — réseau ignoré.")
            return False
        # IG exige une image ; on crée un conteneur média "image_url" puis on publie.
        ig_img = os.environ.get("META_IG_DEFAULT_IMAGE")
        if not ig_img:
            log("Instagram : META_IG_DEFAULT_IMAGE (URL d'image) requise pour poster — réseau ignoré.")
            return False
        create = f"https://graph.facebook.com/v19.0/{node}/media"
        data = urllib.parse.urlencode({
            "image_url": ig_img, "caption": message, "access_token": token,
        }).encode()
        req = urllib.request.Request(create, data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                cid = json.loads(r.read().decode("utf-8")).get("id")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "ignore")[:200]
            log(f"Instagram : erreur création média HTTP {e.code} — {detail}")
            return False
        url = f"https://graph.facebook.com/v19.0/{node}/media_publish"
        data = urllib.parse.urlencode({"creation_id": cid, "access_token": token}).encode()
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
            log(f"{network} : publication OK (id={data.get('id')})")
            return True
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "ignore")[:200]
        log(f"{network} : erreur HTTP {e.code} — {detail}")
        return False


def main():
    dry_run = os.environ.get("DISTRIBUTE_DRY_RUN", "0") == "1" or "--dry-run" in sys.argv
    log(f"Lecture du flux : {RSS_URL}")
    try:
        rss = fetch_rss(RSS_URL)
    except Exception as e:
        log(f"Impossible de lire le flux RSS : {e}")
        sys.exit(1)

    item = parse_latest_item(rss)
    if not item:
        log("Aucun article trouvé dans le flux.")
        sys.exit(0)
    guid, title, link, desc = item
    log(f"Dernier article : {title}")

    state = load_state()
    last = state.get("last_guid")
    if last == guid and not dry_run:
        log(f"Déjà diffusé (guid={guid}). Rien à faire.")
        return

    networks = ["x", "facebook", "instagram"]
    for net in networks:
        msg = build_message(title, link, desc, net)
        if dry_run:
            print(f"\n--- {net.upper()} (dry-run) ---\n{msg}\n")
            continue
        if net == "x":
            post_x(msg)
        else:
            post_meta(msg, net)
        time.sleep(2)  # courtoisie anti-rate-limit

    if not dry_run:
        state["last_guid"] = guid
        save_state(state)
        log("État mis à jour.")


if __name__ == "__main__":
    main()
