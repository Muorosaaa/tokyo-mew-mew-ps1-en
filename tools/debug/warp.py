"""Warp to a scene from tools/debug/scenes.tsv from a cold boot (PCSX-Redux via the skill's emu.py).

    python -X utf8 tools/debug/warp.py SCENE [--disc build/TokyoMewMew_en.cue] [--out work/qa/warp/SCENE]
    python -X utf8 tools/debug/warp.py --all          # every scene, one folder each
    python -X utf8 tools/debug/warp.py --list

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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('scene', nargs='?')
    ap.add_argument('--disc', default=os.path.join(ROOT, 'build/TokyoMewMew_en.cue'))
    ap.add_argument('--out')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
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
