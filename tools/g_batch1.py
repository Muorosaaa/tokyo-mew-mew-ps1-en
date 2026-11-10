import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0,_ROOT+'/tools')
from gedit import *
import g_title,g_loc,g_batch2,g_batch3,g_boot,g_day
DV=lambda *s:[('dv',x,0) for x in s]
DVT=lambda *s:[('dv',x,1) for x in s]
DVC=lambda *s:[('dvc',x,0) for x in s]
def sound(G):
    for i,t in ((12,'Play'),(14,'Stop')):
        px=G.px(i); px[:,:]=0; h,w=px.shape
        text_block(px,[t],(3,4,w-3,h-6),DV(14,13,12,11),[3,4,5,5,6],rings=[(14,1),(8,2)],shadow=(10,1,1))
        G.put(i,px)
    for i,t in ((13,'Play'),(15,'Stop')):
        px=G.px(i); px[:,:]=0; h,w=px.shape
        text_block(px,[t],(4,5,w-4,h-7),DV(18,17,16,15),[13,13,3,3,4],rings=[(14,1),(5,2),(9,3)],shadow=(11,1,1),bold=1)
        G.put(i,px)
    px=G.px(17); px[:,:]=0; h,w=px.shape
    text_block(px,['Sound Mode'],(1,2,w-3,h-3),DV(12,11,10),[5],rings=[(2,1)],shadow=(4,1,1))
    G.put(17,px)
def rooms(G):
    T={26:'Room for 2',27:'Room for 4',28:'Is this OK？',29:'Which one？',30:'Rooms',36:'Yes！',37:'No！'}
    for i,t in T.items():
        t=t.replace('？','?').replace('！','!')
        px=G.px(i); px[:,:]=0; h,w=px.shape
        text_block(px,[t],(4,4,w-4,h-5),DVT(17,16,15,14,13,12)+DV(11,10)+DVC(10,9),[5,4,4,4],rings=[(1,2),(3,3)],bold=1)
        G.put(i,px)
def plaques(G):
    T=['Mew Mew Members','Who\'s Who','Mew Mew Memo']
    for k,t in enumerate(T):
        for i,act in ((k,False),(k+3,True)):
            px=G.px(i); h,w=px.shape
            x0,x1=10,w-10; y0,y1=int(h*0.22),int(h*0.80)
            sub=px[6:h-6]; rowfill(sub,x0,x1,ignore=tuple(range(1,8))+(15,) if act else (8,9,0xc,0xd,0xe))
            if act: text_block(px,[t],(x0+6,y0+2,x1-6,y1-3),DVT(18,17,16,15,14,13),[15,1,2,3],rings=[(5,1),(7,2)],bold=1)
            else: text_block(px,[t],(x0+6,y0+2,x1-6,y1-3),DVT(18,17,16,15,14,13),[8,8,9,9],rings=[(13,1)],bold=1)
            G.put(i,px)
def trade(G):
    T={0:'Trade Items',1:'Your Item Points',2:'Points Needed',3:'You Have'}
    for i,t in T.items():
        px=G.px(i); h,w=px.shape
        rowfill(px,6,w-6,ignore=(8,9,10,11,12,13,14,15))
        text_block(px,[t],(7,4,w-7,h-4),DV(11,10)+DVC(10,9,8),[8,8,9,10],rings=[(14,1)])
        G.put(i,px)
    px=G.px(4); px[:,:]=0; h,w=px.shape
    text_block(px,['Item Trade'],(2,2,w-3,h-3),DV(12,11,10),[5],rings=[(2,1)],shadow=(4,1,1))
    G.put(4,px)
def explore(G):
    for i,t in ((0,'Explore'),(1,'Clear')):
        px=G.px(i); px[:,:]=0; h,w=px.shape
        text_block(px,[t],(1,3,w-1,h-4),DV(10,9)+DVC(9,8),[1,2,3,4,5,6],rings=[(11,1)])
        G.put(i,px)
    for i,t in ((30,'Day'),(31,'Night')):
        px=G.px(i); px[:,:]=0; h,w=px.shape
        text_block(px,[t],(1,3,w-1,h-4),DV(10,9)+DVC(9,8),[1,2,3,4],rings=[(15,1)])
        G.put(i,px)
def movies(G):
    px=G.px(0); h,w=px.shape
    x0,x1=34,w-34
    rowfill(px,x0,x1,ignore=(15,1,2,7))
    text_block(px,['Movie Collection'],(x0+8,8,x1-8,h-9),DV(14,13,12,11),[15,15,1,2],rings=[(7,1)],shadow=(8,1,1))
    G.put(0,px)
JOBS={2:g_batch3.tags,53:g_batch3.profile,0:g_batch2.run,9:g_title.run,33:g_loc.run,**{k:sound for k in range(40,49)},30:rooms,50:plaques,56:trade,24:(lambda G:(explore(G),g_day.day(G))),20:movies,55:g_boot.warn,   # 1: g_logo.run (ribbon) dropped 2026-11-08, user prefers the original logo
      **{83+k:(lambda G,k=k: g_loc.run_single(G,g_loc.NAMES[k])) for k in range(15)}}
