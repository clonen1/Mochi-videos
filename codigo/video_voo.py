"""Vídeo 'Eu a ver o preço do voo para o Japão' (1080x1920, 10 s, 30 fps), em loop.

0-2.4 Mochi feliz com o telemóvel | 2.4-4 o preço sobe | 4.0 susto e cai para trás
4.5-6.6 'o meu saldo: 0€' | 6.8-9.3 'Plano B: ir a nado' | 9-10 levanta-se e volta ao início
"""
import math
import os
import subprocess
import sys

import cairosvg

from mochi_kit import mochi
from musica_voo import MEOWS

W, H, FPS, TOTAL = 1080, 1920, 30, 10
DIR = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(DIR, "frames_voo")
os.makedirs(FRAMES, exist_ok=True)
FONT = "DejaVu Sans"
PRICE = 1400
S = 1.9                      # escala do Mochi
MEOW_LEN = 0.55


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def spring(t):
    return 0 if t < 0 else 1 - math.exp(-t * 7) * math.cos(t * 16)


def card(op, l1, l2="", y=170, s1=68, s2=56, c1="#D8343A"):
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


def fade(t, a, b, fin=0.25, fout=0.25):
    return ease((t - a) / fin) * (1 - ease((t - (b - fout)) / fout))


def phone_in_paws(t):
    glow = 0.75 + 0.25 * math.sin(t * 6)
    return ('<rect x="156" y="262" width="68" height="100" rx="12" fill="#2B2B2B"/>'
            f'<rect x="163" y="271" width="54" height="80" rx="6" fill="#9FD3F5" opacity="{glow:.2f}"/>'
            '<ellipse cx="160" cy="336" rx="17" ry="13" fill="#FFF6EA"/><ellipse cx="220" cy="336" rx="17" ry="13" fill="#FFF6EA"/>')


def big_phone(t):
    op = fade(t, 2.35, 6.6, 0.2, 0.3)
    if op <= 0:
        return ""
    u = clamp((t - 2.5) / 1.5)
    value = int(PRICE * u ** 2.2 / 10) * 10
    landed = t >= 4.0
    pulse = 1 + (0.25 * math.exp(-(t - 4.0) * 7) * math.cos((t - 4.0) * 20) if landed else 0)
    price = f"{PRICE}€" if landed else f"{value}€"
    color = "#D8343A" if landed else "#2B2B2B"
    pop = 0.85 + 0.15 * spring(t - 2.35)
    return (f'<g opacity="{op:.3f}" transform="translate(540,690) scale({pop:.3f}) translate(-540,-690)">'
            '<rect x="300" y="470" width="480" height="440" rx="48" fill="#2B2B2B"/>'
            '<rect x="322" y="492" width="436" height="396" rx="30" fill="#FFFFFF"/>'
            '<rect x="322" y="492" width="436" height="90" rx="30" fill="#3F6FB0"/><rect x="322" y="550" width="436" height="32" fill="#3F6FB0"/>'
            f'<text x="540" y="552" font-family="{FONT}" font-weight="bold" font-size="40" fill="#FFFFFF" text-anchor="middle">Lisboa → Tóquio</text>'
            f'<text x="540" y="640" font-family="{FONT}" font-size="34" fill="#8A8A8A" text-anchor="middle">ida e volta</text>'
            f'<g transform="translate(540,770) scale({pulse:.3f})">'
            f'<text x="0" y="0" font-family="{FONT}" font-weight="bold" font-size="112" fill="{color}" text-anchor="middle">{price}</text></g>'
            '<rect x="400" y="820" width="280" height="54" rx="27" fill="#3CB371"/>'
            f'<text x="540" y="858" font-family="{FONT}" font-weight="bold" font-size="32" fill="#FFFFFF" text-anchor="middle">Comprar</text>'
            '</g>')


def meow_open(t):
    for t0 in MEOWS:
        if t0 <= t <= t0 + MEOW_LEN:
            return math.sin(math.pi * (t - t0) / MEOW_LEN) ** 0.8
    return 0.0


def fall_angle(t):
    if t < 4.3:
        return 0.0
    if t < 4.8:
        return -88 * ((t - 4.3) / 0.5) ** 2
    if t < 9.0:
        return -88 + 5 * math.exp(-(t - 4.8) * 7) * math.sin((t - 4.8) * 25)
    return -88 * (1 - spring((t - 9.0) * 1.1))


def mochi_expr(t):
    if t < 0.5 or 9.0 <= t:
        return "normal"
    if t < 2.5:
        return "happy"
    if t < 4.0:
        return "normal"
    if t < 4.6:
        return "shock"
    return "ko"


def stars(t, hx, hy):
    if not 4.9 < t < 9.0:
        return ""
    op = fade(t, 4.9, 9.0, 0.2, 0.2)
    out = f'<g opacity="{op:.2f}">'
    for i in range(3):
        a = t * 4 + i * 2.094
        x, y = hx + math.cos(a) * 110, hy - 200 + math.sin(a) * 35
        out += f'<path d="M{x:.0f} {y - 32:.0f} L{x + 10:.0f} {y:.0f} L{x:.0f} {y + 32:.0f} L{x - 10:.0f} {y:.0f} Z" fill="#F6C343"/>'
        out += f'<path d="M{x - 32:.0f} {y:.0f} L{x:.0f} {y + 10:.0f} L{x + 32:.0f} {y:.0f} L{x:.0f} {y - 10:.0f} Z" fill="#F6C343"/>'
    return out + "</g>"


def frame_svg(t):
    shake = math.sin(t * 90) * 18 * (1 - (t - 4.0) / 0.45) if 4.0 <= t < 4.45 else 0
    flash = 0.35 * math.exp(-(t - 4.0) * 8) if t >= 4.0 else 0
    ang = fall_angle(t)
    fallen = clamp(-ang / 88)
    bob = math.sin(t * 2 * math.pi) * 6 * (1 - fallen)
    mx = (W - 380 * S) / 2 + 170 * fallen
    my = 1560 - 370 * S + bob
    px, py = mx + 190 * S, my + 375 * S
    r = math.radians(ang)
    hx, hy = px - (-207 * S) * math.sin(r), py + (-207 * S) * math.cos(r)
    expr = mochi_expr(t)
    blink = 1.3 < t < 1.42
    hold_phone = t < 4.3 or t >= 9.3
    title_op = (1 - ease((t - 2.1) / 0.3)) if t < 5 else ease((t - 9.4) / 0.4)
    parts = [
        f'<rect width="{W}" height="{H}" fill="#FDE7D3"/>',
        f'<rect width="{W}" height="{H}" fill="#E5533D" opacity="{flash:.3f}"/>',
        f'<g transform="translate({shake:.1f},0)">',
        '<ellipse cx="540" cy="1640" rx="640" ry="190" fill="#E9C9A8"/>',
        f'<ellipse cx="{540 + 170 * fallen:.0f}" cy="1575" rx="{230 * S / 2.3 * (1 + 0.6 * fallen):.0f}" ry="34" fill="#000" opacity="0.13"/>',
        f'<g transform="translate({mx:.1f},{my:.1f}) scale({S}) rotate({ang:.2f},190,375)">'
        f'{mochi(expr, blink, mouth_open=meow_open(t))}{phone_in_paws(t) if hold_phone else ""}</g>',
        stars(t, hx, hy),
        big_phone(t),
        card(title_op, "Eu a ver o preço", "do voo para o Japão"),
        card(fade(t, 4.6, 6.6), "O meu saldo: 0€", f"faltam só {PRICE}€", s1=72),
        card(fade(t, 6.8, 9.3), "Plano B:", "ir a nado", s1=80, s2=64),
        '</g>',
    ]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(parts)}</svg>'


def render():
    for n in range(FPS * TOTAL):
        cairosvg.svg2png(bytestring=frame_svg(n / FPS).encode(), write_to=os.path.join(FRAMES, f"f{n:04d}.png"))
    out = os.path.join(DIR, "mochi_voo.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", os.path.join(FRAMES, "f%04d.png"), "-i", os.path.join(DIR, "musica_voo.wav"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", out], check=True)
    return out


if __name__ == "__main__":
    if len(sys.argv) > 1:   # pré-visualização de frames: python video_voo.py 0 3.2 4.1 ...
        for s in sys.argv[1:]:
            cairosvg.svg2png(bytestring=frame_svg(float(s)).encode(), write_to=os.path.join(DIR, f"prev_voo_{s}.png"))
    else:
        print(render())
