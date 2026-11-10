import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,re;sys.path.insert(0,_ROOT+'/tools')
from inline import spans
from rawdec import dec
from encode import encode
from pxfit import eng_w,raw_lines_w
def apply(d,a,b,TR):
    d=bytearray(d); issues=[]; n=0
    for s,e in spans(bytes(d),a,b):
        j=dec(bytes(d[s:e]))
        if j not in TR: continue
        new=encode(TR[j]); old=bytes(d[s:e])
        if len(new)>len(old): issues.append(('bytes',hex(s),len(new)-len(old))); continue
        if re.findall(r'\{fc[0-9a-f]+\}',dec(old))!=re.findall(r'\{fc[0-9a-f]+\}',dec(new)): issues.append(('codes',hex(s))); continue
        lim=max(raw_lines_w(old))
        for ln in TR[j].split('\n'):
            if eng_w(ln.replace('{fc0c20}{fcffff}{fcffff}','00').replace('{fcffff}{fcffff}','00').replace('{fcffff}','Card Slot 1'))>max(lim,26)+0.01: issues.append(('wide',hex(s),ln))
        if len(TR[j].split('\n'))>len(raw_lines_w(old))+1: issues.append(('lines',hex(s)))
        d[s:e]=new+b'\x00'*(len(old)-len(new)); n+=1
    return bytes(d),n,issues
