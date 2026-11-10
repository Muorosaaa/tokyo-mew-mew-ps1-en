"""Leftovers found 2026-11-09 from the user's battle screenshots (D_SYSTEM / D_EFFECT / D_UNIT).
SYS:  D_SYSTEM 6:20 すかっ (attack misses) -> WHIFF!, 0:223 げっと! burst -> GOT IT!
EFF:  D_EFFECT 372:6 / 375:6 small ぐもーん -> MMMMM
UNIT: D_UNIT 72:0+1 うき -> OO + K!, 245:10 たんさくモード banner -> Explore Mode
"""
import os as _os; _ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0, _ROOT + '/tools')
import numpy as np
from collections import Counter
from g_sfx4 import redraw
from gedit import hmask, text_block, dil
DV = lambda *s: [('dv', x, 0) for x in s]
DVC = lambda *s: [('dvc', x, 0) for x in s]


def got(G, i):
    """yellow burst with dark lettering: refill the lettering with the burst colour, draw GOT IT! in the same dark."""
    px = G.px(i); h, w = px.shape
    border = np.concatenate([px[0], px[-1], px[:, 0], px[:, -1]])
    bg = Counter(border.tolist()).most_common(1)[0][0]
    pal = G.pal(i)
    lum = lambda k: sum(pal[k][:3])
    inner = px[h // 4:3 * h // 4, w // 4:3 * w // 4].ravel().tolist()
    fill = Counter(v for v in inner if v != bg).most_common(1)[0][0]          # burst yellow
    dark = min(set(px.ravel().tolist()) - {bg}, key=lum)                       # lettering colour
    # lettering = dark pixels inside the burst (the burst's own rim stays)
    rim = dil(px == bg, 2)
    px[(px == dark) & ~rim] = fill
    for cap in (8, 7, 6, 5):
        m = hmask('GOT IT!', cap=cap, font='bold', thr=0.4, minsx=0.6, maxw=w - 10)
        if m.shape[0] <= h - 10 and m.shape[1] <= w - 10: break
    y0 = (h - m.shape[0]) // 2; x0 = (w - m.shape[1]) // 2
    sub = px[y0:y0 + m.shape[0], x0:x0 + m.shape[1]]; sub[m] = dark
    G.put(i, px)


def banner(G, i, text):
    """pink title-menu style banner (D_UNIT 245:10 = the title's たんさくモード button)."""
    px = G.px(i); h, w = px.shape
    x0, x1 = 16, w - 17
    TXT = (11, 12, 13)
    for y in range(h):
        row = px[y, x0:x1]
        keep = [v for v in row.tolist() if v not in TXT]
        if keep:
            c = Counter(keep).most_common(1)[0][0]
            row[np.isin(row, TXT)] = c
    text_block(px, [text], (x0, 2, x1, h - 2), DV(9, 8) + DVC(9, 8, 7), [11, 11, 12], rings=[(13, 1)])
    G.put(i, px)


def sys6(G):
    G.put(20, redraw(G.px(20), 'WHIFF!', 0, None, 'bold', 0.3))


def sys0(G):
    got(G, 223)


def eff_groan(G):
    G.put(6, redraw(G.px(6), 'MMMMM', 1, None, 'bold', 0.4))


def unit72(G):
    G.put(0, redraw(G.px(0), 'OO', 1, None, 'bold', 0.35))
    G.put(1, redraw(G.px(1), 'K!', 1, None, 'bold', 0.35))


def unit245(G):
    banner(G, 10, 'Explore')


SYS = {6: sys6, 0: sys0}
EFF = {372: eff_groan, 375: eff_groan}
UNIT = {72: unit72, 245: unit245}
