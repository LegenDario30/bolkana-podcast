import sys, json, asyncio, pathlib
from playwright.async_api import async_playwright
ROOT=pathlib.Path(__file__).parent.resolve()
CHROME='/home/vscode/.cache/hyperframes/chrome/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell'
CSS_COMMON="""
@font-face{font-family:Outfit;font-weight:600;src:url(assets/outfit/outfit-600.ttf)}
@font-face{font-family:Outfit;font-weight:700;src:url(assets/outfit/outfit-700.ttf)}
@font-face{font-family:Outfit;font-weight:800;src:url(assets/outfit/outfit-800.ttf)}
:root{--graphite:#232323;--lava:#D31C1F;--grass:#5CD41C;--bone:#F3F3F3}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--graphite);font-family:Outfit,sans-serif;color:var(--bone)}
.c{position:relative;overflow:hidden;background:var(--graphite)}
.glow{position:absolute;filter:blur(40px)}
.p{position:absolute}
.hl{color:var(--grass)}
"""
def wide(d):
    return f"""<style>{CSS_COMMON}
.c{{width:1920px;height:1080px}}
.gl{{left:{d.get('glx',-330)}px;top:{d.get('gly',-160)}px;width:{d.get('gs',1150)}px;height:{d.get('gs',1150)}px;border-radius:50%;background:radial-gradient(closest-side,rgba(211,28,31,{d.get('ga',.95)}),rgba(211,28,31,{d.get('gm',.38)}) 45%,rgba(211,28,31,0) 100%)}}
.gr{{right:{d.get('grx',-330)}px;top:{d.get('gry',-180)}px;width:{d.get('gs',1150)}px;height:{d.get('gs',1150)}px;border-radius:50%;background:radial-gradient(closest-side,rgba(92,212,28,{d.get('ga',.95)}),rgba(92,212,28,{d.get('gm',.34)}) 45%,rgba(92,212,28,0) 100%)}}
.mid{{position:absolute;left:500px;right:500px;top:0;bottom:0;background:radial-gradient(closest-side,rgba(35,35,35,.92),rgba(35,35,35,.6) 55%,rgba(35,35,35,0) 100%)}}
.guest{{left:{d.get('gl',-190)}px;bottom:-4px;height:{d.get('gh',1060)}px;-webkit-mask-image:linear-gradient(to right,#000 62%,transparent 100%)}}
.host{{right:{d.get('hr',-210)}px;bottom:-4px;height:{d.get('hh',1040)}px;-webkit-mask-image:linear-gradient(to left,#000 86%,transparent 100%)}}
.t{{position:absolute;left:460px;width:1000px;white-space:nowrap;top:52%;transform:translateY(-50%);text-align:center;font-weight:800;font-size:{d.get('fs',122)}px;line-height:1.0;letter-spacing:-.02em}}
.name{{position:absolute;left:560px;width:800px;bottom:92px;text-align:center;font-weight:600;font-size:36px;letter-spacing:.14em;text-transform:uppercase}}
.co{{position:absolute;left:560px;width:800px;bottom:50px;text-align:center;font-weight:600;font-size:28px;opacity:.8}}
.top{{position:absolute;left:0;right:0;top:40px;display:flex;justify-content:center;align-items:center;gap:20px;font-weight:600;font-size:28px}}
.top img{{height:60px}}
</style>
<div class=c>
<div class="glow gl"></div><div class="glow gr"></div>
<img class="p guest" src="assets/guest.png"><img class="p host" src="assets/host.png">
<div class=mid></div>
<div class=top><span>En colaboración con</span><img src="assets/ibinn.png"></div>
<div class=t>{d['title']}</div>
<div class=name>{d['name']}</div><div class=co>{d['company']}</div>
</div>"""
def tall(d):
    return f"""<style>{CSS_COMMON}
.c{{width:1080px;height:1350px}}
.gl{{left:{d.get('glx2',-330)}px;top:{d.get('gly2',-200)}px;width:{d.get('gs2',900)}px;height:{d.get('gs2',900)}px;border-radius:50%;background:radial-gradient(closest-side,rgba(211,28,31,{d.get('ga',.95)}),rgba(211,28,31,{d.get('gm',.38)}) 45%,rgba(211,28,31,0) 100%)}}
.gr{{right:{d.get('grx2',-330)}px;top:{d.get('gry2',-220)}px;width:{d.get('gs2',900)}px;height:{d.get('gs2',900)}px;border-radius:50%;background:radial-gradient(closest-side,rgba(92,212,28,{d.get('ga',.95)}),rgba(92,212,28,{d.get('gm',.34)}) 45%,rgba(92,212,28,0) 100%)}}
.gw{{left:{d.get('glt',-40)}px;top:100px;height:710px;-webkit-mask-image:linear-gradient(to right,#000 70%,transparent 100%)}}
.hw{{right:{d.get('hrt',-90)}px;top:85px;height:730px;-webkit-mask-image:linear-gradient(to left,#000 88%,transparent 100%)}}
.gw img,.hw img{{height:100%;display:block;-webkit-mask-image:linear-gradient(to bottom,#000 80%,transparent 100%)}}
.t{{position:absolute;left:60px;right:60px;top:776px;text-align:center;font-weight:800;font-size:{d.get('fs2',100)}px;line-height:1.0;letter-spacing:-.02em}}
.name{{position:absolute;left:0;right:0;top:1170px;text-align:center;font-weight:600;font-size:32px;letter-spacing:.14em;text-transform:uppercase}}
.co{{position:absolute;left:0;right:0;top:1214px;text-align:center;font-weight:600;font-size:27px;opacity:.8}}
.top{{position:absolute;left:0;right:0;top:30px;display:flex;justify-content:center;align-items:center;gap:16px;font-weight:600;font-size:21px}}
.top img{{height:42px}}
.bot{{position:absolute;left:60px;right:60px;bottom:26px;display:flex;justify-content:space-between;align-items:flex-end}}
.av{{display:flex;flex-direction:column;gap:8px;font-weight:600;font-size:19px;opacity:.95}}
.av .ic{{display:flex;gap:14px;align-items:center}} .av .ic img{{height:40px}}
.bk{{width:230px;margin-bottom:6px}}
</style>
<div class=c>
<div class="glow gl"></div><div class="glow gr"></div>
<div class="p gw"><img src="assets/{d.get('gt','guest_nomic.png')}"></div><div class="p hw"><img src="assets/host.png"></div>
<div class=top><span>En colaboración con</span><img src="assets/ibinn.png"></div>
<div class=t>{d['title']}</div>
<div class=name>{d['name']}</div><div class=co>{d['company']}</div>
<div class=bot><div class=av><span>Disponible en</span><div class=ic><img src="assets/ic_youtube.png"><img src="assets/ic_spotify.png"><img src="assets/ic_apple.png"><img src="assets/ic_amazon.png"></div></div><img class=bk src="assets/logo.png"></div>
</div>"""
async def render(d, out):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=CHROME if pathlib.Path(CHROME).exists() else None)
        for fmt,fn,(w,h) in [('wide',wide,(1920,1080)),('tall',tall,(1080,1350))]:
            html=fn(d); f=ROOT/f'_{fmt}.html'; f.write_text(f'<!doctype html><meta charset=utf-8>{html}')
            pg=await b.new_page(viewport={'width':w,'height':h})
            await pg.goto(f'file://{f}'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
            await pg.screenshot(path=str(ROOT/f'{out}_{fmt}.png')); await pg.close()
        await b.close()
if __name__=='__main__':
    d=json.loads(sys.argv[1]); asyncio.run(render(d,sys.argv[2]))
