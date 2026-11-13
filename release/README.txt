Tokyo Mew Mew ~Toujou! Shin Mew Mew~ Minna Issho ni Gohoushi Suru Nyan (PS1)
English Fan Translation Patch  -  v1.1  (2026-11-12)
===========================================================================

Japan-only PlayStation RPG by Takara / Winkysoft (2002, SLPM-87178).
Title tagline: "Here Comes the New Mew Mew! We'll All Be at Your Service, Nya♥"

This patch is a WORK IN PROGRESS, made as a fun side hobby. It's fully
playable in English, but you may still run into a typo, an odd line or a
spot of leftover Japanese. Fixes will come in later versions.

Translation and code: Claude (an AI by Anthropic). The translation, the
text and graphics tools, and the patch were all made by Claude.


WHAT'S NEW IN v1.1
------------------
- The whole script got a polish pass for more natural English: about 450
  lines were rewritten, checked against the Japanese, so characters sound
  like themselves (Shirogane's teasing, Mint's airs, Akasaka's calm).
- Fixed lines that didn't make sense or said the wrong thing (for example,
  the cottage has 3 bedrooms, not 5; Ichigo turns into a cat when she gets
  nervous, not when she blushes).
- Restored Ichigo's "nya" and Pudding's "na no da" in lines that had
  dropped them.
- Akasaka no longer giggles "Hehe": he laughs "Ha ha" or just smiles.
- Item names in battle hints now match the item menu.

Already patched v1.0? Apply v1.1 to your ORIGINAL Japanese Track 1, not to
the v1.0 patched file. Your saves keep working.


WHAT'S TRANSLATED
-----------------
- All story and event dialogue, every branch
- Menus, items, skills and their descriptions, save/load messages
- Character profiles, album, item trade, guidebook (88 topics), animal
  encyclopedia (42 animals), cast list, ranger diary
- On-screen graphics: title menu, location banners, battle commands and HUD,
  field menu, name plates, Level Up!, Day 1-6 cards, Game Over, the boot
  warning screen, and the comic sound effects in battles and cutscenes

Names follow the original Japanese (Ichigo, Mint, Lettuce, Pudding, Zakuro,
Ringo, Shirogane, Akasaka, Kisshu). Honorifics are kept (-san, onee-chan,
onee-sama), Ichigo keeps her "nya" and Pudding her "na no da".

Left in Japanese on purpose:
- The title logo
- The staff credits (most staff names can't be romanized reliably)
- The memory card save titles (only shown by the PS1/emulator card manager)


WHAT YOU NEED
-------------
1. Your own copy of the Japanese disc, in Redump format. That's two .bin
   files (Track 1 and Track 2) plus a .cue file. This patch contains no
   game data, so you have to supply the game yourself.

2. The patch file from this zip: TokyoMewMew_en_v1.1.xdelta

3. A patching tool. No Python, command line or programming needed.
   Pick ONE of these:
   - Rom Patcher JS: runs in your web browser, nothing to install.
     https://www.marcrobledo.com/RomPatcher.js/
   - Delta Patcher (Windows): a small program, free. Search for
     "Delta Patcher" on GitHub to download it.

Your Track 1 file should be exactly:
     ...(Track 1).bin   589,989,792 bytes
     CRC32 DDC80CE1   MD5 0c77e4360b931dba18c7f08600a79136
     SHA-1 98d396f93c5fa25232ae5c54a046350dd4c09d47
If it doesn't match, the patch won't work. Try a fresh Redump-format dump.


HOW TO PATCH (step by step)
---------------------------
The patch only changes Track 1. Track 2 (the music track) stays as it is.

Before you start: make a copy of your game folder, so your original disc
image stays untouched.

Option A: Rom Patcher JS (in your browser)
  1. Open https://www.marcrobledo.com/RomPatcher.js/
  2. Next to "ROM file", choose your "(Track 1).bin" file. It's a big file
     (about 590 MB), so give it a moment to load. The page shows its
     CRC32; it should say DDC80CE1.
  3. Next to "Patch file", choose TokyoMewMew_en_v1.1.xdelta.
  4. Click "Apply patch". Your browser downloads the patched Track 1.
  5. Rename the downloaded file to:  TokyoMewMew_en (Track 1).bin

Option B: Delta Patcher (Windows)
  1. Open Delta Patcher.
  2. "Original file": choose your "(Track 1).bin" file.
  3. "XDelta patch": choose TokyoMewMew_en_v1.1.xdelta.
  4. Click "Apply patch". Delta Patcher writes the patched file in place of
     your Track 1 (that's why you made a copy first).

Then set up the disc so your emulator can load it:
  6. Put the patched Track 1 and your original Track 2 in the same folder.
  7. Make the .cue file point at the patched Track 1. The easiest way is to
     open your existing .cue in Notepad and change the Track 1 file name
     to the patched one. It should look like this (with your own
     Track 2 name):

FILE "TokyoMewMew_en (Track 1).bin" BINARY
  TRACK 01 MODE2/2352
    INDEX 01 00:00:00
FILE "Tokyo Mew Mew - Toujou Shin Mew Mew! Minna Issho ni Gohoushi suru nyan (Japan) (Track 2).bin" BINARY
  TRACK 02 AUDIO
    INDEX 00 00:00:00
    INDEX 01 00:02:00

  8. Load the .cue file in your emulator (DuckStation, for example).

To check the patch worked, the patched Track 1 should be:
     CRC32 CEB31835   MD5 8387bfec03b674264393ec49ee91a558
     SHA-1 fd6b3eed40e6ab857b550b695f8124cb8d309013
(Rom Patcher JS shows the CRC32 if you load the patched file as the ROM.)

Tested in DuckStation and PCSX-Redux. Saves from the Japanese version keep
working with the patched game.


FOR ADVANCED USERS
------------------
With xdelta3 on the command line:
  xdelta3 -d -s "original (Track 1).bin" TokyoMewMew_en_v1.1.xdelta "TokyoMewMew_en (Track 1).bin"


PATCH FILE
----------
TokyoMewMew_en_v1.1.xdelta   825,516 bytes   CRC32 C7563F4E
