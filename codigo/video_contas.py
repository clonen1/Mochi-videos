"""Vídeo 'Quantos ramens custa ir ao Japão?' (meme da viagem, 1.ª pessoa; 1080x1920, 10 s, 30 fps), em loop.

0-2     o Mochi faz contas na calculadora: o visor enche-se de ramens
2-4     'Eu a fazer contas...' os ramens transbordam e saltam do visor
4.0     PFFF: ERRO e fumo | 'A calculadora desistiu.'
5.6     'Resposta: MUITOS ramens.' | 7.4 'Plano: comer menos ramen. ...a partir de amanhã.'
9.2-10  o fumo desaparece e as contas recomeçam (loop)
Sem nenhum preço nem número do bilhete.
"""
import math

from mochi_cena import FONT, W, H, burst, card, clamp, ease, fade, main, meow_open, spring, svg_doc
from mochi_kit import mochi
from mochi_props import calculator, mini_ramen, paw, smoke
from musica_contas import MEOWS, TOTAL

S = 2.0
FLOOR = 1720
MX, MY = 360 - 190 * S, FLOOR - 378 * S
CALC = (790, 1380)
KEYS = [(-130, 90), (-45, 175), (40, 90), (-45, 5)]   # teclas que o Mochi carrega (coord. da calculadora)


def n_icons(t):
    if t < 0.2 or t >= 9.4:
        return 0
    if t < 2.0:
        return min(10, 1 + int((t - 0.2) / 0.2))
    return 10


def screen(t):
    if 4.0 <= t < 9.4:
        op = 1 if int(t * 4) % 2 == 0 or t > 5.6 else 0.4
        return (f'<text x="0" y="-140" font-family="{FONT}" font-weight="bold" font-size="92" fill="#D8343A" '
                f'text-anchor="middle" opacity="{op}">ERRO</text>')
    n = n_icons(t)
    if n == 0:
        cur = "_"
        return (f'<text x="140" y="-130" font-family="{FONT}" font-weight="bold" font-size="80" fill="#2B2B2B" '
                f'text-anchor="end">{cur}</text>')
    out = ""
    for i in range(n):
        r, c = divmod(i, 5)
        out += f'<g transform="translate({-130 + c * 65},{-200 + r * 62}) scale(0.9)">{mini_ramen()}</g>'
    return out


def spill(t):
    """Ramens a saltar do visor entre 2.0 e 5.5 s."""
    out = ""
    for i in range(12):
        t0 = 2.05 + i * 0.15
        if not t0 <= t < t0 + 1.6:
            continue
        k = t - t0
        side = -1 if i % 2 == 0 else 1
        x = CALC[0] + side * (60 + 260 * k) + (i % 3 - 1) * 40
        y = CALC[1] - 160 - 900 * k + 1100 * k * k
        out += f'<g transform="translate({x:.0f},{y:.0f}) rotate({side * 400 * k:.0f}) scale(1.6)">{mini_ramen()}</g>'
    return out


def paw_pos(t):
    if 4.0 <= t < 9.4:
        return CALC[0] - 150, CALC[1] + 330          # patinha em baixo, desistiu
    rate = 10 if 2.0 <= t < 4.0 else 6
    k = KEYS[int(t * rate) % 4]
    press = abs(math.sin(math.pi * t * rate))
    return CALC[0] + k[0] + 35, CALC[1] + k[1] + 10 - 30 * press


def expr(t):
    for a, b, e in [(2.0, 4.0, "angry"), (4.0, 5.6, "shock"), (5.6, 7.4, "ko"), (7.4, 9.3, "happy")]:
        if a <= t < b:
            return e
    return "normal"


def frame_svg(t):
    shake = 0.0
    if 2.0 <= t < 4.0:
        shake = (1 + 3 * (t - 2.0)) * math.sin(t * 60)
    hop = 40 * math.sin(math.pi * (t - 7.4) / 0.35) if 7.4 <= t < 7.75 else 0
    tilt = -8 if 5.6 <= t < 7.4 else 0
    blink = 1.1 < t < 1.22 or 8.6 < t < 8.72
    title_op = 1 - ease((t - 2.0) / 0.2) if t < 5 else ease((t - 9.4) / 0.45)
    smk = ""
    sop = fade(t, 4.0, 9.4, 0.1, 0.4)
    for i in range(3):
        ph = ((t - 4.0) * 0.6 + i / 3) % 1
        smk += smoke(sop * (1 - ph), CALC[0] - 80 + i * 80, CALC[1] - 330 - 380 * ph, 50 + 60 * ph)
    px, py = paw_pos(t)
    parts = [
        f'<rect width="{W}" height="{H}" fill="#EFE8FB"/>',
        # quadro com o avião e o Japão (sonho)
        '<rect x="640" y="800" width="380" height="250" rx="18" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="5"/>'
        '<circle cx="940" cy="900" r="45" fill="#F06D5E"/>'
        '<path d="M680 960 Q780 880 900 930" fill="none" stroke="#8DA9C4" stroke-width="6" stroke-dasharray="14 12"/>'
        '<path d="M700 980 l40 -10 l10 -25 l12 22 l40 -8 l-36 22 l8 24 l-14 -18 z" fill="#3F6FB0"/>',
        f'<rect x="0" y="{FLOOR - 40}" width="{W}" height="{H - FLOOR + 40}" fill="#CDBBE6"/>',
        f'<ellipse cx="420" cy="{FLOOR}" rx="300" ry="32" fill="#000" opacity="0.12"/>',
        f'<g transform="translate({MX:.1f},{MY - hop:.1f}) scale({S}) rotate({tilt},190,378)">'
        f'{mochi(expr(t), blink, mouth_open=meow_open(t, MEOWS))}</g>',
        f'<g transform="translate({CALC[0]},{CALC[1]})">{calculator(screen(t), shake)}</g>',
        "" if 4.0 <= t < 9.4 else f'<g transform="translate({px:.0f},{py:.0f})">{paw()}</g>',
        spill(t),
        smk,
        burst(fade(t, 0.2, 0.9, 0.05, 0.25), 230, 1060, "BIP BIP!", 64, r=150),
        burst(fade(t, 4.0, 4.9, 0.05, 0.3), 260, 1060, "PFFF!", 88, color="#2B2B2B", r=150),
        card(title_op, "Quantos ramens custa", "ir ao Japão?", y=480, s1=70, s2=80),
        card(fade(t, 2.05, 4.0), "Eu a fazer contas...", y=480, s1=76),
        card(fade(t, 4.05, 5.6), "A calculadora", "desistiu.", y=480, s1=72, s2=80),
        card(fade(t, 5.65, 7.4), "Resposta:", "MUITOS ramens.", y=480, s1=70, s2=84),
        card(fade(t, 7.45, 9.35, 0.2, 0.2), "Plano: comer menos ramen.", "...a partir de amanhã.", y=480, s1=60, s2=60),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("contas", frame_svg, TOTAL)
