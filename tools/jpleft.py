"""Whole-disc scan for Japanese text nobody translated.

    python -X utf8 tools/jpleft.py [--min 3] [--files SLPM_871.78 D_SCE.BIN D_FIELD.BIN ...] [--out work/jpleft.txt]

Looks for runs of Japanese in two encodings:
  * the game's own glyph codes (F1-F9 xx -> glyph (b-0xF1)*256+xx, tools/table.py), allowing FD newlines and
    FC template codes inside a run;
  * Shift-JIS kana/kanji (the EXE and some data may use it).
Scanned: the EXE and D_SCE as they are, and every LZ entry of the other D_*.BIN archives decompressed (entry i at
table[i]+4*i: u32 size + LZ stream). A run is reported only when its bytes are identical in orig/ and build/ (text
nobody touched); archives with no build/ copy count as untouched. Runs listed in data/jpleft_known.txt (one
"FILE ENTRY OFFSET note" per line, ENTRY - for flat files) are skipped: Japanese kept on purpose (credits, logo, ...).
Exit 1 when anything is reported.
"""
import argparse, os, re, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from lz import decompress
import table

JP = re.compile(r'[぀-ヿ㐀-鿿]')
FLAT = ('SLPM_871.78', 'D_SCE.BIN')
ARCH = ('D_SYSTEM.BIN', 'D_EFFECT.BIN', 'D_UNIT.BIN', 'D_SCREEN.BIN', 'D_FIELD.BIN', 'D_ANIME.BIN', 'D_FACE.BIN')
T = table.load()


def glyph_runs(d, minlen):
    """(start, end, text) runs of the game's glyph encoding with >= minlen Japanese glyphs."""
    out, i, n = [], 0, len(d)
    while i < n - 1:
        j, txt, jp = i, [], 0
        while j < n - 1:
            b = d[j]
            if 0xF1 <= b <= 0xF9:
                ch = T.get((b - 0xF1) * 256 + d[j + 1])
                if ch is None:
                    break
                txt.append(ch); jp += bool(JP.match(ch)); j += 2
            elif b == 0xFD and txt:
                txt.append('/'); j += 1
            elif b == 0xFC and txt and j + 2 < n:
                k = 5 if d[j + 2] == 0x3C else 3
                txt.append('{fc}'); j += k
            else:
                break
        # real messages end in FF (end) or FE/FB codes; bytecode that happens to decode as kanji rarely does
        if jp >= minlen and (j < n and d[j] in (0xFF, 0xFE, 0xFB) or jp >= 12):
            out.append((i, j, ''.join(txt)))
            i = j
        else:
            i += 1
    return out


SJ = re.compile(rb'(?:[\x82][\x9f-\xf1]|[\x83][\x40-\x96]|[\x81][\x40-\xac]|[\x88-\x9f\xe0-\xea][\x40-\x7e\x80-\xfc])+')


def sjis_runs(d, minlen):
    out = []
    for m in SJ.finditer(d):
        s = m.group().decode('cp932', 'replace')
        if len(JP.findall(s)) >= minlen and sum('぀' <= c <= 'ヿ' for c in s) >= 2:   # >= 2 kana
            out.append((m.start(), m.end(), s))
    return out


def entries(d):
    n = struct.unpack_from('<I', d, 0)[0] // 4
    st = [struct.unpack_from('<I', d, 4 * i)[0] + 4 * i for i in range(n)]
    for i in range(n):
        if st[i] + 8 > len(d) or (i + 1 < n and st[i + 1] <= st[i]):
            continue
        try:
            out, _ = decompress(d, st[i] + 4, 10 ** 8)
        except Exception:
            continue
        yield i, out


def known():
    k = set()
    p = os.path.join(ROOT, 'data/jpleft_known.txt')
    if os.path.exists(p):
        for l in open(p, encoding='utf-8'):
            f = l.split()
            if len(f) >= 3 and not l.startswith('#'):
                k.add((f[0], f[1], int(f[2], 16)))
    return k


HIRA = re.compile(r'[ぁ-ん]')


def wordy(txt):
    """Looks like language rather than pixel/bytecode noise: no character 3x in a row, mostly distinct characters,
    and at least two different hiragana (particles/okurigana) or a long katakana word."""
    t = re.sub(r'[/{}fc]', '', txt)
    if not t or re.search(r'(.)\1\1', t) or len(set(t)) < 0.6 * len(t):
        return False
    if len(re.findall(r'[ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヤ＝]', t)) * 4 > len(t) or t[0] in 'ゃゅょっャュョッー':
        return False                            # pixel data in Shift-JIS is full of ャ/ヤ
    return len(set(HIRA.findall(t))) >= 2 or bool(re.search(r'[ァ-ー]{4,}', t))


def scan(name, o, b, entry, minlen, K, report):
    for kind, runs in (('glyph', glyph_runs(b, minlen)), ('sjis', sjis_runs(b, minlen + 1))):
        for s, e, txt in runs:
            if not wordy(txt):
                continue
            if o is not None and o[s:e] != b[s:e]:
                continue                       # changed: translated (or moved)
            if any(f == name and en == entry and s <= off < e for f, en, off in K):
                continue
            report.append((name, entry, s, kind, txt))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--min', type=int, default=3, help='minimum Japanese characters per run')
    ap.add_argument('--files', nargs='*', default=list(FLAT + ARCH))
    ap.add_argument('--out', default=os.path.join(ROOT, 'work/jpleft.txt'))
    a = ap.parse_args()
    K, report = known(), []
    for name in a.files:
        op, bp = os.path.join(ROOT, 'orig', name), os.path.join(ROOT, 'build', name)
        if not os.path.exists(bp):
            bp = op                            # never rebuilt: everything in it is untouched
        o, b = open(op, 'rb').read(), open(bp, 'rb').read()
        before = len(report)
        if name in FLAT:
            scan(name, o, b, '-', a.min, K, report)
        else:
            ob = dict(entries(o)) if bp != op else None
            for i, be in entries(b):
                scan(name, ob.get(i) if ob is not None else be, be, str(i), a.min, K, report)
        print('%-14s %5d runs' % (name, len(report) - before), flush=True)
    with open(a.out, 'w', encoding='utf-8') as f:
        for name, en, s, kind, txt in report:
            f.write('%s\t%s\t%06x\t%s\t%s\n' % (name, en, s, kind, txt))
    print('total', len(report), '->', a.out)
    return 1 if report else 0


if __name__ == '__main__':
    sys.exit(main())
