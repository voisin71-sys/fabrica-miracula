#!/usr/bin/env python3
"""Met le Zombie (PC Windows 192.168.1.100) en veille (S3) via SSH.
En S3 la carte réseau reste alimentée -> Wake-on-LAN fonctionne au réveil.
Prérequis : clé SSH ~/.ssh/id_ed25519_comfy, user Stephane.
"""
import subprocess
import sys

SSH_KEY = "/Users/masterai/.ssh/id_ed25519_comfy"
SSH_USER = "Stephane"
SSH_HOST = "192.168.1.100"

ps_cmd = (
    "Add-Type -AssemblyName System.Windows.Forms; "
    "[System.Windows.Forms.Application]::SetSuspendState("
    "[System.Windows.Forms.PowerState]::Suspend, $false, $false)"
)

cmd = [
    "ssh", "-i", SSH_KEY,
    "-o", "StrictHostKeyChecking=no",
    "-o", "ConnectTimeout=10",
    f"{SSH_USER}@{SSH_HOST}",
    f"powershell -NoProfile -Command \"{ps_cmd}\"",
]

try:
    # En S3 la connexion SSH se coupe -> on attend le timeout puis on considère OK
    subprocess.run(cmd, capture_output=True, text=True, timeout=15)
except subprocess.TimeoutExpired:
    pass
print("[zombie_sleep] Commande de veille (S3) envoyée à Zombie")
sys.exit(0)
