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


# ---------- semana de 02/11 ----------

def ramen_bowl():
    """Taça de ramen vermelha com massa, ovo e naruto, cerca de 340x170."""
    return (
        f'<ellipse cx="0" cy="-40" rx="160" ry="34" fill="#E9B65A"/>'
        f'<path d="M-120 -48 q20 -16 40 0 t40 0 t40 0 t40 0 t40 0" fill="none" stroke="#F6D77A" stroke-width="9" stroke-linecap="round"/>'
        f'<ellipse cx="-70" cy="-50" rx="34" ry="20" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
        f'<ellipse cx="-70" cy="-50" rx="15" ry="11" fill="#F6B93B"/>'
        f'<circle cx="70" cy="-50" r="24" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
        f'<path d="M58 -50 q6 -10 12 0 t12 0" fill="none" stroke="#E77C8A" stroke-width="5" stroke-linecap="round"/>'
        f'<path d="M-170 -40 L170 -40 Q160 90 0 110 Q-160 90 -170 -40 Z" fill="#D8343A" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        f'<path d="M-120 20 l30 0 l0 25 l30 0 M60 20 l30 0 l0 25 l30 0" fill="none" stroke="#FFFFFF" stroke-width="6"/>'
        f'<rect x="-60" y="102" width="120" height="20" rx="8" fill="#B8262C" stroke="{INK}" stroke-width="5"/>'
    )


def noodles():
    """Novelo de massa a voar (ou em cima da cabeça), cerca de 180x90."""
    out = ""
    for i, (dy, a) in enumerate([(-25, 0), (-5, 6), (15, -4), (35, 3)]):
        out += (f'<path d="M-80 {dy} q20 -18 40 0 t40 0 t40 0 t40 0" fill="none" stroke="#E9B65A" '
                f'stroke-width="16" stroke-linecap="round" transform="rotate({a})"/>'
                f'<path d="M-80 {dy} q20 -18 40 0 t40 0 t40 0 t40 0" fill="none" stroke="#F6D77A" '
                f'stroke-width="7" stroke-linecap="round" transform="rotate({a})"/>')
    out += (f'<path d="M-60 40 q-10 30 -5 55 M50 40 q12 28 6 58" fill="none" stroke="#E9B65A" stroke-width="12" stroke-linecap="round"/>')
    return out


def chopstick(length=330):
    """Pauzinho de madeira, de (0,0) até (length,0)."""
    return (f'<path d="M0 -9 L{length} -4 L{length} 4 L0 9 Z" fill="#C98B4E" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="0" y="-9" width="60" height="18" fill="#8E5A2E"/>')


def paw():
    """Patinha do Mochi (laranja com almofada creme)."""
    return (f'<ellipse cx="0" cy="0" rx="36" ry="30" fill="#F2A14A" stroke="#D9802C" stroke-width="4"/>'
            f'<ellipse cx="0" cy="6" rx="18" ry="13" fill="#FFF6EA"/>')


def headband():
    """Bandana de ninja no espaço do Mochi (380x400)."""
    return (f'<path d="M96 128 Q190 100 284 128 L282 152 Q190 126 98 152 Z" fill="#2B2B2B"/>'
            f'<path d="M284 136 Q320 130 340 150 M284 146 Q316 158 330 182" fill="none" stroke="#2B2B2B" stroke-width="10" stroke-linecap="round"/>'
            f'<rect x="170" y="112" width="40" height="22" rx="4" fill="#B9C2CC"/>')


def calculator(screen="", shake=0.0):
    """Calculadora grande, cerca de 420x560. screen: texto do visor."""
    keys = ""
    labels = ["7", "8", "9", "÷", "4", "5", "6", "×", "1", "2", "3", "−", "C", "0", "=", "+"]
    for i, lab in enumerate(labels):
        r, c = divmod(i, 4)
        x, y = -165 + c * 85, -60 + r * 85
        col = "#F28C28" if c == 3 else ("#D8343A" if lab == "C" else "#FFFFFF")
        keys += (f'<rect x="{x}" y="{y}" width="70" height="70" rx="16" fill="{col}" stroke="{INK}" stroke-width="4"/>'
                 f'<text x="{x + 35}" y="{y + 49}" font-family="DejaVu Sans" font-weight="bold" font-size="38" '
                 f'fill="{INK}" text-anchor="middle">{lab}</text>')
    return (f'<g transform="rotate({shake:.1f})">'
            f'<rect x="-210" y="-280" width="420" height="580" rx="40" fill="#4A5568" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="-175" y="-245" width="350" height="150" rx="18" fill="#C8E6B0" stroke="{INK}" stroke-width="5"/>'
            f'{screen}{keys}</g>')


def mini_ramen():
    """Ícone de ramen pequeno para o visor (cerca de 60x40)."""
    return (f'<path d="M-30 -6 L30 -6 Q28 18 0 22 Q-28 18 -30 -6 Z" fill="#D8343A" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M-20 -10 q5 -6 10 0 t10 0 t10 0 t10 0" fill="none" stroke="#E9B65A" stroke-width="4"/>'
            f'<path d="M8 -12 L26 -34 M14 -10 L32 -30" stroke="#8E5A2E" stroke-width="3" stroke-linecap="round"/>')


def smoke(op, x, y, r=60):
    """Nuvem de fumo cinzenta."""
    if op <= 0:
        return ""
    return (f'<g opacity="{op:.2f}" fill="#B9B9B9" stroke="{INK}" stroke-width="4">'
            f'<circle cx="{x - r * 0.7:.0f}" cy="{y + r * 0.2:.0f}" r="{r * 0.7:.0f}"/>'
            f'<circle cx="{x + r * 0.7:.0f}" cy="{y + r * 0.2:.0f}" r="{r * 0.75:.0f}"/>'
            f'<circle cx="{x:.0f}" cy="{y - r * 0.3:.0f}" r="{r:.0f}"/></g>')
