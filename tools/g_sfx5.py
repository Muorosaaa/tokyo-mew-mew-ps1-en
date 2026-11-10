"""Kana lettering found in the 2026-11-09 D_EFFECT survey (never translated). Same style as g_sfx4 (original colours,
row bands). M = stored mirrored in the archive (the game flips it), so the English is mirrored too.
Spec: entry -> [(image, text, outline, cap, font, thr, mirror), ...]"""
import os as _os; _ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0, _ROOT + '/tools')
from g_sfx4 import redraw
M = True
WHOOSH = ('WHOOSH', 1, None, 'bold', 0.35, False)   # ぶん (stored unmirrored)
WHAP = ('WHAP!', 1, None, 'bold', 0.35, M)          # ばっ!
RAAAH = ('RAAAH!', 1, None, 'bold', 0.35, M)        # くわあっ!
GRAB = ('GRAB!', 1, None, 'bold', 0.35, M)          # がしっ!
KABOOM = ('KA-BOOOM!', 1, None, 'bold', 0.35, M)    # ずどぉぉん!
SPEC = {
    22: [(6,) + WHOOSH], 76: [(6,) + WHOOSH],
    25: [(4,) + WHAP], 79: [(4,) + WHAP],
    26: [(0,) + RAAAH, (1,) + GRAB], 80: [(0,) + RAAAH, (1,) + GRAB],
    41: [(6, 'SM', 1, None, 'bold', 0.35, M), (7, 'ASH!', 1, None, 'bold', 0.35, M)],   # ず + がっ = ずがっ
    42: [(10,) + KABOOM],
    160: [(0,) + KABOOM, (1, 'BAM', 1, None, 'bold', 0.35, M)],
    109: [(0,) + RAAAH, (2, 'BOOM!', 1, None, 'bold', 0.35, M)],   # どんっ!
}
def job(f):
    def run(G):
        for sp in SPEC[f]:
            G.put(sp[0], redraw(G.px(sp[0]), *sp[1:]))
    return run
JOBS = {f: job(f) for f in SPEC}
