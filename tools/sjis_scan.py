import sys,re
data=open(sys.argv[1],'rb').read()
minlen=int(sys.argv[2]) if len(sys.argv)>2 else 4
# runs of valid 2-byte SJIS kana/kanji
i=0;n=len(data);runs=[]
while i<n-1:
    j=i;chars=0
    while j<n-1:
        b=data[j]
        if (0x81<=b<=0x9f or 0xe0<=b<=0xea) and (0x40<=data[j+1]<=0xfc and data[j+1]!=0x7f):
            j+=2;chars+=1
        else: break
    if chars>=minlen:
        try: s=data[i:j].decode('cp932')
        except: s=None
        if s: runs.append((i,s))
        i=j
    else: i+=1
print(len(runs),'runs')
lim=int(sys.argv[3]) if len(sys.argv)>3 else 30
for o,s in runs[:lim]: print(hex(o),s)
