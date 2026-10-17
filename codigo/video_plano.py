"""Vídeo 'O meu plano para ir ao Japão' (1080x1920, 10 s, 30 fps), em loop.

0-2.1 'Eu tenho 0€ e quero ir ao Japão': a carteira abre e sai uma traça
2.2-4.4 passo 1: cartaz 'Uma moeda para o Japão?' | 4.5-6.6 passo 2: chuva de moedas no frasco
6.7-8.0 passo 3: ramen no Japão | 8.0 POP, o sonho rebenta: 'Por agora: ainda vou no passo 1'
8.2-9.1 a traça volta para a carteira | 9.2-10 volta ao início
Sem preço do voo: o único número é o valor real da vaquinha (ANGARIADO).
"""
import math

from mochi_cena import W, H, FONT, burst, card, clamp, ease, fade, main, meow_open, spring, svg_doc
from mochi_kit import mochi
from musica_plano import COIN_T, MEOWS, TOTAL

ANGARIADO = 0
S = 2.3
FLOOR = 1760
WAL_X, WAL_Y = 210, FLOOR - 10
JAR_X = 905


def wallet_open(t):
    if 0.15 <= t < 1.3:
        return clamp(spring((t - 0.15) * 1.5)) * (1 - ease((t - 1.0) / 0.3))
    if 8.75 <= t < 9.1:
        return math.sin(math.pi * (t - 8.75) / 0.35)
    return 0.0


def wallet_svg(t):
    o = wallet_open(t)
    return (f'<g transform="translate({WAL_X},{WAL_Y})">'
            '<rect x="-120" y="-130" width="240" height="130" rx="22" fill="#7A4A2A" stroke="#2B2B2B" stroke-width="6"/>'
            f'<g transform="rotate({-110 * o:.1f},-120,-130)">'
            '<rect x="-120" y="-150" width="240" height="70" rx="22" fill="#9C6338" stroke="#2B2B2B" stroke-width="6"/>'
            '<circle cx="90" cy="-112" r="12" fill="#F6C343" stroke="#2B2B2B" stroke-width="4"/></g></g>')


def moth(x, y, t):
    flap = abs(math.sin(t * 40))
    return (f'<g transform="translate({x:.0f},{y:.0f}) scale(1.8)">'
            f'<ellipse cx="-30" cy="0" rx="{34 * (0.4 + 0.6 * flap):.0f}" ry="26" fill="#CFC3B0" stroke="#2B2B2B" stroke-width="4"/>'
            f'<ellipse cx="30" cy="0" rx="{34 * (0.4 + 0.6 * flap):.0f}" ry="26" fill="#CFC3B0" stroke="#2B2B2B" stroke-width="4"/>'
            '<ellipse cx="0" cy="0" rx="10" ry="26" fill="#6B5B4B"/>'
            '<path d="M-4 -24 Q-14 -44 -22 -46 M4 -24 Q14 -44 22 -46" fill="none" stroke="#2B2B2B" stroke-width="3"/></g>')


def moth_svg(t):
    if 0.2 <= t < 2.2:       # sai da carteira e esvoaça até sair do ecrã
        u = (t - 0.2) / 2.0
        x = WAL_X + 950 * u ** 1.6 + 60 * math.sin(u * 14)
        y = WAL_Y - 140 - 650 * math.sin(math.pi * min(u * 1.4, 1)) * (1 - 0.3 * u) + 40 * math.sin(u * 22)
        return moth(x, y, t)
    if 8.2 <= t < 9.0:       # volta para casa
        u = ease((t - 8.2) / 0.8)
        x = 1180 - (1180 - WAL_X) * u
        y = 700 + (WAL_Y - 140 - 700) * u + 50 * math.sin(u * 12)
        return moth(x, y, t)
    return ""


def sign_svg(t, my):
    op = fade(t, 2.15, 4.45, 0.15, 0.2)
    if op <= 0:
        return ""
    sc = 0.6 + 0.4 * clamp(spring((t - 2.15) * 1.4))
    y = my + 290 * S
    wob = 3 * math.sin(t * 6)
    return (f'<g opacity="{op:.2f}" transform="translate(540,{y:.0f}) rotate({wob:.1f}) scale({sc:.2f})">'
            '<rect x="-350" y="-150" width="700" height="300" rx="20" fill="#D9A86C" stroke="#2B2B2B" stroke-width="7"/>'
            f'<text x="0" y="-20" font-family="{FONT}" font-weight="bold" font-size="70" fill="#2B2B2B" text-anchor="middle">Uma moeda</text>'
            f'<text x="0" y="80" font-family="{FONT}" font-weight="bold" font-size="60" fill="#D8343A" text-anchor="middle">para o Japão?</text>'
            '<ellipse cx="-350" cy="40" rx="44" ry="34" fill="#FFF6EA" stroke="#E0C9A8" stroke-width="3"/>'
            '<ellipse cx="350" cy="40" rx="44" ry="34" fill="#FFF6EA" stroke="#E0C9A8" stroke-width="3"/></g>')


def coin(x, y, rot=0):
    return (f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot:.0f})">'
            '<circle r="42" fill="#F6C343" stroke="#2B2B2B" stroke-width="5"/><circle r="30" fill="none" stroke="#D9A21E" stroke-width="4"/>'
            f'<text y="17" font-family="{FONT}" font-weight="bold" font-size="48" fill="#B07A10" text-anchor="middle">€</text></g>')


def jar_svg(t):
    op = fade(t, 4.45, 8.0, 0.2, 0.06)
    if op <= 0:
        return ""
    top, bot = FLOOR - 330, FLOOR - 10
    inside = ""
    landed = sum(1 for c in COIN_T if t >= c + 0.35)
    for k in range(landed):
        inside += coin(JAR_X - 40 + 80 * (k % 2), bot - 45 - 44 * (k // 2), 15 * (k % 3))
    falling = ""
    for i, c in enumerate(COIN_T):
        if c <= t < c + 0.35:
            u = (t - c) / 0.35
            ytgt = bot - 45 - 44 * (i // 2)
            falling += coin(JAR_X - 40 + 80 * (i % 2), -60 + (ytgt + 60) * u * u, 400 * u)
    return (f'<g opacity="{op:.2f}">{falling}'
            f'<rect x="{JAR_X - 120}" y="{top}" width="240" height="{bot - top}" rx="30" fill="#DDF1F7" opacity="0.55" stroke="#2B2B2B" stroke-width="6"/>'
            f'{inside}<rect x="{JAR_X - 130}" y="{top - 30}" width="260" height="40" rx="12" fill="#3F6FB0" stroke="#2B2B2B" stroke-width="5"/>'
            f'<rect x="{JAR_X - 120}" y="{top}" width="240" height="{bot - top}" rx="30" fill="none" stroke="#2B2B2B" stroke-width="6"/></g>')


def ramen_svg(t):
    op = fade(t, 6.65, 8.0, 0.15, 0.06)
    if op <= 0:
        return ""
    sc = 0.5 + 0.5 * clamp(spring((t - 6.65) * 1.4))
    steam = "".join(f'<path d="M{x} -150 Q{x + 20} -190 {x} -230 Q{x - 20} -270 {x} -300" fill="none" stroke="#FFFFFF" '
                    f'stroke-width="10" stroke-linecap="round" opacity="{0.5 + 0.4 * math.sin(t * 6 + x):.2f}"/>' for x in (-80, 0, 80))
    return (f'<g opacity="{op:.2f}" transform="translate(540,{FLOOR - 90}) scale({sc:.2f})">{steam}'
            '<line x1="60" y1="-210" x2="210" y2="-40" stroke="#B5713A" stroke-width="14" stroke-linecap="round"/>'
            '<line x1="100" y1="-220" x2="230" y2="-60" stroke="#B5713A" stroke-width="14" stroke-linecap="round"/>'
            '<ellipse cx="0" cy="-100" rx="230" ry="50" fill="#F2D27A" stroke="#2B2B2B" stroke-width="6"/>'
            '<path d="M-150 -105 Q-100 -130 -50 -105 Q0 -80 50 -105 Q100 -130 150 -105" fill="none" stroke="#E8B84A" stroke-width="10"/>'
            '<circle cx="-90" cy="-112" r="34" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="4"/><circle cx="-90" cy="-112" r="16" fill="#F6C343"/>'
            '<rect x="40" y="-135" width="80" height="40" rx="10" fill="#E77C8A" stroke="#2B2B2B" stroke-width="4"/>'
            '<path d="M-230 -100 Q-220 70 0 80 Q220 70 230 -100 Z" fill="#D8343A" stroke="#2B2B2B" stroke-width="6" stroke-linejoin="round"/>'
            '<path d="M-150 -20 L-110 -20 L-110 20 L-70 20 M70 -20 L110 -20 L110 20 L150 20" fill="none" stroke="#FFFFFF" stroke-width="8"/></g>')


def mochi_expr(t):
    for a, b, e in [(0.2, 2.1, "shock"), (2.15, 4.45, "normal"), (4.75, 6.65, "happy"), (6.65, 8.0, "eat"),
                    (8.0, 8.3, "shock"), (8.3, 9.2, "ko")]:
        if a <= t < b:
            return e
    return "normal"


def frame_svg(t):
    hop = 0.0
    for t0 in (0.2, 4.75, 8.0):
        if t0 <= t < t0 + 0.35:
            hop = 55 * math.sin(math.pi * (t - t0) / 0.35)
    mx = 540 - 190 * S
    my = FLOOR - 378 * S - hop
    blink = 1.7 < t < 1.82 or 3.3 < t < 3.42
    title_op = 1 - ease((t - 2.0) / 0.25) if t < 5 else ease((t - 9.25) / 0.45)
    parts = [
        f'<rect width="{W}" height="{H}" fill="#FDE7D3"/>',
        f'<rect x="0" y="{FLOOR - 40}" width="{W}" height="{H - FLOOR + 40}" fill="#E9C9A8"/>',
        f'<ellipse cx="540" cy="{FLOOR}" rx="280" ry="32" fill="#000" opacity="0.12"/>',
        f'<g transform="translate({mx:.1f},{my:.1f}) scale({S})">{mochi(mochi_expr(t), blink, mouth_open=meow_open(t, MEOWS))}</g>',
        wallet_svg(t),
        sign_svg(t, my),
        jar_svg(t),
        ramen_svg(t),
        moth_svg(t),
        burst(fade(t, 8.0, 8.7, 0.06, 0.3), 540, 860, "POP!", 100, r=170),
        card(title_op, f"Eu tenho {ANGARIADO}€", "e quero ir ao Japão", y=400, s1=84, s2=60, c1="#2B2B2B"),
        card(fade(t, 2.2, 4.4), "Passo 1:", "pedir uma moeda à internet", y=400, s1=72, s2=50),
        card(fade(t, 4.5, 6.6), "Passo 2:", "muita gente faz o mesmo", y=400, s1=72, s2=54),
        card(fade(t, 6.7, 7.98, 0.2, 0.06), "Passo 3:", "ramen no Japão!", y=400, s1=72, s2=64),
        card(fade(t, 8.05, 9.2, 0.1, 0.25), "Por agora:", "ainda vou no passo 1", y=400, s1=72, s2=58),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("plano", frame_svg, TOTAL)
