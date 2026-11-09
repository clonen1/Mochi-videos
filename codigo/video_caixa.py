"""Vídeo 'Caixa pequena' (meme, 1.ª pessoa; 1080x1920, 10 s, 30 fps), em loop.

0-0.9   título 'Caixa pequena' | a caixa aparece
0.9-2.6 'Eu: cabe.' o Mochi anda até à caixa
2.6-4.0 'So a patinha...' | 4.0-5.6 'Não cabe.' a cabeça bate na caixa (TOC!)
5.6-6.4 senta-se em cima (PLOF!) | 6.4-9.3 'Cabe sim.' / 'Problema resolvido.' a transbordar, feliz
9.3-10  levanta-se, a caixa some e tudo recomeça (loop)
"""
import math

from mochi_cena import FONT, W, H, burst, card, clamp, ease, fade, main, meow_open, spring, svg_doc
from mochi_kit import mochi
from mochi_props import paw
from mochi_props_caixa import box_front, box_inside
from musica_caixa import MEOWS, TOTAL

S = 2.0
FLOOR = 1720
BX = 690          # centro da caixa
START = 330       # centro do Mochi no início


def lerp(a, b, u):
    return a + (b - a) * ease(u)


def mochi_x(t):
    if t < 0.9:
        return START
    if t < 2.4:
        return lerp(START, 420, (t - 0.9) / 1.5)
    if t < 5.6:
        return 420
    if t < 6.2:
        return lerp(420, BX, (t - 5.6) / 0.6)
    if t < 9.3:
        return BX
    return lerp(BX, START, (t - 9.3) / 0.7)


def expr(t):
    for a, b, e in [(4.1, 5.6, "shock"), (5.6, 6.4, "angry"), (6.4, 9.3, "happy")]:
        if a <= t < b:
            return e
    return "normal"


def box_scale(t):
    if t < 0.3:
        return 0.0
    if t < 9.3:
        return clamp(spring((t - 0.3) / 1.0) * 1.0, 0, 1.15)
    return max(0.0, 1 - ease((t - 9.3) / 0.5))


def frame_svg(t):
    x = mochi_x(t)
    walking = 0.9 <= t < 2.4 or 5.6 <= t < 6.2 or t >= 9.3
    bob = 14 * abs(math.sin(t * 9)) if walking else 0
    sx = sy = 1.0
    rot = 0.0
    dy = 0.0
    if 2.4 <= t < 4.0:            # inclina-se para a caixa (patinha)
        u = ease((t - 2.4) / 0.5) * (1 - ease((t - 3.6) / 0.4))
        rot = 12 * u
    if 4.0 <= t < 5.6:            # cabeça na caixa: TOC e recua
        u = ease((t - 4.0) / 0.5) * (1 - ease((t - 5.0) / 0.55))
        rot = 26 * u
    if 6.2 <= t < 9.3:            # senta-se: achatado e a transbordar
        k = ease((t - 6.2) / 0.25)
        k += -0.05 * math.sin((t - 6.2) * 18) * math.exp(-(t - 6.2) * 5)
        breath = 0.015 * math.sin(t * 3.2)
        sx = 1 + 0.30 * k + breath
        sy = 1 - 0.40 * k - breath
        dy = -40 * k
        rot = 0
    if 9.3 <= t:
        k = 1 - ease((t - 9.3) / 0.35)
        sx = 1 + 0.30 * k
        sy = 1 - 0.40 * k
        dy = -40 * k
    blink = 1.1 < t < 1.22 or 8.2 < t < 8.32
    hop = 0
    # patinha na caixa (2.6-3.9)
    paw_svg = ""
    if 2.6 <= t < 4.0:
        press = abs(math.sin((t - 2.6) * 5.5)) * fade(t, 2.6, 4.0, 0.3, 0.3)
        paw_svg = f'<g transform="translate({BX - 40},{FLOOR - 240 + 40 * press:.0f}) scale(1.5)">{paw()}</g>'
    bs = box_scale(t)
    box_y = FLOOR
    squash = 1.0
    if 2.9 <= t < 3.9:
        squash = 1 - 0.07 * abs(math.sin((t - 2.9) * 5.5))
    box_shake = 0
    if 4.55 <= t < 5.4:
        box_shake = 18 * math.sin((t - 4.55) * 38) * (1 - (t - 4.55) / 0.85)
    parts = [
        f'<rect width="{W}" height="{H}" fill="#EFE8FB"/>',
        '<rect x="620" y="700" width="380" height="250" rx="18" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="5"/>'
        '<circle cx="920" cy="800" r="45" fill="#F06D5E"/>'
        '<path d="M660 900 Q760 820 880 870" fill="none" stroke="#8DA9C4" stroke-width="6" stroke-dasharray="14 12"/>',
        f'<rect x="0" y="{FLOOR - 40}" width="{W}" height="{H - FLOOR + 40}" fill="#CDBBE6"/>',
        f'<ellipse cx="{x:.0f}" cy="{FLOOR}" rx="{300 * sx:.0f}" ry="30" fill="#000" opacity="0.12"/>',
    ]
    if bs > 0.01:
        parts.append(f'<g transform="translate({BX + box_shake:.0f},{box_y}) scale({bs:.2f},{bs * squash:.2f})">{box_inside()}</g>')
    parts.append(
        f'<g transform="translate({x:.0f},{FLOOR + dy - bob:.0f}) rotate({rot:.1f}) scale({S * sx:.3f},{S * sy:.3f}) translate(-190,-378)">'
        f'{mochi(expr(t), blink, mouth_open=meow_open(t, MEOWS))}</g>')
    if bs > 0.01:
        parts.append(f'<g transform="translate({BX + box_shake:.0f},{box_y}) scale({bs:.2f},{bs * squash:.2f})">{box_front()}</g>')
    parts += [
        paw_svg,
        burst(fade(t, 0.35, 1.0, 0.05, 0.25), 600, 1450, "PUF!", 80, r=140),
        burst(fade(t, 4.55, 5.2, 0.05, 0.25), 850, 1330, "TOC!", 92, color="#2B2B2B", r=150),
        burst(fade(t, 6.0, 6.8, 0.05, 0.3), 330, 1180, "PLOF!", 96, r=160),
        card(1 - ease((t - 0.9) / 0.2) if t < 5 else ease((t - 9.4) / 0.4), "Caixa pequena", y=480, s1=84),
        card(fade(t, 0.95, 2.6), "Eu: cabe.", y=480, s1=84),
        card(fade(t, 2.65, 4.05), "Só a patinha...", y=480, s1=76),
        card(fade(t, 4.1, 5.6), "Não cabe.", y=480, s1=88),
        card(fade(t, 6.35, 7.7), "Cabe sim.", y=480, s1=88),
        card(fade(t, 7.75, 9.3, 0.2, 0.2), "Problema resolvido.", y=480, s1=72),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("caixa", frame_svg, TOTAL)
