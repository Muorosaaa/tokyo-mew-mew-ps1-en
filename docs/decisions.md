# Decisions

- **Names and honorifics:** keep the original Japanese names (Ichigo, Mint, Lettuce, Pudding, Zakuro, Ringo, Ryou Shirogane, Keiichiro Akasaka, Mashio Akai, Kisshu, Gateau du Roi) and honorifics (-san, -kun, onee-chan, onee-sama). Pudding keeps "na no da", Ichigo keeps "nya". (User, at project start.)
- **Terms:** パラパラ = "Parapara", コンゲン = "Source", キメラアニマ = "Chimera Anima", レッド・データ・アニマルズ = "Red Data Animals", リボーン… = "Ribbon …" attacks.
- **Place names:** Cottage Woods, Strolling Woods, Forest of Truth, Tranquil Woods, Singing Wind Plains, Mystic Spring, Lovely Flower Field, Healing Grove, Ranger Forest, Ranger Cottage, Mountain Path, Iceberg Hideout, Secret Cave, Mystery Cave. Narrow menu boxes use short forms (Cottage Wds, Stroll Woods).
- **Battle HUD tags:** first names only (Mew prefix unreadable at that size); enemy tags "Chimera", "Parasite".
- **Sound effects:** translated to English comic onomatopoeia in the original colours; tile-based ones split across the same tiles, "!" tiles kept.
- **Graphics text is in scope**, including sound effects.
- **Testing:** the user tests each build in their emulator and sends screenshots; with this repo, boot builds with emu.py first.
- **Delivery to the user:** built files + `patch/patch.bat`, which injects into their own Track 1 .bin and keeps a `.original` backup.
- **Staff credits stay Japanese** (D_EFFECT 602, 129 one-line strips; user, 2026-11-09). The strips are legible, but most staff names are kanji with several possible readings and no public English credit to check, so a wrong romanization was judged worse than leaving them. Lines 122-126 are already English. Contact sheets: work/credits/credits_0.png, credits_1.png.
- **Memory-card save titles stay Japanese** (EXE 0x2a60 "東京ミュウミュウ　　　データ００", 0x2a84 "東京ミュウミュウ　システムデータ"; user, 2026-11-09). Only the PS1 BIOS / emulator memory-card manager shows them, never the game.
- **Mint's voice** (user, 2026-11-09): she keeps a prim, superior ojou-sama register in English (わたくし/ですわ): "I suppose", "Whatever do you mean？", "dear", "Naturally." ~170 of her 279 unique lines were reworded; the rest already had it. Pudding's "na no da" and dropped honorifics were deliberately NOT restored (user call).
