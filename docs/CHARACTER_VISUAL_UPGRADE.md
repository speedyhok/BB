# Blender Character Visual Upgrade

This change adds a non-destructive art-direction pass for the five individual character assets. It keeps authored geometry and armatures, isolates added details in `Polish_Details`, and creates a dedicated portrait studio setup.

## Included
- Smooth shading plus micro-bevel and weighted-normal modifiers for the unified character mesh.
- Layered eyes, irises, pupils, catchlights, brows and a mouth line, improving facial readability compared with the original primitive faces.
- Character-specific accents: Heisenberg hat piping/glasses arms; Jesse hoodie seams; Saul lapel stitching and buttons; Gus spectacle rims; Mike expression creases and zipper.
- Warm key, cool fill, character-colour rim light, background plane, portrait camera, AgX colour management and denoised Cycles settings.
- Detail collection cleanup on re-run to avoid duplicating details.

## Run on Ubuntu
Back up assets before running, since the script saves over each selected .blend:

```bash
cp -a assets/characters assets/characters-backup
blender -b assets/characters/heisenberg.blend --python scripts/character_polish.py -- --character heisenberg --render
blender -b assets/characters/heisenberg.blend --python scripts/character_polish.py -- --character all
```

Output previews are written to `renders/polish_<character>.png`. After reviewing the blend models, re-export the relevant .glb assets so the website/game loads the improvements. This is a visual detail pass, not a substitute for a hand-sculpted likeness mesh or production facial rig.
