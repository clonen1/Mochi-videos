"""Vídeo 'Eu vs o pepino' (humor de gato, 1.ª pessoa; 1080x1920, 10 s, 30 fps), em loop.

0-1.6   'Eu a comer em paz' | 0.3 um pepino entra devagarinho pela esquerda
1.65    SALTO enorme (AAAH!) e fica a tremer lá em cima
3.8     aterra: 'Inimigo identificado: PEPINO' | 5.5 cheira... 'Ele não faz nada.'
7.2     PLOC: manda o pepino pelo ar | 'Eu sabia. Era um teste.'
8.6-10  volta a comer, igual ao início
"""
import math

from mochi_cena import W, H, FONT, burst, card, clamp, ease, fade, main, meow_open, spring, svg_doc
from mochi_kit import mochi
from mochi_props import bowl, cucumber
from musica_pepino import MEOWS, TOTAL

S = 1.8
FLOOR = 1720
HOME_X = 610
CUKE_Y = FLOOR - 50


def mochi_x(t):
    if 3.8 <= t < 8.6:
        k = ease((t - 3.9) / 0.5) * (1 - ease((t - 8.3) / 0.4))
        return HOME_X - 90 * k
    return HOME_X


def mochi_lift(t):
    """Altura do salto (px para cima)."""
    if 1.65 <= t < 2.0:
        return 600 * spring((t - 1.65) * 2.2) if t < 2.0 else 600
    if 2.0 <= t < 3.6:
        return 600 + 12 * math.sin(t * 60)
    if 3.6 <= t < 3.8:
        return 600 * (1 - ((t - 3.6) / 0.2) ** 2)
    return 0.0


def mochi_expr(t):
    for a, b, e in [(0, 1.62, "eat"), (1.62, 3.8, "shock"), (3.8, 5.5, "angry"), (5.5, 7.15, "normal"),
                    (7.15, 8.6, "happy"), (8.6, 99, "eat")]:
        if a <= t < b:
            return e
    return "normal"


def cuke_pose(t):
    """(x, y, rot, visível)"""
    if t < 0.3:
        return -200, CUKE_Y, 0, True
    if t < 7.2:
        k = ease((t - 0.3) / 0.6)
        return -200 + 380 * k, CUKE_Y, 0, True
    if t < 8.2:
        k = (t - 7.2) / 1.0
        return 180 - 700 * k, CUKE_Y - 1300 * k + 1200 * k * k, -720 * k, True
    return -200, CUKE_Y, 0, True


def frame_svg(t):
    x = mochi_x(t)
    lift = mochi_lift(t)
    eat_bob = 8 * abs(math.sin(t * 6)) if mochi_expr(t) == "eat" else 0
    puff = 1.12 if 1.65 <= t < 3.8 else 1.0
    s = S * puff
    mx = x - 190 * s
    my = FLOOR - 378 * s - lift + eat_bob
    lean = -10 if 5.5 <= t < 7.15 else 0
    swat = -18 * math.sin(math.pi * (t - 7.1) / 0.3) if 7.1 <= t < 7.4 else 0
    blink = 4.5 < t < 4.62 or 6.2 < t < 6.32
    cx, cy, crot, _ = cuke_pose(t)
    peace_op = 1 - ease((t - 1.6) / 0.1) if t < 5 else ease((t - 9.2) / 0.45)
    shadow_rx = 260 * (1 - min(lift, 600) / 900)
    parts = [
        f'<rect width="{W}" height="{H}" fill="#E4F1E1"/>',
        '<rect x="80" y="760" width="260" height="320" rx="16" fill="#CFE3CB"/>'
        '<rect x="100" y="780" width="220" height="280" rx="10" fill="#BFE3F5"/>',
        f'<rect x="0" y="{FLOOR - 40}" width="{W}" height="{H - FLOOR + 40}" fill="#C9B79A"/>',
        f'<ellipse cx="{x:.0f}" cy="{FLOOR}" rx="{shadow_rx:.0f}" ry="30" fill="#000" opacity="0.12"/>',
        f'<g transform="translate({cx:.0f},{cy:.0f}) rotate({crot:.0f}) scale(0.9)">{cucumber()}</g>',
        f'<g transform="translate({mx:.1f},{my:.1f}) scale({s:.3f}) rotate({lean + swat},190,375)">'
        f'{mochi(mochi_expr(t), blink, mouth_open=meow_open(t, MEOWS))}</g>',
        f'<g transform="translate({HOME_X + 40},{FLOOR - 25}) scale(0.85)">{bowl()}</g>',
    ]
    if 1.65 <= t < 3.7:  # traços de tremer
        for i in range(3):
            yy = my + 200 + i * 120
            parts.append(f'<path d="M{x - 400:.0f} {yy:.0f} l-50 -20 M{x + 400:.0f} {yy:.0f} l50 -20" '
                         f'stroke="#2B2B2B" stroke-width="8" stroke-linecap="round" opacity="0.6"/>')
    parts += [
        burst(fade(t, 1.65, 2.9, 0.06, 0.3), 300, 1250, "AAAH!", 88, r=175),
        burst(fade(t, 7.2, 8.0, 0.05, 0.3), 260, 1450, "PLOC!", 78, color="#2E8B57", r=155),
        card(peace_op, "Eu a comer em paz", y=300, s1=72),
        card(fade(t, 2.0, 3.8), "PERIGO MORTAL", y=180, s1=80),
        card(fade(t, 3.9, 5.5), "Inimigo identificado:", "PEPINO", y=300, s1=62, s2=80),
        card(fade(t, 5.6, 7.2), "Ele não faz nada...", y=300, s1=72),
        card(fade(t, 7.25, 9.0), "Eu sabia.", "Era só um teste.", y=300, s1=76, s2=60),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("pepino", frame_svg, TOTAL)
