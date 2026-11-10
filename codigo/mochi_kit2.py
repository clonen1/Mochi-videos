"""Mochi com visual novo: gradientes, sombras suaves, contorno e luz. Mesmas expressoes do mochi_kit."""
from mochi_kit import _eyes, _mouth, _headphones, CREAM, PINK, BLUSH, NOSE, INK, RED, RED_DARK, BAG, BAG_LIGHT

STYLES = {
    # A: suave, sem contorno, volume por gradiente
    "A": dict(outline=None, ow=0, c1="#FFC271", c2="#F2A14A", c3="#D9802C", shade=0.55, rim=0.0, big=1.0),
    # B: autocolante, contorno escuro grosso, sombra plana
    "B": dict(outline="#8A4A1E", ow=7, c1="#F7B35E", c2="#F2A14A", c3="#E08A34", shade=0.25, rim=0.0, big=1.0),
    # C: fofo, cabeça maior, luz de contorno
    "C": dict(outline="#B8661F", ow=3, c1="#FFC978", c2="#F4A650", c3="#D9802C", shade=0.45, rim=0.6, big=1.12),
}


def _defs(s):
    return (f'<defs>'
            f'<radialGradient id="gb" cx="0.38" cy="0.3" r="0.9"><stop offset="0" stop-color="{s["c1"]}"/>'
            f'<stop offset="0.6" stop-color="{s["c2"]}"/><stop offset="1" stop-color="{s["c3"]}"/></radialGradient>'
            f'<radialGradient id="gc" cx="0.4" cy="0.3" r="0.9"><stop offset="0" stop-color="#FFFFFF"/>'
            f'<stop offset="1" stop-color="#F3DEC4"/></radialGradient>'
            f'<radialGradient id="ge" cx="0.5" cy="0.7" r="0.8"><stop offset="0" stop-color="#F59A9A"/>'
            f'<stop offset="1" stop-color="#F8C2C2"/></radialGradient>'
            f'</defs>')


def _shadow():
    # sombra suave no chao: elipses empilhadas com pouca opacidade (o cairosvg nao tem blur)
    out = ""
    for i, (rx, ry, op) in enumerate([(150, 26, .05), (130, 22, .07), (110, 18, .09), (90, 14, .11)]):
        out += f'<ellipse cx="190" cy="372" rx="{rx}" ry="{ry}" fill="#3A2410" opacity="{op}"/>'
    return out


import math

_W = 17
_SEG1 = [(262, 306), (308, 326), (350, 300), (338, 256)]
_SEG2 = [(338, 256), (333, 240), (320, 230), (307, 234)]
_PATH = "M262 306 C308 326 350 300 338 256 C333 240 320 230 307 234"
_ANGLE = 28      # inclinacao do corte da ponta branca (graus)
_BULGE = 3.4     # arredondamento do corte


def _bez(P, t):
    u = 1 - t
    return (u**3 * P[0][0] + 3 * u * u * t * P[1][0] + 3 * u * t * t * P[2][0] + t**3 * P[3][0],
            u**3 * P[0][1] + 3 * u * u * t * P[1][1] + 3 * u * t * t * P[2][1] + t**3 * P[3][1])


def _dbez(P, t):
    u = 1 - t
    return (3 * u * u * (P[1][0] - P[0][0]) + 6 * u * t * (P[2][0] - P[1][0]) + 3 * t * t * (P[3][0] - P[2][0]),
            3 * u * u * (P[1][1] - P[0][1]) + 6 * u * t * (P[2][1] - P[1][1]) + 3 * t * t * (P[3][1] - P[2][1]))


def _build_tail_geometry():
    pts = [(_bez(_SEG1, i / 40), _dbez(_SEG1, i / 40)) for i in range(41)]
    pts += [(_bez(_SEG2, i / 40), _dbez(_SEG2, i / 40)) for i in range(1, 41)]
    h = _W / 2
    left, right = [], []
    for (x, y), (dx, dy) in pts:
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        left.append((x + nx * h, y + ny * h))
        right.append((x - nx * h, y - ny * h))
    ex, ey = _SEG2[3]
    # corte oblíquo e arredondado da ponta branca, a ~50% do segmento final
    t = 0.5
    mx, my = _bez(_SEG2, t)
    dx, dy = _dbez(_SEG2, t)
    n = math.hypot(dx, dy)
    dx, dy = dx / n, dy / n          # tangente (para a ponta)
    nx, ny = -dy, dx
    sh = h * math.tan(math.radians(_ANGLE))
    A = (mx + nx * h + dx * sh, my + ny * h + dy * sh)
    B = (mx - nx * h - dx * sh, my - ny * h - dy * sh)
    exx, eyy = A[0] - B[0], A[1] - B[1]
    el = math.hypot(exx, eyy)
    ex_, ey_ = exx / el, eyy / el
    px, py = -ey_, ex_
    if px * dx + py * dy < 0:
        px, py = -px, -py
    mid = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    c = (mid[0] - px * 2 * _BULGE, mid[1] - py * 2 * _BULGE)
    big = 60
    half = (f"M{A[0]:.1f} {A[1]:.1f} Q{c[0]:.1f} {c[1]:.1f} {B[0]:.1f} {B[1]:.1f} "
            f"L{B[0] - ex_ * big:.1f} {B[1] - ey_ * big:.1f} "
            f"L{B[0] - ex_ * big + px * big:.1f} {B[1] - ey_ * big + py * big:.1f} "
            f"L{A[0] + ex_ * big + px * big:.1f} {A[1] + ey_ * big + py * big:.1f} "
            f"L{A[0] + ex_ * big:.1f} {A[1] + ey_ * big:.1f} Z")
    # interior da cauda desde antes do corte ate a ponta
    L, R = [], []
    for i in range(10, 41):
        (x, y), (ddx, ddy) = _bez(_SEG2, i / 40), _dbez(_SEG2, i / 40)
        m = math.hypot(ddx, ddy) or 1
        L.append((x - ddy / m * (h - 0.2), y + ddx / m * (h - 0.2)))
        R.append((x + ddy / m * (h - 0.2), y - ddx / m * (h - 0.2)))
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in L + R[::-1])
    clip = f'<clipPath id="tailcut"><path d="{half}"/></clipPath>'
    cream = (f'<g clip-path="url(#tailcut)"><polygon points="{poly}" fill="#FFF6EA"/>'
             f'<circle cx="{ex}" cy="{ey}" r="{h - 0.2}" fill="#FFF6EA"/></g>')
    return clip, cream


_CLIP, _CREAM = _build_tail_geometry()


def _tail(s, o):
    """Cauda fina de largura uniforme: contorno, miolo, poucas listras e ponta creme recortada ao interior."""
    out = _CLIP
    if s["outline"]:
        out += f'<path d="{_PATH}" fill="none" stroke="{s["outline"]}" stroke-width="{_W + 2 * s["ow"]}" stroke-linecap="round" stroke-linejoin="round"/>'
    out += f'<path d="{_PATH}" fill="none" stroke="{s["c2"]}" stroke-width="{_W}" stroke-linecap="round"/>'
    out += f'<path d="{_PATH}" fill="none" stroke="{s["c3"]}" stroke-width="{_W}" stroke-dasharray="6 30" stroke-dashoffset="-18"/>'
    out += _CREAM
    return out


def mochi2(style="A", expr="normal", blink=False, headphones=False, mouth_open=0.0):
    s = STYLES[style]
    o = f'stroke="{s["outline"]}" stroke-width="{s["ow"]}" stroke-linejoin="round"' if s["outline"] else ""
    k = s["big"]
    head = f'transform="translate(190 168) scale({k}) translate(-190 -168)"'
    shade = s["shade"]
    rim = (f'<path d="M96 150 Q100 100 150 92" fill="none" stroke="#FFE2B0" stroke-width="7" stroke-linecap="round" opacity="{s["rim"]}"/>'
           f'<path d="M96 292 Q92 250 120 226" fill="none" stroke="#FFE2B0" stroke-width="7" stroke-linecap="round" opacity="{s["rim"]}"/>') if s["rim"] else ""
    angry = '<ellipse cx="190" cy="140" rx="90" ry="40" fill="#E5533D" opacity="0.18"/>' if expr == "angry" else ""
    blush_op = "0.9" if expr != "angry" else "0"
    return f"""{_defs(s)}{_shadow()}
{_tail(s, o)}
<ellipse cx="190" cy="290" rx="95" ry="78" fill="url(#gb)" {o}/>
<ellipse cx="190" cy="318" rx="80" ry="42" fill="#8A4A1E" opacity="{shade*0.22:.2f}"/>
<ellipse cx="190" cy="305" rx="55" ry="55" fill="url(#gc)"/>
<ellipse cx="145" cy="362" rx="28" ry="16" fill="url(#gc)" {o}/><ellipse cx="235" cy="362" rx="28" ry="16" fill="url(#gc)" {o}/>
<path d="M136 356 Q136 363 137 369 M154 356 Q154 363 153 369 M226 356 Q226 363 227 369 M244 356 Q244 363 243 369" fill="none" stroke="#C9A173" stroke-width="2.6" stroke-linecap="round"/>
<g {head}>
<polygon points="108,135 118,58 168,105" fill="url(#gb)" {o}/><polygon points="272,135 262,58 212,105" fill="url(#gb)" {o}/>
<polygon points="120,118 125,78 152,105" fill="url(#ge)"/><polygon points="260,118 255,78 228,105" fill="url(#ge)"/>
<ellipse cx="190" cy="168" rx="93" ry="80" fill="url(#gb)"/>
<ellipse cx="190" cy="232" rx="86" ry="22" fill="#8A4A1E" opacity="{shade*0.18:.2f}"/>
{rim}
<path d="M175 90 Q181 109 172 122" fill="none" stroke="{s['c3']}" stroke-width="6" stroke-linecap="round"/>
<path d="M190 88 Q193 110 190 126" fill="none" stroke="{s['c3']}" stroke-width="6" stroke-linecap="round"/>
<path d="M205 90 Q199 109 208 122" fill="none" stroke="{s['c3']}" stroke-width="6" stroke-linecap="round"/>
<ellipse cx="190" cy="168" rx="93" ry="80" fill="none" {o}/>
{angry}
<ellipse cx="148" cy="160" rx="34" ry="30" fill="url(#gc)"/>
<ellipse cx="190" cy="200" rx="48" ry="32" fill="url(#gc)"/>
{_eyes(expr, blink)}
<ellipse cx="125" cy="198" rx="15" ry="9" fill="{BLUSH}" opacity="{blush_op}"/><ellipse cx="255" cy="198" rx="15" ry="9" fill="{BLUSH}" opacity="{blush_op}"/>
<polygon points="181.5,185.5 198.5,185.5 190,196" fill="{NOSE}" stroke="{NOSE}" stroke-width="5" stroke-linejoin="round"/><ellipse cx="187" cy="186.5" rx="3.2" ry="1.6" fill="#FFD0D6" opacity="0.9"/>
{_mouth(expr, mouth_open)}
<path d="M98 188 Q76 178 54 180 M98 197 Q76 198 56 206 M282 188 Q304 178 326 180 M282 197 Q304 198 324 206" fill="none" stroke="#FFF6EA" stroke-width="3" stroke-linecap="round" opacity="0.95"/>
</g>
<rect x="112" y="228" width="156" height="24" rx="12" fill="{RED}"/><rect x="112" y="228" width="156" height="9" rx="4.5" fill="#EE5A60" opacity="0.7"/><rect x="200" y="240" width="22" height="48" rx="8" fill="{RED_DARK}"/>
{_headphones() if headphones else ""}
"""
