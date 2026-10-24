"""Adereços desenhados em SVG (flat 2D) para os vídeos da semana de 26/10.

Todos centrados em (0,0); posiciona-os com translate/rotate/scale.
"""
import math

INK = "#2B2B2B"


def piggy():
    """Mealheiro cor-de-rosa, cerca de 300x230."""
    return (
        f'<ellipse cx="0" cy="0" rx="150" ry="110" fill="#F4A6B8" stroke="{INK}" stroke-width="6"/>'
        f'<rect x="-100" y="80" width="40" height="55" rx="12" fill="#E98DA3" stroke="{INK}" stroke-width="5"/>'
        f'<rect x="60" y="80" width="40" height="55" rx="12" fill="#E98DA3" stroke="{INK}" stroke-width="5"/>'
        f'<polygon points="-80,-95 -50,-150 -30,-100" fill="#E98DA3" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        f'<ellipse cx="135" cy="10" rx="38" ry="44" fill="#F7BACA" stroke="{INK}" stroke-width="5"/>'
        f'<ellipse cx="128" cy="0" rx="6" ry="9" fill="{INK}"/><ellipse cx="146" cy="0" rx="6" ry="9" fill="{INK}"/>'
        f'<circle cx="70" cy="-35" r="10" fill="{INK}"/>'
        f'<rect x="-40" y="-112" width="70" height="12" rx="6" fill="{INK}"/>'
        f'<path d="M-150 -10 Q-190 -30 -175 -55" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    )


def moth(t):
    """Traça a bater as asas (t em segundos)."""
    flap = abs(math.sin(t * 22))
    wy = 10 + 40 * flap
    return (
        f'<ellipse cx="-32" cy="0" rx="40" ry="{wy:.0f}" fill="#B9B2A6" stroke="{INK}" stroke-width="4"/>'
        f'<ellipse cx="32" cy="0" rx="40" ry="{wy:.0f}" fill="#B9B2A6" stroke="{INK}" stroke-width="4"/>'
        f'<ellipse cx="0" cy="0" rx="12" ry="30" fill="#8A8278" stroke="{INK}" stroke-width="4"/>'
        f'<path d="M-4 -28 Q-14 -50 -24 -52 M4 -28 Q14 -50 24 -52" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    )


def cucumber(face=False):
    """Pepino deitado, cerca de 320x90."""
    out = (
        f'<rect x="-160" y="-45" width="320" height="90" rx="45" fill="#4E9A3A" stroke="{INK}" stroke-width="6"/>'
        f'<rect x="-130" y="-30" width="240" height="18" rx="9" fill="#7CC35E" opacity="0.8"/>'
        f'<circle cx="-80" cy="15" r="5" fill="#2F6B22"/><circle cx="-10" cy="20" r="5" fill="#2F6B22"/>'
        f'<circle cx="60" cy="12" r="5" fill="#2F6B22"/><circle cx="120" cy="22" r="5" fill="#2F6B22"/>'
        f'<rect x="155" y="-12" width="22" height="24" rx="6" fill="#6B4E2E" stroke="{INK}" stroke-width="4"/>'
    )
    if face:
        out += (f'<circle cx="-40" cy="-5" r="7" fill="{INK}"/><circle cx="0" cy="-5" r="7" fill="{INK}"/>'
                f'<path d="M-32 14 Q-20 22 -8 14" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    return out


def bowl(food=True):
    """Taça de comida, cerca de 300x110."""
    out = ""
    if food:
        out += (f'<ellipse cx="0" cy="-30" rx="125" ry="38" fill="#B8733A"/>'
                f'<circle cx="-50" cy="-48" r="16" fill="#9A5B2A"/><circle cx="10" cy="-55" r="16" fill="#A4652F"/>'
                f'<circle cx="60" cy="-45" r="16" fill="#9A5B2A"/>')
    out += (f'<path d="M-150 -30 L150 -30 L115 55 L-115 55 Z" fill="#3F6FB0" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<rect x="-150" y="-42" width="300" height="24" rx="12" fill="#5A8BCC" stroke="{INK}" stroke-width="6"/>'
            f'<text x="0" y="32" font-family="DejaVu Sans" font-weight="bold" font-size="34" fill="#FFFFFF" text-anchor="middle">MOCHI</text>')
    return out


def witch_hat():
    """Chapéu de bruxa no espaço do Mochi (380x400)."""
    return (
        f'<ellipse cx="190" cy="100" rx="135" ry="22" fill="#5B3A8C" stroke="{INK}" stroke-width="5"/>'
        f'<path d="M115 98 Q150 20 175 -40 Q200 -95 255 -70 Q215 -55 230 20 L265 98 Z" fill="#6B47A3" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        f'<rect x="122" y="70" width="136" height="22" fill="#F28C28"/>'
    )


def pumpkin(glow=1.0):
    """Abóbora de Halloween, cerca de 240x200."""
    return (
        f'<rect x="-12" y="-120" width="24" height="40" rx="8" fill="#4E7A2E" stroke="{INK}" stroke-width="5"/>'
        f'<ellipse cx="-60" cy="0" rx="70" ry="95" fill="#E8781E" stroke="{INK}" stroke-width="5"/>'
        f'<ellipse cx="60" cy="0" rx="70" ry="95" fill="#E8781E" stroke="{INK}" stroke-width="5"/>'
        f'<ellipse cx="0" cy="0" rx="70" ry="98" fill="#F28C28" stroke="{INK}" stroke-width="5"/>'
        f'<g fill="#FFD84D" opacity="{glow:.2f}"><polygon points="-60,-30 -30,-30 -45,-60"/><polygon points="30,-30 60,-30 45,-60"/>'
        f'<path d="M-65 20 L-40 35 L-20 20 L0 38 L20 20 L40 35 L65 20 Q30 70 0 70 Q-30 70 -65 20 Z"/></g>'
    )


def bat(t, phase=0.0):
    """Morcego a bater as asas."""
    f = math.sin(t * 14 + phase)
    wy = -35 * f
    return (
        f'<path d="M0 0 Q-40 {wy - 20:.0f} -90 {wy:.0f} Q-70 10 -50 5 Q-30 20 0 0 Z" fill="#2B2238"/>'
        f'<path d="M0 0 Q40 {wy - 20:.0f} 90 {wy:.0f} Q70 10 50 5 Q30 20 0 0 Z" fill="#2B2238"/>'
        f'<ellipse cx="0" cy="0" rx="16" ry="20" fill="#2B2238"/>'
        f'<polygon points="-12,-14 -6,-30 0,-16 6,-30 12,-14" fill="#2B2238"/>'
        f'<circle cx="-6" cy="-4" r="3" fill="#FFD84D"/><circle cx="6" cy="-4" r="3" fill="#FFD84D"/>'
    )
