"""Vídeo 'Halloween: o maior susto é a minha conta' (meme da viagem, 1.ª pessoa; 1080x1920, 10 s, 30 fps), em loop.

0-2     'Coisas que me assustam: 1. O aspirador' (VRUUM! logo aos 0.15 s)
2-4     '2. Pepinos' (o pepino de quarta volta)
4-4.6   '3. A minha conta para o Japão' | 4.6 luzes apagam, só o '0€' a brilhar, relâmpago e grito
7-9     luzes voltam: 'Doces? Não, obrigado. Aceito moedas.'
9-10    volta ao início
O único número é o valor real angariado (ANGARIADO). Nunca a meta nem o preço.
"""
import math

from mochi_cena import W, H, FONT, burst, card, clamp, ease, fade, main, meow_open, spring, svg_doc
from mochi_kit import mochi
from mochi_props import bat, cucumber, pumpkin, witch_hat
from musica_halloween import MEOWS, TOTAL

ANGARIADO = 0
S = 1.9
FLOOR = 1720
MX, MY = 540 - 190 * S, FLOOR - 378 * S
BATS = [(0.0, 700, 0.0), (0.45, 980, 1.7), (0.75, 600, 3.1)]   # (fase, altura, fase da asa)


def dark(t):
    """Opacidade do escuro (0 = luz, 1 = escuro), com relâmpago aos 5.0 s."""
    d = fade(t, 4.6, 7.05, 0.06, 0.2)
    if 5.0 <= t < 5.18:
        d *= 0.15
    return d


def mochi_expr(t):
    for a, b, e in [(0.15, 1.4, "shock"), (2.3, 3.6, "shock"), (4.6, 7.0, "shock"), (7.0, 7.5, "ko"),
                    (7.5, 9.0, "happy")]:
        if a <= t < b:
            return e
    return "normal"


def bats_svg(t):
    out = ""
    for ph, y, wph in BATS:
        k = (t / TOTAL * 2 + ph) % 1.0          # 2 voltas em 10 s: o loop fica perfeito
        x = -120 + 1320 * k
        yy = y + 40 * math.sin(2 * math.pi * (k * 3))
        out += f'<g transform="translate({x:.0f},{yy:.0f}) scale(1.1)">{bat(t * 6 * math.pi / 14, wph)}</g>'
    return out


def cuke_x(t):
    if 2.0 <= t < 4.0:
        return -200 + 420 * ease((t - 2.0) / 0.3) - 420 * ease((t - 3.7) / 0.3)
    return -200


def frame_svg(t):
    hop = 0.0
    for t0 in (0.15, 2.3, 5.0, 7.5):
        if t0 <= t < t0 + 0.35:
            hop = 50 * math.sin(math.pi * (t - t0) / 0.35)
    my = MY - hop
    shake = 10 * math.sin(t * 70) if 4.6 <= t < 5.6 else 0
    tilt = 10 if 7.0 <= t < 7.5 else 0
    blink = 1.7 < t < 1.82 or 8.4 < t < 8.52
    d = dark(t)
    list_op = 1 - ease((t - 4.55) / 0.08) if t < 6 else ease((t - 9.2) / 0.45)
    item = "1. O aspirador" if (t < 2.0 or t >= 9.0) else ("2. Pepinos" if t < 4.0 else "3. A minha conta")
    item2 = "" if item != "3. A minha conta" else "para o Japão"
    glow = 0.75 + 0.25 * math.sin(t * 10)
    parts = [
        f'<rect width="{W}" height="{H}" fill="#3B2A5A"/>',
        '<circle cx="930" cy="770" r="95" fill="#FCEFC7"/><circle cx="900" cy="745" r="18" fill="#EADFB4"/>',
        bats_svg(t),
        f'<rect x="0" y="{FLOOR - 40}" width="{W}" height="{H - FLOOR + 40}" fill="#2A1F3D"/>',
        f'<ellipse cx="540" cy="{FLOOR}" rx="290" ry="32" fill="#000" opacity="0.25"/>',
        f'<g transform="translate(900,{FLOOR - 70}) scale(0.8)">{pumpkin(glow)}</g>',
        f'<g transform="translate({cuke_x(t):.0f},{FLOOR - 50}) scale(0.9)">{cucumber()}</g>',
        f'<g transform="translate({MX + shake:.1f},{my:.1f}) scale({S}) rotate({tilt},190,375)">'
        f'{mochi(mochi_expr(t), blink, mouth_open=meow_open(t, MEOWS))}{witch_hat()}</g>',
        burst(fade(t, 0.15, 1.5, 0.06, 0.3), 290, 1060, "VRUUM!", 68, r=180),
        burst(fade(t, 2.3, 3.5, 0.06, 0.3), 290, 1060, "AAAH!", 76, r=180),
        card(list_op, "Coisas que me assustam:", y=180, s1=56, c1="#6B47A3"),
        card(list_op, item, item2, y=410, s1=72, s2=62),
    ]
    if d > 0:
        parts.append(f'<rect width="{W}" height="{H}" fill="#07040D" opacity="{0.94 * d:.3f}"/>')
        # só os olhos do Mochi e o 0€ se veem no escuro
        ex, ey = MX + shake, my
        parts.append(f'<g opacity="{d:.2f}">'
                     f'<circle cx="{ex + 148 * S:.0f}" cy="{ey + 160 * S:.0f}" r="34" fill="#FFF7C2"/>'
                     f'<circle cx="{ex + 232 * S:.0f}" cy="{ey + 160 * S:.0f}" r="34" fill="#FFF7C2"/>'
                     f'<circle cx="{ex + 148 * S:.0f}" cy="{ey + 162 * S:.0f}" r="10" fill="#07040D"/>'
                     f'<circle cx="{ex + 232 * S:.0f}" cy="{ey + 162 * S:.0f}" r="10" fill="#07040D"/>'
                     f'<text x="540" y="860" font-family="{FONT}" font-weight="bold" font-size="300" fill="#7CFF6B" '
                     f'text-anchor="middle" opacity="{glow:.2f}">{ANGARIADO}€</text>'
                     f'<text x="540" y="1010" font-family="{FONT}" font-weight="bold" font-size="66" fill="#F28C28" '
                     f'text-anchor="middle" opacity="{ease((t - 5.4) / 0.3):.2f}">O MAIOR SUSTO</text></g>')
    parts.append(card(fade(t, 7.1, 9.0), "Doces? Não, obrigado.", "Aceito moedas.", y=300, s1=64, s2=64))
    return svg_doc(parts)


if __name__ == "__main__":
    main("halloween", frame_svg, TOTAL)
