"""Vídeo 'Dia 5: o Mochi treina os pauzinhos' (série Dia N, 3.ª pessoa; 1080x1920, 10 s, 30 fps), em loop.

0-0.35  pauzinhos na taça | 0.35 FLIP: a massa voa | 1.3 PLAF: cai na cabeça do Mochi
2.1-3.9 'Tentativa 2': pauzinhos cruzados, um foge (TOING)
4.0-6.5 'Plano B: cara na taça' | 6.5-8.4 'Dia 5: aprovado (mais ou menos)'
8.4-9.3 'Ajuda o Mochi a ir ao Japão. Link na bio' | 9.2-10 sacode a massa para a taça (loop)
"""
import math

from mochi_cena import W, H, burst, card, clamp, ease, fade, main, meow_open, spring, svg_doc
from mochi_kit import mochi
from mochi_props import chopstick, noodles, paw, ramen_bowl
from musica_dia5 import MEOWS, TOTAL

S = 2.0
FLOOR = 1720
MX, MY0 = 540 - 190 * S, FLOOR - 378 * S
BOWL = (540, 1545)
PAW = (800, 1390)


def mochi_y(t):
    """Desce a cara para dentro da taça no plano B."""
    k = ease((t - 4.1) / 0.3) * (1 - ease((t - 6.3) / 0.25))
    hop = 40 * math.sin(math.pi * (t - 6.55) / 0.35) if 6.55 <= t < 6.9 else 0
    bob = 10 * abs(math.sin(t * 9)) if 4.4 <= t < 6.3 else 0
    return MY0 + 150 * k + bob - hop


def mochi_expr(t):
    for a, b, e in [(0.35, 1.3, "shock"), (1.3, 2.3, "ko"), (2.3, 3.0, "normal"), (3.0, 4.0, "angry"),
                    (4.1, 6.4, "eat"), (6.4, 8.4, "happy"), (8.4, 9.2, "happy")]:
        if a <= t < b:
            return e
    return "normal"


def head_top(t):
    return 540, mochi_y(t) + 92 * S


def noodle_pose(t):
    """(x, y, rot, escala) do novelo de massa, ou None se está na taça."""
    if t < 0.35 or t >= 9.75:
        return None
    if t < 1.3:                                   # voo em arco
        k = (t - 0.35) / 0.95
        hx, hy = head_top(t)
        x = BOWL[0] + (hx - BOWL[0]) * k + 120 * math.sin(math.pi * k)
        y0, y1 = BOWL[1] - 60, hy - 15
        y = y0 + (y1 - y0) * k - 380 * math.sin(math.pi * k)
        return x, y, 540 * k, 0.9 + 0.2 * k
    hx, hy = head_top(t)
    if t < 9.3:                                   # chapéu de massa
        sq = 1 + 0.25 * math.exp(-(t - 1.3) * 8) * math.cos((t - 1.3) * 30)
        wob = 6 * math.sin(t * 40) if 9.2 <= t else 0
        return hx + wob, hy - 15, 0, 1.1 * sq
    k = ease((t - 9.3) / 0.45)                    # sacode e cai na taça
    return hx, hy - 15 + (BOWL[1] - 60 - hy + 15) * k, 0, 1.1 - 0.5 * k


def sticks(t):
    """Dois pauzinhos e a patinha. Devolve SVG."""
    dip = 40 * math.sin(math.pi * clamp(t / 0.35)) if t < 0.35 else 0
    px, py = PAW[0], PAW[1] + dip
    a1, a2 = 152, 159
    if 2.2 <= t < 3.0:                            # cruzam e tremem
        a1, a2 = 165 + 6 * math.sin(t * 45), 146 - 6 * math.sin(t * 45)
    out = ""
    # pauzinho 2 (o que foge)
    if t < 3.0 or t >= 9.7:
        out += f'<g transform="translate({px:.0f},{py:.0f}) rotate({a2:.1f})">{chopstick(310)}</g>'
    elif t < 3.9:
        k = (t - 3.0) / 0.9
        out += (f'<g transform="translate({px + 700 * k:.0f},{py - 1500 * k + 600 * k * k:.0f}) '
                f'rotate({a2 + 900 * k:.0f})">{chopstick(310)}</g>')
    elif 9.3 <= t < 9.7:
        k = ease((t - 9.3) / 0.4)
        out += (f'<g transform="translate({px:.0f},{-300 + (py + 300) * k:.0f}) '
                f'rotate({a2 + 360 * (1 - k):.0f})">{chopstick(310)}</g>')
    if not (4.1 <= t < 6.4):
        out += f'<g transform="translate({px:.0f},{py:.0f}) rotate({a1:.1f})">{chopstick(310)}</g>'
        out += f'<g transform="translate({px:.0f},{py:.0f})">{paw()}</g>'
    return out


def frame_svg(t):
    my = mochi_y(t)
    shake = 8 * math.sin((t - 9.2) * 50) if 9.2 <= t < 9.6 else 0
    blink = 2.6 < t < 2.72 or 7.8 < t < 7.92
    title_op = 1 - ease((t - 2.0) / 0.25) if t < 5 else ease((t - 9.4) / 0.45)
    np_ = noodle_pose(t)
    noodle = ""
    if np_:
        x, y, r, s = np_
        noodle = f'<g transform="translate({x:.0f},{y:.0f}) rotate({r:.0f}) scale({s:.2f})">{noodles()}</g>'
    parts = [
        f'<rect width="{W}" height="{H}" fill="#FCE9D8"/>',
        # janela com o monte ao fundo (o sonho do Japão)
        '<rect x="90" y="900" width="300" height="300" rx="18" fill="#F3D2B6"/>'
        '<rect x="110" y="920" width="260" height="260" rx="10" fill="#BFE3F5"/>'
        '<polygon points="130,1180 240,1030 350,1180" fill="#8DA9C4"/><polygon points="215,1065 240,1030 265,1065" fill="#FFFFFF"/>'
        '<circle cx="320" cy="980" r="26" fill="#F06D5E"/>',
        '<g fill="#F8C8D0"><circle cx="880" cy="980" r="16"/><circle cx="930" cy="1040" r="12"/><circle cx="850" cy="1080" r="10"/></g>',
        f'<g transform="translate({MX:.1f},{my:.1f}) scale({S}) rotate({shake:.1f},190,200)">'
        f'{mochi(mochi_expr(t), blink, mouth_open=meow_open(t, MEOWS))}</g>',
        noodle if np_ and t >= 1.3 else "",
        f'<rect x="0" y="1640" width="{W}" height="{H - 1640}" fill="#B9835A"/>'
        f'<rect x="0" y="1640" width="{W}" height="22" fill="#9A6A45"/>',
        f'<g transform="translate({BOWL[0]},{BOWL[1]}) scale(1.15)">{ramen_bowl()}</g>',
        noodle if np_ and t < 1.3 else "",
        sticks(t),
        burst(fade(t, 0.35, 1.0, 0.05, 0.25), 250, 1080, "FLIP!", 90, r=140),
        burst(fade(t, 1.3, 2.0, 0.05, 0.3), 830, 1060, "PLAF!", 90, color="#B8733A", r=150),
        burst(fade(t, 3.0, 3.7, 0.05, 0.3), 820, 1000, "TOING!", 74, r=150),
        burst(fade(t, 4.4, 6.2, 0.1, 0.3), 840, 1140, "SLURP!", 66, color="#3F6FB0", r=140),
        card(title_op, "Dia 5", "O Mochi treina os pauzinhos", y=520, s1=90, s2=52),
        card(fade(t, 2.15, 3.95), "Tentativa 2...", y=520, s1=80),
        card(fade(t, 4.05, 6.5), "Plano B:", "cara na taça!", y=520, s1=70, s2=72),
        card(fade(t, 6.55, 8.45), "Dia 5: aprovado.", "(mais ou menos)", y=520, s1=72, s2=56),
        card(fade(t, 8.45, 9.4, 0.2, 0.2), "Ajuda o Mochi a ir ao Japão", "Link na bio", y=520, s1=56, s2=66),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("dia5", frame_svg, TOTAL)
