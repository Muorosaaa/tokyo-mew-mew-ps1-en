import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys
out=open(_ROOT+'/data/kanji_tbl.txt','a')
for tok in sys.argv[1:]:
    c,ch=tok.split('=',1); out.write('%x\t%s\n'%(int(c,16),ch))
