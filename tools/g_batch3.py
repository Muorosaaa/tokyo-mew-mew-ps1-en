import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,random; sys.path.insert(0,_ROOT+'/tools')
from gedit import *
DV=lambda *s:[('dv',x,0) for x in s]
DVC=lambda *s:[('dvc',x,0) for x in s]
TAGS={1:'Ichigo',3:'Mint',5:'Lettuce',7:'Pudding',9:'Zakuro',11:'Ringo',
      13:'Kisshu',15:'Gateau',17:'Source',19:'Chimera',21:'Parasite',23:'Chimera RDA'}
SMALL=DV(10,9)+DVC(10,9,8)+[('dvcr',9,0),('dvcr',8,0)]
def tags(G):
    for i,t in TAGS.items():
        px=G.px(i); relabel(px,t,SMALL,align='l',pad=0); G.put(i,px)
PROFILE={0:'Height',1:'Weight',2:'Favorite Food',3:'Disliked Food',4:'Hobby',5:'Talent',6:'Gene RDA',7:'Special'}
def profile(G):
    for i,t in PROFILE.items():
        px=G.px(i); h,w=px.shape
        txt=np.isin(px,[1,2,3,4,5,6,11,12])
        px[txt]=0
        ms,caph=lines_mask([t],w-12,14,DV(11,10)+DVC(10,9))
        m,ct,ch=ms[0]
        fill=[1,2,2,3,3,4]
        fr=[fill[min(len(fill)-1,max(0,int((r-ct)*len(fill)/max(1,ch))))] for r in range(m.shape[0])]
        render(px,m,(w-m.shape[1])//2,4-ct+ (2 if caph<8 else 0),fr,rings=[(6,1)])
        G.put(i,px)
def simple(G,i,t,opts,bold=0):
    px=G.px(i); relabel(px,t,opts,bold=bold); G.put(i,px)
def gameover(G):
    base=G.px(5); st=auto_style(base)
    px=base.copy(); px[:,:]=0; h,w=px.shape
    ms,caph=lines_mask(['Game Over'],w-20,h-12,DV(30,28,26,24,22,20))
    m,ct,ch=ms[0]; m=np.pad(m,((0,0),(0,1))); m[:,1:]|=m[:,:-1]
    fill=st['fill']; fr=[fill[min(len(fill)-1,max(0,int((r-ct)*len(fill)/max(1,ch))))] for r in range(m.shape[0])]
    render(px,m,(w-m.shape[1])//2,(h-caph)//2-ct,fr,rings=[(st['outline'],2)])
    G.put(5,px.copy())
    rnd=random.Random(7)
    # frame 4: slightly jittered rows; frames 0-3: increasing dropout + jitter
    for f,(keep,jit) in {4:(1.0,1),3:(0.75,2),2:(0.55,3),1:(0.35,4),0:(0.15,5)}.items():
        q=np.zeros_like(px)
        for y in range(h):
            for x in range(w):
                v=px[y,x]
                if v and rnd.random()<keep:
                    yy=min(h-1,max(0,y+rnd.randint(-jit,jit)//2)); xx=min(w-1,max(0,x+rnd.randint(-jit,jit)))
                    q[yy,xx]=v
        G.put(f,q)
def eff(arc_i):
    def run(G):
        if arc_i==305: simple(G,0,'Level Up!',DV(24,22,20,18,16),bold=1)
        if arc_i==432: simple(G,0,'30 min later…',DV(20,18,16,14),bold=1)
        if arc_i==439: simple(G,0,'Hours later…',DV(20,18,16,14),bold=1)
        if arc_i in (374,543): gameover(G)
    return run
SYS={2:tags,53:profile}
EFF={k:eff(k) for k in (305,432,439,374,543)}
def daycard(n):
    def run(G):
        px=G.px(0); px[:,:]=0; h,w=px.shape
        ms,caph=lines_mask(['Day %d'%n],w-8,40,[('dv',s,-2) for s in (36,34,32,30)])
        m,ct,ch=ms[0]; m=np.pad(m,((0,0),(0,2))); m[:,1:]|=m[:,:-1]; m[:,1:]|=m[:,:-1]
        fill=[1,1,2,3,4,5,6,7]
        fr=[fill[min(7,max(0,int((r-ct)*8/max(1,ch))))] for r in range(m.shape[0])]
        render(px,m,(w-m.shape[1])//2,(h-caph)//2-ct,fr,rings=[(0xd,2)])
        G.put(0,px)
    return run
def intro(G):
    px=G.px(0); px[:,:]=0; h,w=px.shape
    O=[('dvo',s,0) for s in (17,16,15,14,13)]
    ms,caph=lines_mask(['It was...','one summer day.'],w-30,h-8,O,gap=8)
    y=6
    for k,(m,ct,ch) in enumerate(ms):
        x=4 if k==0 else 30
        fr=[[1,2,3,4][min(3,max(0,int((r-ct)*4/max(1,ch))))] for r in range(m.shape[0])]
        render(px,m,x,y-ct,fr,rings=[(6,1)],shadow=(9,1,1)); y+=caph+12
    G.put(0,px)
for n in range(1,7): EFF[432+n]=daycard(n)
EFF[480]=intro
