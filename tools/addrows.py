import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys
s=open(sys.argv[1]).read().strip()
out=open(_ROOT+'/data/kanji_tbl.txt','a')
for line in s.split('\n'):
    base,t=line.split(' ',1); b=int(base,16); items=[];i=0
    while i<len(t):
        if i+1<len(t) and t[i+1]=='?': items.append(t[i]+'?'); i+=2
        else: items.append(t[i]); i+=1
    assert len(items)==16,(base,len(items),items)
for line in s.split('\n'):
    base,t=line.split(' ',1); b=int(base,16); items=[];i=0
    while i<len(t):
        if i+1<len(t) and t[i+1]=='?': items.append(t[i]+'?'); i+=2
        else: items.append(t[i]); i+=1
    for k,c in enumerate(items): out.write('%x\t%s\n'%(b+k,c))
print('ok')
