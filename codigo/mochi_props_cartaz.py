"""Adereços do Short 'cartaz': o cartaz PROCURA-SE com a cara do Mochi. Centrado em (0,0), cerca de 360x520."""
from mochi_kit import mochi

INK = "#2B2B2B"


def cartaz(slit=True):
    out = (f'<rect x="-180" y="-260" width="360" height="520" rx="10" fill="#FFF6DE" stroke="{INK}" stroke-width="7"/>'
           '<circle cx="0" cy="-246" r="9" fill="#C0392B" stroke="#2B2B2B" stroke-width="3"/>'
           f'<text x="0" y="-176" font-family="DejaVu Sans" font-weight="bold" font-size="48" fill="#D8343A" text-anchor="middle">PROCURA-SE</text>'
           f'<rect x="-120" y="-150" width="240" height="190" rx="14" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
           f'<g transform="translate(-72,-134) scale(0.38)">{mochi("normal")}</g>'
           f'<text x="0" y="82" font-family="DejaVu Sans" font-weight="bold" font-size="44" fill="{INK}" text-anchor="middle">MOCHI</text>'
           f'<text x="0" y="122" font-family="DejaVu Sans" font-size="26" fill="#6B5B45" text-anchor="middle">gato laranja, adora dormir</text>')
    if slit:
        out += f'<line x1="-180" y1="160" x2="180" y2="160" stroke="{INK}" stroke-width="3" stroke-dasharray="10 8"/>'
        for i in range(6):
            x = -150 + i * 60
            out += (f'<line x1="{x}" y1="160" x2="{x}" y2="256" stroke="{INK}" stroke-width="3" stroke-dasharray="8 6"/>'
                    f'<text x="{x + 30}" y="236" font-family="DejaVu Sans" font-size="20" fill="#6B5B45" text-anchor="middle" '
                    f'transform="rotate(-90 {x + 30} 236)">contacto</text>')
    return out
