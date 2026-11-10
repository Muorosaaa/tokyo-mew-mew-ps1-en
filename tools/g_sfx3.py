import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,pickle; sys.path.insert(0,_ROOT+'/tools')
import g_sfx, g_tiles
cl=pickle.load(open(_ROOT+'/data/single_cl.pkl','rb'))
WORD={1:'BAM',5:'THUD',6:'THUD',10:'ZIP'}
EF={}
for c,w in WORD.items():
    for f,i in cl[c]['m']: EF.setdefault(f,[]).append(('t',i,w))
for f,i,w in ((505,2,'WHACK!'),(372,5,'MMPH!'),(375,5,'MMPH!')):
    EF.setdefault(f,[]).append(('w',i,w))
UN={31:[(13,'WH'),(14,'AC'),(15,'K')],38:[(13,'WH'),(14,'AC'),(15,'K')],64:[(0,'RU'),(1,'STLE')],
    65:[(0,'LO'),(1,'O'),(2,'K')],66:[(0,'BA'),(1,'DUM')],67:[(0,'BA'),(1,'DU'),(2,'M')],
    69:[(0,'HI'),(1,'S'),(2,'S'),(3,'S')],71:[(0,'BU'),(1,'ZZ')],73:[(0,'WH'),(1,'OO'),(2,'SH')],78:[(0,'BR'),(1,'RR')],
    79:[(0,'!')]}   # 79 = the っ of ぶるっ (78+79), missed until the 2026-11-09 image survey
def ejob(f):
    def run(G):
        for k,i,w in EF[f]:
            (g_tiles.draw_tile if k=='t' else g_sfx.draw)(G,i,w)
    return run
def ujob(f):
    def run(G):
        for i,w in UN[f]: g_tiles.draw_tile(G,i,w)
    return run
EJOBS={f:ejob(f) for f in EF}
UJOBS={f:ujob(f) for f in UN}
