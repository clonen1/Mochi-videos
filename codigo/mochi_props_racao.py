"""Adereços do Short 'racao': o saco (que afinal é de pão). Centrado em (0,0)."""
INK = "#2B2B2B"


def saco(pao=False, amachucado=0.0):
    """Saco de papel castanho, cerca de 260x340. pao=True mostra um pão e a palavra PÃO."""
    sq = amachucado
    out = (f'<path d="M-120 170 L-105 -150 L-55 -170 L0 -145 L55 -170 L105 -150 L120 170 Z" '
           f'fill="#C99A62" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
           f'<path d="M-105 -150 L-55 -170 L0 -145 L55 -170 L105 -150 L90 -110 L0 -90 L-90 -110 Z" '
           f'fill="#E2B678" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    for i in range(4):
        y = -40 + i * 50
        out += f'<path d="M{-90 + sq * 8 * (i % 2)} {y} L{90 - sq * 8 * (i % 2)} {y + 8}" stroke="#A97C46" stroke-width="5" stroke-linecap="round"/>'
    if pao:
        out += ('<ellipse cx="0" cy="40" rx="75" ry="42" fill="#E9B45F" stroke="#2B2B2B" stroke-width="6"/>'
                '<path d="M-40 18 Q-25 40 -10 18 M-5 12 Q10 34 25 12 M30 18 Q42 36 52 20" fill="none" stroke="#B9822F" stroke-width="5" stroke-linecap="round"/>'
                '<text x="0" y="135" font-family="DejaVu Sans" font-weight="bold" font-size="52" fill="#FFFFFF" '
                'stroke="#2B2B2B" stroke-width="2" text-anchor="middle">PÃO</text>')
    else:
        out += ('<rect x="-60" y="10" width="120" height="90" rx="16" fill="#F6C343" stroke="#2B2B2B" stroke-width="6"/>'
                '<text x="0" y="80" font-family="DejaVu Sans" font-weight="bold" font-size="64" fill="#D8343A" text-anchor="middle">?</text>')
    return out


def speed_lines(op, x, y):
    if op <= 0:
        return ""
    out = ""
    for i in range(6):
        yy = y + (i - 2.5) * 70
        out += f'<line x1="{x}" y1="{yy:.0f}" x2="{x + 260 - i * 20}" y2="{yy:.0f}" stroke="#2B2B2B" stroke-width="10" stroke-linecap="round" opacity="{op:.2f}"/>'
    return out
