import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0,_ROOT+'/tools')
from gedit import *
DV=lambda *s:[('dv',x,0) for x in s]
DVC=lambda *s:[('dvc',x,0) for x in s]
S16=DV(11,10)+DVC(10,9,8)
S8=DVC(8,7)
NAMEOPTS=DV(10)+DVC(10,9)+[('dvcr',10,0),('dvcr',9,0)]
LABELS={78:'Friendship',58:'Free Pocket',59:'Photo Shoot',63:'Ask',64:'Friendship',65:'Spirit',66:'HP',69:'Affinity',70:'Speed',71:'Stamina',
 103:'Active Party',104:'Reserve',105:'Swap Members',106:"Who's Who",107:'Name',109:'Glossary',110:'Stamina',111:'Friendship',112:'Spirit',
 114:'Status',115:'Ichigo Momomiya',116:'Mint Aizawa',117:'Lettuce Midorikawa',118:'Pudding Fong',119:'Zakuro Fujiwara',120:'Ringo Akai',
 121:'Mew Mew Members',124:'Save',125:'Load',126:'Endurance',127:'Defense',157:'Sort',158:'Voice',159:'OK',160:'Cancel',
 168:'Mew Mew Memo',169:'Animals',170:'Album',178:'Back',212:'Lv',214:'Power',221:'Moves',222:'Skills'}
BUTTONS={54:'Map',132:'Wait',145:'Attack',146:'Items',147:'Skills',148:'Switch',149:'Special',150:'Status',151:'Settings',213:'Run'}
def run(G):
    for i,t in LABELS.items():
        px=G.px(i); h,w=px.shape
        if h<=8:
            pal=G.pal(i); nz=sorted(set(px[px!=0].tolist()),key=lambda k:sum(pal[k][:3]))
            px[:,:]=0
            ms,caph=lines_mask([t],w-2,8,S8); m,ct,ch=ms[0]
            al=0 if w>30 else (w-m.shape[1]-1)//2
            render(px,m[:7],max(0,al),0,[nz[-1]]*8,shadow=(nz[0],1,1))
        else:
            opts=DV(20,19,18,17,16) if h>=28 else (NAMEOPTS if 115<=i<=120 else S16)
            relabel(px,t,opts,bold=1 if h>=28 else 0,pad=0 if 115<=i<=120 else 1)
        G.put(i,px)
    for i,t in BUTTONS.items():
        px=G.px(i); rowfill(px,14,66,ignore=(1,2,3,4))
        place(px,t,16,64,3,[1]*5+[2]*3,outline=4,shadow=(3,1,1)); G.put(i,px)
    px=G.px(206); h,w=px.shape
    rowfill(px,6,w-6,ignore=(8,9,10,11,12,13,14,15))
    text_block(px,['Item Points'],(7,4,w-7,h-4),S16,[8,8,9,10],rings=[(14,1)]); G.put(206,px)
