import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0,_ROOT+'/tools')
from gedit import *
NAMES=['Strolling Woods','Cottage Woods','Forest of Truth','Tranquil Woods','Singing Wind Plains','Iceberg Hideout','Secret Cave','Mountain Path','Mystery Cave','Ranger Forest','Mystic Spring','Lovely Flower Field','Healing Grove','Ranger Cottage','Cottage']
O=[('dv',s,0) for s in (17,16,15,14,13,12)]+[('dvc',s,0) for s in (13,12,11,10,9)]
def draw(G,i,t):
    px=G.px(i); px[:,:]=0; w=px.shape[1]
    one,_=lines_mask([t],w-12,20,O[:4])
    lines=[t] if one[0][0].shape[1]<=w-14 else (t.rsplit(' ',1) if ' ' in t else [t])
    text_block(px,lines,(5,8,w-5,32),O,[4,5,5,6,6,6,6,7],rings=[(1,1),(6,2),(8,3)],shadow=(9,1,1),gap=4,bold=1)
    G.put(i,px)
def run(G,idxmap=None):
    for i,t in enumerate(NAMES):
        if i<len(G.E): draw(G,i,t)
def run_single(G,name):
    draw(G,0,name)
    end=max(e['off']+e['w']*e['h']//2 for e in G.E)
    G.d[end:]=bytes(len(G.d)-end)   # junk bytes after the image were drawn as a dotted line
