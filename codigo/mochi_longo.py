"""Utilitários e adereços para os vídeos longos do Mochi (1920x1080, 24 fps)."""
import math

from mochi_kit import RED, RED_DARK, mochi

W, H, FPS = 1920, 1080, 24
FONT = "DejaVu Sans"
INK = "#2B2B2B"
SCARF = (f'<rect x="112" y="228" width="156" height="24" rx="12" fill="{RED}"/>'
         f'<rect x="200" y="240" width="22" height="48" rx="8" fill="{RED_DARK}"/>')


# ---------- matemática ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def spring(t):
    return 0 if t < 0 else 1 - math.exp(-t * 7) * math.cos(t * 16)


def fade(t, a, b, fin=0.4, fout=0.4):
    return ease((t - a) / fin) * (1 - ease((t - (b - fout)) / fout))


def lerp(a, b, u):
    return a + (b - a) * u


# ---------- Mochi ----------
def M(t, x, y, s=1.4, expr="normal", flip=1, sx=1.0, sy=1.0, rot=0.0, scarf=True, mouth=0.0, extra="", op=1.0,
      shadow=True, blink=None, breathe=True):
    """Mochi com os pés em (x, y). `extra` desenha-se no espaço do Mochi (380x400), por cima (chapéu, avental)."""
    if blink is None:
        blink = (t % 3.9) < 0.12 and expr in ("normal", "angry", "eat", "sad")
    svg = mochi(expr, blink, mouth_open=mouth)
    if not scarf:
        svg = svg.replace(SCARF, "")
    if breathe:
        sy = sy * (1 + 0.012 * math.sin(t * 2.4))
    sh = ""
    if shadow:
        sh = f'<ellipse cx="{x:.0f}" cy="{y + 4:.0f}" rx="{74 * s * sx:.0f}" ry="{12 * s:.0f}" fill="#000" opacity="{0.16 * op:.2f}"/>'
    return (sh + f'<g opacity="{op:.2f}" transform="translate({x:.1f},{y:.1f}) rotate({rot:.1f}) scale({s * sx * flip:.3f},{s * sy:.3f})">'
            f'<g transform="translate(-190,-378)">{svg}{extra}</g></g>')


def walk_bob(t, speed=3.4, amp=14):
    """(dy, rot) de um passo: salta e inclina."""
    ph = t * speed * math.pi
    return -abs(math.sin(ph)) * amp, math.sin(ph) * 3.0


CAP = ('<path d="M104 130 Q190 30 276 130 Q190 112 104 130 Z" fill="#D8343A" stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round"/>'
       '<path d="M246 124 Q312 118 322 140 Q290 144 246 136 Z" fill="#B8262C" stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round"/>'
       '<circle cx="190" cy="68" r="8" fill="#FFF6EA" stroke="#2B2B2B" stroke-width="3"/>')

GUARD_CAP = ('<path d="M100 128 Q190 36 280 128 Q190 112 100 128 Z" fill="#2D4A7C" stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round"/>'
             '<rect x="104" y="116" width="172" height="16" rx="8" fill="#1F3560" stroke="#2B2B2B" stroke-width="3"/>'
             '<path d="M190 70 L202 88 L190 106 L178 88 Z" fill="#F6C343" stroke="#2B2B2B" stroke-width="3"/>')

APRON = ('<path d="M140 262 L240 262 L254 346 Q190 366 126 346 Z" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round"/>'
         '<rect x="166" y="296" width="48" height="30" rx="6" fill="#F3E3C8" stroke="#2B2B2B" stroke-width="3"/>')


def drool(t):
    y = (t * 90) % 60
    return f'<ellipse cx="206" cy="{218 + y:.0f}" rx="6" ry="9" fill="#7EC8F2" stroke="#2B2B2B" stroke-width="2" opacity="{1 - y / 60:.2f}"/>'


# ---------- texto e efeitos ----------
def caption(op, txt, y=1012, size=62):
    if op <= 0.01:
        return ""
    w = max(520, len(txt) * size * 0.60 + 130)
    return (f'<g opacity="{op:.2f}" transform="translate(0,{(1 - op) * 18:.0f})">'
            f'<rect x="{(W - w) / 2:.0f}" y="{y - size - 14}" width="{w:.0f}" height="{size + 48}" rx="28" fill="#1E1B2E" opacity="0.9"/>'
            f'<rect x="{(W - w) / 2 + 9:.0f}" y="{y - size - 5}" width="{w - 18:.0f}" height="{size + 30}" rx="20" fill="none" stroke="#F6C343" stroke-width="3"/>'
            f'<text x="{W / 2}" y="{y + 6}" font-family="{FONT}" font-weight="bold" font-size="{size}" fill="#FFF6EA" text-anchor="middle">{txt}</text></g>')


def burst(op, x, y, word, size=84, r=135, color="#D8343A", rot=0):
    if op <= 0.01:
        return ""
    pts = []
    for i in range(24):
        rr = (r if i % 2 == 0 else r * 0.66) * (0.5 + 0.5 * min(op * 1.4, 1))
        a = math.pi * 2 * i / 24
        pts.append(f"{x + math.cos(a) * rr * 1.35:.0f},{y + math.sin(a) * rr:.0f}")
    return (f'<g opacity="{min(op * 2, 1):.2f}" transform="rotate({rot},{x},{y})"><polygon points="{" ".join(pts)}" fill="#F6C343" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<text x="{x}" y="{y + size * 0.36:.0f}" font-family="{FONT}" font-weight="bold" font-size="{size}" fill="{color}" text-anchor="middle">{word}</text></g>')


def stamp(lt, t0, txt="DESPEDIDO", x=960, y=440, size=118):
    """Carimbo vermelho que cai com ressalto."""
    u = lt - t0
    if u < 0:
        return ""
    sc = 1 + 1.6 * math.exp(-u * 14) * max(0, math.cos(u * 22))
    op = clamp(u * 10)
    w = len(txt) * size * 0.72 + 80
    return (f'<g opacity="{op:.2f}" transform="translate({x},{y}) rotate(-8) scale({sc:.2f})">'
            f'<rect x="{-w / 2:.0f}" y="{-size * 0.85:.0f}" width="{w:.0f}" height="{size * 1.35:.0f}" rx="22" fill="#FFFFFF" opacity="0.93"/>'
            f'<rect x="{-w / 2:.0f}" y="{-size * 0.85:.0f}" width="{w:.0f}" height="{size * 1.35:.0f}" rx="22" fill="none" stroke="#D8343A" stroke-width="12"/>'
            f'<text x="0" y="{size * 0.3:.0f}" font-family="{FONT}" font-weight="bold" font-size="{size}" fill="#D8343A" text-anchor="middle">{txt}</text></g>')


def pay(lt, t0, label="Salário: 0€", x=1640, y=120):
    """Etiqueta de salário no canto, com 0€."""
    u = lt - t0
    if u < 0:
        return ""
    op = clamp(u * 6)
    return (f'<g opacity="{op:.2f}" transform="translate({x},{y})"><rect x="-210" y="-58" width="420" height="100" rx="26" fill="#1E1B2E" opacity="0.92"/>'
            f'<text x="0" y="14" font-family="{FONT}" font-weight="bold" font-size="54" fill="#F6C343" text-anchor="middle">{label}</text></g>')


def sparkle(x, y, s, op=1):
    return (f'<path transform="translate({x:.0f},{y:.0f}) scale({s:.2f})" opacity="{op:.2f}" '
            'd="M0 -20 Q3 -3 20 0 Q3 3 0 20 Q-3 3 -20 0 Q-3 -3 0 -20Z" fill="#FFF3B0"/>')


def zzz(t, x, y, n=3, size=60):
    out = ""
    for i in range(n):
        u = ((t * 0.7 + i / n) % 1)
        out += (f'<text x="{x + 30 * u + i * 12:.0f}" y="{y - 150 * u:.0f}" font-family="{FONT}" font-weight="bold" '
                f'font-size="{size * (0.6 + 0.7 * u):.0f}" fill="#FFFFFF" opacity="{math.sin(math.pi * u):.2f}" stroke="#2B2B2B" stroke-width="2">Z</text>')
    return out


def cam(inner, t, a, b, z0=1.0, z1=1.08, fx=960, fy=560, dx=0.0):
    u = ease((t - a) / (b - a))
    z = z0 + (z1 - z0) * u
    return f'<g transform="translate({fx + dx * u:.1f},{fy}) scale({z:.4f}) translate({-fx},{-fy})">{inner}</g>'


def petals(t, n=18, op=1):
    out = ""
    for i in range(n):
        x = (i * 113 + t * 60 + 40 * math.sin(t + i * 1.7)) % (W + 100) - 50
        y = (i * 71 + t * 90) % (H + 100) - 50
        out += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="11" ry="7" fill="#F7B6C8" opacity="{0.85 * op:.2f}" '
                f'transform="rotate({(t * 80 + i * 40) % 360:.0f},{x:.0f},{y:.0f})"/>')
    return out


# ---------- adereços ----------
def coin(x, y, r=30, rot=0.0):
    sx = abs(math.cos(rot)) * 0.85 + 0.15
    return (f'<g transform="translate({x:.0f},{y:.0f})"><ellipse rx="{r * sx:.1f}" ry="{r}" fill="#F6C343" stroke="#B88A1B" stroke-width="5"/>'
            f'<ellipse rx="{r * 0.55 * sx:.1f}" ry="{r * 0.55:.1f}" fill="none" stroke="#B88A1B" stroke-width="3"/></g>')


def bulb(x, y, s=1.0, op=1.0):
    return (f'<g opacity="{op:.2f}" transform="translate({x},{y}) scale({s})">'
            '<g stroke="#F6C343" stroke-width="7" stroke-linecap="round"><line x1="0" y1="-95" x2="0" y2="-125"/><line x1="-70" y1="-70" x2="-92" y2="-92"/>'
            '<line x1="70" y1="-70" x2="92" y2="-92"/><line x1="-90" y1="-10" x2="-122" y2="-14"/><line x1="90" y1="-10" x2="122" y2="-14"/></g>'
            '<circle cx="0" cy="-30" r="58" fill="#FFE98A" stroke="#2B2B2B" stroke-width="6"/>'
            '<path d="M-20 -20 Q0 -50 20 -20" fill="none" stroke="#E0B63A" stroke-width="5"/>'
            '<rect x="-24" y="22" width="48" height="30" rx="6" fill="#B8BCC6" stroke="#2B2B2B" stroke-width="5"/></g>')


def phone(glow=1.0):
    return (f'<rect x="-70" y="-120" width="140" height="240" rx="26" fill="#2B2B2B"/>'
            f'<rect x="-58" y="-104" width="116" height="208" rx="14" fill="#FFF6EA"/>'
            f'<path d="M0 -10 C -30 -48 -62 -10 0 40 C 62 -10 30 -48 0 -10 Z" fill="#D8343A" opacity="{0.5 + 0.5 * glow:.2f}"/>'
            f'<rect x="-40" y="62" width="80" height="22" rx="11" fill="#4CAF50"/>')


def piggy_svg(shake=0.0):
    ink = INK
    return (
        f'<g transform="rotate({shake:.1f})">'
        f'<ellipse cx="0" cy="0" rx="120" ry="88" fill="#F4A6B8" stroke="{ink}" stroke-width="6"/>'
        f'<rect x="-80" y="64" width="34" height="44" rx="10" fill="#E98DA3" stroke="{ink}" stroke-width="5"/>'
        f'<rect x="48" y="64" width="34" height="44" rx="10" fill="#E98DA3" stroke="{ink}" stroke-width="5"/>'
        f'<polygon points="-64,-76 -40,-120 -24,-80" fill="#E98DA3" stroke="{ink}" stroke-width="5" stroke-linejoin="round"/>'
        f'<ellipse cx="108" cy="8" rx="30" ry="35" fill="#F7BACA" stroke="{ink}" stroke-width="5"/>'
        f'<ellipse cx="102" cy="0" rx="5" ry="8" fill="{ink}"/><ellipse cx="118" cy="0" rx="5" ry="8" fill="{ink}"/>'
        f'<circle cx="56" cy="-28" r="8" fill="{ink}"/>'
        f'<rect x="-32" y="-90" width="56" height="10" rx="5" fill="{ink}"/>'
        f'<path d="M-120 -8 Q-152 -24 -140 -44" fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round"/></g>')


def person(x, y, s=1.0, mood="neutral", flip=1, shirt="#6C9BD2", hair="#5A3A22", pants="#3D4B6B", bob=0.0, arms=0.0):
    """Pessoa simples (flat): cabeça redonda, corpo, pernas. `arms`: 0 baixos, 1 para cima (susto)."""
    ink = INK
    face = {
        "neutral": '<circle cx="-16" cy="-224" r="6" fill="#2B2B2B"/><circle cx="16" cy="-224" r="6" fill="#2B2B2B"/><path d="M-14 -196 L14 -196" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/>',
        "angry": '<circle cx="-16" cy="-222" r="6" fill="#2B2B2B"/><circle cx="16" cy="-222" r="6" fill="#2B2B2B"/><path d="M-30 -244 L-6 -234 M30 -244 L6 -234" stroke="#2B2B2B" stroke-width="6" stroke-linecap="round"/><path d="M-16 -194 Q0 -208 16 -194" fill="none" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/>',
        "shock": '<circle cx="-16" cy="-224" r="10" fill="#fff" stroke="#2B2B2B" stroke-width="4"/><circle cx="16" cy="-224" r="10" fill="#fff" stroke="#2B2B2B" stroke-width="4"/><circle cx="-16" cy="-224" r="4" fill="#2B2B2B"/><circle cx="16" cy="-224" r="4" fill="#2B2B2B"/><ellipse cx="0" cy="-192" rx="10" ry="13" fill="#2B2B2B"/>',
        "mask": '<rect x="-44" y="-238" width="88" height="26" rx="10" fill="#2B2B2B"/><circle cx="-16" cy="-225" r="5" fill="#fff"/><circle cx="16" cy="-225" r="5" fill="#fff"/>',
    }[mood]
    aw = -150 + 110 * arms
    return (f'<g transform="translate({x:.0f},{y + bob:.0f}) scale({s * flip:.3f},{s:.3f})">'
            f'<ellipse cx="0" cy="6" rx="70" ry="12" fill="#000" opacity="0.15"/>'
            f'<rect x="-34" y="-100" width="30" height="100" rx="12" fill="{pants}" stroke="{ink}" stroke-width="4"/>'
            f'<rect x="4" y="-100" width="30" height="100" rx="12" fill="{pants}" stroke="{ink}" stroke-width="4"/>'
            f'<rect x="-52" y="-182" width="104" height="104" rx="26" fill="{shirt}" stroke="{ink}" stroke-width="4"/>'
            f'<line x1="-48" y1="-160" x2="-78" y2="{aw + 20:.0f}" stroke="{shirt}" stroke-width="26" stroke-linecap="round"/>'
            f'<line x1="48" y1="-160" x2="78" y2="{aw + 20:.0f}" stroke="{shirt}" stroke-width="26" stroke-linecap="round"/>'
            f'<circle cx="-78" cy="{aw + 14:.0f}" r="15" fill="#F2C6A0" stroke="{ink}" stroke-width="3"/><circle cx="78" cy="{aw + 14:.0f}" r="15" fill="#F2C6A0" stroke="{ink}" stroke-width="3"/>'
            f'<circle cx="0" cy="-222" r="50" fill="#F2C6A0" stroke="{ink}" stroke-width="4"/>'
            f'<path d="M-52 -230 Q-40 -282 0 -280 Q44 -282 52 -230 Q30 -252 0 -250 Q-28 -252 -52 -230 Z" fill="{hair}" stroke="{ink}" stroke-width="4"/>'
            f'{face}</g>')


def bubble(x, y, w, h, inner, tail=(0, 60), op=1.0):
    return (f'<g opacity="{op:.2f}" transform="translate({x},{y})">'
            f'<path d="M{-w / 2 + 30} {-h / 2} H{w / 2 - 30} Q{w / 2} {-h / 2} {w / 2} {-h / 2 + 30} V{h / 2 - 30} Q{w / 2} {h / 2} {w / 2 - 30} {h / 2} '
            f'H{tail[0] + 30} L{tail[0]} {h / 2 + tail[1]} L{tail[0] - 10} {h / 2} H{-w / 2 + 30} Q{-w / 2} {h / 2} {-w / 2} {h / 2 - 30} V{-h / 2 + 30} Q{-w / 2} {-h / 2} {-w / 2 + 30} {-h / 2} Z" '
            f'fill="#FFFFFF" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>{inner}</g>')


def fish_icon(s=1.0, c="#7FB5D8"):
    return (f'<g transform="scale({s})"><ellipse cx="0" cy="0" rx="40" ry="22" fill="{c}" stroke="{INK}" stroke-width="4"/>'
            f'<polygon points="36,0 64,-20 64,20" fill="{c}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<circle cx="-20" cy="-5" r="4" fill="{INK}"/></g>')


def delivery_box(open_amt=0.0, content=1.0):
    """Caixa de entregas (cerca de 190x150), centrada na base. open_amt 0 fechada, 1 aberta."""
    lid = 1 - open_amt
    out = (f'<rect x="-95" y="-150" width="190" height="150" rx="10" fill="#E8A55A" stroke="{INK}" stroke-width="6"/>'
           f'<rect x="-95" y="-150" width="190" height="34" fill="#D18B3C" stroke="{INK}" stroke-width="6"/>')
    if open_amt > 0.1:
        out += f'<rect x="-82" y="-116" width="164" height="100" fill="#8A5A2E"/>'
        if content > 0.05:
            out += f'<g transform="translate(0,{-62:.0f}) scale({content:.2f})">{fish_icon(1.2)}</g>'
        out += (f'<g transform="translate(-95,-150) rotate({-100 * open_amt:.0f})"><rect x="0" y="-26" width="190" height="30" rx="8" '
                f'fill="#E8A55A" stroke="{INK}" stroke-width="6"/></g>')
    else:
        out += f'<rect x="-95" y="-176" width="190" height="30" rx="8" fill="#E8A55A" stroke="{INK}" stroke-width="6"/>'
        out += f'<g transform="translate(0,-70)">{fish_icon(0.9, "#FFFFFF")}</g>'
    return out


def smell(t, x, y, op=1.0):
    out = ""
    for i in range(3):
        u = (t * 0.8 + i / 3) % 1
        out += (f'<path d="M{x + (i - 1) * 40} {y - u * 90:.0f} q 14 -20 0 -40 q -14 -20 0 -40" fill="none" stroke="#9AD0A0" '
                f'stroke-width="7" stroke-linecap="round" opacity="{math.sin(math.pi * u) * op:.2f}"/>')
    return out


def mug(fill=1.0, s=1.0):
    return (f'<g transform="scale({s})"><path d="M-44 -78 H44 V-14 Q44 0 30 0 H-30 Q-44 0 -44 -14 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<rect x="-38" y="{-78 + (1 - fill) * 56:.0f}" width="76" height="{56 * fill + 6:.0f}" fill="#7A4A2A" opacity="0.95"/>'
            f'<path d="M44 -62 Q78 -62 74 -38 Q70 -20 44 -24" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/></g>')


def steam(t, x, y, n=3, s=1.0):
    out = ""
    for i in range(n):
        u = (t * 0.9 + i / n) % 1
        out += (f'<path d="M{x + (i - 1) * 24 * s:.0f} {y - u * 70 * s:.0f} q {10 * s:.0f} {-16 * s:.0f} 0 {-30 * s:.0f}" fill="none" stroke="#FFFFFF" '
                f'stroke-width="6" stroke-linecap="round" opacity="{math.sin(math.pi * u) * 0.8:.2f}"/>')
    return out


def trophy(glow=1.0):
    return (f'<circle cx="0" cy="-70" r="{90 * glow:.0f}" fill="#FFF3B0" opacity="0.28"/>'
            f'<path d="M-46 -140 H46 V-96 Q46 -60 0 -52 Q-46 -60 -46 -96 Z" fill="#F6C343" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M-46 -128 Q-80 -128 -76 -104 Q-72 -84 -48 -86 M46 -128 Q80 -128 76 -104 Q72 -84 48 -86" fill="none" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="-12" y="-54" width="24" height="26" fill="#F6C343" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="-40" y="-30" width="80" height="26" rx="6" fill="#E0A82E" stroke="{INK}" stroke-width="5"/>')


def clock(hours, x, y, r=70):
    """Relógio de parede; `hours` em horas (pode ser fracionário)."""
    ah = (hours % 12) / 12 * 2 * math.pi
    am = (hours % 1) * 2 * math.pi
    out = (f'<g transform="translate({x},{y})"><circle r="{r}" fill="#FFF6EA" stroke="{INK}" stroke-width="8"/>')
    for i in range(12):
        a = i / 12 * 2 * math.pi
        out += (f'<line x1="{math.sin(a) * (r - 14):.1f}" y1="{-math.cos(a) * (r - 14):.1f}" x2="{math.sin(a) * (r - 6):.1f}" '
                f'y2="{-math.cos(a) * (r - 6):.1f}" stroke="{INK}" stroke-width="4"/>')
    out += (f'<line x1="0" y1="0" x2="{math.sin(ah) * r * 0.5:.1f}" y2="{-math.cos(ah) * r * 0.5:.1f}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
            f'<line x1="0" y1="0" x2="{math.sin(am) * r * 0.75:.1f}" y2="{-math.cos(am) * r * 0.75:.1f}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<circle r="6" fill="{INK}"/></g>')
    return out


def fuji(x, y, w, h, snow=True):
    out = f'<polygon points="{x},{y + h} {x + w * 0.42},{y} {x + w * 0.58},{y} {x + w},{y + h}" fill="#5B6FA8"/>'
    if snow:
        out += (f'<polygon points="{x + w * 0.32},{y + h * 0.24} {x + w * 0.42},{y} {x + w * 0.58},{y} {x + w * 0.68},{y + h * 0.24} '
                f'{x + w * 0.6},{y + h * 0.2} {x + w * 0.54},{y + h * 0.28} {x + w * 0.47},{y + h * 0.2} {x + w * 0.4},{y + h * 0.28}" fill="#FFFFFF"/>')
    return out


def poster(x, y, w=360, h=480):
    return (f'<g transform="translate({x},{y})"><rect width="{w}" height="{h}" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="14" y="14" width="{w - 28}" height="{h - 28}" fill="#FDD9B5"/><circle cx="{w * 0.62}" cy="{h * 0.3}" r="46" fill="#F26B5B"/>'
            + fuji(30, h * 0.4, w - 60, h * 0.42) +
            f'<rect x="14" y="{h * 0.82}" width="{w - 28}" height="{h * 0.18 - 14}" fill="#7FBF8E"/>'
            f'<circle cx="70" cy="{h * 0.22}" r="14" fill="#F7B6C8"/><circle cx="100" cy="{h * 0.3}" r="10" fill="#F7B6C8"/><circle cx="60" cy="{h * 0.34}" r="11" fill="#F7B6C8"/></g>')


def torii(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<rect x="-230" y="-380" width="460" height="40" rx="10" fill="#2B2B2B"/>'
            '<rect x="-210" y="-345" width="420" height="34" fill="#D8343A"/>'
            '<rect x="-190" y="-280" width="380" height="26" fill="#D8343A"/>'
            '<rect x="-170" y="-345" width="40" height="345" fill="#D8343A"/><rect x="130" y="-345" width="40" height="345" fill="#D8343A"/>'
            '<rect x="-180" y="-20" width="60" height="20" fill="#2B2B2B"/><rect x="120" y="-20" width="60" height="20" fill="#2B2B2B"/></g>')


def sunrise_sky(u):
    """u 0..1: o sol sobe atrás do Fuji."""
    sun_y = 760 - 330 * ease(u)
    return (f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6C5CE7"/>'
            f'<stop offset="0.6" stop-color="#FD9A8C"/><stop offset="1" stop-color="#FFD39A"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
            f'<circle cx="1300" cy="{sun_y:.0f}" r="120" fill="#FFE8A3" opacity="0.95"/>' + fuji(380, 330, 1160, 520) +
            '<rect x="0" y="830" width="1920" height="250" fill="#3E7D5A"/><rect x="0" y="830" width="1920" height="20" fill="#4E9A6E"/>')
