# Tokyo Mew Mew ~Tōjō Shin Mew Mew!~ (PS1, SLPM-87178) English translation

Skill: translate-retro-game; `python tools/skill.py` prints its folder. Read its SKILL.md before ROM, text or QA work. `"$(python tools/skill.py)"` works in bash and PowerShell; never paste a `plugins/cache/<hash>` path.

## Commands (run from repo root)
- Text build: `python -X utf8 tools/build.py` -> `build/D_SCE.BIN`, `build/SLPM_871.78` (seconds)
- Graphics build: `python -X utf8 tools/build_gfx.py [D_SYSTEM] [D_EFFECT] [D_UNIT]` -> `build/D_*.BIN` (slow: D_EFFECT ~20 min; run in background)
- Disc: `python -X utf8 tools/build_disc.py [--only FILE..]` -> `build/TokyoMewMew_en.cue/.bin` (needs `rom/*.cue` + `.bin`)
- Check: `python -X utf8 tools/check.py` (hashes, text build, codec round-trip, width lint; the pre-commit hook runs this)
- Smoke: `python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/TokyoMewMew_en.cue --out work/qa/smoke --smoke --mash-key circle`
- Warp (debug tool, cold boot, no save): `xvfb-run -a python -X utf8 tools/debug/warp.py SCENE` (`--list`, `--all`); scenes in `tools/debug/scenes.tsv`. Use it to reach any scene instead of asking the user for saves.
- User-side injector: `patch/patch.bat` + `patch/inject.py` (drops built files into their own Track 1 .bin)

## Paths
- Original disc files: `orig/` (gitignored; hashes in `orig.sha1`). Full dump for emulator QA: `rom/` (gitignored). Emulator: `tools/pcsx-redux/` via `fetch_emu.py pcsx`; BIOS via `fetch_emu.py psx-bios`.
- Translations: `tr/` (`eNNN.py` per script entry, `mem_*.py` translation memory, `blk_*`/`sys_*`/`inline_*`/`exe_script` for the EXE, `guide_en.py`/`animal_en.py` encyclopedias). Glossary: `glossary.md`. Formats: `docs/re/README.md`.
- Graphics jobs: `tools/g_*.py` (draw English into decoded images); packing: `tools/inplace.py` + `tools/lzlead.py`.

## Rulings
- Edit source files only with the file-edit tool. Many strings contain `{fcXXXX}`/`<xx>` codes and full-width punctuation (！？…「」); keep them.
- Every recompressed archive entry MUST go through the lead-limited packer (`build(..., leadlimit=True)`): the game decompresses in place, and a smaller stream that outruns the original freezes the game (Level Up hang). Entries that can't be packed safely are skipped and stay Japanese.
- Built files must keep their original size; entries are written in place at original offsets.
- Decisions with reasons: `docs/decisions.md`. Read it before asking the user anything.

## Status
`docs/status.md`: done, next, open bugs. Update it at the end of every session.
