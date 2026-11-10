"""Pixel-width check: half-width glyph = 1.0, full-width = 1.45 (measured on screen)."""
import re
FW_RATIO=1.45
_codes=re.compile(r'\{[0-9a-f]+\}|<[0-9a-f]{2}>')
def eng_w(line):
    line=_codes.sub('',line)
    return sum(1.0 if (ord(c)<128) else FW_RATIO for c in line)
def raw_lines_w(raw):
    """width of each line of an original raw byte string"""
    out=[];w=0.0;i=0
    while i<len(raw):
        b=raw[i]
        if 0xf0<=b<=0xfa: w+=FW_RATIO; i+=2
        elif b==0xfc: i+= 5 if raw[i+2]==0x3c else 3
        elif b==0xfd: out.append(w); w=0.0; i+=1
        elif b<0x4b: w+=1.0; i+=1
        else: i+=1
    out.append(w); return out
