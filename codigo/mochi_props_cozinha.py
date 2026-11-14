"""Adereços da cozinha para 'O Mochi tenta cozinhar' (coordenadas locais; origem indicada em cada função)."""
import math

from mochi_longo import INK, H, W

CHEF = ('<path d="M112 130 L112 96 Q96 60 128 52 Q140 14 190 30 Q240 14 252 52 Q284 60 268 96 L268 130 Z" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round"/>'
        '<rect x="108" y="108" width="164" height="26" rx="10" fill="#F4F1EA" stroke="#2B2B2B" stroke-width="4"/>')

SOOT = ('<ellipse cx="190" cy="205" rx="92" ry="64" fill="#2B2B2B" opacity="0.55"/>'
        '<ellipse cx="190" cy="128" rx="70" ry="22" fill="#2B2B2B" opacity="0.5"/>')


def kitchen_bg():
    out = f'<rect width="{W}" height="{H}" fill="#FFF1DA"/>'
    for i in range(0, W, 120):
        out += f'<line x1="{i}" y1="0" x2="{i}" y2="720" stroke="#F0DDBB" stroke-width="3"/>'
    for j in range(0, 720, 120):
        out += f'<line x1="0" y1="{j}" x2="{W}" y2="{j}" stroke="#F0DDBB" stroke-width="3"/>'
    # janela e prateleira
    out += (f'<rect x="150" y="120" width="320" height="300" fill="#BFE3F5" stroke="{INK}" stroke-width="9"/>'
            f'<line x1="310" y1="120" x2="310" y2="420" stroke="{INK}" stroke-width="7"/><line x1="150" y1="270" x2="470" y2="270" stroke="{INK}" stroke-width="7"/>'
            f'<ellipse cx="240" cy="200" rx="50" ry="20" fill="#FFFFFF" opacity="0.9"/>'
            f'<rect x="700" y="330" width="420" height="16" rx="6" fill="#B8774A" stroke="{INK}" stroke-width="4"/>')
    for k, c in enumerate(["#D8343A", "#4FA3D9", "#F6C343", "#7FC28F"]):
        out += f'<rect x="{730 + k * 95}" y="{270}" width="64" height="60" rx="10" fill="{c}" stroke="{INK}" stroke-width="4"/><rect x="{722 + k * 95}" y="262" width="80" height="14" rx="6" fill="#F4F1EA" stroke="{INK}" stroke-width="4"/>'
    # chão
    out += f'<rect y="900" width="{W}" height="{H - 900}" fill="#E7C9A0"/><rect y="890" width="{W}" height="14" fill="#C9A06C"/>'
    for i in range(0, W, 240):
        out += f'<line x1="{i}" y1="904" x2="{i - 60}" y2="{H}" stroke="#D3B07F" stroke-width="3"/>'
    # bancada
    out += (f'<rect y="700" width="{W}" height="200" fill="#C98B4E" stroke="{INK}" stroke-width="6"/>'
            f'<rect y="690" width="{W}" height="26" fill="#F4F1EA" stroke="{INK}" stroke-width="6"/>')
    for i in range(0, W, 320):
        out += f'<line x1="{i}" y1="716" x2="{i}" y2="896" stroke="#A9703A" stroke-width="5"/><circle cx="{i + 160}" cy="760" r="9" fill="#F6C343" stroke="{INK}" stroke-width="3"/>'
    return out


def stove(x=1340, y=690, w=420):
    """Fogão: topo em (x, y), largura w, cai até ao chão (~900)."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{900 - y}" fill="#8A8FA3" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{x}" y="{y - 16}" width="{w}" height="26" fill="#3B3F54" stroke="{INK}" stroke-width="6"/>'
            + "".join(f'<circle cx="{x + 90 + i * 120}" cy="{y + 58}" r="22" fill="#3B3F54" stroke="{INK}" stroke-width="5"/>' for i in range(3))
            + f'<rect x="{x + 40}" y="{y + 110}" width="{w - 80}" height="150" rx="12" fill="#555A73" stroke="{INK}" stroke-width="5"/>')


def flame(t, cx, cy, s=1.0):
    out = ""
    for i in range(5):
        h = (34 + 12 * math.sin(t * 17 + i * 2)) * s
        out += (f'<path d="M{cx - 40 * s + i * 20 * s:.0f} {cy:.0f} Q{cx - 46 * s + i * 20 * s:.0f} {cy - h:.0f} {cx - 40 * s + i * 20 * s:.0f} {cy - h - 14:.0f} '
                f'Q{cx - 34 * s + i * 20 * s:.0f} {cy - h:.0f} {cx - 40 * s + i * 20 * s:.0f} {cy:.0f}Z" fill="#F28C28" stroke="#D8343A" stroke-width="3"/>')
    return out


def pan(batter=0.0, burnt=0.0):
    """Frigideira, origem no centro do fundo; ~300 de largura, cabo para a direita."""
    cook = "#F6D77A" if burnt < 0.5 else "#4A3B2E"
    out = (f'<rect x="130" y="-34" width="230" height="26" rx="12" fill="#6B4A2E" stroke="{INK}" stroke-width="5"/>'
           f'<path d="M-150 -90 L150 -90 L120 -10 L-120 -10 Z" fill="#3B3F54" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
           f'<ellipse cx="0" cy="-90" rx="150" ry="24" fill="#555A73" stroke="{INK}" stroke-width="6"/>')
    if batter > 0:
        out += f'<ellipse cx="0" cy="-90" rx="{118 * batter:.0f}" ry="{17 * batter:.0f}" fill="{cook}"/>'
    return out


def pancake(r=110, burnt=0.0):
    col = "#E9B65A" if burnt < 0.5 else "#6B4A2E"
    return (f'<ellipse cx="0" cy="0" rx="{r}" ry="{r * 0.34:.0f}" fill="{col}" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="0" cy="-4" rx="{r * 0.78:.0f}" ry="{r * 0.22:.0f}" fill="#F6D77A" opacity="0.8"/>'
            f'<rect x="-22" y="-16" width="44" height="22" rx="6" fill="#FFF3B0" stroke="{INK}" stroke-width="4"/>')


def pot(lid=True, lid_dy=0.0, lid_rot=0.0):
    """Panela, origem no centro do fundo; ~300 largura x 220 alto."""
    out = (f'<rect x="-190" y="-170" width="46" height="18" rx="8" fill="#555A73" stroke="{INK}" stroke-width="5"/>'
           f'<rect x="144" y="-170" width="46" height="18" rx="8" fill="#555A73" stroke="{INK}" stroke-width="5"/>'
           f'<path d="M-150 -220 L150 -220 L140 0 L-140 0 Z" fill="#B8BCC6" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
           f'<rect x="-120" y="-200" width="26" height="170" rx="12" fill="#FFFFFF" opacity="0.35"/>'
           f'<ellipse cx="0" cy="-220" rx="150" ry="24" fill="#8A8FA3" stroke="{INK}" stroke-width="6"/>')
    if lid:
        out += (f'<g transform="translate(0,{lid_dy - 230:.0f}) rotate({lid_rot:.0f})"><path d="M-155 0 Q0 -90 155 0 Z" fill="#8A8FA3" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
                f'<circle cx="0" cy="-58" r="14" fill="#3B3F54" stroke="{INK}" stroke-width="5"/></g>')
    return out


def fish(rot=0.0):
    return (f'<g transform="rotate({rot:.0f})"><path d="M-60 0 Q-20 -40 40 -4 L80 -34 L80 34 L40 4 Q-20 40 -60 0Z" fill="#7FB5D8" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<circle cx="-34" cy="-6" r="6" fill="{INK}"/></g>')


def carrot(rot=0.0):
    return (f'<g transform="rotate({rot:.0f})"><path d="M-50 -14 L50 0 L-50 14 Z" fill="#F28C28" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M-50 0 L-82 -18 M-50 0 L-86 0 M-50 0 L-82 18" stroke="#4FA35A" stroke-width="8" stroke-linecap="round"/></g>')


def spoon():
    return (f'<rect x="-8" y="-150" width="16" height="170" rx="6" fill="#C98B4E" stroke="{INK}" stroke-width="4"/>'
            f'<ellipse cx="0" cy="-160" rx="26" ry="34" fill="#C98B4E" stroke="{INK}" stroke-width="4"/>')


def foam(cx, y, w, h, t=0.0):
    """Montanha de espuma: bolhas brancas; (cx, y) = base."""
    out = ""
    n = 14
    for i in range(n):
        u = i / (n - 1)
        bx = cx - w / 2 + u * w
        hh = h * (0.35 + 0.65 * math.sin(math.pi * u) ** 0.7)
        r = max(14, hh * 0.28 + 10 * math.sin(t * 5 + i))
        out += f'<circle cx="{bx:.0f}" cy="{y - hh * 0.55:.0f}" r="{r:.0f}" fill="#FFFFFF" stroke="#CFE3EE" stroke-width="4"/>'
        out += f'<circle cx="{bx + 10:.0f}" cy="{y - hh * 0.95 + 20:.0f}" r="{r * 0.8:.0f}" fill="#FFFFFF" stroke="#CFE3EE" stroke-width="4"/>'
    out += f'<rect x="{cx - w / 2:.0f}" y="{y - h * 0.3:.0f}" width="{w:.0f}" height="{h * 0.3:.0f}" fill="#FFFFFF"/>'
    return out


def oven(door_open=0.0, glow=0.0, cake=0.0, burnt=0.0, x=1340, y=500, w=460, h=400):
    """Forno: caixa com janela. cake 0..1 = bolo crescido; burnt 0..1 escurece."""
    cx, cy = x + w / 2, y + h * 0.58
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="#8A8FA3" stroke="{INK}" stroke-width="7"/>'
           f'<rect x="{x}" y="{y}" width="{w}" height="70" rx="22" fill="#555A73" stroke="{INK}" stroke-width="7"/>'
           + "".join(f'<circle cx="{x + 70 + i * 90}" cy="{y + 35}" r="20" fill="#F4F1EA" stroke="{INK}" stroke-width="5"/>' for i in range(4))
           + f'<rect x="{x + 40}" y="{y + 96}" width="{w - 80}" height="{h - 130}" rx="16" fill="#2B2B2B" stroke="{INK}" stroke-width="6"/>')
    inner = f'<rect x="{x + 56}" y="{y + 112}" width="{w - 112}" height="{h - 162}" rx="10" fill="{"#F2A14A" if glow > 0.3 else "#4A4A55"}" opacity="{0.35 + 0.5 * glow:.2f}"/>'
    out += inner
    if cake > 0:
        ch = 40 + 70 * cake
        col = "#E9B65A" if burnt < 0.4 else ("#8A5A2E" if burnt < 0.8 else "#2B2B2B")
        out += (f'<rect x="{cx - 100}" y="{y + h - 90 - 6}" width="200" height="14" rx="6" fill="#3B3F54"/>'
                f'<path d="M{cx - 90} {y + h - 90} L{cx - 90} {y + h - 90 - ch * 0.7:.0f} Q{cx} {y + h - 90 - ch * 1.3:.0f} {cx + 90} {y + h - 90 - ch * 0.7:.0f} L{cx + 90} {y + h - 90} Z" fill="{col}" stroke="{INK}" stroke-width="5"/>')
    out += f'<rect x="{x + 40}" y="{y + 96}" width="{w - 80}" height="{h - 130}" rx="16" fill="#FFFFFF" opacity="{0.14 * (1 - door_open):.2f}"/>'
    out += f'<rect x="{x + 70}" y="{y + 82}" width="{w - 140}" height="12" rx="6" fill="#F4F1EA" stroke="{INK}" stroke-width="4"/>'
    return out


def timer(t, ring=0.0):
    sh = 7 * math.sin(t * 60) * ring
    return (f'<g transform="translate({sh:.1f},0) rotate({sh:.1f})"><circle r="56" fill="#D8343A" stroke="{INK}" stroke-width="6"/><circle r="40" fill="#FFF6EA" stroke="{INK}" stroke-width="4"/>'
            f'<line x1="0" y1="0" x2="0" y2="-28" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><line x1="0" y1="0" x2="18" y2="8" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<circle cx="-40" cy="-52" r="12" fill="#F6C343" stroke="{INK}" stroke-width="4"/><circle cx="40" cy="-52" r="12" fill="#F6C343" stroke="{INK}" stroke-width="4"/></g>')


def cake(burnt=0.0, candle=False, t=0.0):
    col = "#F4B6C2" if burnt < 0.5 else "#2B2B2B"
    top = "#FFF6EA" if burnt < 0.5 else "#4A4A55"
    out = (f'<path d="M-120 0 L-120 -100 Q0 -150 120 -100 L120 0 Z" fill="{col}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
           f'<path d="M-120 -100 Q-90 -70 -60 -100 T0 -100 T60 -100 T120 -100 Q0 -150 -120 -100Z" fill="{top}" stroke="{INK}" stroke-width="5"/>')
    if candle:
        out += (f'<rect x="-8" y="-170" width="16" height="50" fill="#4FA3D9" stroke="{INK}" stroke-width="4"/>'
                f'<path d="M0 {-210 - 4 * math.sin(t * 18):.0f} Q-14 -190 0 -176 Q14 -190 0 {-210 - 4 * math.sin(t * 18):.0f}Z" fill="#F28C28" stroke="#D8343A" stroke-width="3"/>')
    return out


def plate():
    return (f'<ellipse cx="0" cy="0" rx="150" ry="26" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/><ellipse cx="0" cy="-4" rx="100" ry="14" fill="#F0ECE4"/>')


def cookbook():
    return (f'<rect x="-90" y="-26" width="180" height="26" rx="6" fill="#D8343A" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="-84" y="-52" width="168" height="26" rx="6" fill="#FFF6EA" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="-90" y="-78" width="180" height="26" rx="6" fill="#4FA3D9" stroke="{INK}" stroke-width="5"/>')
