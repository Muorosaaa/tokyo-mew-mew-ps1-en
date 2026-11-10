"""Sound effects the lead-limited packer could not fit with the earlier drawings (status: Open bugs, 2026-11-08):
D_EFFECT 2 ぺしっ, 109 (lone tile), 372/375 ぐもっ. Redrawn in the ORIGINAL's style with as little detail as possible,
so they compress into their original slots:
  * colours are taken from the original image: background, fill (per row, like the original's gradient bands) and
    outline (only where the original has one);
  * no speckles, no extra gradient steps.
build_gfx.py uses these jobs INSTEAD of the older ones for these entries (they start from the original pixels).
"""
import os as _os; _ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0, _ROOT + '/tools')
import numpy as np
from collections import Counter
from gedit import hmask, dil

# entry: [(image index, text, outline width, cap height, font[, stroke threshold]), ...] (lower threshold = heavier strokes)
SPEC = {
    2:   [(0, 'SMACK', 0, None, 'bold')],
    109: [(1, 'THUD', 0, 16, 'bold', 0.25)],   # SMACK's style (no outline, user 2026-11-09), heavy strokes
    372: [(5, 'MMPH!', 2, None, 'bold')],
    375: [(5, 'MMPH!', 2, None, 'bold')],
}


def _edge(m):
    """glyph pixels touching the background (4-neighbour)."""
    p = np.pad(m, 1)
    inner = p[1:-1, 1:-1] & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    return m & ~inner


def redraw(px, text, ow, cap, font, thr=0.5, mirror=False):
    h, w = px.shape
    border = np.concatenate([px[0], px[-1], px[:, 0], px[:, -1]])
    bg = Counter(border.tolist()).most_common(1)[0][0]
    g = px != bg
    edge = _edge(g)
    out_c = Counter(px[edge].tolist()).most_common(1)[0][0] if ow else None
    body = g & ~edge if ow else g
    # per-row fill colour from the original's body pixels (nearest row that has any)
    rows = {}
    for y in range(h):
        v = px[y][body[y]]
        if v.size:
            if ow:
                v = v[v != out_c]
            if v.size:
                rows[y] = Counter(v.tolist()).most_common(1)[0][0]
    ys = sorted(rows)
    # text mask: as tall as the original glyphs allow, centred on them
    gy = np.where(g.any(1))[0]; gx = np.where(g.any(0))[0]
    H = gy[-1] - gy[0] + 1; W = gx[-1] - gx[0] + 1
    m = None
    for c in range(cap or H, 4, -1):
        m = hmask(text, cap=c, font=font, maxw=W - 2 * ow, minsx=0.55, thr=thr)
        if m.shape[0] <= H - 2 * ow and m.shape[1] <= W - 2 * ow:
            break
    mh, mw = m.shape
    y0 = gy[0] + (H - mh) // 2; x0 = gx[0] + (W - mw) // 2
    if mirror: m = m[:, ::-1]   # stored mirrored like the Japanese (the game flips it when drawing)
    M = np.zeros_like(g); M[y0:y0 + mh, x0:x0 + mw] = m
    new = np.full_like(px, bg)
    if ow:
        new[dil(M, ow) & ~M] = out_c
    # map the text's rows onto the original's colour bands (same relative height)
    for y in range(y0, y0 + mh):
        t = gy[0] + (y - y0) * (H - 1) // max(1, mh - 1)
        c = rows[min(ys, key=lambda r: abs(r - t))]
        new[y][M[y]] = c
    return new


def job(f):
    def run(G):
        for sp in SPEC[f]:
            i = sp[0]
            G.put(i, redraw(G.px(i), *sp[1:]))
    return run


JOBS = {f: job(f) for f in SPEC}
