import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
hira="ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろわをん"
kata="ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロワヲンヴヵヶ"
def load():
    t={}
    for i,c in enumerate(hira): t[i]=c
    for i,c in enumerate(kata): t[0x50+i]=c
    t.update({0xab:'ー',0xac:'、',0xad:'。',0xae:'？',0xaf:'！',0xb2:'…',0xb5:'「',0xb6:'」',0xc0:'～',0xc2:'○',0xc3:'×',0xc4:'△',0xc5:'□',0xc6:'♥',0xcb:'♪',0xcd:'―'})
    for l in open(_ROOT+'/data/kanji_tbl.txt'):
        if l.startswith('#') or not l.strip(): continue
        c,ch=l.rstrip('\n').split('\t'); c=int(c,16)
        ch=ch.rstrip('?') if ch!='?' else None
        if ch: t[c]=ch
    return t
