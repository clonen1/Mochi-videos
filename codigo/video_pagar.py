"""Vídeo 'Eu a tentar pagar o voo para o Japão' (1080x1920, 10 s, 30 fps), em loop.

0.15-2.3 o Mochi põe no balcão: meia, bola de lã, espinha, botão (cada um +0€)
2.6-4.6 'Isto tudo vale 0€' / faltam 1400€ | 4.7-6.6 'Aceitam ronrons?'
6.6 RECUSADO | 7.95-9 atira tudo ao chão, como um bom gato | 9.35-10 início
"""
import math

from mochi_cena import W, H, FONT, card, clamp, ease, fade, main, meow_open, spring, svg_doc
from mochi_kit import mochi
from musica_pagar import ITEM_T, MEOWS, TOTAL

PRICE = 1400
S = 2.0
COUNTER = 1520
ITEM_X = [210, 390, 700, 880]


def sock():
    return ('<path d="M-25 -95 L25 -95 L25 -10 Q60 0 70 25 Q70 45 40 45 L-25 45 Q-35 45 -35 30 Z" '
            'fill="#FFFFFF" stroke="#2B2B2B" stroke-width="5" stroke-linejoin="round"/>'
            '<rect x="-25" y="-80" width="50" height="14" fill="#3F6FB0"/><rect x="-25" y="-55" width="50" height="14" fill="#3F6FB0"/>')


def yarn():
    return ('<circle cx="0" cy="0" r="48" fill="#9B6BCB" stroke="#2B2B2B" stroke-width="5"/>'
            '<path d="M-40 -20 Q0 10 40 -25 M-46 5 Q0 35 44 0 M-30 32 Q5 45 30 35" fill="none" stroke="#C9A6EA" stroke-width="5"/>'
            '<path d="M40 25 Q70 40 60 50" fill="none" stroke="#9B6BCB" stroke-width="5"/>')


def fishbone():
    ribs = "".join(f'<line x1="{x}" y1="-22" x2="{x}" y2="22" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/>'
                   for x in (-30, -10, 10))
    return ('<line x1="-55" y1="0" x2="35" y2="0" stroke="#2B2B2B" stroke-width="6" stroke-linecap="round"/>' + ribs +
            '<polygon points="35,-22 75,0 35,22" fill="#DDDDDD" stroke="#2B2B2B" stroke-width="5" stroke-linejoin="round"/>'
            '<polygon points="-55,0 -75,-20 -75,20" fill="#DDDDDD" stroke="#2B2B2B" stroke-width="5" stroke-linejoin="round"/>')


def button():
    holes = "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="#2B2B2B"/>' for x in (-12, 12) for y in (-12, 12))
    return '<circle cx="0" cy="0" r="40" fill="#F6C343" stroke="#2B2B2B" stroke-width="5"/>' + holes


TY = 560
ITEMS = [sock, yarn, fishbone, button]
REST_Y = [COUNTER - 45, COUNTER - 50, COUNTER - 24, COUNTER - 42]


def paw_x(t):
    return 960 - 820 * clamp((t - 7.85) / 1.05)


def item_launch(i):
    return 7.85 + (960 - ITEM_X[i]) / 820 * 1.05


def items_svg(t):
    out = ""
    for i, draw in enumerate(ITEMS):
        t0 = ITEM_T[i]
        if t < t0 - 0.15:
            continue
        x, y, rot, op = ITEM_X[i], REST_Y[i], 0.0, 1.0
        if t < t0:                               # a cair
            u = (t - (t0 - 0.15)) / 0.15
            y -= 360 * (1 - u * u)
            op = clamp(u * 4)
        elif t < t0 + 0.3:                       # ressalto
            y -= 30 * math.sin(math.pi * (t - t0) / 0.3)
        tl = item_launch(i)
        if t >= tl:                              # atirado ao chão pela pata
            u = (t - tl) / 0.9
            if u > 1:
                continue
            x -= 700 * u
            y += -220 * u + 1500 * u * u
            rot = -540 * u
        out += f'<g opacity="{op:.2f}" transform="translate({x:.0f},{y:.0f}) rotate({rot:.0f})">{draw()}</g>'
        if t0 + 0.05 <= t < t0 + 0.9:            # +0€
            u = (t - t0 - 0.05) / 0.85
            op = math.sin(math.pi * u)
            out += (f'<text x="{ITEM_X[i]}" y="{REST_Y[i] - 90 - 90 * u:.0f}" font-family="{FONT}" font-weight="bold" '
                    f'font-size="72" fill="#D8343A" text-anchor="middle" opacity="{op:.2f}" stroke="#FFFFFF" stroke-width="3">+0€</text>')
    return out


def paw_svg(t, my):
    if not 7.8 <= t < 9.05:
        return ""
    px = paw_x(t)
    sx, sy = 540 + 60 * S, my + 270 * S
    py = COUNTER - 30
    return (f'<line x1="{sx:.0f}" y1="{sy:.0f}" x2="{px:.0f}" y2="{py}" stroke="#F2A14A" stroke-width="60" stroke-linecap="round"/>'
            f'<ellipse cx="{px:.0f}" cy="{py}" rx="40" ry="32" fill="#FFF6EA"/>')


def ticket_svg(t):
    stamp_op = fade(t, 6.6, 9.3, 0.08, 0.3)
    st = 1 + 0.6 * (1 - spring(t - 6.6)) if t >= 6.6 else 1.6
    stamp = ""
    if stamp_op > 0:
        stamp = (f'<g opacity="{stamp_op:.2f}" transform="translate(540,{TY + 230}) rotate(-10) scale({st:.2f})">'
                 '<rect x="-215" y="-55" width="430" height="110" rx="16" fill="#FFFFFF" opacity="0.92"/>'
                 '<rect x="-215" y="-55" width="430" height="110" rx="16" fill="none" stroke="#D8343A" stroke-width="10"/>'
                 f'<text x="0" y="24" font-family="{FONT}" font-weight="bold" font-size="66" fill="#D8343A" text-anchor="middle">RECUSADO</text></g>')
    return (f'<rect x="230" y="{TY}" width="620" height="390" rx="40" fill="#2B2B2B"/>'
            f'<rect x="250" y="{TY + 20}" width="580" height="350" rx="28" fill="#FFFFFF"/>'
            f'<rect x="250" y="{TY + 20}" width="580" height="88" rx="28" fill="#3F6FB0"/><rect x="250" y="{TY + 78}" width="580" height="30" fill="#3F6FB0"/>'
            f'<text x="540" y="{TY + 80}" font-family="{FONT}" font-weight="bold" font-size="42" fill="#FFFFFF" text-anchor="middle">Lisboa → Tóquio</text>'
            f'<text x="540" y="{TY + 230}" font-family="{FONT}" font-weight="bold" font-size="120" fill="#2B2B2B" text-anchor="middle">{PRICE}€</text>'
            f'<text x="540" y="{TY + 330}" font-family="{FONT}" font-weight="bold" font-size="52" fill="#D8343A" text-anchor="middle">Pago: 0€</text>'
            + stamp)


def mochi_expr(t):
    for a, b, e in [(2.7, 4.2, "shock"), (4.7, 6.6, "happy"), (6.6, 9.3, "angry")]:
        if a <= t < b:
            return e
    return "normal"


def frame_svg(t):
    hop = 0.0
    for t0 in ITEM_T:
        w = min(0.3, t0)
        if t0 - w <= t < t0:
            hop = 25 * math.sin(math.pi * (t - t0 + w) / w)
    if 2.7 <= t < 3.0:
        hop = 60 * math.sin(math.pi * (t - 2.7) / 0.3)
    my = COUNTER - 300 * S - hop
    mx = 540 - 190 * S
    blink = 1.2 < t < 1.32 or 5.6 < t < 5.72
    shake = math.sin(t * 90) * 14 * (1 - (t - 6.6) / 0.35) if 6.6 <= t < 6.95 else 0
    title_op = 1 - ease((t - 2.35) / 0.3) if t < 5 else ease((t - 9.35) / 0.4)
    parts = [
        f'<rect width="{W}" height="{H}" fill="#FDE7D3"/>',
        f'<g transform="translate({shake:.1f},0)">',
        ticket_svg(t),
        f'<g transform="translate({mx:.1f},{my:.1f}) scale({S})">{mochi(mochi_expr(t), blink, mouth_open=meow_open(t, MEOWS))}</g>',
        f'<rect x="-20" y="{COUNTER}" width="1120" height="{H - COUNTER + 20}" fill="#B5713A"/>',
        f'<rect x="-20" y="{COUNTER - 6}" width="1120" height="40" fill="#C98B52"/>',
        f'<line x1="-20" y1="{COUNTER + 150}" x2="1100" y2="{COUNTER + 150}" stroke="#9C5F2E" stroke-width="8"/>',
        f'<line x1="-20" y1="{COUNTER + 330}" x2="1100" y2="{COUNTER + 330}" stroke="#9C5F2E" stroke-width="8"/>',
        items_svg(t),
        paw_svg(t, my),
        card(title_op, "Eu a tentar pagar", "o voo para o Japão", s1=68, s2=60, c1="#2B2B2B"),
        card(fade(t, 2.6, 4.6), "Isto tudo vale 0€", f"Faltam {PRICE}€", s1=68, s2=60),
        card(fade(t, 4.7, 6.55), "Aceitam ronrons?", s1=72, c1="#3F6FB0"),
        card(fade(t, 7.7, 9.3), "Então vai tudo", "ao chão.", s1=70, s2=70),
        '</g>',
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("pagar", frame_svg, TOTAL)
