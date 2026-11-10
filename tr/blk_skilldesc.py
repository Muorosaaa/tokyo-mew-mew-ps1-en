# exe block 0x1c61c: Ichigo's skill names (<=10) + skill/move descriptions (<=36 x3). Keyed by Japanese.
TR={
'よける':'Dodge','ねらう':'Aim','ためる':'Charge','まもる':'Guard','とんずら':'Escape','にらむ':'Glare','いのる':'Pray',
'ぽじてぃぶ':'Positive','すてっぷ':'Step','しゅうちゅう':'Focus','黄家伝来の……':'Fong Art','きょううん':'Lucky','かるわざ':'Acrobat','きづかい':'Caring',
'戦闘中に使え、攻撃をよけやすくなります。/何回も使えばもっとよけやすくなります。/その戦闘の間ならずっと効果があります。':'Use in battle to dodge more easily.\nUse it again to dodge even better.\nLasts for the whole battle.',
'戦闘中に使え、攻撃があたりやすくなります。/何回も使えばもっとあたりやすくなります。/その戦闘の間ならずっと効果があります。':'Use in battle to hit more easily.\nUse it again to hit even better.\nLasts for the whole battle.',
'戦闘中に使え、「やるき」をけっこうふやします。':'Use in battle to raise “Spirit”\na lot.',
'戦闘中に使え、受けるダメージを少しだけ/へらします。何回も使えばもっとへります。/その戦闘の間ならずっと効果があります。':'Use in battle to take a bit less\ndamage. Use again to reduce more.\nLasts for the whole battle.',
'戦闘中に使え、逃げることができます。/負けそうな時はムリをせずに使いましょう。/でもたまに失敗することも……':'Use in battle to run away.\nUse it if you\'re about to lose.\nBut it sometimes fails…',
'戦闘中に使え、にらんで相手をびびらせます。/使った相手の「すばやさ」が下がります。':'Use in battle to glare and scare a\nfoe. Lowers that foe\'s “Speed.”',
'戦闘中に使え、誰か<37>人の「たいりょく」を/<3b><36>回復させます。':'Use in battle to restore 50 HP\nto one person.',
'セットしていれば効果があります。/「こうどうメンバー」なら「やるき」が/ふえる時にボーナスがつきます（仲間も）。':'Works while set. In the Active\nParty, “Spirit” gains get a bonus.\n（Allies too.）',
'セットしていれば効果があります。/見事なステップで「すばやさ」が上がります。':'Works while set. Fancy footwork\nraises “Speed.”',
'セットしていれば効果があります。/「やるき」がふえるときにボーナスが/つきます（自分だけ）。':'Works while set. “Spirit” gains\nget a bonus. （Self only.）',
'セットしていれば効果があります。/たいりょく回復などのアイテムを使ったとき/普通より効果が高くなります。':'Works while set. Healing items and\nthe like work better than usual.',
'セットしていれば効果があります。/攻撃が少しだけあたりやすくなり、/自分への攻撃をよけやすくなります。':'Works while set. Attacks hit a bit\nmore often, and you dodge attacks\nmore easily.',
'セットしていれば効果があります。/すばやい動きで敵の攻撃を少しだけ/よけやすくなります。':'Works while set. Quick moves make\nfoe attacks a bit easier to dodge.',
'セットしていれば効果があります。/戦闘でもらえる「なかよしど」がちょっとふえます。/（敵が弱いとふえないこともあります）':'Works while set. “Friendship” from\nbattles rises a little.\n（May not work vs weak foes.）',
'あまりつよくない攻撃です。':'A not-so-strong attack.',
'あまりつよくない攻撃です。/ときどき、敵の「すばやさ」を少し下げます。':'A not-so-strong attack.\nSometimes lowers foe “Speed” a bit.',
'パワーアップしたミュウイチゴの攻撃！':'Powered-up Mew Ichigo\'s attack！',
'ミュウイチゴのあたらしいワザです。/「ネコぱんち」より強い攻撃をします。':'Mew Ichigo\'s new move.\nStronger than “Kitty Punch.”',
'パワーアップしたミュウイチゴの新しいワザです。/「ネコあっぱー！」より強い攻撃をします。':'Powered-up Mew Ichigo\'s new move.\nStronger than “Kitty Uppercut！”',
'ミュウミントの新しいワザです。/「インコロンすてっぷ」より強い攻撃をします。':'Mew Mint\'s new move.\nStronger than “Inkoron Step.”',
'ミュウレタスの新しいワザです。/「スナメリーあたっく」より強い攻撃をします。':'Mew Lettuce\'s new move.\nStronger than “Porpoise Attack.”',
'ミュウプリンの新しいワザです。/「うっきースクラッチなのだ！」より/強い攻撃をします。':'Mew Pudding\'s new move.\nStronger than “Ukky Scratch！”',
'ミュウザクロの新しいワザです。/「ザクロスカッター」より強い攻撃をします。':'Mew Zakuro\'s new move.\nStronger than “Zakuross Cutter.”',
'ミュウリンゴの新しいワザです。/敵みんなにダメージをあたえます。':'Mew Ringo\'s new move.\nDamages all foes.',
}
SP='Uses 1 “Spirit.”'
for jp,en,extra in (('ネコぱんち','Kitty Punch','Lowers foe “Accuracy” a bit.'),('ネコきっく','Kitty Kick',None),('インコロンすてっぷ','Inkoron Step','Lowers foe “Accuracy” a bit.'),
    ('スナメリーあたっく','Porpoise Attack','Lowers foe “Speed” a bit.'),('うっきースクラッチなのだ！','Ukky Scratch！','Lowers foe “Speed” a bit.'),
    ('ザクロスカッター','Zakuross Cutter','Raises own “Speed” a bit.'),('ぽかぽかぽかーん','Poka-Poka-Pokaan','Lowers foe “Speed” a bit.'),
    ('ネコあっぱー！','Kitty Uppercut！','Lowers foe “Accuracy” a bit.'),('サービスあたっく！','Service Attack！',None),
    ('プリンむーんきっくなのだ！','Pudding Moon Kick','Raises own “Speed” a bit.')):
    k='「%s」の強力攻撃！/「やるき」を<37>コ使います。'%jp
    tail={'Lowers foe “Accuracy” a bit.':'/敵の「めいちゅうりつ」を少し下げます。','Lowers foe “Speed” a bit.':'/敵の「すばやさ」を少し下げます。','Raises own “Speed” a bit.':'/「すばやさ」が少し上がります。',None:''}[extra]
    TR[k+tail]='Strong “%s”！\n%s'%(en,SP)+('\n'+extra if extra else '')
TR.update({
'「ローリングすぱいく」の強力攻撃！/「やるき」を<37>コ使いますが、敵の「めいちゅうりつ」/を少し下げます。':'Strong “Rolling Spike”！\nUses 1 “Spirit.”\nLowers foe “Accuracy” a bit.',
'「レタスすぺしゃる」の強力攻撃！/「やるき」を<37>コ使います。ミュウレタスと/敵の「すばやさ」が少し下がります。':'Strong “Lettuce Special”！\nUses 1 “Spirit.” Lowers “Speed”\nof Mew Lettuce and foe a bit.',
'「イリュージョンソニック」の強力攻撃！/「やるき」を<37>コ使いますが、敵の「すばやさ」を/少し下げます。':'Strong “Illusion Sonic”！\nUses 1 “Spirit.”\nLowers foe “Speed” a bit.',
'「リンゴのドレミ♪」の強力攻撃！/「やるき」を<37>コ使いますが、敵みんなに/防御無視でダメージをあたえます。':'Strong “Ringo\'s Do-Re-Mi♪”！\nUses 1 “Spirit.” Hits all foes,\nignoring defense.',
'ミュウイチゴの強力なスペシャルワザです。/「やるき」を<38>コ使いますが、/「すばやさ」が少し上がります。':'Mew Ichigo\'s strong Special.\nUses 2 “Spirit.”\nRaises own “Speed” a bit.',
'ミュウミントの強力なスペシャルワザです。/「やるき」を<38>コ使いますが、防御無視でダメージを/あたえ、敵の「めいちゅうりつ」も下げます。':'Mew Mint\'s strong Special.\nUses 2 “Spirit.” Ignores defense\nand lowers foe “Accuracy.”',
'ミュウレタスの強力なスペシャルワザです。/「やるき」を<38>コ使いますが、敵みんなにダメージ/をあたえ、「すばやさ」もけっこう下げます。':'Mew Lettuce\'s strong Special.\nUses 2 “Spirit.” Hits all foes\nand lowers their “Speed” a lot.',
'ミュウプリンの強力なスペシャルワザです。/「やるき」を<38>コ使いますが、敵みんなに防御無視で/ダメージをあたえます。':'Mew Pudding\'s strong Special.\nUses 2 “Spirit.” Hits all foes,\nignoring defense.',
'ミュウザクロの強力なスペシャルワザです。/「やるき」を<38>コ使いますが、敵みんなにダメージ/をあたえ、「すばやさ」も少し下げます。':'Mew Zakuro\'s strong Special.\nUses 2 “Spirit.” Hits all foes\nand lowers their “Speed” a bit.',
'ミュウリンゴのスペシャルワザです。/「やるき」を<37>コ使いますが、「こうどうメンバー」/の「たいりょく」を<3b><36>回復します。':'Mew Ringo\'s Special.\nUses 1 “Spirit.” Restores\n50 HP to the Active Party.',
'ミュウリンゴのスペシャルワザです。/「やるき」を<37>コ使いますが、ミュウイチゴを/パワーアップ（変身）させます。':'Mew Ringo\'s Special.\nUses 1 “Spirit.” Powers up\n（transforms） Mew Ichigo.',
'ミュウイチゴの新しいスペシャルワザです。/「やるき」を<39>コ使いますが、敵みんなにダメージを/あたえます。':'Mew Ichigo\'s new Special.\nUses 3 “Spirit.”\nHits all foes.',
})
# team-attack descriptions: generate from pattern
EFF={'/敵の「すばやさ」をけっこう下げます。':'Lowers foe “Speed” a lot.','/防御無視でダメージをあたえます。':'Ignores defense.',
 '/<38>人の「すばやさ」を少し上げます。':'Raises both users\' “Speed” a bit.','/敵の「すばやさ」を少し下げます。':'Lowers foe “Speed” a bit.',
 '/敵の「めいちゅうりつ」をけっこう下げます。':'Lowers foe “Accuracy” a lot.','/仲間みんなの「たいりょく」を<3b><36>回復します。':'Heals all allies 50 HP.','':None}
N={'<37>':'1','<38>':'2','<39>':'3'}
for tgt,te in (('敵みんなにダメージ！','Damages all foes！'),('敵<37>体にダメージ！','Damages one foe！')):
    for n in N:
        for je,ee in EFF.items():
            TR['%s/「やるき」を%sコずつ使います。%s'%(tgt,n,je)]='%s\nUses %s “Spirit” each.%s'%(te,N[n],('\n'+ee) if ee else '')
TR.update({
'敵<37>体にダメージ！_「やるき」を<37>コずつ使います。/「こうどうメンバー」の「たいりょく」を/<3b><36>回復します。':'Damages one foe！ Uses 1 “Spirit”\neach. Heals the Active\nParty 50 HP.',
'敵みんなにダメージ！_「やるき」を<38>コずつ/使います。「こうどうメンバー」の/「たいりょく」を<3b><36>回復します。':'Damages all foes！ Uses 2 “Spirit”\neach. Heals the Active\nParty 50 HP.',
'敵<37>体にダメージ！_「やるき」を<38>コずつ使います。/敵の「めいちゅうりつ」をけっこう下げ、/防御無視でダメージをあたえます。':'Damages one foe！ Uses 2 “Spirit”\neach. Lowers foe “Accuracy” a lot\nand ignores defense.',
'敵<37>体にダメージ！_「やるき」を<38>コずつ使います。/敵の「めいちゅうりつ」と「すばやさ」を/けっこう下げます。':'Damages one foe！ Uses 2 “Spirit”\neach. Lowers foe “Accuracy”\nand “Speed” a lot.',
'ミュウリンゴ以外の<3b>人といっしょに全体攻撃！/「やるき」を<38>コずつ使います。/防御無視でダメージをあたえます。':'All-out attack with everyone but\nRingo！ Uses 2 “Spirit” each.\nIgnores defense.',
'ミュウリンゴ以外の<3b>人といっしょに全体攻撃！/「やるき」を<38>コずつ使います。/仲間みんなの「たいりょく」を<3b><36>回復します。':'All-out attack with everyone but\nRingo！ Uses 2 “Spirit” each.\nHeals all allies 50 HP.',
'<3c>人みんなで全体攻撃‼_最強攻撃です。/「やるき」を<38>コずつ使います。/防御無視でダメージをあたえます。':'All 6 attack together‼ The\nstrongest move. Uses 2 “Spirit”\neach. Ignores defense.',
})
M3={'ミュウイチゴ':'Ichigo','ミュウミント':'Mint','ミュウレタス':'Lettuce','ミュウプリン':'Pudding','ミュウザクロ':'Zakuro','ミュウリンゴ':'Ringo'}
EFF3={'「こうどうメンバー」/の「たいりょく」を<3b><36>回復します。':('','Heals the Active Party 50 HP.'),
 '/敵みんなの「めいちゅうりつ」をすごく下げます。':('/','Lowers all foes\' “Accuracy” hugely.'),
 '/防御無視でダメージをあたえます。':('/','Ignores defense.'),'/敵みんなの「すばやさ」をけっこう下げます。':('/','Lowers all foes\' “Speed” a lot.'),
 '/<39>人の「すばやさ」をけっこう上げます。':('/','Raises the trio\'s “Speed” a lot.'),'/敵みんなの「すばやさ」を少し下げます。':('/','Lowers all foes\' “Speed” a bit.'),
 '/<39>人の「すばやさ」を少し上げます。':('/','Raises the trio\'s “Speed” a bit.'),'/仲間みんなの「たいりょく」を<3b><36>回復します。':('/','Heals all allies 50 HP.')}
import itertools
for a,b,c in itertools.permutations(M3,3):
    for n in ('<38>','<39>'):
        for je,(_,ee) in EFF3.items():
            TR['%s＆%s＆%sで全体攻撃/「やるき」を%sコずつ使います。%s'%(a,b,c,n,je)]='%s, %s ＆ %s hit all！\nUses %s “Spirit” each.\n%s'%(M3[a],M3[b],M3[c],N[n],ee)
