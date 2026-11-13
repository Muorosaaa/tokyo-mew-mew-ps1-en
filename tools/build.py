import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,importlib,struct,hashlib
sys.path.insert(0,_ROOT+'/tools');sys.path.insert(0,_ROOT+'/tr')
from sdis import entry_bounds,textlen
from patcher import find_messages,rebuild
from fit import check
import names
ENTRIES=[0,2,3,4,5,6,7,24,29,30,31,224]
def _mem():
    from msgs import dec
    d=open(_ROOT+'/orig/D_SCE.BIN','rb').read(); B=entry_bounds(d); mem={}
    for n in ENTRIES:
        TR=importlib.import_module('e%03d'%n).TR; s,t=B[n]; e=d[s:t]; M=find_messages(e)
        for k,v in TR.items(): mem.setdefault(dec(e[M[k]['text_at']:M[k]['end']-1]),v)
    return mem
MEM=_mem()
import json as _json, importlib as _il
_L=_json.load(open(_ROOT+'/data/todo_0_31.json'))
for _mod in ('mem_b1','mem_b2','mem_b3','mem_b4'):
    for _i,_v in _il.import_module(_mod).T.items(): MEM.setdefault(_L[_i][0],_v)
_L2=_json.load(open(_ROOT+'/data/todo_all.json'))
for _mod in ('mem_c1','mem_c2','mem_c3','mem_c4'):
    for _i,_v in _il.import_module(_mod).T.items(): MEM.setdefault(_L2[_i][0],_v)
from extra_sce import X as EXTRA
# naturalness-pass overrides for lines that come from translation memory (keyed by Japanese; tr/natural.py)
from natural import N as _NAT
MEM.update(_NAT)
SKIPPED=[]
SHORT={'_この先“遊歩の森”':'“Strolling Woods”','「りょうかいなのだ！」':'Roger, na no da！','「よかったらこれ……」':'Take this, if you like'}
def build_sce():
    d=bytearray(open(_ROOT+'/orig/D_SCE.BIN','rb').read())
    B=entry_bounds(bytes(d)); report=[]
    for n in range(256):
        if B[n][1]-B[n][0]<8: continue
        TR=dict(importlib.import_module('e%03d'%n).TR) if n in ENTRIES else {}
        for k,t in TR.items(): assert not check(t),(n,k,check(t))
        s,t=B[n]; e=bytes(d[s:t]); M=find_messages(e)
        # messages find_messages misses (tr/extra_sce.py), appended so existing indexes don't shift
        for at,_jp,en in EXTRA.get(n,[]):
            assert e[at]==0x78 and not (e[at+1]&1),(n,hex(at))
            p=at+2; M.append(dict(at=at,hdr=e[at:p],text_at=p,end=p+textlen(e,p),spk=None,mode=e[at+1]))
            assert not check(en),(n,hex(at),check(en)); TR[len(M)-1]=en
        # fill from translation memory (identical Japanese elsewhere)
        from msgs import dec as _dec
        for k,m in enumerate(M):
            if k not in TR:
                j=_dec(e[m['text_at']:m['end']-1])
                if j in MEM:
                    from encode import encode as _enc
                    if len(m['hdr'])+len(_enc(MEM[j]))+1<=m['end']-m['at']: TR[k]=MEM[j]
                    elif j in SHORT and len(m['hdr'])+len(_enc(SHORT[j]))+1<=m['end']-m['at']: TR[k]=SHORT[j]
                    else: SKIPPED.append((n,k))
        try: ne,nover=rebuild(e,M,TR)
        except RuntimeError as x: raise RuntimeError("entry %d: %s"%(n,x))
        assert len(ne)==len(e)
        # verify: messages re-parse to expected text, jumps land correctly
        d[s:t]=ne
        if TR: report.append((n,len(TR),nover))
    return bytes(d),report
def build_exe():
    import exeblock
    d=open(_ROOT+'/orig/SLPM_871.78','rb').read()
    nd,_,_=names.build(d)
    SYS=importlib.import_module('sys_efbc').TR
    nd,free=exeblock.rebuild(nd,0xefbc,208,SYS)
    print('system text block: %d bytes free'%free)
    import jpblock,limits
    for S,N,mod,lim,ex in ((0x107e9,256,'blk_menu',limits.menu,range(215,244)),(0x12606,256,'blk_items',limits.items,()),(0x13d86,255,'blk_skills',31.9,()),(0x1c61c,192,'blk_skilldesc',limits.skilldesc,())):
        nd,iss=jpblock.apply(nd,S,N,importlib.import_module(mod).TR,lim,ex)
        assert not iss,(mod,iss)
        print('block %s ok'%mod)
    import inlinepatch
    nd,n,iss=inlinepatch.apply(nd,0xbc00,0xd400,importlib.import_module('inline_save').TR)
    assert not iss,iss; print('save/load messages: %d'%n)
    import exescript
    T=importlib.import_module('exe_script').TR
    nd,n1,i1=exescript.apply(nd,0x800,0xbc00,T); nd,n2,i2=exescript.apply(nd,0xdd00,0xe800,T)
    assert not (i1 or i2),(i1,i2); print('profile/album/trade/guide lines: %d'%(n1+n2))
    import json as _j
    from inline_misc_en import E as _E
    _K=_j.load(open(_ROOT+'/data/inline_misc.json')); MTR={_K[i]:v for i,v in _E.items()}; tot=0
    for a,b in ((0x8300,0x8a00),(0x9500,0x9530),(0xa080,0xa0c0),(0xa100,0xa500),(0xd380,0xd700),(0xe6f0,0xe900)):
        nd,n,iss=inlinepatch.apply(nd,a,b,MTR); tot+=n
        iss=[x for x in iss if not (x[0]=='wide' and x[1]=='0xe787')]; assert not iss,iss
    print('profile/album/save/diary leftovers: %d'%tot)
    import seqblock,encyc
    ETR,eiss=encyc.build(); assert not eiss,eiss
    nd,n,free=seqblock.apply(nd,0x1638b,0x1c2bd,[(0x1600b,224)],ETR); print('guidebook: %d strings, %d bytes free'%(n,free))
    # 0x228a0-0x22aa3 is a data table, not text, and entry 127 of 0x1f212 points at it (fixed 2026-11-09:
    # the old end 0x22aa3 / 128 entries filled that table with FF padding)
    nd,n,free=seqblock.apply(nd,0x1f412,0x228a0,[(0x1f112,64),(0x1f212,127)],ETR); print('animal book: %d strings, %d bytes free'%(n,free))
    return nd
if __name__=='__main__':
    sce,rep=build_sce(); exe=build_exe()
    open(_ROOT+'/build/D_SCE.BIN','wb').write(sce)
    open(_ROOT+'/build/SLPM_871.78','wb').write(exe)
    for r in rep: print('entry %d: %d lines, %d moved'%r)
    print('memory lines skipped (too long for slot):',len(SKIPPED))
    for f in ('D_SCE.BIN','SLPM_871.78'):
        print(f,hashlib.md5(open(_ROOT+'/build/'+f,'rb').read()).hexdigest())
