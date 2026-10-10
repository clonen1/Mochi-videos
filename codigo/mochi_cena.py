"""Utilitários partilhados pelos vídeos do Mochi (animação, cartões de texto, render)."""
import math
import os
import subprocess
import sys

import cairosvg

W, H, FPS = 1080, 1920, 30
FONT = "DejaVu Sans"
DIR = os.path.dirname(os.path.abspath(__file__))
MEOW_LEN = 0.55


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def spring(t):
    return 0 if t < 0 else 1 - math.exp(-t * 7) * math.cos(t * 16)


def fade(t, a, b, fin=0.25, fout=0.25):
    return ease((t - a) / fin) * (1 - ease((t - (b - fout)) / fout))


def card(op, l1, l2="", y=170, s1=68, s2=56, c1="#D8343A"):
    """Cartão branco com 1 ou 2 linhas de texto grande e centrado."""
    if op <= 0:
        return ""
    dy = (1 - op) * -30
    h = 280 if l2 else 190
    out = (f'<g opacity="{op:.3f}" transform="translate(0,{dy:.1f})">'
           f'<rect x="90" y="{y}" width="900" height="{h}" rx="44" fill="#FFFFFF" opacity="0.96"/>'
           f'<text x="540" y="{y + 115}" font-family="{FONT}" font-weight="bold" font-size="{s1}" fill="{c1}" text-anchor="middle">{l1}</text>')
    if l2:
        out += (f'<text x="540" y="{y + 210}" font-family="{FONT}" font-weight="bold" font-size="{s2}" '
                f'fill="#2B2B2B" text-anchor="middle">{l2}</text>')
    return out + "</g>"


def meow_open(t, meows):
    """Abertura da boca (0 a 1) sincronizada com os miados da música."""
    for t0 in meows:
        if t0 <= t <= t0 + MEOW_LEN:
            return math.sin(math.pi * (t - t0) / MEOW_LEN) ** 0.8
    return 0.0


def burst(op, x, y, word, size=110, color="#D8343A", r=190):
    """Estrela de banda desenhada com uma onomatopeia (POP!, TRIM!, PAF!)."""
    if op <= 0:
        return ""
    pts = []
    for i in range(24):
        rr = (r if i % 2 == 0 else r * 0.66) * (0.6 + 0.4 * op)
        a = math.pi * 2 * i / 24
        pts.append(f"{x + math.cos(a) * rr * 1.35:.0f},{y + math.sin(a) * rr:.0f}")
    return (f'<g opacity="{op:.3f}"><polygon points="{" ".join(pts)}" fill="#F6C343" stroke="#2B2B2B" stroke-width="6" stroke-linejoin="round"/>'
            f'<text x="{x}" y="{y + size * 0.36:.0f}" font-family="{FONT}" font-weight="bold" font-size="{size}" '
            f'fill="{color}" text-anchor="middle">{word}</text></g>')


def svg_doc(parts):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(parts)}</svg>'


def main(name, frame_svg, total):
    """python video_x.py           -> render completo (precisa de musica_x.wav)
       python video_x.py 0 2.5 9.9 -> só frames de pré-visualização"""
    if len(sys.argv) > 1:
        for s in sys.argv[1:]:
            cairosvg.svg2png(bytestring=frame_svg(float(s)).encode(), write_to=os.path.join(DIR, f"prev_{name}_{s}.png"))
        return
    frames = os.path.join(DIR, f"frames_{name}")
    os.makedirs(frames, exist_ok=True)
    for n in range(int(FPS * total)):
        cairosvg.svg2png(bytestring=frame_svg(n / FPS).encode(), write_to=os.path.join(frames, f"f{n:04d}.png"))
    out = os.path.join(DIR, f"mochi_{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", os.path.join(frames, "f%04d.png"), "-i", os.path.join(DIR, f"musica_{name}.wav"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", out], check=True)
    print(out)
