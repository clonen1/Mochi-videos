"""Vídeo v2 do 'Dia 1' (1080x1920, 14 s, 30 fps), sincronizado com musica_dia1.wav.

Cenas: 0-4 sonho | 4-8 o plano (vaquinha) | 8-12 noite | 12-14 cartão final.
Transições: fundos em crossfade, textos entram/saem com deslize e fade, Mochi salta no tempo (120 BPM).
"""
import math
import os
import subprocess

import cairosvg

from mochi_kit import mochi

W, H, FPS, TOTAL = 1080, 1920, 30, 14
DIR = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(DIR, "frames_dia1")
os.makedirs(FRAMES, exist_ok=True)
META, ANGARIADO = 3000, 0
FONT = "DejaVu Sans"


# ---------- utilitários de animação ----------

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def spring(t):
    return 0 if t < 0 else 1 - math.exp(-t * 7) * math.cos(t * 16)


def window(t, a, b, fin=0.3, fout=0.25):
    """Opacidade de um elemento visível entre a e b, com entrada/saída suaves."""
    return ease((t - a) / fin) * (1 - ease((t - (b - fout)) / fout))


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def mixc(c1, c2, k):
    a, b = hexrgb(c1), hexrgb(c2)
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * k) for i in range(3))


def keyed_color(t, keys):
    """keys: lista de (tempo, cor). Interpola com easing."""
    for (t0, c0), (t1, c1) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            return mixc(c0, c1, ease((t - t0) / (t1 - t0)))
    return keys[-1][1] if t > keys[-1][0] else keys[0][1]


# ---------- elementos ----------

def text_card(t, a, b, l1, l2, dark=False, y=200):
    op = window(t, a, b)
    if op <= 0:
        return ""
    dy = (1 - ease((t - a) / 0.3)) * -40
    box, c1, c2 = ("#1F2740", "#FFD166", "#FFFFFF") if dark else ("#FFFFFF", "#D8343A", "#2B2B2B")
    return (f'<g opacity="{op:.3f}" transform="translate(0,{dy:.1f})">'
            f'<rect x="90" y="{y}" width="900" height="280" rx="44" fill="{box}" opacity="0.96"/>'
            f'<text x="540" y="{y + 118}" font-family="{FONT}" font-weight="bold" font-size="88" fill="{c1}" text-anchor="middle">{l1}</text>'
            + _sub(t, l2, c2, y) +
            f'</g>')


def _sub(t, l2, color, y):
    """Segunda linha: texto fixo ou lista [(inicio, texto), ...] com troca suave."""
    if isinstance(l2, str):
        l2 = [(-1, l2)]
    out = ""
    for i, (ts, txt) in enumerate(l2):
        te = l2[i + 1][0] if i + 1 < len(l2) else 99
        op = window(t, ts, te, 0.25, 0.2) if ts > 0 else 1 - ease((t - (te - 0.2)) / 0.2)
        if op > 0 and txt:
            out += (f'<text x="540" y="{y + 215}" font-family="{FONT}" font-weight="bold" font-size="52" '
                    f'fill="{color}" text-anchor="middle" opacity="{op:.3f}">{txt}</text>')
    return out


def fuji(op):
    return (f'<g opacity="{op:.3f}">'
            '<circle cx="780" cy="1120" r="150" fill="#F28B6B" opacity="0.55"/>'
            '<polygon points="380,1500 700,1160 760,1125 820,1160 1140,1500" fill="#9FB4D6"/>'
            '<polygon points="660,1205 700,1160 760,1125 820,1160 860,1205 800,1190 760,1215 720,1190" fill="#FFFFFF"/>'
            '</g>')


def thought_bubble(t, a, b):
    op = window(t, a, b, 0.25, 0.3)
    if op <= 0:
        return ""
    s = 0.6 + 0.4 * spring(t - a)
    fl = math.sin(t * 3) * 8
    return (f'<g opacity="{op:.3f}" transform="translate(830,{640 + fl:.1f}) scale({s:.3f})">'
            '<circle cx="-150" cy="200" r="16" fill="#FFFFFF"/><circle cx="-105" cy="150" r="24" fill="#FFFFFF"/>'
            '<ellipse cx="0" cy="0" rx="170" ry="120" fill="#FFFFFF"/>'
            # tigela de ramen
            '<path d="M-90 0 A90 70 0 0 0 90 0 Z" fill="#D8343A"/>'
            '<rect x="-96" y="-8" width="192" height="14" rx="7" fill="#B8262C"/>'
            '<path d="M-60 -10 Q-40 -40 -20 -10 Q0 -40 20 -10 Q40 -40 60 -10" fill="none" stroke="#F6C343" stroke-width="9" stroke-linecap="round"/>'
            '<circle cx="35" cy="-22" r="16" fill="#FFF6EA"/><circle cx="35" cy="-22" r="7" fill="#F6C343"/>'
            '<line x1="-20" y1="-90" x2="70" y2="-15" stroke="#8A5A3C" stroke-width="8" stroke-linecap="round"/>'
            '<line x1="0" y1="-98" x2="85" y2="-25" stroke="#8A5A3C" stroke-width="8" stroke-linecap="round"/>'
            '<path d="M-40 -60 Q-30 -80 -40 -100 M-70 -50 Q-60 -70 -70 -90" fill="none" stroke="#CCCCCC" stroke-width="5" stroke-linecap="round"/>'
            '</g>')


def progress_card(t, a, b):
    op = window(t, a, b)
    if op <= 0:
        return ""
    pct = ANGARIADO / META
    shine = (t * 0.6) % 1
    fill_w = max(24, 760 * pct)
    return (f'<g opacity="{op:.3f}">'
            '<rect x="140" y="520" width="800" height="170" rx="34" fill="#FFFFFF" opacity="0.95"/>'
            f'<text x="180" y="580" font-family="{FONT}" font-weight="bold" font-size="38" fill="#2B2B2B">Vaquinha</text>'
            f'<text x="900" y="580" font-family="{FONT}" font-weight="bold" font-size="38" fill="#2E8B57" text-anchor="end">{ANGARIADO}€ / {META}€</text>'
            '<rect x="160" y="612" width="760" height="46" rx="23" fill="#E6E6E6"/>'
            f'<rect x="160" y="612" width="{fill_w:.0f}" height="46" rx="23" fill="#3CB371"/>'
            f'<rect x="{160 + 700 * shine:.0f}" y="612" width="60" height="46" rx="23" fill="#FFFFFF" opacity="0.35"/>'
            '</g>')


def coins(t):
    out = ""
    for i in range(7):
        t0 = 4.5 + i * 0.5
        lt = t - t0 + 0.9
        if not (0 < lt < 1.6) or t > 7.9:
            continue
        x = [200, 860, 330, 760, 160, 920, 520][i]
        y = -60 + lt * 900 + 260 * lt * lt
        rx = 44 * abs(math.cos(lt * 7 + i))
        op = 1 - ease((t - 7.6) / 0.3)
        out += (f'<g opacity="{op:.2f}"><ellipse cx="{x}" cy="{y:.0f}" rx="{max(rx, 6):.0f}" ry="44" fill="#F6C343" stroke="#C9971C" stroke-width="6"/>'
                f'<text x="{x}" y="{y + 17:.0f}" font-family="{FONT}" font-weight="bold" font-size="46" fill="#9A6F0C" text-anchor="middle" opacity="{min(1, rx / 30):.2f}">€</text></g>')
    return out


def night_sky(op, t):
    if op <= 0:
        return ""
    out = f'<g opacity="{op:.3f}">'
    moon_y = 760 - 120 * ease((t - 8) / 1.5)
    out += (f'<mask id="lua"><rect width="{W}" height="{H}" fill="#fff"/>'
            f'<circle cx="888" cy="{moon_y - 22:.0f}" r="64" fill="#000"/></mask>'
            f'<circle cx="860" cy="{moon_y:.0f}" r="72" fill="#F4E9C8" mask="url(#lua)"/>')
    for i, (sx, sy) in enumerate([(150, 620), (300, 760), (720, 860), (980, 960), (110, 980), (560, 600), (420, 900), (930, 560)]):
        tw = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(t * 3 + i * 1.7))
        out += f'<circle cx="{sx}" cy="{sy}" r="{5 + i % 3}" fill="#FFFFFF" opacity="{tw:.2f}"/>'
    return out + "</g>"


def zzz(t):
    if not 8.8 < t < 12.1:
        return ""
    out = ""
    for i in range(3):
        p = ((t - 8.8) * 0.45 + i / 3) % 1
        fade = 1 - ease((t - 11.8) / 0.3)
        out += (f'<text x="{690 + p * 140:.0f}" y="{1000 - p * 300:.0f}" font-family="{FONT}" font-weight="bold" '
                f'font-size="{48 + p * 44:.0f}" fill="#FFFFFF" opacity="{(1 - p) * fade:.2f}">Z</text>')
    return out


def sparkles(t):
    if t < 12:
        return ""
    out = ""
    for i, (x, y) in enumerate([(200, 760), (880, 820), (150, 1250), (930, 1300), (540, 640)]):
        p = ((t - 12) * 0.9 + i * 0.21) % 1
        s = math.sin(math.pi * p) * 22
        out += f'<path d="M{x} {y - s:.0f} L{x + s * .3:.0f} {y} L{x} {y + s:.0f} L{x - s * .3:.0f} {y} Z" fill="#F6C343"/>'
    return out


# ---------- composição ----------

BG = [(0, "#FDE7D3"), (3.8, "#FDE7D3"), (4.2, "#DFF1E4"), (7.6, "#DFF1E4"), (8.6, "#2E3A5C"),
      (11.6, "#2E3A5C"), (12.3, "#FFE3C4")]
FLOOR = [(0, "#E9C9A8"), (3.8, "#E9C9A8"), (4.2, "#BFE0C8"), (7.6, "#BFE0C8"), (8.6, "#1E2742"),
         (11.6, "#1E2742"), (12.3, "#F2C79A")]


def mochi_state(t):
    if t < 2.2:
        expr = "normal"
    elif t < 8.4:
        expr = "happy"
    elif t < 12:
        expr = "sleep"
    else:
        expr = "happy"
    blink = 1.55 < t < 1.7 or 6.9 < t < 7.0
    # entrada com mola, saltos no tempo no groove, respiração à noite
    scale = 2.3 * (spring(t) if t < 1 else 1)
    bob = 0.0
    if 4 <= t < 8:
        bob = -abs(math.sin(math.pi * (t - 4) / 0.5)) * 34
    elif 8.4 <= t < 12:
        scale *= 1 + 0.02 * math.sin((t - 8.4) * 2.4)
    else:
        bob = math.sin(t * 3) * 8
    if 12 <= t:
        scale *= 1 + 0.12 * math.exp(-(t - 12) * 6) * math.cos((t - 12) * 18)
    return expr, blink, scale, bob


def frame_svg(t):
    bg = keyed_color(t, BG)
    floor = keyed_color(t, FLOOR)
    night = ease((t - 7.6) / 1.0) * (1 - ease((t - 11.6) / 0.7))
    expr, blink, scale, bob = mochi_state(t)
    mx = (W - 380 * scale) / 2
    my = 1560 - 370 * scale + bob
    shadow_w = 230 * scale / 2.3 * (1 + bob / 200)
    fuji_op = 0.9 * ease(t / 0.8) * (1 - ease((t - 3.7) / 0.4)) + 0.9 * ease((t - 12) / 0.5)
    parts = [
        f'<rect width="{W}" height="{H}" fill="{bg}"/>',
        night_sky(night, t),
        fuji(fuji_op),
        f'<ellipse cx="540" cy="1640" rx="640" ry="190" fill="{floor}"/>',
        coins(t),
        f'<ellipse cx="540" cy="1575" rx="{shadow_w:.0f}" ry="34" fill="#000" opacity="0.13"/>',
        f'<g transform="translate({mx:.1f},{my:.1f}) scale({scale:.3f})">{mochi(expr, blink)}</g>',
        thought_bubble(t, 2.0, 3.9),
        zzz(t),
        sparkles(t),
        text_card(t, 0.25, 3.95, "Dia 1", [(-1, "O Mochi tem um sonho..."), (2.1, "comer ramen no Japão!")]),
        text_card(t, 4.1, 7.9, "O plano:", "juntar 3000€ para a viagem"),
        progress_card(t, 4.35, 7.9),
        text_card(t, 8.3, 11.95, "Primeiro passo...", [(-1, ""), (9.9, "uma sestinha")], dark=True),
        text_card(t, 12.15, 14.5, "Segue o Mochi!", "Dia 2 já amanhã"),
        f'<text x="540" y="560" font-family="{FONT}" font-weight="bold" font-size="40" fill="#8A6A50" '
        f'text-anchor="middle" opacity="{window(t, 12.4, 14.5):.2f}">Ajuda a vaquinha: link na bio</text>',
    ]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(parts)}</svg>'


def render():
    for n in range(FPS * TOTAL):
        cairosvg.svg2png(bytestring=frame_svg(n / FPS).encode(), write_to=os.path.join(FRAMES, f"f{n:04d}.png"))
    out = os.path.join(DIR, "mochi_dia1_v2.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", os.path.join(FRAMES, "f%04d.png"), "-i", os.path.join(DIR, "musica_dia1.wav"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", out], check=True)
    return out


if __name__ == "__main__":
    print(render())
