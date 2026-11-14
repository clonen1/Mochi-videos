"""Adereços do Short 'copo': o copo de água, salpico e poça. Copo centrado na base em (0,0), ~110x150."""
INK = "#2B2B2B"


def copo(water=1.0):
    """Copo de vidro com água. water 0..1."""
    wy = -128 + (1 - water) * 100
    out = ('<path d="M-55 -150 L55 -150 L44 0 L-44 0 Z" fill="#DFF1FA" opacity="0.75"/>')
    if water > 0.02:
        out += (f'<path d="M{-55 + (wy + 150) * 0.0786:.1f} {wy:.1f} L{55 - (wy + 150) * 0.0786:.1f} {wy:.1f} L44 0 L-44 0 Z" fill="#6FB8E8" opacity="0.9"/>'
                f'<path d="M{-55 + (wy + 150) * 0.0786:.1f} {wy:.1f} L{55 - (wy + 150) * 0.0786:.1f} {wy:.1f}" stroke="#A6D8F5" stroke-width="6"/>')
    out += (f'<path d="M-55 -150 L55 -150 L44 0 L-44 0 Z" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            '<path d="M-38 -135 L-30 -40" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.85"/>')
    return out


def poca(u, x, y):
    """Poça de água que alastra (u 0..1) no chão e gotas a saltar."""
    if u <= 0:
        return ""
    rx = 40 + 190 * u
    out = (f'<ellipse cx="{x}" cy="{y}" rx="{rx:.0f}" ry="{14 + 22 * u:.0f}" fill="#6FB8E8" opacity="0.85" stroke="#4A94C8" stroke-width="4"/>'
           f'<ellipse cx="{x - rx * 0.3:.0f}" cy="{y - 4}" rx="{rx * 0.3:.0f}" ry="5" fill="#A6D8F5" opacity="0.8"/>')
    return out


def gotas(u, x, y):
    if u <= 0 or u >= 1:
        return ""
    out = ""
    for i, (dx, vy) in enumerate([(-150, 330), (-80, 480), (0, 540), (90, 470), (160, 340), (-40, 400), (50, 420)]):
        tt = u * 0.55
        px = x + dx * u * 1.3
        py = y - vy * tt + 900 * tt * tt
        out += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{12 - 6 * u:.0f}" fill="#6FB8E8" stroke="#4A94C8" stroke-width="3" opacity="{1 - u:.2f}"/>'
    return out


def vidro(u, x, y):
    """Cacos de vidro à volta da poça."""
    if u <= 0:
        return ""
    out = ""
    for dx, dy, r in [(-210, 6, 25), (190, 14, 22), (-120, 30, 18), (250, -2, 16)]:
        out += (f'<polygon points="{x + dx - r},{y + dy} {x + dx},{y + dy - r} {x + dx + r},{y + dy + 4}" fill="#DFF1FA" '
                f'stroke="{INK}" stroke-width="4" stroke-linejoin="round" opacity="{min(1, u * 3):.2f}"/>')
    return out
