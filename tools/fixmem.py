import re,sys
def fix(path,upd):
    s=open(path).read()
    for k,v in upd.items():
        pat=re.compile(r'\n%d:(".*?"|\'.*?\'),\n'%k,re.S)
        assert pat.search(s),k
        s=pat.sub(lambda m:'\n%d:%r,\n'%(k,v),s,count=1)
    open(path,'w').write(s)
