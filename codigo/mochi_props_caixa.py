"""Caixa de cartão minúscula para o Short 'caixa'. Centrada em (0,0) = meio da base."""
INK = "#2B2B2B"


def box_inside(w=260, h=170):
    """Interior escuro da caixa (desenhar ANTES do Mochi)."""
    return (f'<ellipse cx="0" cy="{-h + 6}" rx="{w / 2 - 8}" ry="26" fill="#7A5230" stroke="{INK}" stroke-width="5"/>')


def box_front(w=260, h=170):
    """Frente da caixa com abas e fita (desenhar DEPOIS do Mochi)."""
    x = -w / 2
    return (
        f'<rect x="{x}" y="{-h}" width="{w}" height="{h}" rx="8" fill="#D9A566" stroke="{INK}" stroke-width="6"/>'
        f'<rect x="{x + 6}" y="{-h + 8}" width="{w - 12}" height="22" fill="#C58E4E"/>'
        f'<rect x="-34" y="{-h}" width="68" height="{h * 0.55:.0f}" fill="#E9CFA0" opacity="0.85"/>'
        f'<polygon points="{x},{-h} {x - 46},{-h - 34} {x + 20},{-h - 40} {x + 46},{-h}" fill="#C58E4E" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        f'<polygon points="{-x},{-h} {-x + 46},{-h - 34} {-x - 20},{-h - 40} {-x - 46},{-h}" fill="#C58E4E" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    )
