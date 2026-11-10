"""Make a playable English disc image from the original dump plus whatever is in build/.

    python -X utf8 tools/build_disc.py            -> build/TokyoMewMew_en.bin + .cue
    python -X utf8 tools/build_disc.py --only D_SCE.BIN SLPM_871.78   (bisect a hang)

Needs rom/ to hold the original dump: one .cue and its .bin tracks (Track 1 = data).
Copies every track, injects the patched files into the Track 1 copy (same-size, EDC/ECC fixed),
and writes a .cue pointing at the copies. Runs before emu.py; close the emulator first.
"""
import os, sys, glob, shutil, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'patch'))
import inject

PATCHABLE = ['D_SCE.BIN', 'SLPM_871.78', 'D_SYSTEM.BIN', 'D_EFFECT.BIN', 'D_UNIT.BIN']


def main():
    args = sys.argv[1:]
    only = args[args.index('--only') + 1:] if '--only' in args else None
    cues = glob.glob(os.path.join(ROOT, 'rom', '*.cue'))
    if len(cues) != 1:
        sys.exit('build_disc: put exactly one .cue (and its .bin files) in rom/')
    cue = open(cues[0], encoding='utf-8', errors='replace').read()
    bins = re.findall(r'FILE\s+"([^"]+)"', cue)
    out_dir = os.path.join(ROOT, 'build')
    os.makedirs(out_dir, exist_ok=True)
    new_cue = cue
    data_bin = None
    for k, b in enumerate(bins):
        new_name = 'TokyoMewMew_en (Track %d).bin' % (k + 1) if len(bins) > 1 else 'TokyoMewMew_en.bin'
        shutil.copyfile(os.path.join(ROOT, 'rom', b), os.path.join(out_dir, new_name))
        new_cue = new_cue.replace('"%s"' % b, '"%s"' % new_name)
        if k == 0:
            data_bin = os.path.join(out_dir, new_name)
    open(os.path.join(out_dir, 'TokyoMewMew_en.cue'), 'w', encoding='utf-8').write(new_cue)
    for name in PATCHABLE:
        if only is not None and name not in only:
            continue
        f = os.path.join(out_dir, name)
        if not os.path.isfile(f):
            print('skip (not built):', name); continue
        sys.argv = ['inject.py', data_bin, f]
        inject.main()
    print('disc:', os.path.join(out_dir, 'TokyoMewMew_en.cue'))


if __name__ == '__main__':
    main()
