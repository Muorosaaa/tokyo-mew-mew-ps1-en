"""Optimal-parse compressor for the game's LZ format, optionally lead-limited (2026-11-09).

Better than lzopt (only tried long-copy lengths 3-9, max, 16/32/64/128; 48-deep match search) and lzlead (greedy):
every copy length is considered and match chains are searched deeper, so even the unchanged original entries come out
at or below their original size. compress(data, maxlead=None, lam=0) returns the stream (with end marker).

Format (tools/lz.py): flag bits MSB-first; 1 = literal (9 bits); 01 = long copy, 2 bytes: offset = (w>>3)-0x2000
(1..8192 back), len = (w&7)+2 (3..9), or w&7 == 0 + length byte n (len n+1, 2..256; n = 0 is the end marker);
00 + 2 bits = short copy, len 2..5, 1 byte offset (1..256 back).

Lead (lzlead.lead_profile): how far decompressed output runs ahead of the compressed input consumed; the game
decompresses in place, so a new stream must not exceed the original's maximum lead. With maxlead set, the DP adds a
penalty `lam` per bit-saving that pushes the lead over the limit; compress_fit() searches lam.
"""
import os as _os; _ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0, _ROOT + '/tools')
from lzc import W


def _cands(data, tries=512):
    n = len(data)
    head2, prev2 = {}, [-1] * n
    head3, prev3 = {}, [-1] * n
    S = [None] * n      # short: best length per offset (1..256): list of (off, len 2..5)
    L = [None] * n      # long: list of (off, len) with increasing len
    for p in range(n):
        s = []
        if p + 1 < n:
            q = head2.get(data[p:p + 2], -1); seen = 0
            while q >= 0 and p - q <= 256 and seen < 64:
                l = 2
                while l < 5 and p + l < n and data[q + l] == data[p + l]: l += 1
                s.append((p - q, l)); q = prev2[q]; seen += 1
        lc = []
        if p + 2 < n:
            q = head3.get(data[p:p + 3], -1); t = 0; bestl = 2; mx = min(256, n - p)
            while q >= 0 and p - q <= 8192 and t < tries:
                l = 3
                while l < mx and data[q + l] == data[p + l]: l += 1
                if l > bestl: lc.append((p - q, l)); bestl = l
                if l == mx: break
                q = prev3[q]; t += 1
        S[p] = s; L[p] = lc
        if p + 1 < n: k = data[p:p + 2]; prev2[p] = head2.get(k, -1); head2[k] = p
        if p + 2 < n: k = data[p:p + 3]; prev3[p] = head3.get(k, -1); head3[k] = p
    return S, L


def _parse(data, S, L):
    """backward DP: minimal bits from p to the end. Returns choice list."""
    n = len(data); INF = 1 << 60
    cost = [INF] * (n + 1); cost[n] = 0; ch = [None] * n
    for p in range(n - 1, -1, -1):
        bc = 9 + cost[p + 1]; bch = None
        best_s = 0
        for o, l in S[p]:
            if l > best_s: best_s = l; so = o
        if best_s:
            for k in range(2, best_s + 1):
                v = 12 + cost[p + k]
                if v < bc: bc, bch = v, (so, k, 's')
        if L[p]:
            # lengths 3..9 cost 18 bits, 10..256 cost 26 bits; candidates have increasing lengths
            lo = 3
            for o, l in L[p]:
                for k in range(lo, min(l, 9) + 1):
                    v = 18 + cost[p + k]
                    if v < bc: bc, bch = v, (o, k, 'l')
                for k in range(max(lo, 10), l + 1):
                    v = 26 + cost[p + k]
                    if v < bc: bc, bch = v, (o, k, 'l')
                lo = l + 1
        cost[p] = bc; ch[p] = bch
    return ch


def _emit(data, ch):
    n = len(data); w = W(); p = 0
    while p < n:
        c = ch[p]
        if c is None: w.bit(1); w.byte(data[p]); p += 1; continue
        o, l, kind = c
        if kind == 's':
            w.bit(0); w.bit(0); x = l - 2; w.bit(x >> 1); w.bit(x & 1); w.byte((0x100 - o) & 0xff)
        else:
            v = (0x2000 - o) << 3
            w.bit(0); w.bit(1)
            if l <= 9: v |= l - 2; w.byte(v >> 8); w.byte(v & 255)
            else: w.byte(v >> 8); w.byte(v & 255); w.byte(l - 1)
        p += l
    w.bit(0); w.bit(1); w.byte(0); w.byte(0); w.byte(0)   # end marker
    return bytes(w.out)


def compress(data, tries=512):
    S, L = _cands(data, tries)
    return _emit(data, _parse(data, S, L))


def _lead_tokens(data, ch):
    """per token: (start p, output after, bits after) -> lead in bytes (as the decoder sees it, flags read ahead)."""
    toks = []; p = 0; bits = 0
    while p < len(data):
        c = ch[p]
        if c is None: k, b = 1, 9
        else:
            o, k, kind = c
            b = 12 if kind == 's' else (18 if k <= 9 else 26)
        bits += b; p += k; toks.append((p - k, p, bits))
    return toks


def _emit_tokens(data, toks):
    w = W()
    for kind, o, l, p in toks:
        if kind == 'lit': w.bit(1); w.byte(data[p])
        elif kind == 's':
            w.bit(0); w.bit(0); x = l - 2; w.bit(x >> 1); w.bit(x & 1); w.byte((0x100 - o) & 0xff)
        else:
            v = (0x2000 - o) << 3; w.bit(0); w.bit(1)
            if l <= 9: v |= l - 2; w.byte(v >> 8); w.byte(v & 255)
            else: w.byte(v >> 8); w.byte(v & 255); w.byte(l - 1)
    w.bit(0); w.bit(1); w.byte(0); w.byte(0); w.byte(0)
    return bytes(w.out)


def compress_lead(data, maxlead, slot=None, tries=512):
    """optimal parse, then emit the first B bytes of copied data as literals (splitting a copy where needed: the
    rest stays a copy from the same offset), with B the smallest that brings lead_profile(stream) <= maxlead
    (binary search). Literals spend bits and lower the lead at every later point; for these streams the lead
    peaks at the very end (lead = output size - stream size), so this tops the stream up to about the original
    size. Returns the stream, or None if it no longer fits `slot` (4-byte size header included)."""
    import lzlead
    S, L = _cands(data, tries)
    ch = _parse(data, S, L)
    base = []; p = 0
    while p < len(data):
        t = ch[p]
        if t is None: base.append(('lit', 0, 1, p)); p += 1
        else: base.append((t[2], t[0], t[1], p)); p += t[1]
    def build(B):
        toks = []
        for kind, o, l, p0 in base:
            if kind == 'lit' or B <= 0: toks.append((kind, o, l, p0)); continue
            m = min(B, l); rest = l - m
            if rest and rest < (2 if kind == 's' else 3): m, rest = l, 0
            if kind == 's' and rest > 5: rest = 5
            for j in range(m): toks.append(('lit', 0, 1, p0 + j))
            if rest: toks.append((kind, o, rest, p0 + m))
            B -= m
        c = _emit_tokens(data, toks)
        return c, lzlead.lead_profile(c, 0, 0)
    c, lp = build(0)
    if lp > maxlead:
        lo, hi = 0, len(data)
        if build(hi)[1] > maxlead: return None
        while lo < hi:
            mid = (lo + hi) // 2
            if build(mid)[1] <= maxlead: hi = mid
            else: lo = mid + 1
        c, lp = build(lo)
    if slot is not None and len(c) + 4 > slot:
        return None
    return c
