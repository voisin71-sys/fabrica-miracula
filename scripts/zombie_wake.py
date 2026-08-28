#!/usr/bin/env python3
"""Envoie un paquet Wake-on-LAN au Zombie (ComfyUI / PC Windows 192.168.1.100).
Sort le PC de la veille (S3) ; ComfyUI reste en RAM et reprend automatiquement.
MAC : A0-36-BC-A7-F7-45
"""
import socket

MAC = "A0-36-BC-A7-F7-45"
mac_bytes = bytes.fromhex(MAC.replace("-", ""))
magic = b"\xff" * 6 + mac_bytes * 16

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto(magic, ("192.168.1.255", 9))
s.sendto(magic, ("<broadcast>", 9))
s.close()
print(f"[zombie_wake] WoL envoyé à {MAC}")
