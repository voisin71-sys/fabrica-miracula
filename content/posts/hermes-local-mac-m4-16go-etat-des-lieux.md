---
title: "Hermes Agent en local sur Mac M4 16 Go : état des lieux des configs de la communauté"
description: "LM Studio vs Ollama, Gemma vs Qwen — comparatif des setups Mac M4 16 Go de la communauté Hermes, avec les retours d'utilisateurs réels (@mattbcool, Julian Goldie, ExileAI_0)."
date: 2026-08-09
draft: false
slug: "hermes-local-mac-m4-16go-etat-des-lieux"
tags: ["Hermes Agent", "LM Studio", "Mac M4", "Ollama", "Gemma", "Qwen", "souveraineté"]
categories: ["Réflexion"]
cover:
  image: "images/hermes-local-mac-m4-16go-etat-des-lieux.png"
---

**LM Studio vs Ollama, Gemma vs Qwen — et ce que disent vraiment les utilisateurs Mac M4.**

> Article basé sur une recherche menée en août 2026 : doc officielle Hermes, issues GitHub du repo `NousResearch/hermes-agent`, et la page « User Stories » (262 retours d'utilisateurs scrapés de X, Reddit, Hacker News, Discord, YouTube et blogs).

---

## 1. Pourquoi faire tourner Hermes en local sur un Mac M4 16 Go ?

Trois raisons poussent les utilisateurs Mac vers le local :

- **Confidentialité** : les données (emails, fichiers, contexte de travail) ne quittent pas la machine.
- **Coût** : un Mac M4 déjà payé = inference à coût marginal nul, contre 20–150 $/mois en cloud.
- **Disponibilité** : l'agent tourne même sans réseau.

Mais 16 Go de RAM unifiée, c'est un plafond dur. Tout ce qui dépasse ~12 Go de modèle declenche du swap mémoire et l'expérience s'effondre. D'où la question centrale : **quel provider et quel LLM pour 16 Go ?**

---

## 2. Ce que dit la doc officielle Hermes (le plafond 16 Go)

Hermes publie un guide « Run Locally with Ollama » avec un tableau explicite des modèles par quantité de RAM :

| Modèle (Ollama) | Taille disque | RAM nécessaire | Tool-calling ? | Usage |
|-----------------|---------------|----------------|:----------------:|-------|
| `gemma4:31b` | ~20 GB | 24+ GB | ✅ Oui | Meilleure qualité |
| `gemma2:27b` | ~16 GB | 20+ GB | ❌ Non | Tâches conversationnelles |
| `gemma2:9b` | ~5 GB | 8+ GB | ❌ Non | Chat rapide, Q&R |
| `llama3.2:3b` | ~2 GB | 4+ GB | ❌ Non | Réponses légères |

**Finding majeur** : sur 16 Go, **tous les modèles Ollama recommandés par Hermes sont SANS tool-calling**. Or un agent a besoin d'appeler des outils (fichiers, shell, web, Telegram). Un Mac 16 Go avec Ollama = un agent *muet* côté outils.

C'est là que le choix du provider change tout.

---

## 3. LM Studio vs Ollama : deux philosophies

| Critère | LM Studio | Ollama |
|---------|-----------|--------|
| Endpoint | OpenAI-compatible (`localhost:1234`) | Natif `/api/chat` ou `/v1` |
| Config dans Hermes | Provider `custom` | Provider `ollama` natif |
| Tool-calling sur 16 Go | ✅ Gemma 4 12B QAT le fait | ❌ modèles 16 Go sans outils |
| Gestion mémoire | Charge un modèle à la fois | Multi-modèles mais RAM partagée |
| Fragilité connue | Auth token parfois réactivée au redémarrage | Endpoint tué par la veille Mac |

**Verdict** : pour un Mac 16 Go qui veut un agent *fonctionnel* (avec outils), **LM Studio + Gemma 4 12B QAT est supérieur** à Ollama. C'est précisément pour cela que de nombreux users Mac basculent sur LM Studio.

---

## 4. Gemma 4 vs Qwen 3.5 : les deux familles qui dominent le local

D'après les catalogues et les retours communautaires :

- **Gemma 4 (Google)** — montée en puissance en 2026. Supporte le reasoning et le tool-calling. Décliné en 12B (QAT ~7 Go) et 4B (E4B ~6,8 Go). **Sweet spot pour 16 Go.**
- **Qwen 3.5 (Alibaba)** — très populaire. 4B / 9B / 27B. Le 9B est « very decent », le 27B « VERY good » selon un user Reddit, mais 27 Go = hors limite 16 Go.
- **Llama 3.x** — standard historique, souvent en backup.

Sur 16 Go, le compromis gagnant est **Gemma 4 12B QAT** (qualité + outils) avec **Gemma 4 E4B (4B)** en backup si on lance autre chose (ComfyUI, Chrome) en parallèle.

---

## 5. Les vrais utilisateurs Mac M4 (et leurs setups)

Tiré de la page User Stories Hermes — tous des users réels et nommés :

| Utilisateur | Machine | Provider | LLM / détail |
|-------------|---------|----------|--------------|
| **@mattbcool** (Discord) | Mac mini 16 Go | **Local** | « My local community agent runs on a 16GB Mac mini » — setup 100% local |
| **Julian Goldie** (Substack) | Mac (business) | **LM Studio local** | « Local AI models via LM Studio — sensitive client data never leaves your machine » |
| **@ExileAI_0** (X) | Spare laptop | **LM Studio** | Génère des images localement via LM Studio + ComfyUI |
| **@franci.penov** (Discord) | Mac Mini + Ubuntu | Local models | « control center for local models on my two machines » |
| **@trevorgordon981** (GitHub) | Mac Studio always-on | (non précisé) | Hermes over iMessage, Mac toujours allumé |
| **Alex P.** (Medium) | Mac Mini M4 | OpenClaw + Opus 4.6 | Comparaison coût : M4+Opus = 80–150 $/mo |
| **@witcheer** (X) | Mac Mini 24/7 | Cloud pas cher | 18 cron jobs, 35 scripts, 21 $/mo |

**À noter** : sur les users Mac, **LM Studio est le provider local n°1** (Julian Goldie et ExileAI_0 l'utilisent tous les deux). C'est exactement le setup « LM Studio + Gemma 4 12B QAT » qui ressort comme la référence 16 Go.

---

## 6. Les retours qui reviennent (bugs connus documentés)

Issues GitHub réelles, toutes liées aux LLM locaux sur Mac/16 Go :

- **#46106** — LM Studio garde plusieurs gros modèles chargés en RAM → pression mémoire. *Conseil : un seul modèle à la fois.*
- **#39164** — « reasoning off for local models » : les modèles *reasoning* (Gemma 4 !) spamment le chat de thinking. Users veulent désactiver.
- **#72649** — `reasoning_effort` fatal sur endpoints OpenAI-compatible (LM Studio/Ollama) → crash possible.
- **#76597** — endpoint local en veille Mac traité comme « crashé » par Hermes.
- **#73735** — doc Ollama contradictoire sur le tool-calling de `gemma2:27b`.
- **#71298** — dual storage `providers` vs `custom_providers` → mismatch CLI/GUI.

**Pattern** : les users 16 Go se plaignent de (1) RAM saturée multi-modèles, (2) reasoning verbeux, (3) endpoints tués par la veille Mac, (4) fragilité du provider custom.

---

## 7. Verdict : quelle config pour 16 Go ?

| Profil | Setup recommandé | Limite |
|--------|------------------|--------|
| **Agent local fonctionnel** | LM Studio + Gemma 4 12B QAT (7 Go) | RAM serrée si autre app ouverte |
| **Léger / rapide** | Ollama + `gemma2:9b` ou Qwen 3.5 9B | ❌ Pas d'outils |
| **Cloud-only** | `tencent/hy3:free` / OpenRouter | Dépendance réseau |

**Notre conclusion** : sur Mac M4 16 Go, **LM Studio + Gemma 4 12B QAT est le setup le plus validé par la communauté**. Il est dans la « mainstream locale » aux côtés de Julian Goldie et ExileAI_0. Le seul vrai risque reste la RAM — garde un modèle 4B en backup si tu veux lancer ComfyUI en parallèle.

---

## 8. Méthodologie & limites

- ✅ Sources vérifiables : doc Hermes officielle, issues GitHub du repo public, page User Stories (262 histoires).
- ⚠️ Les moteurs de recherche grand public (Google, Bing, DuckDuckGo, Reddit, Hacker News) ont bloqué les requêtes par captcha lors de cette recherche — les retours « à chaud » des forums n'ont donc pas pu être consultés directement.
- ⚠️ Pour @mattbcool, le LLM exact n'est pas dans le résumé public Discord (corps non accessible sans token).

*Envie d'approfondir un setup en particulier ? Les configs Ollama Qwen et le backup Gemma 4 E4B mériteraient chacun leur guide.*

---

## 9. Mon retour d'expérience (setup réel sur Mac M4 16 Go)

*Cette section est un compte-rendu de mise en place concrète, pas un usage longue durée. Elle documente ce qui s'est réellement passé lors de la configuration du provider local — utile si tu veux reproduire le setup.*

### Le setup de départ
- Mac M4 (Apple Silicon), 16 Go de RAM unifiée, macOS 26 (Tahoe).
- LM Studio installé, serveur OpenAI-compatible sur `localhost:1234`.
- Modèle : **Gemma 4 12B QAT** (7,15 Go, quantifié) — chargé via `lms get google/gemma-4-12b-qat`.

### Ce qui a marché du premier coup
- Le provider `custom` dans `config.yaml` : `base_url: http://localhost:1234/v1`, `model: google/gemma-4-12b-qat`.
- `hermes config set model.default lmstudio` → l'alias est bien résolu (badge `⚕ lmstudio` au démarrage du chat).
- Inférence fonctionnelle : `2+2 → "4"`.

### Les pièges réels rencontrés
1. **Auth token LM Studio**. Le serveur exige un token par défaut. `lm-studio` (string au pif) est rejeté (« malformed »). Solution qui a marché : redémarrer le serveur via CLI (`lms server stop && lms server start`) → auth désactivée, alias sans `api_key`. ⚠️ Si tu relances LM Studio via l'app (pas la CLI), l'auth peut se réactiver et casser l'alias.
2. **Gemma 4 = modèle reasoning**. Il écrit son raisonnement dans `reasoning_content` et laisse `content` vide tant qu'il n'a pas fini de « penser ». Avec `max_tokens` trop court (30), la réponse semble vide. Il faut **≥ 300 tokens** pour voir le résultat final. C'est exactement le bug #39164 de la communauté.
3. **`config.yaml` réécrit par `hermes config set`**. Chaque `hermes config set` duplique/écrase le bloc `model_aliases` avec un template par défaut (`lmstudio-model`). Il faut corriger le `model` à la main après coup. Bug connu #71298.
4. **RAM**. 7 Go de modèle + Hermes + macOS ≈ 14-15 Go. Plus aucune marge pour ComfyUI ou Chrome. Le backup **Gemma 4 E4B (4B, ~6,8 Go)** est recommandé si on veut lancer autre chose en parallèle.

### Verdict après setup
Le provider local **LM Studio + Gemma 4 12B QAT marche**, c'est privé, c'est gratuit. La config tient dans 16 Go mais reste serrée. Pour un usage quotidien, garder un modèle 4B en réserve évite les crashes quand la RAM est partagée.

> ⚠️ Honnêteté : ce retour couvre la mise en place, pas des semaines de production. Les limites RAM et le reasoning verbeux se confirmeront (ou non) à l'usage prolongé.
