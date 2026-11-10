# Formats

## Archives (D_*.BIN)
- u32 offset table; entry i starts at `table[i] + 4*i`. Each entry: u32 decompressed size, then an LZ stream (`tools/lz.py`, ported from MIPS at 0x8003fb0c).
- The size header can be a few bytes short of what the stream really produces; keep the full stream output (`build_gfx.py` does).
- LZ: flag bits MSB-first; 1 = literal; 01 = long copy (2 bytes: offset = (w>>3)-0x2000, len = (w&7)+2, or len byte+1 when w&7==0; len byte 0 = end marker); 00 = short copy (2 bits len+2, 1 byte offset-0x100). Streams end with the 01-00-00-00 end marker; the game stops there, not at the size.
- The game decompresses (at least some entries) in place: output must never run further ahead of input than in the original stream (`lzlead.lead_profile`). Use `lzlead.compress` via `inplace.py --leadlimit`.
- Images: `0x71 'X'/'_'` 4bpp with 16-colour palettes per entry (`a[0]` = palette), `0x51` 8bpp. Entry table at 4: 16 bytes each (offset, attrs, w, h, x, y). `tools/gfx.py`, `tools/gedit.py`.

## D_SCE.BIN (scripts)
- 256 entries, uncompressed bytecode. Text op 0x78 + mode; odd mode (0x13) = speaker byte + 00 before text. Messages patched in place, padding 0x23; overflow relocated via op 01 (pc = addr+1+s16).
- One entry per map id: entering map N loads D_FIELD entry N and D_SCE entry N (the script is copied to 0x801E8000). Several maps are the same room on different days (4 and 5 = Ichigo's bedroom on two nights; 77/78, 86/87, 94/95 likewise). Entries 224-254 are special (224/225 long story scenes, 241-245 per-character, 248 "collection complete", 254 iceberg).
- Interpreter: context at 0x800FF4B8 (+0x40 pc pointer, +0x54 copy of the current instruction), handler table 0x800FA7B4 (one u32 per opcode).
- Ops worked out (2026-11-08): `11 lo hi` set/clear one flag bit (bit = u16 & 0x7fff, bit 15 = value). `12 bit:u16 n val:u16` store n-bit field. `14 rel:s16 bit:u16` jump on one flag (bit 15 negates). `15 rel:s16 bitmode:u16 n val:u16` compare n-bit field (low 14 bits = bit, top 2 = eq/ne/lt/gt). `40 19 50 06 03 MAP ENTRANCE` = go to map.

## Game state (RAM, 2026-11-08)
- Load requests: `0x8003C544(flags, file, entry, ...)`; file ids from table 0x800E1FD0: 1 UNIT, 2 SCREEN, 3 SYSTEM, 4 SCE, 5 ANIME, 6 EFFECT, 7 FACE, 8 FIELD. The map's field load is at 0x80082454 (`lhu a2, 0x800FF708`), its script load at 0x80083D20.
- 0x800FF708 u16: current map id. 0x800FF828: copy used for the script load (0x800FF826 looks like the entrance).
- 0x800FF722: story flags, 0x600 bits (0xC0 bytes), bit b = byte b>>3, mask 1<<(b&7); n-bit fields are LSB-first (helpers 0x80071E1C set, 0x80071EDC read).
- Field 0x178 (8 bits): event progress counter; map scripts branch on it (map 4: 1 = night chat, 21 = save prompt -> Day card -> "You slept soundly"). Field 0x17E (4 bits) is also an event condition (setting it on map 4 suppresses the sleep event). Field 0x1B0 (16 bits) is compared with 0-4 in many maps.
- Save data = RAM from 0x800FF520 (card block offset 0x238 onward). Card block 1 = system data (`...MYUMYUS`), block 2 = save slot A (`...MYUMYUA`).
- Day counter: **0x800FF83A** (u8, base+0x31A), what the save list shows as "DayN" (checked 2026-11-09: poke 3 -> "Day3"). Save header word at block offset 0x200, built at 0x80079078: `0xFC | map<<8 | day<<16 | flagfield(0x68, 8 bits)<<24` (field 0x68 = 1 after a warp, 2 on the user's Day 2 save; unknown meaning, maybe a chapter). The old candidates 0x800FF5F9/5E9/772 do not feed it.
- Day/time cards are script op `1E 05 44 04 NN 20 A0 00 78 00` (NN = card; map 4's sleep event at entry offset 0x1A89 uses 0x14 = "Day 4", which loads ANIME/EFFECT entry 436). The card is chosen by the script, not by the day counter. NN 0x10-0x17 occur in entries 0, 1, 2, 4, 5, 39, 224, 225.
- User's card (work/card.mcd): slot 01 map 34, progress 16, Day 2 night; slot 02 map 44, Day 2 day. All slots live in card block 2: header words at 0x200 + slot*4, slot data at 0x238 + slot*0x328.

## Special scripts (2026-11-09, unfinished)
- Script ops that load another D_SCE entry: `0B lo hi` = jump to entry (handler 0x800771E4; starts at byte 0 of the entry), `44 77 E_lo E_hi I_lo I_hi` = call entry E at sub-scene I with return (handler 0x80091DA4; sub-op table 0x800FAE74, sub byte = instruction byte 1; I indexes the entry's self-relative u16 table, offset = s16(table[I]) + 2 + 2*I), `5F` = load entry 254 (0x800926B8). Op 0x23 (0x8007EDE8) loads the map script.
- Entries 224/225 start with a 0x202-byte table (257 slots; 224 has ~9 distinct sub-scenes, 225 has 2): sub-scene libraries for 44 77. 241-248 have no header (start with code); 254 has a 10-byte header.
- Nothing in D_SCE or the EXE contains `0B`/`44 77` with 224/225/241-248 (only `0B F2 00` in entries 61/65/83 and `0B FD 00` in the EXE at 0x7427), so the callers are probably in data not unpacked yet (D_FIELD?) or build the number at run time.
- Tried with warp.lua (map 4 sleep event patched at 0x801E9A89): `0B F6 00` (246) plays a Shirogane night scene in English, then hangs on Ichigo's "Bleh!"; `0B FE 00` (254) hangs on the cottage background; `0B E0/E1` crashes (runs the offset table as code); `44 77 E0/E1 00 00 00` plays nothing and the night continues normally. Loading them as map scripts (warp.lua SCRIPT=n) does nothing: map scripts start through their entry-point header.

## Battle (RAM, 2026-11-09)
- Units: 0x44-byte records at `*(0x800FEACC)` = 0x801190F4 + i*0x44; i 0-2 = party in order (Ichigo first on slot 02), then enemies. Record +0x0A u16 flags (bit 0 = can act, bit 4 = knocked out, bit 0x100 = HP changed, 0x8000 checked by the damage routine), +0x24 HP, +0x26 max HP, +0x28 pending HP delta (s16).
- Damage routine 0x80070F90(unit): HP += delta, clamped to 0..max; it doesn't knock anyone out. The KO happens when a unit with 0 HP is hit (first party member's KO turned flag byte 0x01 -> 0x10). Callers 0x8004CC80 (multi-target loop) / 0x8004CD50 (single); target unit byte at `*(0x800FEAB0) + 0x1CD1`.
- Game Over: all three party records knocked out (HP 0, flags |= 0x10, &= ~1) -> the game plays the Game Over screen within ~300 frames.

## Text encoding
- F1–F9 xx = glyph (b-0xF1)*256+xx: hiragana 0+, katakana 0x50+, kanji ~0xC0+ (`data/kanji_tbl.txt`).
- Half-width English font: A–Z 0x01–0x1A, a–z 0x1B–0x34, 0–9 0x36–0x3F, space 0x00, `. , : ; ' / = + - %` = 0x40–0x4A.
- FD newline, FF end, FC template code (3 bytes, 5 if 3rd byte is 0x3C). Dialogue box 30 half-width per line, 3 lines, line 3 max 28. Full-width = 1.45 half-width.

## EXE (SLPM_871.78)
- Self-relative u32 string tables: 0xefbc (208), 0x107e9 (256 menu), 0x1200e (128 names), 0x12606 (256 items), 0x13d86 (255 skills), 0x1c61c (192 skill descs).
- Guidebook strings 0x1638b–0x1c2bd (table 0x1600b, 224); animal book 0x1f412–0x22aa3 (tables 0x1f112/64, 0x1f212/128). Rewritten sequentially by `seqblock.py`.
- Inline save/load strings 0xbc00–0xd400; embedded script 0x800–0xbc00 and 0xdd00–0xe800.

## Sound effects (D_EFFECT, D_UNIT)
- Whole-word images (e.g. どかっ!) and kana tiles (one kana per small image, flown in one by one). Tile words were grouped by consecutive entry index, split after "!" tiles (`tools/tiles.py`, `data/words2.pkl`); lone tiles clustered by shape (`data/single_cl.pkl`).

## D_SCREEN / D_UNIT images (2026-11-09)
- D_SCREEN: one 8bpp image per entry (magic 0x5851, 256-colour palette). Most are stored as 32x32 tiles, row-major (tile = 32 rows of 32 bytes); entries 018 and 127-159 (384x256 room/field backdrops) are plain row-major. Pick the layout that gives smoother rows (see the survey script in the 2026-11-09 session; gfx.image() alone draws the tiled ones scrambled).
- D_UNIT: 0x71 4bpp sprite sheets, gfx.image() works. Lettering tiles are the ones with an opaque saturated background box: entries 31, 38, 64-67, 69, 71, 73, 78, 79 (all translated now).
- Unit graphics are loaded by script op `40 00 SLOT ENTRY` (e.g. `40 00 02 22` = unit 34 into slot 2); most sound-effect units are not loaded that way (probably from D_FIELD data).
