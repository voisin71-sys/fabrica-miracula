---
title: "Wake-on-LAN et hibernation : pourquoi mon PC de rendu ne se réveille plus la nuit"
date: 2026-08-29T06:06:04+02:00
draft: false
description: "Mon PC de rendu, que j'appelle affectueusement le « Zombie », est une tour Windows équipée d'une RTX 3060. C'est lui qui fait tourner ComfyUI et le mo"
tags: ["redaction-manuelle"]
cover:
  image: "images/wake-on-lan_et_hibernation__pourquoi_mon_pc_de_rendu_ne_se_r.png"
  alt: "Illustration generee pour l'article Wake-on-LAN et hibernation : pourquoi mon PC de rendu ne se réveille plus la nuit"
  caption: "Généré avec ComfyUI"
---

Mon PC de rendu, que j'appelle affectueusement le « Zombie », est une tour Windows équipée d'une RTX 3060. C'est lui qui fait tourner ComfyUI et le modèle Flux pour générer les couvertures illustrées de ce blog. Le piège, quand on monte une ferme GPU chez soi, ce n'est pas de la faire tourner : c'est de la faire dormir sans la tuer, et de la réveiller à distance sans avoir à appuyer sur un bouton.

Pendant des semaines, j'ai cru que mon Zombie se réveillerait pour peu que je lui envoie un « magic packet » Wake-on-LAN (WoL). Le matin, un cron à 7 h 30 sur mon Mac expédie le paquet, la carte réseau sort la machine de sa torpeur, ComfyUI démarre, et les images du jour se génèrent toutes seules. Sauf que certains jours, plus rien. Le paquet partait dans le vide, la machine restait froide, et je devais traverser la pièce pour appuyer sur le bouton power. La cause était bête, et typique de l'auto-hébergement maison : je confondais veille et hibernation.

Il existe deux façons « éteintes » de faire dormir un PC Windows. La **veille (S3)** garde l'alimentation présente sur la carte mère et sur la carte réseau. La NIC continue de recevoir quelques milliampères et reste à l'écoute d'un magic packet WoL. L'**hibernation (S4)**, en revanche, sauvegarde l'état de la RAM sur le disque puis coupe presque tout — la carte réseau n'est plus alimentée du tout. À partir de là, aucun paquet ne peut la réveiller : seul le bouton physique fonctionne. Mon ancien script de mise en veille appelait `rundll32 powrprof.dll SetSuspendState 1,1,0`, ce qui déclenche précisément l'hibernation S4. Je croyais le mettre en veille ; je le tuais. Le lendemain, le WoL était mort.

La correction tient en un changement de niveau d'énergie : je garde le Zombie en **veille S3** la nuit (un cron le bascule en S3 à 0 h 15), et c'est bien S3 qui préserve le Wake-on-LAN. Le réveil du matin reste un simple magic packet adressé à la MAC de la carte (`A0-36-BC-A7-F7-45`), expédié par un petit script Python depuis le Mac. La nuisance lumineuse, elle, est réglée à part : un script PowerShell éteint les LEDs via OpenRGB avant la veille, pour que la tour ne transforme pas la pièce en sapin de Noël.

Le plus beau, c'est que même quand ComfyUI plante en cours de route, je n'ai pas à me lever. Le symptôme classique : un contexte CUDA reste bloqué après une génération avortée, et l'API renvoie un `500` sur `/system_stats`. Je ouvre alors une session SSH (clé ed25519, sans mot de passe) et je tue le process Python, puis je relance `start_comfy.ps1` en arrière-plan. Un autre crash que j'ai croisé venait d'un `transformers` corrompu au démarrage ; un `pip install --force-reinstall transformers` suffit à le réparer, toujours à distance. Tout se gère depuis le Mac, headless, comme s'il s'agissait d'un service dans le cloud — sauf que le cloud est sous mon bureau.

Cette petite affaire de WoL m'a rappelé une règle générale de la souveraineté matérielle : on ne maîtrise vraiment un serveur que lorsqu'on comprend son cycle de vie complet, du démarrage à la mise en veille, et pas seulement son exécution. Pour une box de rendu orchestrée à distance, le couple **veille S3 + Wake-on-LAN** est le compromis idéal. L'hibernation S4 a ses mérites — elle ne consomme quasiment rien et protège la RAM —, mais elle sacrifie la joignabilité, et avec elle toute l'automatisation. Autant le savoir avant de construire son pipeline dessus.

À l'heure où j'écris, le Zombie dort en S3 dans la pièce d'à côté. Demain à 7 h 30, un paquet de quelques octets traversera le réseau local, la tour s'ébrouera, et les couvertures du blog se dessineront sans qu'un doigt n'ait touché aucun bouton. C'est exactement ce que je voulais : de l'infrastructure qui travaille pour moi, pas que je travaille pour elle.
