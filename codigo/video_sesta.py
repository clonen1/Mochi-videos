"""Vídeo 'Eu quando me acordam da sesta' (1080x1920, 10 s, 30 fps), em loop.

0-0.3 Mochi a dormir | 0.3-2 despertador toca | 2 acorda zangado | 3 PAF, o despertador voa
3.4-5.6 'Ninguém me acorda.' | 5.8-8.2 chega a comida, come | 8.3-9.3 volta a dormir | 9.35-10 início
"""
import math

from mochi_cena import W, H, FONT, card, clamp, ease, fade, main, meow_open, spring, burst, svg_doc
from mochi_kit import mochi
from musica_sesta import MEOWS, TOTAL

S = 1.75
MX = 540 - 190 * S - 110
FLOOR = 1600
CLOCK_X, CLOCK_Y = 900, 1480


def clock_svg(t):
    ring = 0.3 <= t < 2.95
    x, y, rot = CLOCK_X, CLOCK_Y, 0.0
    if ring:
        rot = math.sin(t * 70) * 12
        x += math.sin(t * 55) * 6
    if 3.0 <= t < 8.8:             # voou para fora do ecrã
        u = clamp((t - 3.0) / 0.6)
        x += 520 * u
        y -= 700 * u - 900 * u * u
        rot = 720 * u
    elif 8.8 <= t < 9.6:           # volta devagarinho
        x += 300 * (1 - ease((t - 8.8) / 0.8))
    return (f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot:.1f})">'
            '<line x1="-50" y1="70" x2="-70" y2="105" stroke="#2B2B2B" stroke-width="12" stroke-linecap="round"/>'
            '<line x1="50" y1="70" x2="70" y2="105" stroke="#2B2B2B" stroke-width="12" stroke-linecap="round"/>'
            '<circle cx="-55" cy="-78" r="32" fill="#F6C343" stroke="#2B2B2B" stroke-width="6"/>'
            '<circle cx="55" cy="-78" r="32" fill="#F6C343" stroke="#2B2B2B" stroke-width="6"/>'
            '<circle cx="0" cy="0" r="92" fill="#D8343A" stroke="#2B2B2B" stroke-width="6"/>'
            '<circle cx="0" cy="0" r="70" fill="#FFFFFF"/>'
            '<line x1="0" y1="0" x2="0" y2="-48" stroke="#2B2B2B" stroke-width="8" stroke-linecap="round"/>'
            '<line x1="0" y1="0" x2="34" y2="10" stroke="#2B2B2B" stroke-width="8" stroke-linecap="round"/>'
            '<circle cx="0" cy="0" r="8" fill="#2B2B2B"/></g>')


def bowl_x(t):
    if t < 5.8 or t >= 9.2:
        return None
    if t < 6.2:
        return -200 + 640 * ease((t - 5.8) / 0.4)
    if t < 8.6:
        return 440
    return 440 - 640 * ease((t - 8.6) / 0.6)


def bowl_svg(t):
    x = bowl_x(t)
    if x is None:
        return ""
    full = 1 - clamp((t - 6.8) / 1.2)
    food = ""
    if full > 0.02:
        food = f'<ellipse cx="0" cy="-28" rx="{95 * (0.4 + 0.6 * full):.0f}" ry="{26 * full + 4:.0f}" fill="#B5713A"/>'
    return (f'<g transform="translate({x:.0f},1700) scale(1.3)">{food}'
            '<path d="M-130 -30 L130 -30 L105 40 L-105 40 Z" fill="#3F6FB0" stroke="#2B2B2B" stroke-width="6" stroke-linejoin="round"/>'
            f'<text x="0" y="25" font-family="{FONT}" font-weight="bold" font-size="40" fill="#FFFFFF" text-anchor="middle">MOCHI</text></g>')


def paw_svg(t, my):
    if not 2.75 <= t < 3.35:
        return ""
    u = math.sin(math.pi * (t - 2.75) / 0.6)
    sx, sy = MX + 321 * S, my + 240 * S
    ex, ey = sx + 200 * u, sy + 60 * u
    return (f'<line x1="{sx}" y1="{sy}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="#F2A14A" stroke-width="56" stroke-linecap="round"/>'
            f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="36" ry="30" fill="#FFF6EA"/>')


def zzz(t):
    if not (t < 2.0 or t >= 8.6):
        return ""
    out = ""
    for i in range(3):
        ph = ((t * 0.6) + i / 3) % 1
        op = math.sin(math.pi * ph)
        x = MX + 290 * S + 70 * ph + 20 * math.sin(ph * 6)
        y = 1000 - 260 * ph
        out += (f'<text x="{x:.0f}" y="{y:.0f}" font-family="{FONT}" font-weight="bold" font-size="{50 + 40 * ph:.0f}" '
                f'fill="#3F6FB0" opacity="{op:.2f}">Z</text>')
    return out


def mochi_expr(t):
    for a, b, e in [(2.0, 5.8, "angry"), (5.8, 6.1, "shock"), (6.1, 6.8, "happy"), (6.8, 8.0, "eat"), (8.0, 8.6, "happy")]:
        if a <= t < b:
            return e
    return "sleep"


def frame_svg(t):
    expr = mochi_expr(t)
    breathe = math.sin(t * math.pi * 1.2) * 0.015 if expr == "sleep" else 0
    hop = 70 * math.sin(math.pi * (t - 2.0) / 0.35) if 2.0 <= t < 2.35 else 0
    hop += 60 * math.sin(math.pi * (t - 5.95) / 0.3) if 5.95 <= t < 6.25 else 0
    nom = 10 * abs(math.sin((t - 6.8) * 13)) if 6.8 <= t < 8.0 else 0
    my = FLOOR - 10 - 372 * S - hop + nom
    shake = math.sin(t * 90) * 14 * (1 - (t - 3.0) / 0.35) if 3.0 <= t < 3.35 else 0
    title_op = 1 - ease((t - 2.05) / 0.3) if t < 5 else ease((t - 9.35) / 0.4)
    parts = [
        f'<rect width="{W}" height="{H}" fill="#E4E8F7"/>',
        '<rect x="680" y="560" width="300" height="360" rx="20" fill="#C9D3F0"/>',
        '<line x1="830" y1="560" x2="830" y2="920" stroke="#E4E8F7" stroke-width="14"/>',
        '<line x1="680" y1="740" x2="980" y2="740" stroke="#E4E8F7" stroke-width="14"/>',
        f'<g transform="translate({shake:.1f},0)">',
        f'<ellipse cx="540" cy="{FLOOR + 120}" rx="700" ry="230" fill="#C7B8E0"/>',
        f'<ellipse cx="{MX + 190 * S:.0f}" cy="{FLOOR - 5}" rx="330" ry="70" fill="#F5B5B5"/>',
        f'<ellipse cx="{MX + 190 * S:.0f}" cy="{FLOOR - 25}" rx="300" ry="45" fill="#F7C9C9"/>',
        f'<g transform="translate({MX:.1f},{my:.1f}) scale({S},{S * (1 + breathe):.4f})">'
        f'{mochi(expr, mouth_open=meow_open(t, MEOWS))}</g>',
        paw_svg(t, my),
        clock_svg(t),
        bowl_svg(t),
        zzz(t),
        burst(fade(t, 0.3, 2.0, 0.08, 0.2) * (0.92 + 0.08 * math.sin(t * 40)), 800, 1180, "TRIM!", 76, r=120),
        burst(fade(t, 3.0, 3.6, 0.05, 0.25), 830, 1150, "PAF!", 84, r=125),
        card(title_op, "Eu quando me acordam", "da sesta", s1=64, s2=64, c1="#2B2B2B"),
        card(fade(t, 3.4, 5.65), "Ninguém me acorda.", s1=70),
        card(fade(t, 5.8, 8.2), "...a não ser", "que seja comida", s1=70, s2=64),
        card(fade(t, 8.3, 9.35), "Agora sim: sesta.", s1=70, c1="#3F6FB0"),
        '</g>',
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("sesta", frame_svg, TOTAL)
