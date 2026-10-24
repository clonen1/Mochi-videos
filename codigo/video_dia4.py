"""Vídeo 'Dia 4: o Mochi conta a vaquinha' (1080x1920, 10 s, 30 fps), em loop.

0-0.45  o mealheiro cai do céu e o Mochi apanha-o (PUM!)
2.2-4.4 abana o mealheiro de pernas para o ar... só sai uma traça
4.5-6.9 painel 'Total contado: 0€' com a barra vazia, susto
7.0-9.0 'Dia 5 há de ser melhor. Link na bio'
9.0-10  atira o mealheiro ao ar (sai por cima) e volta ao início
O único número é o valor real angariado (ANGARIADO). Nunca a meta.
"""
import math

from mochi_cena import W, H, FONT, burst, card, clamp, ease, fade, main, meow_open, spring, svg_doc
from mochi_kit import mochi
from mochi_props import moth, piggy
from musica_dia4 import MEOWS, TOTAL

ANGARIADO = 0
S = 2.0
FLOOR = 1720
MX, MY = 540 - 190 * S, FLOOR - 378 * S
HOLD = (540, 1500)      # mealheiro nos braços
UP = (540, 1020)        # mealheiro por cima da cabeça


def pig_pose(t):
    """(x, y, rotação) do mealheiro."""
    if t < 0.45:                               # cai do céu
        k = (t / 0.45) ** 2
        return HOLD[0], -250 + (HOLD[1] + 250) * k, 0
    if t < 2.2:
        sq = 30 * math.exp(-(t - 0.45) * 8) * math.cos((t - 0.45) * 25)
        return HOLD[0], HOLD[1] + sq, 0
    if t < 4.45:                               # sobe e abana de pernas para o ar
        k = ease((t - 2.2) / 0.3)
        y = HOLD[1] + (UP[1] - HOLD[1]) * k
        rot = 180 * k + (14 * math.sin(t * 50) if 2.5 < t < 3.35 else 0)
        dy = 25 * math.sin(t * 50) if 2.5 < t < 3.35 else 0
        return UP[0], y + dy, rot
    if t < 9.0:                                # volta aos braços
        k = ease((t - 4.45) / 0.3)
        return HOLD[0], UP[1] + (HOLD[1] - UP[1]) * k, 180 * (1 - k)
    k = ease((t - 9.0) / 0.6)                  # atira ao ar
    return HOLD[0], HOLD[1] + (-250 - HOLD[1]) * k, 0


def mochi_expr(t):
    for a, b, e in [(0.45, 2.0, "happy"), (2.2, 3.35, "angry"), (3.35, 4.5, "shock"),
                    (4.75, 5.5, "shock"), (5.5, 6.95, "ko"), (7.0, 9.0, "happy")]:
        if a <= t < b:
            return e
    return "normal"


def moth_svg(t):
    if not 3.35 <= t < 5.2:
        return ""
    k = t - 3.35
    x = 540 + 160 * math.sin(k * 4) + 60 * k
    y = 900 - 330 * k
    return f'<g transform="translate({x:.0f},{y:.0f}) scale(1.3)">{moth(t)}</g>'


def total_panel(t):
    op = fade(t, 4.5, 6.95, 0.15, 0.3)
    if op <= 0:
        return ""
    sc = 0.7 + 0.3 * clamp(spring((t - 4.5) * 1.4))
    # a barra tenta encher e volta ao zero
    wob = max(0.0, math.sin((t - 4.6) * 9)) * 14 * math.exp(-(t - 4.6) * 1.5) if t > 4.6 else 0
    glow = 0.6 + 0.4 * math.sin(t * 8)
    return (f'<g opacity="{op:.2f}" transform="translate(540,620) scale({sc:.2f})">'
            '<rect x="-450" y="-250" width="900" height="500" rx="44" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="6"/>'
            f'<text x="0" y="-150" font-family="{FONT}" font-weight="bold" font-size="60" fill="#2B2B2B" text-anchor="middle">Total contado:</text>'
            f'<text x="0" y="40" font-family="{FONT}" font-weight="bold" font-size="190" fill="#D8343A" text-anchor="middle" opacity="{glow:.2f}">{ANGARIADO}€</text>'
            '<rect x="-380" y="110" width="760" height="70" rx="35" fill="#EEE3D6" stroke="#2B2B2B" stroke-width="5"/>'
            f'<rect x="-376" y="114" width="{30 + wob:.0f}" height="62" rx="31" fill="#4FBF7A"/>'
            '</g>')


def frame_svg(t):
    px, py, prot = pig_pose(t)
    hop = 0.0
    for t0 in (0.45, 4.75, 7.0):
        if t0 <= t < t0 + 0.35:
            hop = 45 * math.sin(math.pi * (t - t0) / 0.35)
    my = MY - hop
    tilt = 8 if 5.5 <= t < 6.95 else 0
    blink = 1.6 < t < 1.72 or 8.3 < t < 8.42
    title_op = 1 - ease((t - 2.0) / 0.25) if t < 5 else ease((t - 9.3) / 0.45)
    coins = ""
    if 0.45 <= t < 1.2:  # brilhos quando apanha
        k = (t - 0.45) / 0.75
        for i in range(6):
            a = math.pi * 2 * i / 6
            coins += (f'<circle cx="{540 + math.cos(a) * 260 * k:.0f}" cy="{1480 + math.sin(a) * 200 * k:.0f}" '
                      f'r="{14 * (1 - k):.1f}" fill="#F6C343"/>')
    parts = [
        f'<rect width="{W}" height="{H}" fill="#FDE7D3"/>',
        '<rect x="760" y="760" width="230" height="300" rx="16" fill="#F7D9BC"/>'
        '<rect x="780" y="780" width="190" height="260" rx="10" fill="#BFE3F5"/>',
        f'<rect x="0" y="{FLOOR - 40}" width="{W}" height="{H - FLOOR + 40}" fill="#E9C9A8"/>',
        f'<ellipse cx="540" cy="{FLOOR}" rx="300" ry="34" fill="#000" opacity="0.12"/>',
        f'<g transform="translate({MX:.1f},{my:.1f}) scale({S}) rotate({tilt},190,375)">'
        f'{mochi(mochi_expr(t), blink, mouth_open=meow_open(t, MEOWS))}</g>',
        coins,
        f'<g transform="translate({px:.0f},{py:.0f}) rotate({prot:.1f})">{piggy()}</g>',
        burst(fade(t, 0.45, 1.3, 0.06, 0.3), 820, 960, "PUM!", 100, r=140),
        moth_svg(t),
        total_panel(t),
        card(title_op, "Dia 4", "O Mochi conta a vaquinha", y=300, s1=90),
        card(fade(t, 2.3, 3.4), "A abanar o mealheiro...", y=300, s1=62),
        card(fade(t, 3.4, 4.5), "...só saiu uma traça.", y=300, s1=64),
        card(fade(t, 7.0, 9.1), "Dia 5 há de ser melhor.", "Ajuda o Mochi: link na bio", y=300, s1=62, s2=52),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("dia4", frame_svg, TOTAL)
