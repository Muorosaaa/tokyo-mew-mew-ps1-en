# exe block 0x13d86: move names (<=31). Keyed by Japanese.
M={'ミュウイチゴ':'Ichigo','ミュウミント':'Mint','ミュウレタス':'Lettuce','ミュウプリン':'Pudding','ミュウザクロ':'Zakuro','ミュウリンゴ':'Ringo'}
TR={
'ネコぱんち':'Kitty Punch','ネコネコぱんち！':'Kitty-Kitty Punch！','ネコきっく':'Kitty Kick','ネコネコきっく！':'Kitty-Kitty Kick！',
'インコロンすてっぷ':'Inkoron Step','インコロンだんす':'Inkoron Dance','スナメリーあたっく':'Porpoise Attack','スナメリーあたっく<05><18>':'Porpoise Attack EX',
'うっきースクラッチなのだ！':'Ukky Scratch, na no da！','うっきークローなのだ！':'Ukky Claw, na no da！',
'ザクロスカッター':'Zakuross Cutter','ザクロスブレード':'Zakuross Blade','ぽかぽかぽかーん':'Poka-Poka-Pokaan','ぽかぽかぽかーん！！':'Poka-Poka-Pokaan！！',
'リボーンストロベリーチェック':'Ribbon Strawberry Check','リボーンミントエコー':'Ribbon Mint Echo','リボーンレタスラッシュ':'Ribbon Lettuce Rush',
'リボーンプリングリングインフェルノ':'Ribbon Pudding Ring Inferno','リボーンザクロスピュア':'Ribbon Zakuross Pure',
'リボーンアップルポップ':'Ribbon Apple Pop','リボーンアップルパワー':'Ribbon Apple Power',
'リボーントリニティプレリュード':'Ribbon Trinity Prelude','リボーントリニティソナタ':'Ribbon Trinity Sonata','リボーントリニティコンチェルト':'Ribbon Trinity Concerto',
'リボーントリニティセレナーデ':'Ribbon Trinity Serenade','リボーントリニティマーチ':'Ribbon Trinity March','リボーントリニティロンド':'Ribbon Trinity Rondo',
'リボーントリニティレクイエム':'Ribbon Trinity Requiem','リボーントリニティシンフォニー':'Ribbon Trinity Symphony','リボーントリニティラプソディー':'Ribbon Trinity Rhapsody',
'リボーントリニティノクターン':'Ribbon Trinity Nocturne','リボーンストロベリーエクセレント':'Ribbon Strawberry Excellent',
'リボーンストロベリーチェックヒーリング':'Ribbon Strawberry Heal','リボーンインペリアルプレアー':'Ribbon Imperial Prayer',
'ネコあっぱー！':'Kitty Uppercut！','ちょうネコあっぱー！':'Super Kitty Uppercut！','サービスあたっく！':'Service Attack！','ちょうサービスあたっく！':'Super Service Attack！',
'ローリングすぱいく':'Rolling Spike','はいぱーローリングすぱいく！':'Hyper Rolling Spike！','レタスすぺしゃる':'Lettuce Special','レタスすぺしゃる<05><18>':'Lettuce Special EX',
'プリンむーんきっくなのだ！':'Pudding Moon Kick, na no da！','すっごいプリンむーんきっくなのだ！':'Mega Pudding Moon Kick！',
'イリュージョンソニック':'Illusion Sonic','イリュージョンソニックⅡ':'Illusion Sonic II','リンゴのドレミ♪':'Ringo\'s Do-Re-Mi♪','リンゴのソラシド♪':'Ringo\'s So-La-Ti-Do♪',
'リボーンストロベリーサプライズ！':'Ribbon Strawberry Surprise！',
}
import itertools
for a,b in itertools.permutations(M,2):
    TR['ダブルアタック（%s＆%s）'%(a,b)]='Double Attack（%s＆%s）'%(M[a],M[b])
