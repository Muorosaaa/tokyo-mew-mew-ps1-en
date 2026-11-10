"""One-command check (run by the pre-commit hook). Fast: no graphics rebuild.

1. orig/ files match orig.sha1
2. text build succeeds, outputs keep their original sizes, and no translated memory line was skipped
3. LZ codecs round-trip on a sample of archive entries (plain and lead-limited)
4. every translation-memory batch passes the box-width check
Exit 0 = ok.
"""
import os, sys, subprocess, hashlib, struct

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
sys.path.insert(0, os.path.join(ROOT, 'tr'))
fail = []

# 1
for line in open(os.path.join(ROOT, 'orig.sha1')):
    h, p = line.split()
    f = os.path.join(ROOT, p)
    if not os.path.isfile(f):
        fail.append('missing ' + p); continue
    if hashlib.sha1(open(f, 'rb').read()).hexdigest() != h:
        fail.append('hash mismatch ' + p)
if fail:
    sys.exit('check: original files: ' + '; '.join(fail))

# 2
r = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(ROOT, 'tools', 'build.py')],
                   capture_output=True, text=True, cwd=ROOT)
if r.returncode:
    print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit('check: text build failed')
if 'memory lines skipped (too long for slot): 0' not in r.stdout:
    fail.append('text build skipped translated lines')
for n in ('D_SCE.BIN', 'SLPM_871.78'):
    a = os.path.getsize(os.path.join(ROOT, 'orig', n)); b = os.path.getsize(os.path.join(ROOT, 'build', n))
    if a != b: fail.append('%s size changed %d -> %d' % (n, a, b))

# 3
import repack, lzopt, lzlead
from lz import decompress
d = open(os.path.join(ROOT, 'orig', 'D_SYSTEM.BIN'), 'rb').read()
for i in (7, 9, 20, 90):
    raw = repack.raw(d, i)
    for name, c in (('lzopt', lzopt.compress(raw)), ('lzlead', lzlead.compress(raw, 10 ** 9))):
        back, _ = decompress(struct.pack('<I', 0) + c, 4, 10 ** 8)
        if back != raw: fail.append('%s round-trip failed on D_SYSTEM entry %d' % (name, i))

# 4
for mod in ('mem_b1', 'mem_b2', 'mem_b3', 'mem_b4'):
    r = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(ROOT, 'tools', 'memcheck.py'), mod,
                        os.path.join(ROOT, 'data', 'todo_0_31.json')], capture_output=True, text=True, cwd=ROOT)
    if 'issues 0 of' not in r.stdout: fail.append('memcheck ' + mod + ': ' + r.stdout.strip()[-200:])
for mod in ('mem_c1', 'mem_c2', 'mem_c3', 'mem_c4'):
    r = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(ROOT, 'tools', 'memcheck.py'), mod,
                        os.path.join(ROOT, 'data', 'todo_all.json')], capture_output=True, text=True, cwd=ROOT)
    if 'issues 0 of' not in r.stdout: fail.append('memcheck ' + mod + ': ' + r.stdout.strip()[-200:])

if fail:
    print('\n'.join(fail)); sys.exit(1)
print('check: ok')
