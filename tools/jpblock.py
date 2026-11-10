import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys;sys.path.insert(0,_ROOT+'/tools')
from exeblock import read_raw,rebuild
from rawdec import dec
from pxfit import eng_w,raw_lines_w
def apply(d,S,N,TR,limit=None,exempt=(),report=None):
    """TR keyed by Japanese dec(); limit: None=per-entry original width, number=fixed max"""
    raw=read_raw(d,S,N); tr={}; issues=[]
    for i,r in enumerate(raw):
        j=dec(r)
        if j in TR:
            en=TR[j]; tr[i]=en
            ow=raw_lines_w(r); lim=(limit(i) if callable(limit) else limit) if limit is not None else max(ow)
            if lim is None: lim=max(ow)
            for ln in en.split('\n'):
                if i not in exempt and eng_w(ln)>lim+0.01: issues.append((i,round(eng_w(ln),1),round(lim,1),ln))
            if len(en.split('\n'))>max(len(ow),3 if limit is not None else 0) and i not in exempt: issues.append((i,'lines',en))
    nd,free=rebuild(d,S,N,tr)
    if report is not None: report.append((hex(S),len(tr),free,issues))
    return nd,issues
