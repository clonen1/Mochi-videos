"""Vídeo 'Madrugada' (meme 1.ª pessoa; 1080x1920, 10 s, 30 fps), em loop.

0-2.3   3 da manhã: o Mochi sentado no quarto escuro, olhos arregalados, relógio a marcar 3:00
2.4-3.0 agacha-se | 3.0-6.4 correria pelo quarto sem motivo (linhas de velocidade, ZUUM!, almofada a voar)
6.4-7.4 pára e senta-se | 7.4-9.4 olha para a câmara como se nada fosse ('Eu: ...') | 9.4-10 volta ao início
Sem nenhum preço, cidade ou link.
"""
import math

from mochi_cena import FONT, W, H, burst, card, clamp, ease, fade, main, meow_open, svg_doc
from mochi_kit import mochi
from mochi_props_madrugada import clock, pillow, speed_lines, window_moon
from musica_madrugada import MEOWS, TOTAL

S = 2.0
FLOOR = 1700
WAY = [(3.0, 540), (3.4, 170), (3.85, 910), (4.3, 200), (4.8, 880), (5.3, 300), (5.8, 800), (6.4, 540)]


def lerp(a, b, u):
    return a + (b - a) * u


def run_x(t):
    """Posição horizontal e sentido do movimento (+1 direita, -1 esquerda, 0 parado)."""
    if t < 3.0 or t >= 6.4:
        return 540, 0
    for (t0, x0), (t1, x1) in zip(WAY, WAY[1:]):
        if t0 <= t < t1:
            u = ease((t - t0) / (t1 - t0)) * 0.6 + 0.4 * (t - t0) / (t1 - t0)
            return lerp(x0, x1, u), (1 if x1 > x0 else -1)
    return 540, 0


def mochi_pose(t):
    """Devolve (x, hop, sx, sy, rot, expr)."""
    x, d = run_x(t)
    hop = 0.0
    sx = sy = 1.0
    rot = 0.0
    expr = "shock"
    if 2.4 <= t < 3.0:                       # agacha-se, a tremer de excitação
        k = ease((t - 2.4) / 0.6)
        sy = 1 - 0.14 * k
        sx = 1 + 0.08 * k
        x += 5 * math.sin(t * 70) * k
    elif 3.0 <= t < 6.4:
        expr = "happy"
        hop = 120 * abs(math.sin((t - 3.0) * 9.0))
        rot = 12 * d
    elif 6.4 <= t < 7.4:                     # derrapa e pára
        k = (t - 6.4) / 1.0
        rot = 6 * math.sin(k * 9) * (1 - k)
        sy = 1 + 0.05 * math.sin(k * 14) * (1 - k)
        expr = "shock"
    elif 7.4 <= t < 9.4:
        expr = "normal"
    return x, hop, sx, sy, rot, expr


def pillow_pos(t):
    """A almofada voa da cama (esq.) até ao chão (dir.) entre 3.6 e 5.2 s; antes e depois está parada."""
    if t < 3.6:
        return 150, 1640, 0.0, 1.0, 1.0
    if t >= 5.2:
        k = clamp((t - 5.2) / 0.25)
        return 860, 1665, 8, 1.0 + 0.12 * (1 - k) * math.sin(k * 20), 1.0
    u = (t - 3.6) / 1.6
    x = lerp(150, 860, u)
    y = lerp(1640, 1665, u) - 760 * math.sin(math.pi * u)
    return x, y, 720 * u, 1.0, 1.0


def frame_svg(t):
    x, hop, sx, sy, rot, expr = mochi_pose(t)
    blink = 1.3 < t < 1.42 or 8.2 < t < 8.32
    _, d = run_x(t)
    title_op = 1 - ease((t - 2.3) / 0.2) if t < 5 else ease((t - 9.4) / 0.45)
    px, py, pr, ps, _ = pillow_pos(t)
    pop = 1 - ease((t - 9.3) / 0.25) if t > 5 else ease(t / 0.3)
    glow = 0.5 + 0.5 * math.sin(t * 3)
    lines = speed_lines(fade(t, 3.05, 6.3, 0.1, 0.15), -d if d else 1, x, FLOOR - 420 - hop, 6)
    parts = [
        '<rect width="1080" height="1920" fill="#1D2147"/>',
        f'<rect x="0" y="{FLOOR - 70}" width="{W}" height="{H - FLOOR + 70}" fill="#2B2F63"/>',
        f'<g transform="translate(280,900)">{window_moon()}</g>',
        f'<g transform="translate(820,1080)">{clock(glow)}</g>',
        # tapete
        f'<ellipse cx="540" cy="{FLOOR + 10}" rx="420" ry="50" fill="#3A3F7E"/>',
        # sombra e Mochi
        f'<ellipse cx="{x:.0f}" cy="{FLOOR + 6}" rx="{250 - 70 * hop / 120:.0f}" ry="30" fill="#000" opacity="0.28"/>',
        lines,
        f'<g transform="translate({x:.1f},{FLOOR - hop:.1f}) rotate({rot:.1f}) scale({S * sx:.3f},{S * sy:.3f}) translate(-190,-378)">'
        f'{mochi(expr, blink, mouth_open=meow_open(t, MEOWS))}</g>',
        f'<g opacity="{pop:.2f}" transform="translate({px:.0f},{py:.0f}) rotate({pr:.0f}) scale({ps:.2f},{1 / ps:.2f})">{pillow()}</g>',
        burst(fade(t, 3.0, 3.8, 0.05, 0.25), 260, 1500, "ZUUM!", 100, r=150),
        burst(fade(t, 5.2, 5.9, 0.05, 0.25), 800, 1480, "PUF!", 90, color="#2B2B2B", r=150),
        card(title_op, "3 da manhã", y=480, s1=100),
        card(fade(t, 2.45, 6.4), "Eu, sem motivo", "nenhum.", y=480, s1=64, s2=64),
        card(fade(t, 7.4, 9.35, 0.2, 0.2), "Eu: ...", "(nada aconteceu)", y=480, s1=76, s2=56),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("madrugada", frame_svg, TOTAL)
