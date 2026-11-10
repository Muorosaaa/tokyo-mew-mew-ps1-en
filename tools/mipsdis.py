import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,re
a=int(sys.argv[1],16)-0x80010000; n=int(sys.argv[2])
for l in open(_ROOT+'/exe.asm'):
    m=re.match(r'\s+([0-9a-f]+):\s+(?:[0-9a-f]{2} ){4}\s*(.*)',l)
    if m:
        o=int(m.group(1),16)
        if a<=o<a+n*4: print(hex(o+0x80010000),m.group(2))
