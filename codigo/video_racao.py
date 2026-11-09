"""Vídeo 'O Mochi e o saco de ração' (meme em 1.ª pessoa, 1080x1920, 10 s, 30 fps), em loop.

0-2.4   Mochi a dormir: 'Eu a dormir...' (zzz)
2.4-3.5 CRRR! um saco amachuca ao longe: 'Barulho de saco de ração' | 3.2 abre os olhos de repente
3.5     teletransporte: já está ao pé da taça | 'Eu, 0,2 s depois' | miados 4.3 e 6.1
5.5     'Onde está a ração?' | 7.5 o saco afinal é do pão: 'Era só o saco do pão.'
9.4-10  volta a dormir (liga ao início)
Sem preços, nomes de cidades nem link.
"""
import math

from mochi_cena import FONT, W, H, burst, card, clamp, ease, fade, main, meow_open, svg_doc
from mochi_kit import mochi
from mochi_longo import zzz
from mochi_props import bowl
from mochi_props_racao import saco, speed_lines
from musica_racao import MEOWS, TOTAL

S = 2.0
FLOOR = 1720
SLEEP_X, AWAKE_X = -50, 150
MY = FLOOR - 378 * S
BOWL = (870, FLOOR - 55)
BAG = (860, 1200)


def sleeping_group(t):
    nod = math.sin(t * 2.2) * 3
    expr = "sleep"
    blink = False
    if 3.2 <= t < 3.5:
        expr = "shock"
    bob = 6 * math.sin(t * 2.2)
    return (f'<g transform="translate({SLEEP_X},{MY + 70 + bob:.1f}) scale({S}) rotate({-10 + nod:.1f},190,378)">'
            f'{mochi(expr, blink)}</g>')


def awake_group(t):
    if 3.5 <= t < 5.5:
        expr = "angry" if t > 4.9 else "shock"
    elif 5.5 <= t < 7.5:
        expr = "sad"
    else:
        expr = "ko" if t >= 8.4 else "sad"
    hop = 0.0
    if 3.5 <= t < 3.95:
        hop = 90 * math.sin(math.pi * (t - 3.5) / 0.45)
    tilt = 0
    if 5.5 <= t < 7.5:
        tilt = 4 * math.sin((t - 5.5) * 5)
    blink = 8.0 < t < 8.12
    return (f'<g transform="translate({AWAKE_X},{MY - hop:.1f}) scale({S}) rotate({tilt:.1f},190,378)">'
            f'{mochi(expr, blink, mouth_open=meow_open(t, MEOWS))}</g>')


def frame_svg(t):
    sleep_op = 1.0 if t < 3.5 else (ease((t - 9.4) / 0.5) if t >= 9.4 else 0.0)
    awake_op = 1.0 - sleep_op if t >= 3.5 else 0.0
    title_op = 1.0
    parts = [
        f'<rect width="{W}" height="{H}" fill="#FDEFD8"/>',
        f'<rect x="0" y="{FLOOR - 40}" width="{W}" height="{H - FLOOR + 40}" fill="#EBC99B"/>',
        f'<ellipse cx="{SLEEP_X + 380}" cy="{FLOOR + 10}" rx="300" ry="38" fill="#000" opacity="0.10"/>',
        # almofada do Mochi
        f'<ellipse cx="{SLEEP_X + 380}" cy="{FLOOR - 15}" rx="320" ry="60" fill="#8FB8DE" stroke="#2B2B2B" stroke-width="6"/>',
        f'<g transform="translate({BOWL[0]},{BOWL[1]}) scale(0.95)">{bowl(food=False)}</g>',
    ]
    if sleep_op > 0:
        parts.append(f'<g opacity="{sleep_op:.2f}">{sleeping_group(t)}</g>')
    if t < 3.2 or t >= 9.4:
        zop = fade(t, 0.0, 2.6, 0.1, 0.3) if t < 3.2 else ease((t - 9.4) / 0.5)
        parts.append(f'<g opacity="{zop:.2f}">{zzz(t, 520, 1150, 3, 70)}</g>')
    if awake_op > 0:
        parts.append(f'<g opacity="{awake_op:.2f}">{awake_group(t)}</g>')
    # o saco (primeiro um mistério, depois é de pão)
    if 2.4 <= t < 3.5:
        shake = 6 * math.sin(t * 60)
        parts.append(f'<g transform="translate({BAG[0] + shake:.0f},{BAG[1]}) rotate({shake:.1f}) scale(0.8)" '
                     f'opacity="{fade(t, 2.4, 3.5, 0.1, 0.2):.2f}">{saco(False, 1)}</g>')
    if 7.5 <= t < 9.4:
        pop = 1 + 0.08 * math.sin((t - 7.5) * 14) * (1 - ease((t - 7.5) / 0.8))
        parts.append(f'<g transform="translate({BAG[0]},{BAG[1]}) scale({0.85 * pop:.3f})" '
                     f'opacity="{fade(t, 7.5, 9.4, 0.2, 0.3):.2f}">{saco(True)}</g>')
    parts += [
        burst(fade(t, 2.45, 3.3, 0.05, 0.25), 300, 1020, "CRRR!", 100, r=170),
        burst(fade(t, 3.5, 4.2, 0.05, 0.3), 280, 1000, "ZUM!", 100, color="#2B2B2B", r=160),
        speed_lines(fade(t, 3.5, 3.8, 0.05, 0.2), 80, 1350),
        card(fade(t, 0.2, 2.4, 0.3, 0.2), "Eu a dormir...", y=480, s1=84),
        card(fade(t, 2.45, 3.5, 0.2, 0.2), "Barulho de", "saco de ração", y=480, s1=76, s2=84),
        card(fade(t, 3.55, 5.5, 0.15, 0.2), "Eu, 0,2 s depois", y=480, s1=80),
        card(fade(t, 5.55, 7.5, 0.2, 0.2), "Onde está", "a ração?", y=480, s1=76, s2=88),
        card(fade(t, 7.55, 9.35, 0.2, 0.2), "Era só o saco", "do pão...", y=480, s1=72, s2=88),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("racao", frame_svg, TOTAL)
