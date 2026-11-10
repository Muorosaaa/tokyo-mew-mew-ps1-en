"""Day counter (D_SYSTEM 024, image 2): the game draws a digit, then 日目 to its right ("2日目" = Day 2).
English needs the word first, so image 2 becomes "Day" and its anchor (the x field of its entry, which the game
subtracts from the draw position, like the centred anchors elsewhere in D_SYSTEM) moves it left of the digit:
"Day 2". The digit is ~10 px wide and sits right before where 日目 started.
"""
import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,struct; sys.path.insert(0,_ROOT+'/tools')
from gedit import *

SHIFT=38   # image 28 px; text set in its x 5..25 so it ends 2 px before the digit and clears the slot's faces

def day(G):
    px=G.px(2); px[:,:]=0; h,w=px.shape
    text_block(px,['Day'],(5,2,25,h-3),[('dvc',s,0) for s in (13,12,11,10)],[1,1,2,3,4],rings=[(11,1)],shadow=(9,1,1))
    G.put(2,px)
    struct.pack_into('<H',G.d,12+16*2+4,SHIFT)    # entry 2: w,h,x,y at 12+16*i; x = anchor
    G.E[2]['x']=SHIFT
