"""Adereços do Short 'madrugada' (quarto à noite): relógio digital, almofada, janela com lua, linhas de velocidade."""
import math

INK = "#2B2B2B"


def clock(glow=1.0):
    """Despertador digital a marcar 3:00, cerca de 330x200, centrado em (0,0)."""
    return (
        f'<rect x="-165" y="-100" width="330" height="200" rx="30" fill="#2A2D4F" stroke="{INK}" stroke-width="6"/>'
        f'<rect x="-135" y="-70" width="270" height="130" rx="16" fill="#14162B"/>'
        f'<text x="0" y="28" font-family="DejaVu Sans Mono, DejaVu Sans" font-weight="bold" font-size="100" fill="#FF5A4F" '
        f'text-anchor="middle" opacity="{0.8 + 0.2 * glow:.2f}">3:00</text>'
        f'<rect x="-120" y="100" width="30" height="24" rx="6" fill="#2A2D4F" stroke="{INK}" stroke-width="5"/>'
        f'<rect x="90" y="100" width="30" height="24" rx="6" fill="#2A2D4F" stroke="{INK}" stroke-width="5"/>'
    )


def pillow():
    """Almofada azul-clara, cerca de 260x180, centrada em (0,0)."""
    return (
        f'<rect x="-130" y="-90" width="260" height="180" rx="55" fill="#8FB4E8" stroke="{INK}" stroke-width="6"/>'
        f'<path d="M-90 -40 Q0 -70 90 -40" fill="none" stroke="#C5DBF7" stroke-width="8" stroke-linecap="round"/>'
        f'<circle cx="-120" cy="0" r="8" fill="#C5DBF7"/><circle cx="120" cy="0" r="8" fill="#C5DBF7"/>'
    )


def window_moon():
    """Janela de noite com lua e estrelas, cerca de 380x520, centrada em (0,0)."""
    return (
        f'<rect x="-190" y="-260" width="380" height="520" fill="#0F1330" stroke="{INK}" stroke-width="10"/>'
        f'<circle cx="60" cy="-120" r="70" fill="#FFF3C4"/><circle cx="85" cy="-140" r="62" fill="#0F1330"/>'
        f'<circle cx="-110" cy="-170" r="5" fill="#FFFFFF"/><circle cx="-40" cy="-60" r="4" fill="#FFFFFF"/>'
        f'<circle cx="-120" cy="20" r="4" fill="#FFFFFF"/><circle cx="110" cy="40" r="5" fill="#FFFFFF"/>'
        f'<line x1="0" y1="-260" x2="0" y2="260" stroke="{INK}" stroke-width="10"/>'
        f'<line x1="-190" y1="0" x2="190" y2="0" stroke="{INK}" stroke-width="10"/>'
    )


def speed_lines(op, direction, x, y, n=5):
    """Linhas de velocidade atrás do Mochi; direction = +1 (a andar para a direita) ou -1."""
    if op <= 0.02:
        return ""
    out = f'<g opacity="{op:.2f}">'
    for i in range(n):
        yy = y + (i - n / 2) * 70
        L = 220 + 70 * ((i * 37) % 3)
        x0 = x - direction * (150 + (i % 2) * 40)
        out += (f'<line x1="{x0:.0f}" y1="{yy:.0f}" x2="{x0 - direction * L:.0f}" y2="{yy:.0f}" '
                f'stroke="#E9E3FF" stroke-width="10" stroke-linecap="round"/>')
    return out + "</g>"
