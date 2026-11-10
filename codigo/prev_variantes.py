import cairosvg, io
from PIL import Image
from mochi_kit import mochi
from mochi_kit2 import mochi2
def room(inner, bg1, bg2, floor):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="540" height="640" viewBox="0 0 540 640"><defs>'
            f'<linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></linearGradient></defs>'
            f'<rect width="540" height="640" fill="url(#w)"/><rect y="470" width="540" height="170" fill="{floor}"/>'
            f'<g transform="translate(75,150) scale(1.0)">{inner}</g></svg>')
panels=[("Atual",mochi("happy")),("A suave",mochi2("A","happy")),("B autocolante",mochi2("B","happy")),("C fofo",mochi2("C","happy"))]
panels2=[mochi("shock"),mochi2("A","shock"),mochi2("B","shock"),mochi2("C","shock")]
W=540
img=Image.new("RGB",(W*4,640*2))
for i,(n,p) in enumerate(panels):
    for j,pp in enumerate([p,panels2[i]]):
        png=cairosvg.svg2png(bytestring=room(pp,"#FFE9D2","#F7CFA6","#C98F5E").encode())
        img.paste(Image.open(io.BytesIO(png)).convert("RGB"),(i*W,j*640))
img.save("variantes.png")
