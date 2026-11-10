import cairosvg, io
from PIL import Image
from mochi_kit2 import mochi2
def room(inner):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="540" height="640" viewBox="0 0 540 640"><rect width="540" height="640" fill="#FBE0C0"/>'
            '<rect y="470" width="540" height="170" fill="#C98F5E"/>'
            f'<g transform="translate(75,150)">{inner}</g></svg>')
ex=["happy","shock","angry","sleep"]
img=Image.new("RGB",(540*4,640))
for i,e in enumerate(ex):
    png=cairosvg.svg2png(bytestring=room(mochi2("B",e)).encode(),scale=1)
    img.paste(Image.open(io.BytesIO(png)).convert("RGB"),(i*540,0))
img.save("mochiB.png")
