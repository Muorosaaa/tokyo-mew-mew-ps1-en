-- Tokyo Mew Mew (SLPM-87178) warp. Needs emu.py --debugger. Start from a cold boot with a New Game route.
-- MAP:   map id (= D_FIELD and D_SCE entry), written to 0x800FF708 right before the first map load after New Game.
-- FLAGS: "bit:nbits:value,..." story-flag fields (0x600-bit array at 0x800FF722, LSB-first), applied at the same moment.
--        e.g. "0x178:8:3" = progress counter 3.
-- POKE:  "addr:byte,..." raw RAM bytes, applied at the same moment. Day counter (save list "DayN"): 0x800FF83A.
-- SPATCH: see below.
local ffi = require("ffi")
local mem = ffi.cast("uint8_t*", PCSX.getMemPtr())
local function u16(a) a = a & 0x1fffff; return mem[a] | (mem[a+1] << 8) end
local function w16(a, v) a = a & 0x1fffff; mem[a] = v & 0xff; mem[a+1] = (v >> 8) & 0xff end
local MAPID, FLAGBASE = 0x800FF708, 0x800FF722
local function setfield(bit, n, v)
  for k = 0, n - 1 do
    local b = bit + k; local a = (FLAGBASE + (b >> 3)) & 0x1fffff; local m = 1 << (b & 7)
    if (v >> k) & 1 == 1 then mem[a] = mem[a] | m else mem[a] = mem[a] & (~m & 0xff) end
  end
end
local function getfield(bit, n)
  local v = 0
  for k = 0, n - 1 do local b = bit + k; if mem[(FLAGBASE + (b >> 3)) & 0x1fffff] & (1 << (b & 7)) ~= 0 then v = v | (1 << k) end end
  return v
end
_G.TMM = { setfield = setfield, getfield = getfield, u16 = u16, w16 = w16 }
local frame, done = 0, false
L.on_frame(function(n) frame = n end)
L.on_exec(0x8008244C, function()   -- field load: lhu a2, MAPID follows
  L.log(string.format("f%d map load %d", frame, u16(MAPID)))
  if done or not MAP then return end
  done = true
  w16(MAPID, MAP)
  for bit, n, v in string.gmatch(FLAGS or "", "([%dxa-fA-F]+):(%d+):([%dxa-fA-F]+)") do
    setfield(tonumber(bit), tonumber(n), tonumber(v))
  end
  for addr, v in string.gmatch(POKE or "", "([%dxa-fA-F]+):([%dxa-fA-F]+)") do
    mem[tonumber(addr) & 0x1fffff] = tonumber(v) & 0xff
  end
  L.log(string.format("  -> map %d flags %s (progress %d)", MAP, FLAGS or "-", getfield(0x178, 8)))
end)
-- SCRIPT=n: run D_SCE entry n instead of the map's own script at the first map load (the map's field still loads).
-- 0x80083D34 is right before the script load reads its entry number from 0x800FF828 (copied from the map id).
-- For the special entries no map jumps to (224/225 story scenes, 241-248, 254).
if SCRIPT then
  local swapped = false
  L.on_exec(0x80083D34, function()
    if swapped or not done then return end
    swapped = true
    w16(0x800FF828, SCRIPT)
    L.log(string.format("f%d script load -> entry %d", frame, SCRIPT))
  end)
end
-- TEXTFILE=path: show chosen dialogue boxes in the opening. The file holds ready-made script bytes (per message the
-- 14-byte box set-up `7b SPK 00 1f 0c FACE 10 1f 08 0a 04 00 28 00` + the message `78 ..` up to its FF, then a
-- self-jump), written by warp.py --lines from build/D_SCE.BIN. As soon as entry 0 (the New Game opening) is in RAM
-- at 0x801E8000 and before its first box (Ichigo's "Yaaay！", set-up at entry offset 0x473), the block is copied over it, so the
-- game draws each chosen line in its real box, one per circle press.
if TEXTFILE then
  local f = assert(io.open(TEXTFILE, "rb")); local blk = f:read("a"); f:close()
  local HEAD = { 0xa0, 0x00, 0x6b, 0x01, 0x84, 0x01, 0x82, 0x01 }     -- first bytes of entry 0
  local PRE = { 0x7b, 0x01, 0x00, 0x1f, 0x0c, 0x00, 0x10 }              -- entry 0 offset 0x473: the opening's first box
  local BASE, AT = 0x1E8000, 0x1E8000 + 0x473
  local placed = false
  L.on_frame(function(n)
    if placed then return end
    for k = 1, #HEAD do if mem[BASE + k - 1] ~= HEAD[k] then return end end
    for k = 1, #PRE do if mem[AT + k - 1] ~= PRE[k] then return end end
    for k = 1, #blk do mem[AT + k - 1] = blk:byte(k) end
    placed = true
    L.log(string.format("f%d textfile: %d bytes placed at entry 0 offset 0x473", n, #blk))
  end)
end
-- KILLPARTY=1: Game Over on demand. Battle units: 0x44-byte records at 0x801190F4 + i*0x44 (i 0-2 party, then
-- enemies; base pointer at 0x800FEACC). Record +0x0A flags (bit 0 = can act, bit 4 = knocked out), +0x24 HP,
-- +0x26 max HP. At the battle's first hit (0x80070FC0, inside the damage routine 0x80070F90) the whole party is set
-- to HP 0 + knocked out; the game notices within ~300 frames and plays the Game Over screen.
if KILLPARTY then
  local killed = false
  L.on_exec(0x80070FC0, function()
    if killed then return end
    killed = true
    for k = 0, 2 do
      local rec = 0x801190F4 + k * 0x44
      w16(rec + 0x24, 0)
      local a = (rec + 0x0a) & 0x1fffff
      mem[a] = (mem[a] & 0xfe) | 0x10
    end
    L.log(string.format("f%d killparty: party knocked out", frame))
  end)
end
-- SPATCH: "addr:oldhex:newhex,..." rewrites RAM whenever it still holds oldhex (checked every frame), so it also
-- survives script reloads. Map scripts sit at 0x801E8000 + offset in their D_SCE entry.
-- e.g. "0x801E9A8B:44041420:44041120" = map 4's sleep event shows card 0x11 instead of 0x14 (Day 4).
local spatch = {}
for addr, old, new in string.gmatch(SPATCH or "", "([%dxa-fA-F]+):(%x+):(%x+)") do
  local o, n = {}, {}
  for h in old:gmatch("%x%x") do o[#o + 1] = tonumber(h, 16) end
  for h in new:gmatch("%x%x") do n[#n + 1] = tonumber(h, 16) end
  if old:lower() ~= new:lower() then   -- old == new would match every frame
    spatch[#spatch + 1] = { a = tonumber(addr) & 0x1fffff, o = o, n = n, hits = 0 }
  end
end
if #spatch > 0 then
  L.on_frame(function(n)
    for _, p in ipairs(spatch) do
      local ok = true
      for k = 1, #p.o do if mem[p.a + k - 1] ~= p.o[k] then ok = false; break end end
      if ok then
        for k = 1, #p.n do mem[p.a + k - 1] = p.n[k] end
        p.hits = p.hits + 1
        L.log(string.format("f%d spatch %06x (%d)", n, p.a, p.hits))
      end
    end
  end)
end
