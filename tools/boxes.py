"""Box sizes that were fitted to the Japanese text (EXE, 2026-11-23).

1. Battle popups (window 7, the one-line/two-line boxes in the middle of the battle screen). Their size is not
   measured from the text: each battle script opens the box with op `a0 07 06 X 00 58 00 W H` (x in px, W and H in
   8-px units) sized for its Japanese message, and the message is chosen later by code from the skill's effect.
   Each box gets W = the widest English popup message whose Japanese would have fitted the original box (so every
   message that could appear there fits), centred.
2. Skill-learned messages (sys_efbc 136 "X taught you Y!", 137 "X learned Y!"): the box width counted the skill name
   two bytes at a time (one Japanese glyph = 12 px), so English names came out ~half width, and an odd-length name
   ran on into the next string (screen-wide box). Replaced by a call to the game's own width routine 0x8005a76c
   (8 px per half-width char, 12 per full-width) plus room for the rest of the message.
3. The field item menu's target list (name_list).
"""
import os as _os, re, struct
R=lambda a:a-0x80010000+0x800
MSGW=0x8005a76c

def _tables(d):
    p=struct.unpack_from('<I',d,R(0x8001E770))[0]
    return [p+struct.unpack_from('<I',d,R(p)+4*t)[0]+4*t for t in range(12)]
def string(d,mid):
    t=_tables(d)[mid>>8]; q=R(t)+4*(mid&0xff); s=q+struct.unpack_from('<I',d,q)[0]; e=s
    while d[e]!=0xff:
        b=d[e]; e+= 2 if 0xf0<=b<=0xfa else (5 if d[e+2]==0x3c else 3) if b==0xfc else 1
    return d[s:e]
def widths(b):
    """pixel width of each line, as the game draws it (half 8, full 12, a {fcffff} value ~24)"""
    L=[0]; i=0
    while i<len(b):
        c=b[i]
        if c==0xfd: L.append(0); i+=1
        elif c==0xfc:
            if b[i+1]==0xff: L[-1]+=24
            i+= 5 if b[i+2]==0x3c else 3
        elif c>=0xf1: L[-1]+=12; i+=2
        else: L[-1]+=8; i+= 2 if c==0xf0 else 1
    return L

# messages the battle code shows in popups (efbc ids; 133/136-138/141-143/146/148-159 are other windows)
POPUPS=[i for i in range(128,207) if i not in (133,136,137,138,141,142,143,146)+tuple(range(148,160))]+[0x3cd,0x3d2,0x3d4,0x3d5]
A0=re.compile(rb'\xa0\x07\x06(.)\x00\x58\x00(.)(.)',re.S)
def battle_popups(orig,d,regions=((0x800,0xbc00),(0xdd00,0xe800)),log=None):
    one=[];two=[]
    for m in POPUPS:
        j=widths(string(orig,m)); e=widths(string(d,m))
        (one if len(j)==1 else two).append((max(j),max(e),m))
    d=bytearray(d); n=0
    for a,b in regions:
        for mm in A0.finditer(bytes(d[a:b])):
            x,w,h=mm.group(1)[0],mm.group(2)[0],mm.group(3)[0]
            if not (3<=w<=40 and 4<=h<=12 and x%8==0): continue
            inner=w*8-24
            need=max([e for j,e,_ in (one if h<6 else one+two) if j<=inner]+[inner])
            nw=min(38,max(w,(need+24+7)//8))
            if nw!=w:
                nx=(320-nw*8)//2//8*8; p=a+mm.start()
                # the text area (op a2 07 07 X Y ..) starts one unit inside the box: move it with the box
                q=bytes(d[p+9:p+40]).find(b'\xa2\x07\x07')
                if q<0 or d[p+9+q+3]!=x//8+1:
                    if log is not None: log.append(('no text op',hex(p)))
                    continue
                d[p+9+q+3]=nx//8+1
                d[p+3]=nx; d[p+7]=nw; n+=1
                if log is not None: log.append((hex(p),w,nw,x,nx))
    return bytes(d),n

def _enc_i(op,rs,rt,imm): return struct.pack('<I',(op<<26)|(rs<<21)|(rt<<16)|(imm&0xffff))
def _jal(t): return struct.pack('<I',(3<<26)|((t>>2)&0x3ffffff))
def _j(t): return struct.pack('<I',(2<<26)|((t>>2)&0x3ffffff))
NOP=b'\0\0\0\0'
A0_,V0,T0,S0,S2=4,2,8,16,18
def _patch(d,start,end,cont,idxreg,table,extra):
    """replace [start,end) with: a0=idxreg|table<<8; v0=msgwidth(a0); t0=v0+extra; goto cont"""
    code=(_enc_i(0x0d,idxreg,A0_,table<<8)+_jal(MSGW)+NOP+_enc_i(0x09,V0,V0,extra)+_enc_i(0x0c,V0,T0,0xffff)
          +_j(cont)+NOP)
    n=(end-start)
    assert len(code)<=n
    code+=NOP*((n-len(code))//4)
    d[R(start):R(end)]=code
def learn_boxes(d):
    d=bytearray(d)
    # 137 "{names}\nlearned\n{skill}!": skill name (table 4) + 56 px
    for a,want in ((0x800a2d58,'0280043c'),(0x800a2de4,'21202002'),(0x800a2a0c,'0280043c'),(0x800a2a9c,'21202002')):
        assert d[R(a):R(a)+4].hex()==want,hex(a)
    _patch(d,0x800a2d58,0x800a2de4,0x800a2de4,S0,4,56)
    # 136 "{teacher} taught you {skill}!": skill name (table 8, entries <32) + 204 px (teacher name and the rest)
    _patch(d,0x800a2a0c,0x800a2a9c,0x800a2a9c,S0,8,204)
    return bytes(d)

def name_list(d):
    """3. Field item menu, "Choose who uses it." list (window 6): fixed 64 px wide, 6 half-width chars inside;
    Lettuce/Pudding are 7. 72 px."""
    d=bytearray(d); p=R(0x800b4028)
    assert d[p:p+4]==bytes.fromhex('40000324'),d[p:p+4].hex()
    d[p:p+4]=bytes.fromhex('48000324'); return bytes(d)

def apply(orig,d,log=None):
    d=name_list(learn_boxes(d))
    return battle_popups(orig,d,log=log)
