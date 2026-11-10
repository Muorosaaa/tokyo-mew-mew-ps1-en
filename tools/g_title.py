import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0,_ROOT+'/tools')
from gedit import *
def run(G):
    labels={4:'New Game',5:'Continue',6:'Explore Mode',7:'Options',11:'Animals',12:'Album',13:'Glossary',14:'Sound Mode',15:'Settings',16:'Movies'}
    for i,t in labels.items():
        px=G.px(i); rowfill(px,14,81,ignore=(1,2,3,4))
        place(px,t,16,79,3,[1]*5+[2]*3,outline=4,shadow=(3,1,1)); G.put(i,px)
    # "press a button" banner (entry 0, palette 2): yellow gradient, dark red outline
    px=G.px(0); px[:,:]=0
    place(px,'Press Any Button',2,126,3,[4,4,5,5,6,7,8,9,10],outline=12,shadow=(12,1,1),opts=(('dv',11,0),('dvc',11,0),('dv',10,0)))
    G.put(0,px)
