import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import struct,sys
sys.path.insert(0,_ROOT+'/tools')
from table import load
from encode import encode
S=0x1200e; END=0x12606; N=128
EN={'いちご':'Ichigo','みんと':'Mint','れたす':'Lettuce','歩鈴':'Pudding','ざくろ':'Zakuro','りんご':'Ringo',
    '白金':'Shirogane','赤坂':'Akasaka','マシャ':'Masha','真潮':'Mashio','ガトー':'Gateau','キッシュ':'Kisshu',
    '蒼の騎士':'Blue Knight','ミュウイチゴ':'Mew Ichigo','ミュウミント':'Mew Mint','ミュウレタス':'Mew Lettuce',
    'ミュウプリン':'Mew Pudding','ミュウザクロ':'Mew Zakuro','ミュウリンゴ':'Mew Ringo','ユキ':'Yuki','？？？':'？？？'}
def read(d):
    T=load(); out=[]
    for i in range(N):
        p=S+4*i+struct.unpack_from('<I',d,S+4*i)[0]
        j=d.index(b'\xff',p); s=d[p:j]
        out.append(''.join(T[(s[k]-0xf1)*256+s[k+1]] for k in range(0,len(s),2)))
    return out
def translate(jp):
    return ', '.join(EN[x] for x in jp.split('、')) if jp else ''
def build(d):
    d=bytearray(d); jp=read(d); en=[translate(x) for x in jp]
    pool={}; blob=bytearray(); base=S+4*N
    offs=[]
    for i,s in enumerate(en):
        if s not in pool:
            pool[s]=base+len(blob); blob+=encode(s)+b'\xff'
        offs.append(pool[s]-(S+4*i))
    assert base+len(blob)<=END,(base+len(blob),END)
    for i,o in enumerate(offs): struct.pack_into('<I',d,S+4*i,o)
    d[base:base+len(blob)]=blob; d[base+len(blob):END]=b'\xff'*(END-base-len(blob))
    return bytes(d),jp,en
if __name__=='__main__':
    d=open(_ROOT+'/orig/SLPM_871.78','rb').read()
    nd,jp,en=build(d)
    for i,(a,b) in enumerate(zip(jp,en)):
        if i<30 or '、' in a and i<70: print(i,a,'->',b)
    print('bytes used',len(set(en)))
