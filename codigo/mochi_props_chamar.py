"""Adereços do Short 'chamar': ondas da voz do dono, mão com a lata de petiscos, notas de assobio."""
INK = "#2B2B2B"


def ondas(op, x, y, t):
    """Arcos de som que vêm da esquerda (a voz do dono, sem texto)."""
    if op <= 0:
        return ""
    out = ""
    for i in range(3):
        k = ((t * 1.6 + i / 3) % 1.0)
        r = 60 + k * 150
        o = op * (1 - k) * 0.9
        out += (f'<path d="M{x + r * 0.5:.0f} {y - r:.0f} Q{x + r * 1.3:.0f} {y:.0f} {x + r * 0.5:.0f} {y + r:.0f}" '
                f'fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round" opacity="{o:.2f}"/>')
    return out


def lata(shake=0.0):
    """Lata de petiscos com tampa aberta, cerca de 260x300, centrada em (0,0)."""
    return (f'<g transform="rotate({shake:.1f})">'
            f'<rect x="-110" y="-110" width="220" height="250" rx="22" fill="#4FA3A5" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="-120" y="-135" width="240" height="40" rx="16" fill="#E7EEF0" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="-85" y="-60" width="170" height="130" rx="18" fill="#FFF6EA" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M-30 0 Q0 -40 30 0 Q40 30 0 55 Q-40 30 -30 0 Z" fill="#F2A14A" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="-12" cy="10" r="5" fill="{INK}"/><circle cx="12" cy="10" r="5" fill="{INK}"/>'
            f'<path d="M-85 100 L85 100" stroke="#3B8587" stroke-width="6"/>'
            f'</g>')


def mao(shake=0.0):
    """Braço + mão a segurar a lata (vem da direita). Origem no centro da lata."""
    return (f'<g transform="translate(150,40)"><rect x="40" y="-60" width="420" height="130" rx="60" fill="#6C9BD2" stroke="{INK}" stroke-width="7"/>'
            f'<ellipse cx="0" cy="0" rx="62" ry="58" fill="#F2C9A5" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M-30 -40 Q-45 -10 -30 20 M0 -52 Q-10 -10 0 30" fill="none" stroke="#D9A57F" stroke-width="5" stroke-linecap="round"/></g>'
            + lata(shake))


def notas(op, x, y, t):
    """Notinhas de assobio fingido."""
    if op <= 0:
        return ""
    out = ""
    for i in range(3):
        k = (t * 0.7 + i / 3) % 1.0
        out += (f'<text x="{x + i * 70 + 20 * __import__("math").sin(k * 6):.0f}" y="{y - k * 160:.0f}" font-family="DejaVu Sans" '
                f'font-weight="bold" font-size="64" fill="{INK}" opacity="{op * (1 - k):.2f}">&#9834;</text>')
    return out
