"""Gera a foto de perfil e o banner do YouTube do Mochi."""
import os

import cairosvg

from mochi_kit import mochi

DIR = os.path.dirname(os.path.abspath(__file__))


def avatar():
    s = 3.6
    mx = (1080 - 380 * s) / 2
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080">'
        '<rect width="1080" height="1080" fill="#FDE7D3"/>'
        '<circle cx="540" cy="540" r="470" fill="#F9D2B3"/>'
        f'<g transform="translate({mx:.0f},120) scale({s})">{mochi("happy")}</g>'
        '</svg>'
    )
    cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(DIR, "mochi_perfil.png"))


def banner():
    s = 1.25
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="2560" height="1440">'
        '<rect width="2560" height="1440" fill="#FDE7D3"/>'
        '<circle cx="1960" cy="560" r="150" fill="#F28B6B" opacity="0.55"/>'
        '<polygon points="1500,900 1840,560 1900,520 1960,560 2300,900" fill="#9FB4D6"/>'
        '<polygon points="1780,620 1840,560 1900,520 1960,560 2020,620 1960,600 1900,630 1840,600" fill="#FFFFFF"/>'
        '<rect x="0" y="900" width="2560" height="540" fill="#E9C9A8"/>'
        f'<g transform="translate(1180,450) scale({s})">{mochi("normal", headphones=False)}</g>'
        '<text x="1120" y="650" font-family="DejaVu Sans" font-weight="bold" font-size="104" fill="#D8343A" text-anchor="end">Mochi</text>'
        '<text x="1120" y="760" font-family="DejaVu Sans" font-weight="bold" font-size="64" fill="#2B2B2B" text-anchor="end">rumo ao Japão</text>'
        '<text x="1120" y="840" font-family="DejaVu Sans" font-size="40" fill="#8A6A50" text-anchor="end">novo vídeo todas as semanas</text>'
        '</svg>'
    )
    cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(DIR, "mochi_banner_youtube.png"))


if __name__ == "__main__":
    avatar()
    banner()
    print("ok")
