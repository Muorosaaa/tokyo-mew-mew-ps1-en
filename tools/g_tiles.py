import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,pickle; sys.path.insert(0,_ROOT+'/tools')
import g_sfx
from gedit import *
WS=lambda s: s.split()
T={0:'CR UN CH',2:'U NG H WH AC K !',3:'SW I I SH !',4:'WH AC K !',5:'KA PO W !',6:'BO O OM !',9:'CL AN G !',
10:'WH IR L TH U D !',11:'BA N G !',16:'PF FF T SM AC K !',17:'SL UR R P !',18:'WH AP !',19:'PO O F !',21:'BA N G !',
22:'- BO N K !',23:'WH O OS H',25:'SM AS H !',26:'WH O OS H !',27:'VR R R R M !',29:'WH O OS H !',30:'SL UR R P !',
32:'RU STLE',33:'BO O OM !',35:'GR OO AR !',36:'HM MM MM M',38:'BL AH',40:'WH AC K !!',41:'BO I NG G !',42:'SW I I SH !',
44:'WH IR R L',45:'PO OF',47:'! - BO O OM !',48:'SH TH U D !',49:'BA M !',50:'S CL A N K !',51:'BA N G !',53:'WH AC K !',
54:'SN A P !',55:'WH AC K !',56:'BO O OM !',57:'BO IN G !',58:'CL AN G !',59:'VR R OO O M !',60:'SH I I I NG !',
61:'YO U CA N DO IT !',62:'YO U CA N DO IT !',63:'KA B OO O M !',64:'- TW IN K LE !',65:'SL A A SH !',66:'CL AN G',
67:'CR UN CH !',68:'CR AC K !',69:'SL A A SH !',70:'TW IN K LE !',71:'BO N N K !',72:'SP L A S H !',73:'ZA P',
74:'CL O N K !',80:'RU STLE',81:'LO O K',82:'BA DUM',83:'BA DU M !',84:'HI S S S !',85:'GR RR',86:'BU ZZ',87:'OO K',
88:'WH OO SH',89:'GR R',94:'- WH AC K !'}
U,S=pickle.load(open(_ROOT+'/data/words2.pkl','rb'))
FILES={}
for w,parts in T.items():
    ids,occ=U[w]; P=WS(parts)
    for f,ii in occ:
        assert len(ii)==len(P),(w,len(ii),P)
        for i,p in zip(ii,P):
            if p in ('-','!','!!'): continue
            FILES.setdefault(f,[]).append((i,p))
def draw_tile(G,i,text):
    px=G.px(i); h,w=px.shape; pal=G.pal(i); R=g_sfx.ramp(pal)
    px[:,:]=0
    m=g_sfx.sfx_mask(text,w-4,int(h*0.8),shear=0.15)
    fill=R[:max(3,len(R)*2//3)]; outline=R[-1]; mid=R[len(R)*3//4]
    y0=(h-m.shape[0])//2; x0=(w-m.shape[1])//2
    rows=[fill[min(len(fill)-1,int(r*len(fill)/m.shape[0]))] for r in range(m.shape[0])]
    render(px,m,x0,y0,rows,rings=[(mid,1),(outline,2)])
    G.put(i,px)
def job(f):
    def run(G):
        for i,t in FILES[f]: draw_tile(G,i,t)
    return run
JOBS={f:job(f) for f in FILES}
