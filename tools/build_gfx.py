import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,time; sys.path.insert(0,_ROOT+'/tools')
import repack
from gedit import Gfx
def build(arc,jobs,out,leadlimit=False):
    orig=open(_ROOT+'/orig/%s.BIN'%arc,'rb').read()
    repl={}; hdr={}
    from lz import decompress
    import struct as _st
    n0,o0=repack.entries(orig)
    for i,fn in jobs.items():
        path=_ROOT+'/dec/%s/%03d.bin'%(arc,i)
        full,_=decompress(orig,o0[i]+4,10**8)          # full stream output (may exceed header size)
        hdr[i]=_st.unpack_from('<I',orig,o0[i])[0]
        assert full[:hdr[i]]==repack.raw(orig,i)
        G=Gfx(path,full); fn(G); repl[i]=bytes(G.d)
        assert len(repl[i])==len(full)
    import inplace
    new,rep=inplace.inplace(orig,repl,hdr,leadlimit); over=-sum(a-b for _,a,b in rep if isinstance(_,int)); extra=[]
    print('  skipped',[x[1] for x in rep if x[0]=='SKIPPED'])
    for x in rep:
        if x[0]=='SKIPPED': repl[x[1]]=None
    repl={k:v for k,v in repl.items() if v is not None}
    if new is None:
        # recompress biggest untouched entries until it fits
        n,o=repack.entries(orig)
        cand=sorted((o[i+1]-o[i],i) for i in range(n-1) if i not in repl and o[i+1]>o[i])[::-1]
        for _,i in cand:
            extra.append(i); new,over=repack.repack(orig,repl,extra)
            print('  recompressing',i,'over',over)
            if new is not None: break
    n,o=repack.entries(new)
    from lz import decompress
    import struct as _s
    for i in repl:
        st=o[i]; got,_=decompress(new,st+4,10**8)
        assert got==repl[i],('marker-decode mismatch',i,len(got),len(repl[i]))
    for i in range(n-1):
        r=repack.raw(new,i)
        assert r==(repl[i][:hdr[i]] if i in repl else repack.raw(orig,i)),('verify',i)
    assert len(new)==len(orig)
    open(out,'wb').write(new)
    return len(repl),extra,-over
def effect_jobs():
    import g_sfx2,g_tiles,g_batch3,g_sfx3,g_sfx4
    J=dict(g_sfx2.JOBS); J.update(g_batch3.EFF)
    for f,fn in g_tiles.JOBS.items():
        if f in J:
            a=J[f]; J[f]=(lambda G,a=a,b=fn:(a(G),b(G)))
        else: J[f]=fn
    for f,fn in g_sfx3.EJOBS.items():
        if f in J:
            a=J[f]; J[f]=(lambda G,a=a,b=fn:(a(G),b(G)))
        else: J[f]=fn
    J.update(g_sfx4.JOBS)   # 2, 109, 372, 375: simpler redraws that fit (replace the older jobs for those entries)
    import g_sfx5            # lettering found in the 2026-11-09 survey: chained after any existing job
    for f,fn in g_sfx5.JOBS.items():
        J[f]=(lambda G,a=J[f],b=fn:(a(G),b(G))) if f in J else fn
    import g_sfx6
    return _chain(J,g_sfx6.EFF)
def _chain(J,extra):
    J=dict(J)
    for f,fn in extra.items():
        J[f]=(lambda G,a=J[f],b=fn:(a(G),b(G))) if f in J else fn
    return J
def system_jobs():
    import g_batch1,g_sfx6
    return _chain(g_batch1.JOBS,g_sfx6.SYS)
def unit_jobs():
    import g_sfx3,g_sfx6
    return _chain(g_sfx3.UJOBS,g_sfx6.UNIT)
if __name__=='__main__':
    import g_batch1,g_batch3
    t=time.time()
    which=sys.argv[1:] or ['D_SYSTEM','D_EFFECT','D_UNIT']
    if 'D_SYSTEM' in which: print('D_SYSTEM',build('D_SYSTEM',system_jobs(),_ROOT+'/build/D_SYSTEM.BIN',True),round(time.time()-t))
    if 'D_EFFECT' in which:
        print('D_EFFECT',build('D_EFFECT',effect_jobs(),_ROOT+'/build/D_EFFECT.BIN',True),round(time.time()-t))

    if 'D_UNIT' in which:
        import g_sfx3
        print('D_UNIT',build('D_UNIT',unit_jobs(),_ROOT+'/build/D_UNIT.BIN',True),round(time.time()-t))
