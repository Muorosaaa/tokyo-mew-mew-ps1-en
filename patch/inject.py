#!/usr/bin/env python3
"""Replace a file inside a PS1 .bin (raw 2352-byte sectors, Mode 2 Form 1)
with a same-size replacement, recomputing EDC/ECC.

usage:  python inject.py "Tokyo Mew Mew.bin" D_SCE.BIN
Make a backup copy of your .bin first!
"""
import sys, struct, os

# ---------- EDC / ECC (standard CD-ROM algorithms) ----------
EDC = []
for i in range(256):
    e = i
    for _ in range(8):
        e = (e >> 1) ^ (0xD8018001 if e & 1 else 0)
    EDC.append(e)
ECC_F = [0]*256; ECC_B = [0]*256
for i in range(256):
    j = (i << 1) ^ (0x11D if i & 0x80 else 0)
    ECC_F[i] = j & 0xFF
    ECC_B[i ^ j & 0xFF] = i

def edc(data):
    e = 0
    for b in data:
        e = EDC[(e ^ b) & 0xFF] ^ (e >> 8)
    return e

def ecc_block(sec, major_count, minor_count, major_mult, minor_inc, dest):
    size = major_count * minor_count
    for major in range(major_count):
        index = (major >> 1) * major_mult + (major & 1)
        a = b = 0
        for _ in range(minor_count):
            t = sec[12 + index]
            index += minor_inc
            if index >= size: index -= size
            a ^= t; b ^= t; a = ECC_F[a]
        a = ECC_B[ECC_F[a] ^ b]
        sec[dest + major] = a
        sec[dest + major + major_count] = a ^ b

def fix_sector(sec):
    # Mode 2 Form 1: EDC over subheader+data (16..2071), stored at 2072
    struct.pack_into('<I', sec, 2072, edc(sec[16:2072]))
    hdr = bytes(sec[12:16]); sec[12:16] = b'\0\0\0\0'   # header zeroed for ECC
    ecc_block(sec, 86, 24, 2, 86, 2076)   # P parity
    ecc_block(sec, 52, 43, 86, 88, 2248)  # Q parity
    sec[12:16] = hdr

# ---------- ISO9660 lookup ----------
def read_user(f, lba):
    f.seek(lba * 2352 + 24); return f.read(2048)

def find_file(f, name):
    pvd = read_user(f, 16)
    assert pvd[1:6] == b'CD001', 'not a PS1 data track (expected raw 2352-byte .bin)'
    root = pvd[156:156+34]
    lba, size = struct.unpack_from('<I', root, 2)[0], struct.unpack_from('<I', root, 10)[0]
    data = b''.join(read_user(f, lba + i) for i in range((size + 2047)//2048))
    i = 0
    while i < len(data):
        ln = data[i]
        if ln == 0:
            i = (i // 2048 + 1) * 2048; continue
        flba = struct.unpack_from('<I', data, i+2)[0]; fsize = struct.unpack_from('<I', data, i+10)[0]
        nl = data[i+32]; fname = data[i+33:i+33+nl].decode('ascii', 'replace').split(';')[0]
        if fname.upper() == name.upper(): return flba, fsize
        i += ln
    raise SystemExit('%s not found in disc root' % name)

def main():
    if len(sys.argv) != 3: print(__doc__); return
    binpath, newfile = sys.argv[1], sys.argv[2]
    new = open(newfile, 'rb').read()
    with open(binpath, 'r+b') as f:
        lba, size = find_file(f, os.path.basename(newfile))
        if size != len(new):
            raise SystemExit('size mismatch: disc %d vs new %d' % (size, len(new)))
        for k in range((size + 2047)//2048):
            f.seek((lba + k) * 2352); sec = bytearray(f.read(2352))
            if sec[18] & 0x20: raise SystemExit('unexpected Form 2 sector')
            chunk = new[k*2048:(k+1)*2048]
            sec[24:24+len(chunk)] = chunk
            fix_sector(sec)
            f.seek((lba + k) * 2352); f.write(sec)
    print('Replaced %s (%d bytes at LBA %d). Done.' % (os.path.basename(newfile), size, lba))

if __name__ == '__main__': main()
