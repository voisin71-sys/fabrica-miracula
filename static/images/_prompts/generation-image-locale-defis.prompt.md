# Prompt de couverture — article "L'illusion de la simplicité : Les défis de la génération d'images locale"

Slug cible : `generation-image-locale-defis`
Fichier de sortie : `static/images/generation-image-locale-defis.png`
Format recommandé : 1200 x 630 px (ratio 1.91:1, vignette réseaux + OpenGraph)
Style attendu : cohérent avec les autres couvertures Fabrica Miracula
(illustrations tech/souveraineté, ambiance "local-first", palette sombre + accents cyan/orange).

## Prompt positif (SDXL) — à coller tel quel
```
A conceptual illustration about running AI image generation locally on a Mac,
souveraineté numérique theme. Centered: a sleek Apple-Silicon Mac mini glowing
with a neural network circuit pattern, emitting a beam that paints a colorful
digital artwork on a floating canvas. Around it: subtle chain-link fence
metaphor breaking, symbolizing escaping proprietary cloud APIs. Dark navy
background, cyan and warm orange accents, clean vector-style, soft volumetric
lighting, editorial tech-magazine cover art, high detail, 1200x630 composition.
```

## Prompt négatif (SDXL)
```
photo, photograph, realistic face, text, watermark, logo, signature, blurry,
lowres, deformed, extra limbs, messy, cluttered, overexposed, 3d render clay look
```

## Paramètres suggérés (SDXL local, M4 16 Go)
- Checkpoint : sd_xl_base_1.0.safetensors (fp16) ou sdxl-fp8 si VRAM serrée
- Steps : 30
- CFG : 7.0
- Sampler : DPM++ 2M Karras (ou Euler a)
- Seed : -1 (aléatoire) — noter la seed retenue pour itérer
- Resolution de génération : 1024x576 puis upscale léger vers 1200x630
  (ou direct 1200x630 si VRAM suffisante)
- Refiner optionnel : sd_xl_refiner_1.0 (à 0.2-0.3 denoise) pour le polish

## Note pour LLM légers (réutilisation du skill)
Ce fichier sert de "brief" : un petit LLM (ex. Gemma 4 12B QAT) peut relire
ce prompt et en générer des variantes thémátiques sans avoir à inventer le
style de zéro. Le workflow ComfyUI (SDXL txt2img) consomme :
  - prompt positif
  - prompt négatif
  - seed / steps / cfg / sampler / resolution
Tout le reste (connexion 127.0.0.1:PORT, upload, poll, download) est géré
par le skill comfyui (run_workflow.py) — voir SKILL.md.
