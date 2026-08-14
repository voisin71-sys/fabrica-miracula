#!/usr/bin/env python3
"""
Fabrica Miracula — Vérification locale des clés API (dry-run de connexion).

Ce script NE poste RIEN. Pour chaque réseau configuré, il effectue un
appel API en lecture seule (GET) afin de valider que :
  - les clés sont présentes,
  - l'authentification fonctionne (token valide, permissions OK).

Réseaux testés :
  - X (Twitter)      : GET /2/users/me            (OAuth 1.0a)
  - Facebook         : GET /{page-id}?fields=name (Graph API)
  - Instagram        : GET /{ig-user-id}?fields=username (Graph API)
  - LinkedIn         : GET /v2/me                 (Bearer)

Usage :
  python3 scripts/verify_keys.py            # présence + test réseau réel
  python3 scripts/verify_keys.py --no-net   # présence des clés seulement
"""

import os
import sys
import json
import time
import base64
import hmac
import hashlib
import urllib.request
import urllib.error
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

OK = "✅"
WARN = "⚠️ "
FAIL = "❌"

REQUIRED = {
    "x": ["X_API_KEY", "X_API_KEY_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET"],
    "facebook": ["META_ACCESS_TOKEN", "META_FB_PAGE_ID"],
    "instagram": ["META_ACCESS_TOKEN", "META_IG_USER_ID", "META_IG_DEFAULT_IMAGE"],
    "linkedin": ["LINKEDIN_ACCESS_TOKEN", "LINKEDIN_USER_ID"],
}

LABELS = {
    "x": "X (Twitter)",
    "facebook": "Facebook",
    "instagram": "Instagram",
    "linkedin": "LinkedIn",
}

# Nom lisible de chaque clé (pour l'affichage, jamais la valeur)
def log(msg):
    print(msg, flush=True)


def present(name):
    # Présente ET non-vide (un placeholder vide est traité comme absent)
    v = os.environ.get(name)
    return bool(v and v.strip())


def oauth1_get(url, ck, cs, at, ats):
    """GET signé OAuth 1.0a (réutilise la logique de distribute.py)."""
    method = "GET"
    oauth_params = {
        "oauth_consumer_key": ck,
        "oauth_token": at,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_nonce": os.urandom(16).hex(),
        "oauth_version": "1.0",
    }
    param_str = "&".join(
        f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(v, safe='')}"
        for k, v in sorted(oauth_params.items())
    )
    base = "&".join([
        method,
        urllib.parse.quote(url, safe=""),
        urllib.parse.quote(param_str, safe=""),
    ])
    signing_key = f"{urllib.parse.quote(cs, safe='')}&{urllib.parse.quote(ats, safe='')}"
    sig = base64.b64encode(
        hmac.new(signing_key.encode(), base.encode(), hashlib.sha1).digest()
    ).decode()
    oauth_params["oauth_signature"] = sig
    auth_header = "OAuth " + ", ".join(
        f'{urllib.parse.quote(k, safe="")}="{urllib.parse.quote(v, safe="")}"'
        for k, v in sorted(oauth_params.items())
    )
    req = urllib.request.Request(url, headers={"Authorization": auth_header}, method=method)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def http_get_json(url):
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def verify_x():
    ck = os.environ["X_API_KEY"]
    cs = os.environ["X_API_KEY_SECRET"]
    at = os.environ["X_ACCESS_TOKEN"]
    ats = os.environ["X_ACCESS_TOKEN_SECRET"]
    data = oauth1_get("https://api.twitter.com/2/users/me", ck, cs, at, ats)
    uname = data.get("data", {}).get("username", "?")
    return f"authentifié en tant que @{uname}"


def verify_facebook():
    token = os.environ["META_ACCESS_TOKEN"]
    pid = os.environ["META_FB_PAGE_ID"]
    url = f"https://graph.facebook.com/v19.0/{pid}?fields=name&access_token={token}"
    data = http_get_json(url)
    return f"page « {data.get('name', '?')} »"


def verify_instagram():
    token = os.environ["META_ACCESS_TOKEN"]
    uid = os.environ["META_IG_USER_ID"]
    url = f"https://graph.facebook.com/v19.0/{uid}?fields=username&access_token={token}"
    data = http_get_json(url)
    return f"compte @{data.get('username', '?')}"


def verify_linkedin():
    token = os.environ["LINKEDIN_ACCESS_TOKEN"]
    req = urllib.request.Request(
        "https://api.linkedin.com/v2/me",
        headers={"Authorization": f"Bearer {token}", "X-Restli-Protocol-Version": "2.0.0"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8"))
    name = data.get("localizedFirstName", "")
    return f"{name} ({data.get('id', '?')})"


VERIFIERS = {
    "x": verify_x,
    "facebook": verify_facebook,
    "instagram": verify_instagram,
    "linkedin": verify_linkedin,
}


def main():
    no_net = "--no-net" in sys.argv
    log("=== Présence des clés (depuis .env) ===")
    all_present = True
    for net, keys in REQUIRED.items():
        for k in keys:
            v = os.environ.get(k)
            if v and v.strip():
                mark = OK
            elif v == "" or (v is not None and not v.strip()):
                mark = FAIL + "VIDE (placeholder)"
                all_present = False
            else:
                mark = FAIL + "MANQUANT"
                all_present = False
            log(f"  {k:<26} {mark}")
    if not all_present:
        log("\n⚠️  Certaines clés sont vides ou absentes. Renseignez-les dans .env")
        log("    (ou dans GitHub Secrets) AVANT de lancer la distribution.")
    if no_net:
        log("\n[--no-net] Pas de test réseau demandé.")
        sys.exit(0 if all_present else 1)

    log("\n=== Test d'authentification (lecture seule, AUCUN post) ===")
    failures = 0
    for net in REQUIRED:
        keys = REQUIRED[net]
        missing = [k for k in keys if not present(k)]
        if missing:
            log(f"  {LABELS[net]:<12} {WARN} ignoré — clé(s) vide(s)/manquante(s): {', '.join(missing)}")
            failures += 1
            continue
        try:
            result = VERIFIERS[net]()
            log(f"  {LABELS[net]:<12} {OK} {result}")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "ignore")[:160]
            log(f"  {LABELS[net]:<12} {FAIL} erreur HTTP {e.code} — {detail}")
            failures += 1
        except Exception as e:
            log(f"  {LABELS[net]:<12} {FAIL} {type(e).__name__}: {e}")
            failures += 1

    log("")
    if failures == 0:
        log("🎉 Toutes les clés configurées sont valides. Vous pouvez lancer la distribution.")
        sys.exit(0)
    else:
        log(f"⚠️  {failures} réseau(x) en échec. Corrigez avant de déclencher la distribution.")
        sys.exit(1)


if __name__ == "__main__":
    main()
