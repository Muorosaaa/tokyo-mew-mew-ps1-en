# Tokyo Mew Mew: Tōjō Shin Mew Mew! (PS1) – English fan translation

Japan-only PS1 RPG by Takara/Winkysoft (2002, SLPM-87178), translated to English.
Work in progress: dialogue, menus, encyclopedias and most on-screen graphics are done; see `docs/status.md`.

## Layout
- `tools/` – build scripts and game-format tools (Python 3, needs numpy + Pillow for graphics)
- `tr/` – English text, keyed by original message/string
- `data/` – extracted lookup data the build needs
- `orig/` – the original files from the disc (not in git)
- `rom/` – the full disc dump for emulator testing (not in git)
- `patch/` – `patch.bat` + `inject.py` to apply built files to your own disc image
- `docs/` – status, decisions, format notes

## Build
```
python -X utf8 tools/build.py          # text   -> build/D_SCE.BIN, build/SLPM_871.78
python -X utf8 tools/build_gfx.py      # graphics -> build/D_SYSTEM.BIN, D_EFFECT.BIN, D_UNIT.BIN
python -X utf8 tools/build_disc.py     # disc image from rom/ -> build/TokyoMewMew_en.cue
python -X utf8 tools/check.py          # tests
```

## Patching your own disc
Copy the files from `build/` next to `patch/patch.bat` and `patch/inject.py`, put the bat in the folder with your `(Track 1).bin` (or drag the .bin onto it) and run it. It makes a `.original` backup first.

Releases will ship as patches only, never game data. AI assistance (Claude) was used for this translation.
