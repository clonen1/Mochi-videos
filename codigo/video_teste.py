"""Gera o video de teste 'Dia 1' do Mochi (1080x1920, 9 s, 30 fps)."""
import math
import os
import subprocess

import cairosvg

from mochi_kit import mochi

W, H, FPS, DUR = 1080, 1920, 30, 9
OUT = os.path.join(os.path.dirname(__file__), "frames")
os.makedirs(OUT, exist_ok=True)

SCENES = [
    # (inicio, fim, fundo, expressao, linha1, linha2)
    (0, 3, "#FDE7D3", "normal", "Dia 1", "O Mochi quer ir ao Japão"),
    (3, 6, "#DFF1E4", "happy", "O plano:", "juntar dinheiro para o voo"),
    (6, 9, "#2E3A5C", "sleep", "Começa amanhã...", "segue para veres o dia 2"),
]


def caption(l1, l2, dark):
    box = "#1F2740" if dark else "#FFFFFF"
    c1 = "#FFD166" if dark else "#D8343A"
    c2 = "#FFFFFF" if dark else "#2B2B2B"
    return (
        f'<rect x="90" y="190" width="900" height="300" rx="40" fill="{box}" opacity="0.95"/>'
        f'<text x="540" y="310" font-family="DejaVu Sans" font-weight="bold" font-size="92" fill="{c1}" text-anchor="middle">{l1}</text>'
        f'<text x="540" y="420" font-family="DejaVu Sans" font-weight="bold" font-size="56" fill="{c2}" text-anchor="middle">{l2}</text>'
    )


def extras(idx, t):
    if idx == 1:
        out = ""
        for i, x in enumerate([180, 900, 260, 820]):
            y = 1450 - ((t * 260 + i * 180) % 700)
            out += (f'<circle cx="{x}" cy="{y:.0f}" r="42" fill="#F6C343" stroke="#C9971C" stroke-width="6"/>'
                    f'<text x="{x}" y="{y + 18:.0f}" font-family="DejaVu Sans" font-weight="bold" font-size="48" fill="#9A6F0C" text-anchor="middle">€</text>')
        return out
    if idx == 2:
        out = '<circle cx="880" cy="640" r="70" fill="#F4E9C8"/><circle cx="905" cy="620" r="62" fill="#2E3A5C"/>'
        for sx, sy in [(160, 600), (300, 720), (760, 820), (980, 900), (120, 900), (620, 580)]:
            out += f'<circle cx="{sx}" cy="{sy}" r="6" fill="#FFFFFF" opacity="0.8"/>'
        for i in range(3):
            p = ((t * 0.6) + i / 3) % 1
            out += (f'<text x="{720 + p * 120:.0f}" y="{1050 - p * 260:.0f}" font-family="DejaVu Sans" font-weight="bold" '
                    f'font-size="{50 + p * 40:.0f}" fill="#FFFFFF" opacity="{1 - p:.2f}">Z</text>')
        return out
    return ""


def frame(n):
    t = n / FPS
    idx = next(i for i, s in enumerate(SCENES) if s[0] <= t < s[1])
    start, _, bg, expr, l1, l2 = SCENES[idx]
    ts = t - start
    blink = idx == 0 and 1.4 < ts < 1.55
    pop = 1 + 0.18 * math.exp(-ts * 9) * math.cos(ts * 20)
    bob = math.sin(t * (2 if expr == "sleep" else 5)) * (8 if expr == "sleep" else 14)
    scale = 2.4 * pop
    mx = (W - 380 * scale) / 2
    my = 680 + bob - (400 * scale - 400 * 2.4) / 2
    floor = "#E9C9A8" if idx == 0 else ("#BFE0C8" if idx == 1 else "#1E2742")
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        f'<rect width="{W}" height="{H}" fill="{bg}"/>'
        f'<ellipse cx="540" cy="1620" rx="600" ry="160" fill="{floor}"/>'
        f'{extras(idx, ts)}'
        f'<ellipse cx="540" cy="1580" rx="{300 - abs(bob) * 4:.0f}" ry="40" fill="#000" opacity="0.12"/>'
        f'<g transform="translate({mx:.1f},{my:.1f}) scale({scale:.3f})">{mochi(expr, blink)}</g>'
        f'{caption(l1, l2, idx == 2)}'
        f'<text x="540" y="1840" font-family="DejaVu Sans" font-size="38" fill="{"#AAB4D4" if idx == 2 else "#8A6A50"}" text-anchor="middle">@mochi.rumoaojapao</text>'
        f'</svg>'
    )
    cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(OUT, f"f{n:04d}.png"))


if __name__ == "__main__":
    for n in range(FPS * DUR):
        frame(n)
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(OUT, "f%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
        os.path.join(os.path.dirname(__file__), "mochi_dia1.mp4"),
    ], check=True)
    print("ok")
