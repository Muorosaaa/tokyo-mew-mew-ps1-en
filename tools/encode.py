FW={'！':0xaf,'？':0xae,'…':0xb2,'「':0xb5,'」':0xb6,'・':0xb1,'（':0xb3,'）':0xb4,'“':0xbb,'”':0xbc,'♥':0xc6,'～':0xc0,'×':0xc3,'○':0xc2,'△':0xc4,'□':0xc5,'‼':0xbd,'『':0xb7,'』':0xb8,'＆':0xcc,'　':0xb0,'⁉':0xbe,'⁈':0xbf,'♪':0xcb,'、':0xac,'。':0xad}
def enc_char(c):
    if 'A'<=c<='Z': return bytes([ord(c)-64])
    if 'a'<=c<='z': return bytes([ord(c)-97+0x1b])
    if '0'<=c<='9': return bytes([ord(c)-48+0x36])
    one={' ':0x00,'.':0x40,',':0x41,':':0x42,';':0x43,"'":0x44,'/':0x45,'=':0x46,'+':0x47,'-':0x48,'%':0x4a}
    if c in one: return bytes([one[c]])
    if c=='\n': return b'\xfd'
    if c in FW: v=FW[c]; return bytes([0xf1+(v>>8), v&0xff])
    raise ValueError('no glyph for %r'%c)
def encode(s): return b''.join(enc_char(c) for c in s)
import re as _re
_raw=_re.compile(r'\{([0-9a-f]+)\}|<([0-9a-f]{2})>')
_plain=encode
def encode(s):
    out=b'';pos=0
    for m in _raw.finditer(s):
        out+=_plain(s[pos:m.start()]); out+=bytes.fromhex(m.group(1) or m.group(2)); pos=m.end()
    return out+_plain(s[pos:])
