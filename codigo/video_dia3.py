"""Vídeo 'Dia 3: o Mochi aprende japonês' (1080x1920, 10 s, 30 fps), em loop.

0-2.1 'Obrigado = Arigatô' -> o Mochi diz 'Miaugatô!' -> ERRADO
2.2-4.4 'Olá = Konnichiwa' -> 'Konni-MIAU!' -> 'Quase, Mochi.'
4.5-6.6 'Ramen, por favor' -> 'Ramen kudasai!' -> PERFEITO (comida aprende à primeira)
6.7-8.8 'Bilhete de avião = ?' -> susto -> 'Falta só o voo. 0€ até agora'
8.9-10 volta ao início
"""
import math

from mochi_cena import W, H, FONT, card, clamp, ease, fade, main, meow_open, spring, burst, svg_doc
from mochi_kit import mochi
from musica_dia3 import MEOWS, TOTAL

ANGARIADO = 0
S = 2.0
FLOOR = 1720
BOARD = [  # (início, fim, linha PT, linha JP)
    (-1.0, 2.15, "Obrigado", "Arigatô"),
    (2.15, 4.45, "Olá", "Konnichiwa"),
    (4.45, 6.65, "Ramen, por favor", "Ramen kudasai"),
    (6.65, 8.85, "Bilhete de avião", "???"),
    (8.85, 99, "Obrigado", "Arigatô"),
]
BUBBLES = [(MEOWS[0], 1.9, "Miaugatô!"), (MEOWS[1], 4.2, "Konni-MIAU!"), (MEOWS[2], 6.4, "Ramen kudasai!")]


def board_svg(t):
    pt, jp = "", ""
    for a, b, p, j in BOARD:
        if a <= t < b:
            pt, jp, t0 = p, j, a
    # o giz "escreve": a linha nova aparece depressa
    op = clamp((t - t0) / 0.15) if t0 > 0 else 1.0
    return ('<rect x="90" y="490" width="900" height="400" rx="26" fill="#8B5A2B"/>'
            '<rect x="110" y="510" width="860" height="360" rx="16" fill="#2F5D50"/>'
            f'<text x="540" y="580" font-family="{FONT}" font-weight="bold" font-size="40" fill="#BFD8CF" text-anchor="middle">Aula de japonês</text>'
            f'<g opacity="{op:.2f}">'
            f'<text x="540" y="705" font-family="{FONT}" font-weight="bold" font-size="70" fill="#FFFFFF" text-anchor="middle">{pt} =</text>'
            f'<text x="540" y="815" font-family="{FONT}" font-weight="bold" font-size="80" fill="#F6C343" text-anchor="middle">{jp}</text></g>'
            '<rect x="700" y="868" width="90" height="18" rx="6" fill="#FFFFFF"/>')


def bubble_svg(t):
    for t0, t1, txt in BUBBLES:
        op = fade(t, t0 - 0.05, t1, 0.12, 0.2)
        if op <= 0:
            continue
        sc = 0.6 + 0.4 * clamp(spring((t - t0 + 0.05) * 1.3))
        size = 62
        w = len(txt) * size * 0.62 + 90
        cx, cy = 720 if w < 600 else 1080 - w / 2 - 40, 990
        return (f'<g opacity="{op:.2f}" transform="translate({cx:.0f},{cy}) scale({sc:.2f})">'
                f'<polygon points="-120,40 -60,40 -190,150" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="6" stroke-linejoin="round"/>'
                f'<rect x="{-w / 2:.0f}" y="-70" width="{w:.0f}" height="130" rx="60" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="6"/>'
                f'<polygon points="-118,34 -64,34 -170,128" fill="#FFFFFF"/>'
                f'<text x="0" y="18" font-family="{FONT}" font-weight="bold" font-size="{size}" fill="#2B2B2B" text-anchor="middle">{txt}</text></g>')
    return ""


def mochi_expr(t):
    for a, b, e in [(0.95, 2.0, "angry"), (3.2, 4.3, "normal"), (5.4, 6.6, "happy"), (6.9, 8.8, "shock")]:
        if a <= t < b:
            return e
    return "normal"


def frame_svg(t):
    hop = 0.0
    for t0 in (0.95, 5.4, 6.9):
        if t0 <= t < t0 + 0.35:
            hop = 50 * math.sin(math.pi * (t - t0) / 0.35)
    mx = 540 - 190 * S
    my = FLOOR - 378 * S - hop
    sad = 3.2 <= t < 4.3
    tilt = -6 if sad else 0
    blink = 1.6 < t < 1.72 or 3.4 < t < 3.55 or 8.2 < t < 8.32
    title_op = 1 - ease((t - 2.0) / 0.25) if t < 5 else ease((t - 9.2) / 0.45)
    parts = [
        f'<rect width="{W}" height="{H}" fill="#FDE7D3"/>',
        f'<rect x="0" y="{FLOOR - 40}" width="{W}" height="{H - FLOOR + 40}" fill="#E9C9A8"/>',
        f'<ellipse cx="540" cy="{FLOOR}" rx="300" ry="34" fill="#000" opacity="0.12"/>',
        board_svg(t),
        burst(fade(t, 0.95, 2.0, 0.08, 0.3), 540, 690, "ERRADO!", 84, r=240),
        burst(fade(t, 5.4, 6.55, 0.08, 0.3), 540, 690, "PERFEITO!", 76, color="#2E8B57", r=250),
        f'<g transform="translate({mx:.1f},{my:.1f}) scale({S}) rotate({tilt},190,375)">'
        f'{mochi(mochi_expr(t), blink or sad, mouth_open=meow_open(t, MEOWS))}</g>',
        bubble_svg(t),
        card(title_op, "Dia 3", "O Mochi aprende japonês", s1=84),
        card(fade(t, 3.15, 4.4), "Quase, Mochi.", s1=76),
        card(fade(t, 5.4, 6.6), "Palavras de comida:", "aprende à primeira", s1=64),
        card(fade(t, 7.35, 9.25), "Falta só o voo.", f"{ANGARIADO}€ até agora. Link na bio", s1=72, s2=50),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("dia3", frame_svg, TOTAL)
