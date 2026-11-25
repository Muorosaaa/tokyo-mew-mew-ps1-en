"""Warp to a scene from tools/debug/scenes.tsv from a cold boot (PCSX-Redux via the skill's emu.py).

    python -X utf8 tools/debug/warp.py SCENE [--disc build/TokyoMewMew_en.cue] [--out work/qa/warp/SCENE]
    python -X utf8 tools/debug/warp.py --all          # every scene, one folder each
    python -X utf8 tools/debug/warp.py --list
    python -X utf8 tools/debug/warp.py --lines 16,23,4370      # any dialogue lines, in their real boxes

--lines takes sheet rows (TokyoMewMew_script_proofread.xlsx numbering, from work/script/script.json: run
work/script/dump.py after a build) or ENTRY:LINE pairs. It boots a New Game and, when the opening's first box comes
up, shows each line instead (warp.lua TEXTFILE): box size, line breaks, name plate and font as the player sees them,
one box per circle press. Writes lines.txt and sheet_boxes.png (last frame of each box) in the output folder. The
background is always the opening's airport; the face is the one the line's own scene uses.

Boots, starts a New Game, and on the first map load writes the scene's map id, story flags and pokes (tools/debug/warp.lua;
the spatch column rewrites script bytes in RAM whenever they match, e.g. to pick which Day card the sleep event shows),
then mashes circle (fresh blank memory card each run) and takes a shot every 250 frames plus a contact sheet. Linux: run under xvfb-run, with env
PCSX_REDUX pointing at an extracted PCSX-Redux AppImage (see docs/status.md, QA setup).

A scene's `start` column can replace the New Game: `ROUTE@CARD` plays tools/routes/ROUTE (load a save, walk) with that
memory card (the card is copied per run, never written). Leave `map` empty to skip the warp. `opts` sets extra Lua
globals for warp.lua, e.g. `KILLPARTY=1` (every hit on an enemy knocks out the next party member -> Game Over).
"""
import argparse, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from skill import SCRIPTS

NEWGAME = "1500 -;6 start;400 -;6 start;400 -;6 circle;400 -;6 circle;400 -"


def scenes():
    out = {}
    for line in open(os.path.join(ROOT, 'tools/debug/scenes.tsv'), encoding='utf-8'):
        if not line.strip() or line.startswith('#'):
            continue
        f = (line.rstrip('\n').split('\t') + [''] * 9)[:9]
        out[f[0]] = dict(map=int(f[1], 0) if f[1] else None, flags=f[2], poke=f[3], spatch=f[4], start=f[5],
                         opts=f[6], frames=int(f[7] or 9000), note=f[8])
    return out


def route_of(start):
    """(route string, memory card) for a scene's start column."""
    if not start:
        return NEWGAME, os.path.join(ROOT, 'tools/debug/blank.mcd')   # fresh empty card: no 'Overwrite?' prompt
    route, card = start.split('@')
    lines = [l.strip() for l in open(os.path.join(ROOT, 'tools/routes', route), encoding='utf-8')
             if l.strip() and not l.startswith('#')]
    return ';'.join(lines), os.path.join(ROOT, card)


def run(name, sc, disc, out):
    route, card = route_of(sc['start'])
    cmd = [sys.executable, '-X', 'utf8', os.path.join(SCRIPTS, 'emu.py'), disc, '--out', out,
           '--route-str', route, '--mash', '40', '--mash-key', 'circle', '--frames', str(sc['frames']),
           '--shot-every', '250', '--sheet', '--debugger', '--timeout', '3000',
           '--var', 'MAP=%s' % (sc['map'] if sc['map'] is not None else 'nil'),
           '--var', "FLAGS='%s'" % sc['flags'], '--var', "POKE='%s'" % sc['poke'],
           '--var', "SPATCH='%s'" % sc['spatch'],
           '--script', os.path.join(ROOT, 'tools/debug/warp.lua'), '--sav', card]
    for o in sc['opts'].split(','):
        if o.strip():
            cmd += ['--var', o.strip()]
    print(name, '->', out, flush=True)
    return subprocess.call(cmd, cwd=ROOT)


def lines_block(spec):
    """Script bytes that show the given lines in the opening (warp.lua TEXTFILE). spec: sheet rows ("16,23,4370")
    or ENTRY:LINE pairs ("31:62"), numbered like work/script/script.json (run work/script/dump.py after a build)."""
    import json, re
    from sdis import entry_bounds
    from patcher import find_messages
    from encode import encode
    r = json.load(open(os.path.join(ROOT, 'work/script/script.json'), encoding='utf-8'))
    rows = [x for x in r if x['en'] and re.search(r'[぀-ヿ一-鿿]', x['jp'])]
    by = {(x['entry'], x['line']): x for x in r}
    orig = open(os.path.join(ROOT, 'orig/D_SCE.BIN'), 'rb').read(); B = entry_bounds(orig)
    blk, shown = b'', []
    for item in spec.split(','):
        item = item.strip()
        if not item: continue
        x = by[tuple(int(v) for v in item.split(':'))] if ':' in item else rows[int(item) - 1]
        s, t = B[x['entry']]; e = orig[s:t]; M = find_messages(e)
        if x['line'] >= len(M):
            print('skip %s: message added by tr/extra_sce.py, not supported' % item); continue
        m = M[x['line']]; hdr = m['hdr']
        pre = e[m['at'] - 14:m['at']]
        if not (pre[:1] == b'\x7b' and pre[3:5] == b'\x1f\x0c' and pre[-2:] == b'\x28\x00'):
            spk = hdr[2] if len(hdr) >= 3 and hdr[1] & 1 else 0
            pre = bytes([0x7b, spk, 0x00, 0x1f, 0x0c, 0x25, 0x10, 0x1f, 0x08, 0x0a, 0x04, 0x00, 0x28, 0x00])
        blk += pre + hdr + encode(x['en']) + b'\xff'
        shown.append('%s = entry %d line %d %s: %s' % (item, x['entry'], x['line'], x['speaker'] or '(narration)',
                                                        x['en'].replace('\n', ' / ')))
    return blk + b'\x01\xff\xff', shown      # self-jump: the script waits here after the last box


def run_lines(spec, disc, out):
    blk, shown = lines_block(spec)
    os.makedirs(out, exist_ok=True)
    path = os.path.abspath(os.path.join(out, 'texts.bin')); open(path, 'wb').write(blk)
    open(os.path.join(out, 'lines.txt'), 'w', encoding='utf-8').write('\n'.join(shown) + '\n')
    print('\n'.join(shown))
    frames = 7800 + 160 * len(shown)          # opening fade-in ~6900, then one box per circle press
    cmd = [sys.executable, '-X', 'utf8', os.path.join(SCRIPTS, 'emu.py'), disc, '--out', out,
           '--route-str', NEWGAME, '--mash', '150', '--mash-key', 'circle', '--frames', str(frames),
           '--shot-every', '25', '--debugger', '--timeout', '3000', '--var', 'MAP=nil',
           '--var', "TEXTFILE='%s'" % path.replace('\\', '/'),
           '--script', os.path.join(ROOT, 'tools/debug/warp.lua'), '--sav', os.path.join(ROOT, 'tools/debug/blank.mcd')]
    print('lines ->', out, flush=True)
    rc = subprocess.call(cmd, cwd=ROOT)
    boxes_sheet(out)
    return rc


def boxes_sheet(out):
    """sheet_boxes.png: the last frame of every dialogue box shown after the block was placed (text fully typed)."""
    import glob, re
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        return
    placed = 0
    for ln in open(os.path.join(out, 'log.txt'), encoding='utf-8', errors='replace'):
        m = re.search(r'f(\d+) textfile', ln)
        if m: placed = int(m.group(1))
    fs = [f for f in sorted(glob.glob(os.path.join(out, 'f[0-9]*.png')))
          if int(re.search(r'f(\d+)\.png$', f).group(1)) > placed + 300]
    groups, last = [], None
    for f in fs:                                   # a new box = the bottom third (the text box) changes a lot
        im = Image.open(f).convert('L'); b = np.asarray(im.resize((80, 60)), dtype=np.int16)[40:]
        if last is None or np.abs(b - last).mean() > 3: groups.append([])
        groups[-1].append(f); last = b
    keep = [g[-1] for g in groups if len(g) >= 2]
    if not keep: return
    w, h = Image.open(keep[0]).size; cols = 4; tw, th = w // 2, h // 2
    sheet = Image.new('RGB', (cols * tw, ((len(keep) + cols - 1) // cols) * th))
    for i, f in enumerate(keep):
        sheet.paste(Image.open(f).convert('RGB').resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    sheet.save(os.path.join(out, 'sheet_boxes.png'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('scene', nargs='?')
    ap.add_argument('--lines', help='show these lines in real boxes: sheet rows "16,23" or ENTRY:LINE "31:62"')
    ap.add_argument('--disc', default=os.path.join(ROOT, 'build/TokyoMewMew_en.cue'))
    ap.add_argument('--out')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    if a.lines:
        return run_lines(a.lines, a.disc, a.out or os.path.join(ROOT, 'work/qa/warp', 'lines_' + a.lines.split(',')[0].replace(':', '_')))
    sc = scenes()
    if a.list:
        for k, v in sc.items():
            print('%-22s map %3s  %-14s %s' % (k, v['map'] if v['map'] is not None else '-', v['flags'], v['note']))
        return 0
    names = list(sc) if a.all else [a.scene]
    if not names[0] or names[0] not in sc:
        sys.exit('unknown scene %r; --list shows them' % names[0])
    rc = 0
    for n in names:
        rc |= run(n, sc[n], a.disc, a.out if a.out and not a.all else os.path.join(ROOT, 'work/qa/warp', n))
    return rc


if __name__ == '__main__':
    sys.exit(main())
