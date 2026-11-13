import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# script entry 0 – opening (msgs 0-37 from pilot) + cottage arrival (38-49)
import sys; sys.path.insert(0,_ROOT+'/pilot')
from scene0 import TR as _P
TR = dict(_P)
TR.update({
38: "Meet the Mew Mew members？\n  「Sure！」\n  「Not now」",
39: "This is the terrace.\nIt's so warm and cozy～",
40: "Okay, that's enough looking\naround. Maybe I'll go chat\nwith everyone.",
41: "I could go outside from here…\nbut I'd better stay inside\nuntil the others get back.",
42: "Oh, Ichigo onee-chan！\nPerfect timing！ Let's go\nexplore together, na no da！",
43: "Exploring？ We're supposed to\nbe house-sitting. If we slack\noff, we might lose dinner！",
44: "Uuu～ Okay, na no da. Too bad.\nThanks for warning me！ You\nsaved my dinner, na no da！",
45: "You're exaggerating～\nBut don't wander off, OK？",
46: "Roooger that, na no da！",  # deliberately 2 bytes over: tests relocation
47: "It's okay, na no da.\nI'll be patient, na no da.\nThanks for caring, na no da.",
48: "Heh heh heh…",
49: 'Now then… what shall I do\nwith you？ Kukukuku…',
})
SAVE="Save your game？\n   「Sure！」\n   「Not now」"
TR.update({
50: SAVE,
51: "You slept soundly.\nEveryone's HP is fully\nrestored！",
52: 'Chimera Animas appeared,\nPudding went missing, and\nthey met a girl named Ringo',
53: "and her friend, a penguin\nnamed Yuki-chan…",
54: 'After an eventful Day 1,\nIchigo woke up refreshed and\nset on “having a blast.”',
55: "But then…",
56: 'Yaaawn…',
57: "Hm？",
58: "（Huh？ They look serious…\nWhat's going on？）",
59: "…Right. It was in R-2000's\nrecords too, wasn't it？",
60: "Yes. It's too early to say,\nbut the penguin Ichigo-san met\nmay be the RDA we're after.",
61: "（What they're after…？）",
62: '（No, no, Ichigo！\nEavesdropping is bad…）',
63: "Yeah. It's still a chick, but\nit's a Humboldt penguin, sure.\nNow to get the girls on it.",
64: 'Why not just ask them\nnicely？',
65: "How's that any fun？",
66: "Sigh…",
67: "I can't let that slide,\nI'm afraid.",
68: "Whoa！ M-Mint… when did\nyou get here⁈",
69: "Everyone's here！",
70: "Eavesdropping, huh？ Shameful.",
71: "That's beside the point！\nYou kept secrets from us and\ntried to use us！",
72: "Not a pleasant feeling.",
73: "Um, if you don't mind,\ncould you tell us？",
74: "Ryou…",
75: "……",
76: "Fine, fine.",
77: 'Truth is, the island…',
78: 'was built using Mew Aqua, to\nraise RDA and make it a good\nhome for the animals.',
79: "As a result, some RDA born\nhere can sense Mew Aqua.",
80: 'The plan was to use that DNA\nto find 100%-pure Mew Aqua.',
81: "You shouldn't use Mew Aqua,\nna no da！",
82: "Mew Aqua is precious, but it\nonly means something when it's\nused for projects like this.",
83: "Besides, what we used was\nunder 50% purity. We need\n100% purity Mew Aqua.",
84: "So you brought us to this\nisland with an ulterior\nmotive, did you？",
85: "Nothing's ever really free.",
86: "Ugh, not a shred of remorse.",
87: 'Shut it.',
88: "Hmph！",
89: "Now, now.",
90: "…So we just find\nthat RDA？",
91: "Yes, exactly. The penguin\nIchigo-san met is an RDA\nHumboldt penguin.",
92: "It's a heat-hardy species, but\nfor it to get this far inland,\nthe Mew Aqua must be strong.",
93: "First, please find that\nHumboldt penguin… er,\n“Yuki-chan.”",
94: "About the girl who's its\nfriend: aside from staff, the\nonly people here are family",
95: "of staff, and you lot.\nShe's likely a ranger's kid.\nWe'll look into that too,",
96: "but I figure you'll find\nher faster yourselves.",
97: "You're trying to smooth-talk\nus, but it won't work.\nIsn't that right, Ichigo？",
98: "Well, yeah, but…",
99: "Wait, Ichigo⁈",
100: "Too late to complain now.",
101: 'You too, onee-sama…？',
102: "Pudding wants to see\nYuki-chan too！",
103: "That's true.",
104: "『Mint-san, could you watch\nIchigo-san so she doesn't\nget lost again？』",
105: "Ah-ahem.",
106: "Well, if that's the case,\nI suppose I could help.",
107: "Now that it's settled,\nshall we have breakfast？",
108: "Okaaay！",
109: "Oh, I need to pick who's\ncoming before we head out.",
110: "Oh, one moment, please. I've\nbrought along some items that\ncould come in handy, but",
111: "I'll give them to you in\nexchange for animal DNA data\nyou collect.",
112: "Trade？ Why not just\ngive them to us？",
113: "I tried to, but…",
114: "The island's been through a\nlot, right？ And life's not\nthat sweet. Give ＆ Take！",
115: "That's the rule for living！\nAnyway, if you want a trade,\ntalk to Keiichiro.",
116: "Very well, but how exactly\ndoes this system work？",
117: "Ask Keiichiro that too.\nThat's all.",
118: "H-hey…",
119: "Shall I explain？",
120: "  「Y-yes！」\n  「Trade items, please」\n  「Um, later」",
121: "Yes, certainly.",
122: "To trade items, you'll need\nanimal DNA data. When you\ndefeat a Chimera Anima,",
123: "R-2000 collects it\nautomatically, so you\ndon't have to do anything.",
124: "The DNA data you gather is\nrecorded as “Item Points,”\nwhich you can trade.",
125: "Like money？",
126: "Yes. Each item has a set\npoint cost, so you can\nthink of it that way.",
127: 'The “Item Points” you get\nvary by animal, so try out\nlots of different ones.',
128: "Oh, and… for DNA data you\nhave, you can check each\nanimal's “Item Points”",
129: "in R-2000's “Animal Guide.”\nPlease make use of it.",
130: "Yes. Got it.",
131: "  「Trade items, please」\n  「Thank you」",
132: "Certainly. Then…",
133: "  「Explain it after all」\n  「Thank you」",
134: "Well, I'm counting on you.\nWith the Chimera Animas\naround,",
135: "if it gets too much, come\nback to the cottage and rest.",
136: 'Resting in your room a bit\nmatters too, after all.',
137: "Got it！",
138: 'Take care out there.',
})
# naturalness pass: lines that came from translation memory
TR.update({141: '…Where are you off to？'})
# naturalness pass: lines that came from translation memory
TR.update({145: 'Heading to the “cave”？'})
# naturalness pass: lines that came from translation memory
TR.update({148: "Okay. I'll take you there."})
# naturalness pass: lines that came from translation memory
TR.update({155: 'Mm-mm… Are you going\nalready？'})
# naturalness pass: lines that came from translation memory
TR.update({158: 'Bringing my sister here was\nthe right call.'})
# naturalness pass: lines that came from translation memory
TR.update({161: 'Think nothing of it.'})
# naturalness pass: lines that came from translation memory
TR.update({162: 'Honestly, Mint-san…'})
# naturalness pass: lines that came from translation memory
TR.update({168: "Isn't that an aquamarine？"})
# naturalness pass: lines that came from translation memory
TR.update({171: 'Ooh～'})
# naturalness pass: lines that came from translation memory
TR.update({179: 'I, for one, would choose\nyou over any legend.'})
# naturalness pass: lines that came from translation memory
TR.update({181: "Aren't you popular～"})
# naturalness pass: lines that came from translation memory
TR.update({186: "Um… Ichigo onee-chan.\nYou can have Ringo's pendant."})
# naturalness pass: lines that came from translation memory
TR.update({187: "Isn't it special to you？"})
# naturalness pass: lines that came from translation memory
TR.update({192: 'Okay… Can we meet again？'})
# naturalness pass: lines that came from translation memory
TR.update({193: "Of course. 'Cause we're\nfriends… no, best\nfriends, nya♪"})
# naturalness pass: lines that came from translation memory
TR.update({199: '…And so, after lots of new\nfriends, goodbyes, and a new\npromise, we left the island.'})
# naturalness pass: lines that came from translation memory
TR.update({203: "No, I won't let it happen.\nThat's why we've got to\ntry even harder…"})
# naturalness pass: lines that came from translation memory
TR.update({204: "I know we can. After all,\nI've got wonderful friends！\nHehe."})
# naturalness pass: lines that came from translation memory
TR.update({206: 'Okay, got everything.'})
# naturalness pass: lines that came from translation memory
TR.update({208: 'It was tough, but making\nfriends with Ringo was fun,\nna no da！'})
# naturalness pass: lines that came from translation memory
TR.update({211: "Indeed. We can meet again\nanytime. Isn't that so,\nIchigo？"})
# naturalness pass: lines that came from translation memory
TR.update({222: "Oh, and I didn't come\nempty-handed. I've got a\npresent ready for you."})
# naturalness pass: lines that came from translation memory
TR.update({223: "A present？\nI don't want any present！"})
# naturalness pass: lines that came from translation memory
TR.update({224: "Don't be like that… Not\nthat you have a choice now."})
# naturalness pass: lines that came from translation memory
TR.update({226: 'Nothing big. I just\nscattered Parapara again.'})
# naturalness pass: lines that came from translation memory
TR.update({229: 'Stronger Chimeras…？\nWhat are you after？'})
# naturalness pass: lines that came from translation memory
TR.update({230: 'Nothing, really. I just\nwanted to give you a hard\ntime. Nice present, huh？'})
# naturalness pass: lines that came from translation memory
TR.update({245: 'So we just collect them？'})
# naturalness pass: lines that came from translation memory
TR.update({248: "I'll do my best！"})
# naturalness pass: lines that came from translation memory
TR.update({250: "It's the “Animal Guide”！"})
# naturalness pass: lines that came from translation memory
TR.update({261: "Leave it to us.\nWe'll make sure Ringo…"})
# naturalness pass: lines that came from translation memory
TR.update({265: 'Leave the rest to us,\nna no da！'})
# naturalness pass: lines that came from translation memory
TR.update({266: "We're all together, so\nwe'll be okay."})
# naturalness pass: lines that came from translation memory
TR.update({267: 'Heh… I suppose so.\nGoes without saying.'})
# naturalness pass: lines that came from translation memory
TR.update({210: "Goodbye isn't forever."})
# naturalness pass: lines that came from translation memory
TR.update({225: 'I knew it！\nYou did something⁈'})
