FWCH=set('！？…「」・（）“”♥～、。　⁉⁈♪『』＆○△□×')
import re as _re
def width(line):
    line=_re.sub(r'\{[0-9a-f]+\}|<[0-9a-f]{2}>','',line)
    return sum(2 if c in FWCH else 1 for c in line)
def check(t, maxw=30, last=28):
    lines=t.split('\n'); errs=[]
    if len(lines)>3: errs.append('more than 3 lines')
    for i,l in enumerate(lines):
        lim = last if i==2 else maxw
        if width(l)>lim: errs.append('line %d width %d>%d: %s'%(i+1,width(l),lim,l))
    return errs
