"""Short 'Eu quando o dono me chama pelo nome e finjo que não ouço' (1080x1920, 10 s, 30 fps), em loop.

0-1.0   ouço o chamado: orelha mexe (tremor), ondas de som | 'O dono me chama...' (já legível no 1.º quadro)
1.0-5.0 viro-me para o lado oposto de olhos fechados, assobio | chamados 1.6 e 3.3 | 'Eu: não ouvi nada'
5.0     a lata de petiscos aparece | 5.4 aparece num instante | 'Petisco?' | miados 5.9 e 7.4
7.5-9.4 'Já cheguei.' | 9.4-10 volta ao início (loop)
"""
import math
import os
import subprocess
import sys

import cairosvg

from mochi_cena import FONT, W, H, FPS, burst, card, clamp, ease, fade, meow_open, svg_doc
from mochi_kit import mochi, MOCHI_VF
from mochi_props_chamar import ondas, mao, notas
from musica_chamar import MEOWS, TOTAL

S = 2.0
FLOOR = 1720
MY = FLOOR - 378 * S
X0, X1 = 240, 330   # posições do centro (início / ao pé da lata)
CALLS = [0.0, 1.6, 3.3]


def mochi_g(t):
    # estado
    flip, expr, x, hop, rot = 1, "normal", X0 + 190 * 0, 0.0, 0.0
    cx = 400
    if t < 1.0:
        # orelha mexe: tremor rápido; olhos abertos, atento
        rot = 5 * math.sin(t * 38) * (1 - ease((t - 0.1) / 0.9)) + 3
        expr = "shock" if t < 0.5 else "normal"
    elif t < 5.0:
        k = ease((t - 1.0) / 0.25)
        flip = 1 - 2 * k
        expr = "sleep"
        rot = -4 + 2 * math.sin(t * 3)
        for c in CALLS[1:]:  # a orelha ainda mexe a cada chamado
            if 0 <= t - c < 0.5:
                rot += 5 * math.sin((t - c) * 40) * (1 - (t - c) / 0.5)
    elif t < 9.4:
        k = ease((t - 5.2) / 0.2)
        flip = -1 + 2 * ease((t - 5.2) / 0.15)
        cx = 400 + 100 * ease((t - 5.2) / 0.25)
        expr = "happy" if t >= 5.5 else "shock"
        hop = 70 * math.sin(math.pi * clamp((t - 5.2) / 0.5)) if t < 5.7 else 5 * math.sin(t * 9)
        rot = 3 * math.sin(t * 7)
    else:
        k = ease((t - 9.4) / 0.6)
        cx = 500 - 100 * k
        flip = 1
        expr = "happy" if k < 0.3 else "normal"
    if t >= 9.4:
        flip = 1
    mo = meow_open(t, MEOWS)
    blink = False
    return (f'<g transform="translate({cx:.1f},{MY - hop:.1f}) scale({S * (flip if abs(flip) > 0.05 else 0.05):.3f},{S}) '
            f'rotate({rot:.1f},0,378) translate(-190,0)">{mochi(expr, blink, mouth_open=mo)}</g>')


def lata_x(t):
    if t < 4.8 or t >= 9.4:
        return None
    if t < 5.0:
        return 1250 - 450 * ease((t - 4.8) / 0.2)
    if t < 9.0:
        return 800
    return 800 + 500 * ease((t - 9.0) / 0.4)


def frame_svg(t):
    parts = [
        f'<rect width="{W}" height="{H}" fill="#FDEFD8"/>',
        f'<rect x="0" y="{FLOOR - 40}" width="{W}" height="{H - FLOOR + 40}" fill="#EBC99B"/>',
        f'<ellipse cx="540" cy="{FLOOR + 10}" rx="360" ry="38" fill="#000" opacity="0.10"/>',
    ]
    ow = 0.0
    for c in CALLS:
        if 0 <= t - c < 1.2:
            ow = max(ow, 1 - ease((t - c - 0.9) / 0.3))
    parts.append(ondas(ow, 20, 1050, t))
    parts.append(mochi_g(t))
    if 1.3 < t < 5.0:
        parts.append(notas(fade(t, 1.3, 5.0, 0.3, 0.3), 500, 1000, t))
    lx = lata_x(t)
    if lx is not None:
        sh = 6 * math.sin(t * 40) if 5.0 <= t < 5.8 else 0
        parts.append(f'<g transform="translate({lx:.0f},1180) scale(1.15)">{mao(sh)}</g>')
    parts += [
        burst(fade(t, 4.95, 5.6, 0.05, 0.25), 760, 900, "CLAC!", 96, r=150),
        # cartões: o 1.º já visível no quadro 0
        card((1 - ease((t - 0.85) / 0.2)) if t < 1.05 else 0, "O dono", "chama-me...", y=480, s1=76, s2=88),
        card(fade(t, 1.05, 5.0, 0.2, 0.2), "Eu: não ouvi", "nada nenhum", y=480, s1=76, s2=84),
        card(fade(t, 5.05, 7.5, 0.15, 0.2), "Petisco?!", y=480, s1=96),
        card(fade(t, 7.55, 9.4, 0.2, 0.2), "Já cheguei.", y=480, s1=88),
    ]
    return svg_doc(parts)


def main():
    if len(sys.argv) > 1:
        for s in sys.argv[1:]:
            cairosvg.svg2png(bytestring=frame_svg(float(s)).encode(), write_to=os.path.join(DIR, f"prev_chamar_{s}.png"))
        return
    frames = os.path.join(DIR, "frames_chamar")
    os.makedirs(frames, exist_ok=True)
    for n in range(int(FPS * TOTAL)):
        cairosvg.svg2png(bytestring=frame_svg(n / FPS).encode(), write_to=os.path.join(frames, f"f{n:04d}.png"))
    out = os.path.join(DIR, "..", "videos", "mochi_chamar.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(frames, "f%04d.png"),
                    "-i", os.path.join(DIR, "..", "musica", "musica_chamar.wav"),
                    "-vf", MOCHI_VF, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", out], check=True)
    print(out)


DIR = os.path.dirname(os.path.abspath(__file__))
if __name__ == "__main__":
    main()
