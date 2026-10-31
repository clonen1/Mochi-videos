"""Vídeo 'Tipos de gato quando chega a comida' (humor de gato, 1.ª pessoa; 1080x1920, 10 s, 30 fps), em loop.

0-0.25  a taça cai (PUM) | 0.25-0.9 chegam três Mochis a correr
1.6-3.6 '1. O educado' | 3.6-5.8 '2. O dramático' (desmaia e mia)
5.8-7.8 '3. O ninja' (PUF: já comeu tudo) | 7.9-9.3 'Eu sou os três. E tu?'
9.3-10  saem a correr e a taça sobe (volta ao início)
"""
import math

from mochi_cena import W, H, burst, card, clamp, ease, fade, main, meow_open, spring, svg_doc
from mochi_kit import mochi
from mochi_props import bowl, headband, smoke
from musica_comida import MEOWS, TOTAL

S = 1.15
FLOOR = 1740
XS = [210, 540, 870]
BOWL_Y = FLOOR - 45


def focus(t):
    if 1.6 <= t < 3.6:
        return 0
    if 3.6 <= t < 5.8:
        return 1
    if 5.8 <= t < 7.8:
        return 2
    return None


def enter(t, i):
    """(dx, dy) de entrada (0.25-0.9) e saída (9.3-9.8)."""
    k_in = ease((t - 0.25 - 0.08 * i) / 0.5)
    k_out = ease((t - 9.3 - 0.05 * i) / 0.45)
    k = k_in * (1 - k_out)
    if i == 0:
        return -650 * (1 - k), 0
    if i == 2:
        return 650 * (1 - k), 0
    return 0, -2300 * (1 - k)


def bowl_y(t):
    if t < 0.25:
        return -200 + (BOWL_Y + 200) * (t / 0.25) ** 2
    if t >= 9.3:
        return BOWL_Y + (-200 - BOWL_Y) * ease((t - 9.3) / 0.5)
    sq = 25 * math.exp(-(t - 0.25) * 9) * math.cos((t - 0.25) * 26)
    return BOWL_Y + sq


def expr(t, i):
    if t < 0.9 or t >= 9.3:
        return "shock" if t < 0.9 else "happy"
    if 7.8 <= t:
        return ["happy", "happy", "eat"][i]
    if i == 0:
        return "happy" if t < 5.9 else "shock"
    if i == 1:
        if 3.85 <= t < 5.6:
            return "ko"
        return "shock" if 5.9 <= t < 7.8 else "normal"
    # ninja
    if 5.8 <= t:
        return "eat"
    return "angry"


def cat(t, i):
    dx, dy = enter(t, i)
    x = XS[i] + dx
    y = FLOOR - 378 * S + dy
    rot = 0
    bob = 0
    if i == 0 and 1.8 <= t < 3.4:               # vénia educada
        rot = 10 * math.sin(math.pi * (t - 1.8) / 1.6)
    if i == 1:                                    # desmaio dramático
        k = ease((t - 3.75) / 0.25) * (1 - ease((t - 5.5) / 0.3))
        rot = -78 * k
    if i == 2 and t >= 6.0:                       # o ninja já está na taça
        k = ease((t - 6.0) / 0.15) * (1 - ease((t - 7.8) / 0.2))
        x -= 130 * k
    if expr(t, i) == "eat":
        bob = 7 * abs(math.sin(t * 9))
    blink = (i == 0 and (2.2 < t < 2.32 or 3.0 < t < 3.12)) or (i == 2 and 8.6 < t < 8.72)
    mo = meow_open(t, MEOWS) if i == 1 else 0.0
    f = focus(t)
    op = 1.0 if f is None or f == i else 0.3
    if i == 2 and 5.85 <= t < 6.0:
        op = 0.0                                  # some no fumo
    return (f'<g opacity="{op}" transform="translate({x - 190 * S:.1f},{y + bob:.1f}) scale({S}) rotate({rot:.1f},190,378)">'
            f'{mochi(expr(t, i), blink, mouth_open=mo)}{headband() if i == 2 else ""}</g>')


def frame_svg(t):
    title_op = 1 - ease((t - 1.45) / 0.2) if t < 5 else ease((t - 9.4) / 0.45)
    tiles = "".join(f'<rect x="{x}" y="{y}" width="116" height="116" rx="8" fill="#D9EEF0"/>'
                    for x in range(0, W, 124) for y in range(820, FLOOR - 40, 124))
    f = focus(t)
    order = [0, 1, 2] if f is None else [j for j in range(3) if j != f] + [f]
    parts = [
        f'<rect width="{W}" height="{H}" fill="#EAF6F7"/>',
        tiles,
        f'<rect x="0" y="{FLOOR - 40}" width="{W}" height="{H - FLOOR + 40}" fill="#D7B98E"/>',
        f'<ellipse cx="540" cy="{FLOOR}" rx="470" ry="30" fill="#000" opacity="0.10"/>',
    ]
    parts += [cat(t, j) for j in order]
    food = not (5.9 <= t < 9.3)
    parts.append(f'<g transform="translate(540,{bowl_y(t):.0f}) scale(0.95)">{bowl(food=food)}</g>')
    parts += [
        burst(fade(t, 0.25, 1.0, 0.05, 0.3), 540, 1080, "PUM!", 100, r=150),
        smoke(fade(t, 5.82, 6.6, 0.05, 0.4), 870, 1450, 130),
        burst(fade(t, 5.85, 6.5, 0.05, 0.3), 860, 1080, "PUF!", 90, color="#2B2B2B", r=130),
        card(title_op, "Tipos de gato", "quando chega a comida", y=520, s1=86, s2=60),
        card(fade(t, 1.65, 3.6), "1. O educado", "espera com calma", y=520, s1=80, s2=58),
        card(fade(t, 3.65, 5.8), "2. O dramático", "“Não como há 100 anos!”", y=520, s1=80, s2=52),
        card(fade(t, 5.85, 7.8), "3. O ninja", "...já comeu tudo.", y=520, s1=80, s2=60),
        card(fade(t, 7.9, 9.4, 0.2, 0.2), "Eu sou os três.", "E tu, qual és?", y=520, s1=76, s2=66),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("comida", frame_svg, TOTAL)
