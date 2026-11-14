"""Vídeo 'O Mochi e o copo' (meme em 1.ª pessoa, 1080x1920, 10 s, 30 fps), em loop.

0-5.5   empurra o copo centímetro a centímetro, a olhar fixo para a câmara (já em movimento no 1.º quadro)
5.5-6.2 último empurrão, o copo tomba e cai | 6.2 CRASH! (choque a fingir)
6.5-9.4 olha para o lado a assobiar: 'Não fui eu.' / 'Estava a ver um passarinho.'
9.4-10  volta a olhar para a câmara com copo novo (liga ao início)
Sem preços, nomes de cidades nem link.
"""
import math
import os
import shutil
import sys

from mochi_cena import FONT, W, H, burst, card, clamp, ease, main, meow_open, svg_doc
from mochi_kit import mochi
from musica_copo import MEOWS, TOTAL
from mochi_props_copo import copo, gotas, poca, vidro

S = 2.0
TABLE_Y = 1380
EDGE = 900
FLOOR = 1720
X0 = 640
CUP_Y_FLOOR = FLOOR - 4
PUSHES = [(-0.3, 0.4, 672), (1.0, 0.45, 704), (1.9, 0.45, 738), (2.9, 0.45, 775), (3.9, 0.45, 812),
          (4.8, 0.5, 852), (5.45, 0.4, 912)]
FALL_T = 5.95   # instante em que o copo passa a borda e cai
HIT_T = 6.35


def cup_state(t):
    """Devolve (x, y, rot, water, paw_gap, visible, on_floor)."""
    x = X0
    gap = 45.0
    prev = X0
    for ts, d, xe in PUSHES:
        h = d * 0.45
        if t < ts:
            break
        if t < ts + h:
            gap = 45 * (1 - ease((t - ts) / h))
            x = prev
            break
        if t < ts + d:
            u = ease((t - ts - h) / (d - h))
            x = prev + (xe - prev) * u
            gap = 0
            break
        x = xe
        prev = xe
        r = (t - ts - d) / 0.3
        gap = 45 * ease(r)
    return x, gap


def frame_svg(t):
    x, gap = cup_state(t)
    cy, rot, water = TABLE_Y, 0.0, 1.0
    cup_vis = True
    floor_u = 0.0
    if t >= 9.45:           # copo novo (loop)
        x, gap = X0, 45.0
        cup_vis = True
        k = ease((t - 9.45) / 0.25)
    else:
        k = 1.0
    if t >= 5.75:
        # tomba sobre a borda e cai
        tt = t - 5.75
        x = 912 + 40 * min(tt, 0.6)
        if tt < 0.2:
            rot = 40 * ease(tt / 0.2)
            cy = TABLE_Y + 8 * ease(tt / 0.2)
        else:
            u = tt - 0.2
            rot = 40 + 520 * u
            cy = TABLE_Y + 8 + 2600 * u * u
        water = max(0.0, 1 - 2.2 * tt)
        if cy >= CUP_Y_FLOOR - 20 or t >= HIT_T:
            cy = CUP_Y_FLOOR
            rot = 98
            x = 915 + 40 * min(1, (t - HIT_T + 0.2))
            water = 0.0
            floor_u = clamp((t - HIT_T) / 0.5)
        if t >= 9.3:
            cup_vis = False
    if t >= 9.3 and t < 9.45:
        cup_vis = False
    if t >= 9.45:
        cy, rot, water = TABLE_Y, 0.0, 1.0

    # expressão do Mochi
    if t < 5.75 or t >= 9.4:
        e = "normal"
    elif t < 6.7:
        e = "shock"
    else:
        e = "happy"
    blink = (1.55 < t < 1.67) or (3.4 < t < 3.52) or (8.2 < t < 8.32)
    # cabeça vira para o lado e inocente (rodar/inclinar)
    look = 0.0
    if 6.55 <= t < 9.4:
        look = ease((t - 6.55) / 0.35)
    elif t >= 9.4:
        look = 1 - ease((t - 9.4) / 0.4)
    rot_m = -7 * look + 1.2 * math.sin(t * 2.0)
    mx_off = 22 * look
    bob = 3 * math.sin(t * 2.4)
    # inclina-se para a frente a empurrar
    lean = 0.0
    for ts, d, xe in PUSHES:
        if ts <= t < ts + d + 0.2:
            lean = 5 * math.sin(math.pi * clamp((t - ts) / (d + 0.2)))
    mo = meow_open(t, MEOWS)
    cup_left = x - 52
    paw_x = cup_left - 40 - gap if t < 5.75 else None
    parts = [
        f'<rect width="{W}" height="{H}" fill="#FFF0DC"/>',
        # janela com passarinho (para onde o Mochi finge olhar)
        '<rect x="90" y="900" width="0" height="0"/>',
        f'<rect x="0" y="{FLOOR - 40}" width="{W}" height="{H - FLOOR + 40}" fill="#E4C08F"/>',
        # sombra do Mochi na mesa
        f'<ellipse cx="380" cy="{TABLE_Y + 4}" rx="330" ry="22" fill="#000" opacity="0.12"/>',
        f'<g transform="translate({mx_off:.1f},{640 + bob - lean:.1f}) rotate({rot_m + lean * 0.6:.1f},380,756) scale({S})">'
        f'{mochi(e, blink, mouth_open=mo)}</g>',
        # mesa: tampo, avental e pernas
        f'<rect x="780" y="{TABLE_Y + 70}" width="60" height="{FLOOR - TABLE_Y - 70}" fill="#9A6A3C" stroke="#2B2B2B" stroke-width="6"/>',
        f'<rect x="-30" y="{TABLE_Y + 70}" width="900" height="26" fill="#8A5A30" stroke="#2B2B2B" stroke-width="6"/>',
        f'<rect x="-30" y="{TABLE_Y}" width="{EDGE + 30}" height="70" rx="10" fill="#C98B4E" stroke="#2B2B2B" stroke-width="6"/>',
        f'<rect x="-24" y="{TABLE_Y + 4}" width="{EDGE + 18}" height="14" fill="#E2A868" opacity="0.8"/>',
    ]
    if floor_u > 0:
        parts.append(poca(ease(floor_u), 880, FLOOR + 22))
    if cup_vis:
        op = 1.0 if t < 9.45 else k
        parts.append(f'<g opacity="{op:.2f}" transform="translate({x:.1f},{cy:.1f}) rotate({rot:.1f},{0 if rot < 90 else 0},{0})">'
                     f'{copo(water if t < 6.4 else 0.0)}</g>' if rot < 60 else
                     f'<g opacity="{op:.2f}" transform="translate({x:.1f},{cy - 0:.1f}) rotate({rot:.1f}) translate(0,-55)">{copo(water)}</g>')
    if floor_u > 0:
        parts.append(vidro(ease(floor_u), 880, FLOOR + 30))
        parts.append(gotas(clamp((t - HIT_T) / 0.7), 880, FLOOR))
    # braço e patinha
    if paw_x is not None or t >= 9.4:
        px = paw_x if paw_x is not None else X0 - 52 - 40 - 45
        py = TABLE_Y - 62
        sx0, sy0 = 440, TABLE_Y - 40
        if t >= 9.4:
            px = X0 - 52 - 40 - 45 - 40 * ease((t - 9.4) / 0.6)
        parts.append(f'<line x1="{sx0}" y1="{sy0}" x2="{px:.0f}" y2="{py}" stroke="#8A4A1E" stroke-width="58" stroke-linecap="round"/>'
                     f'<line x1="{sx0}" y1="{sy0}" x2="{px:.0f}" y2="{py}" stroke="#F2A14A" stroke-width="44" stroke-linecap="round"/>'
                     f'<ellipse cx="{px + 6:.0f}" cy="{py}" rx="42" ry="38" fill="#F2A14A" stroke="#8A4A1E" stroke-width="6"/>'
                     f'<ellipse cx="{px + 14:.0f}" cy="{py + 4}" rx="20" ry="16" fill="#FFF6EA"/>')
    # assobio (notas) quando finge inocência
    if 6.9 <= t < 9.3:
        for i in range(3):
            u = ((t - 6.9) * 0.7 + i / 3) % 1
            parts.append(f'<text x="{250 + 300 * 0 + 40 * math.sin(u * 6 + i):.0f}" y="{1060 - 150 * u:.0f}" font-family="{FONT}" '
                         f'font-size="{56 + i * 6}" fill="#2B2B2B" opacity="{math.sin(math.pi * u):.2f}">♪</text>')
    # linhas de movimento do empurrão
    parts += [
        burst(clamp((HIT_T - 0.05 <= t) * (1 - ease((t - HIT_T - 0.5) / 0.4)) * ease((t - HIT_T + 0.05) / 0.1)), 560, 1560, "CRASH!", 100, r=170),
    ]
    c1 = lambda a, b, l1, l2="", **kw: card(1.0 if (a <= t < b - 0.12) else (ease((b - t) / 0.12) if a <= t < b else
                                          ease((t - a) / 0.15) if a - 0.15 < t < a else 0.0), l1, l2, **kw)
    parts += [
        card(1.0 if t < 2.28 else (ease((2.4 - t) / 0.12) if t < 2.4 else (ease((t - 9.45) / 0.2) if t >= 9.45 else 0)),
             "Devagarinho...", y=480, s1=84),
        c1(2.4, 4.4, "A olhar para ti.", y=480, s1=76),
        c1(4.4, 6.0, "Só mais um", "bocadinho...", y=480, s1=76, s2=88),
        c1(6.45, 7.9, "Não fui eu.", y=480, s1=88),
        c1(7.9, 9.4, "Estava a ver", "um passarinho.", y=480, s1=72, s2=88),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("copo", frame_svg, TOTAL)
    if len(sys.argv) == 1:
        d = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(os.path.join(d, "../videos"), exist_ok=True)
        os.makedirs(os.path.join(d, "../musica"), exist_ok=True)
        shutil.move(os.path.join(d, "mochi_copo.mp4"), os.path.join(d, "../videos/mochi_copo.mp4"))
        shutil.copy(os.path.join(d, "musica_copo.wav"), os.path.join(d, "../musica/musica_copo.wav"))
