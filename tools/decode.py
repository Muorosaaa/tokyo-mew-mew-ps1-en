import sys,glob
hira="ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろわをん"
kata="ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロワヲンヴ"
tbl={}
for i,c in enumerate(hira): tbl[i]=c
for i,c in enumerate(kata): tbl[0x50+i]=c
def dec(d,i):
    out=[]
    while i<len(d)-1:
        b=d[i]
        if b==0xff: return ''.join(out),i+1
        if b==0xfd: out.append('/'); i+=1; continue
        if 0xf1<=b<=0xfc:
            code=(b-0xf1)*256+d[i+1]
            out.append(tbl.get(code,'[%03x]'%code)); i+=2; continue
        out.append('<%02x>'%b); i+=1
        if len(out)>200: break
    return ''.join(out),i
d=open(sys.argv[1],'rb').read()
i=0;n=0
while i<len(d)-3:
    if d[i]==0xf1 and d[i+2]==0xf1:
        s,j=dec(d,i); print(hex(i),s); i=j; n+=1
        if n>=int(sys.argv[2]): break
    else: i+=1
