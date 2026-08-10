---
title: "Installer Hermes Agent sur macOS (guide débutant)"
description: "Mettre en place son agent local en quelques minutes, sans dépendre du cloud."
date: 2026-08-09
draft: false
tags: ["Hermes Agent", "macOS", "tutoriel"]
categories: ["Tutoriel"]
images: ["/images/installer-hermes-agent.png"]
---

Ce guide vous accompagne pas à pas pour installer **Hermes Agent** sur macOS.
L'objectif : disposer d'un assistant qui tourne sur votre machine, et non sur
un serveur tiers.

## Prérequis

- Un Mac récent (Apple Silicon ou Intel).
- Une connexion internet pour le téléchargement initial.
- Le Terminal (déjà présent sur macOS).

## Étape 1 — Ouvrir le Terminal

Appuyez sur `Cmd + Espace`, tapez **Terminal**, puis validez.

## Étape 2 — Vérifier les outils de base

```bash
git --version
```

Si une version s'affiche, vous êtes prêt. Sinon, installez les outils de
ligne de commande via `xcode-select --install`.

## Étape 3 — Installer Hermes Agent

> Note : la procédure exacte d'installation dépend de votre canal de
> distribution Hermes. Ce guide présente la structure générale ; adaptez la
> commande à la documentation officielle fournie avec votre licence.

```bash
# Exemple de structure d'installation
brew install --cask hermes-agent
```

## Étape 4 — Lancer et vérifier

```bash
hermes --version
```

Si la version s'affiche, votre agent local fonctionne.

## Étape 5 — Sécuriser l'accès

Configurez un mot de passe ou une clé locale. Ne exposez jamais votre agent
sur le réseau public sans authentification. Pour le reste, nous verrons dans
les prochains articles comment **relier plusieurs machines en réseau local
sécurisé**.

## Et après ?

Vous avez posé la première pierre de votre atelier. Dans les prochains
articles, nous aborderons l'isolement des données et la mise en réseau locale.
