import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import re,struct,json
ins={}
order=[]
for l in open(_ROOT+'/exe.asm'):
    m=re.match(r'\s+([0-9a-f]+):\s+(?:[0-9a-f]{2} ){4}\s*(.*)',l)
    if m:
        a=int(m.group(1),16)+0x80010000; t=m.group(2).split(' <')[0]; ins[a]=t; order.append(a)
d=open(_ROOT+'/orig/SLPM_871.78','rb').read()
def rd(a): return struct.unpack_from('<I',d,a-0x80010000+0x800)[0]
def analyze(h,maxn=400):
    """collect constants stored to 0x48 field and reads of operand bytes 0x55.."""
    regs={}; stores=set(); reads=set(); a=h; n=0
    while n<maxn and a in ins:
        t=ins[a]
        m=re.match(r'addiu\t(\$\w+), \$zero, (-?0x[0-9a-f]+|\d+)$',t)
        if m: regs[m.group(1)]=int(m.group(2),16)
        m=re.match(r'sw\t(\$\w+), 0x48\(',t)
        if m: stores.add(regs.get(m.group(1),'?') if m.group(1)!='$zero' else 0)
        m=re.match(r'lbu\t\$\w+, (-?0x[0-9a-f]+)\(',t)
        if m:
            v=int(m.group(1),16)
            if 0x55<=v<=0x70: reads.add(v-0x54)
            if -0xaf3<=v<=-0xad0: reads.add(v+0xaf3+1)
        if t.startswith('jr\t$ra'): break
        a+=4;n+=1
    return stores,reads
res={}
for name,tbl,n in (('40',0x80100000-0x526c,40),('43',0x80100000-0x51cc,16),('44',0x80100000-0x518c,40)):
    for i in range(n):
        h=rd(tbl+4*i)
        if not (0x80010000<h<0x800f0000): break
        s,r=analyze(h); res['%s_%02x'%(name,i)]=(sorted(map(str,s)),sorted(r))
        print(name,'%02x'%i,hex(h),sorted(map(str,s)),sorted(r))
