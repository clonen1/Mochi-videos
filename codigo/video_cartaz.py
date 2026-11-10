"""Vídeo 'O Mochi e o cartaz' (meme em 1.ª pessoa, 1080x1920, 10 s, 30 fps), em loop. Divulga o PetPapers sem parecer anúncio.

0-2.6   Mochi a dormir: 'Eu a dormir 10 min' (zzz)
2.7     o cartaz PROCURA-SE com a cara dele cola-se à parede: 'O dono:' 'perdeu-se!'
4.4     acorda, lê o cartaz | 5.2 ofendido, olha para a câmara | miados 5.8 e 7.0 | 'Eu: estava aqui.'
7.6-9.4 cartão final: 'Cartaz grátis: PetPapers' + 'link na bio'
9.4-10  volta a dormir (liga ao início)
Sem preços, cidades, URL nem vaquinha.
"""
import math

from mochi_cena import FONT, W, H, burst, card, ease, fade, main, meow_open, svg_doc
from mochi_kit import mochi
from mochi_longo import zzz
from mochi_props_cartaz import cartaz
from musica_cartaz import MEOWS, TOTAL

S = 2.0
FLOOR = 1720
MX = -50
MY = FLOOR - 378 * S
POSTER = (740, 800)


def mochi_group(t):
    if t < 4.4 or t >= 9.5:
        expr, blink = "sleep", False
        bob = 6 * math.sin(t * 2.2)
        return (f'<g transform="translate({MX},{MY + 70 + bob:.1f}) scale({S}) rotate({-10 + 3 * math.sin(t * 2.2):.1f},190,378)">'
                f'{mochi(expr, blink)}</g>')
    hop = 0.0
    if 4.4 <= t < 4.85:
        hop = 90 * math.sin(math.pi * (t - 4.4) / 0.45)
    if t < 5.2:
        expr = "shock"
    elif t < 7.6:
        expr = "angry"
    else:
        expr = "sad"
    tilt = 4 * math.sin((t - 5.2) * 5) if 5.2 <= t < 7.6 else 0
    return (f'<g transform="translate({MX + 200 * ease((t - 4.4) / 0.4):.0f},{MY - hop:.1f}) scale({S}) rotate({tilt:.1f},190,378)">'
            f'{mochi(expr, 8.2 < t < 8.32, mouth_open=meow_open(t, MEOWS))}</g>')


def end_card(op):
    if op <= 0:
        return ""
    return (f'<g opacity="{op:.2f}"><rect x="90" y="470" width="900" height="520" rx="50" fill="#FFFFFF" opacity="0.97"/>'
            f'<text x="540" y="630" font-family="{FONT}" font-weight="bold" font-size="76" fill="#2B2B2B" text-anchor="middle">Cartaz grátis:</text>'
            f'<text x="540" y="760" font-family="{FONT}" font-weight="bold" font-size="120" fill="#D8343A" text-anchor="middle">PetPapers</text>'
            f'<rect x="300" y="820" width="480" height="96" rx="48" fill="#2B2B2B"/>'
            f'<text x="540" y="888" font-family="{FONT}" font-weight="bold" font-size="54" fill="#FFF6DE" text-anchor="middle">link na bio</text></g>')


def frame_svg(t):
    parts = [
        f'<rect width="{W}" height="{H}" fill="#FDEFD8"/>',
        f'<rect x="0" y="{FLOOR - 40}" width="{W}" height="{H - FLOOR + 40}" fill="#EBC99B"/>',
        f'<ellipse cx="{MX + 380}" cy="{FLOOR + 10}" rx="300" ry="38" fill="#000" opacity="0.10"/>',
        f'<ellipse cx="{MX + 380}" cy="{FLOOR - 15}" rx="320" ry="60" fill="#8FB8DE" stroke="#2B2B2B" stroke-width="6"/>',
    ]
    if t >= 2.7:
        u = min(1.0, (t - 2.7) / 0.35)
        pop = 1 + 0.12 * (1 - u) + 0.04 * math.sin((t - 2.7) * 14) * (1 - ease((t - 2.7) / 0.8))
        tilt = -4 + 3 * (1 - u)
        op = 1.0 if t < 9.4 else 1 - ease((t - 9.4) / 0.4)
        parts.append(f'<g opacity="{op:.2f}" transform="translate({POSTER[0]},{POSTER[1]}) rotate({tilt:.1f}) scale({0.92 * pop:.3f})">{cartaz()}</g>')
    parts.append(mochi_group(t))
    if t < 2.7 or t >= 9.4:
        zop = fade(t, 0.0, 2.7, 0.1, 0.3) if t < 2.7 else ease((t - 9.4) / 0.5)
        parts.append(f'<g opacity="{zop:.2f}">{zzz(t, 520, 1150, 3, 70)}</g>')
    parts += [
        burst(fade(t, 2.7, 3.5, 0.05, 0.25), 360, 760, "PAF!", 100, r=170),
        card(fade(t, 0.0, 2.6, 0.04, 0.2), "Eu a dormir 10 min", y=170, s1=76),
        card(fade(t, 2.8, 5.1, 0.2, 0.2), "O dono:", "perdeu-se!", y=170, s1=76, s2=88),
        card(fade(t, 5.3, 7.5, 0.2, 0.2), "Eu:", "estava aqui.", y=170, s1=76, s2=88),
        end_card(fade(t, 7.6, 9.4, 0.3, 0.3)),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("cartaz", frame_svg, TOTAL)
