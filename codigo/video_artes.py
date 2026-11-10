"""'O Mochi tentou 3 artes' (1920x1080, 24 fps, 90 s). Sem falas: conta-se com animação.

casa (0-10) | pintura (10-30) | música (30-50) | barro (50-70) | quadro vendido (70-84) | cartão (84-90)
"""
import math
import os
import subprocess
from mochi_kit import MOCHI_VF
import sys
from multiprocessing import Pool

import cairosvg

from mochi_longo import (H, W, FPS, FONT, INK, M, bulb, burst, caption, clamp, ease, ease_out, fade, lerp, sparkle,
                         spring, stamp, walk_bob, zzz, petals)
from tempos_artes import *  # noqa: F401,F403
from video_trabalhos import room_bg

VAQUINHA = "gofund.me/5d9e87b27"
CUTS = [T["e1"], T["e2"], T["e3"], T["fim"]]
COLS = ["#D8343A", "#3F6FB0", "#F6C343", "#4EA66A"]
CLAY = "#A8723F"


def meow(t):
    for t0 in MEOWS:
        if t0 <= t <= t0 + 0.55:
            return max(0.0, math.sin(math.pi * (t - t0) / 0.55)) ** 0.8
    return 0.0


def dip(t):
    op = 0.0
    for c in CUTS:
        if c - 0.3 <= t < c + 0.3:
            op = max(op, 1 - abs(t - c) / 0.3)
    if t < 0.6:
        op = max(op, 1 - t / 0.6)
    if t > TOTAL - 1.2:
        op = max(op, ease((t - (TOTAL - 1.2)) / 1.2))
    return f'<rect width="{W}" height="{H}" fill="#1E1B2E" opacity="{op:.2f}"/>' if op > 0.01 else ""


def paw(x, y, col, s=1.0, op=1.0):
    toes = "".join(f'<circle cx="{dx * s:.0f}" cy="{dy * s:.0f}" r="{9 * s:.0f}" fill="{col}"/>'
                   for dx, dy in ((-24, -22), (-8, -34), (8, -34), (24, -22)))
    return (f'<g transform="translate({x:.0f},{y:.0f})" opacity="{op:.2f}"><ellipse cx="0" cy="0" rx="{22 * s:.0f}" ry="{17 * s:.0f}" fill="{col}"/>{toes}</g>')


# ---------- cartões de título ----------
def title_card(lt, n, name, c1, c2, icon):
    if lt >= 2.5:
        return ""
    a = ease(lt / 0.5)
    b = ease((lt - 0.15) / 0.5)
    ic = spring((lt - 0.4) / 1.0) if lt > 0.4 else 0
    op = 1 - ease((lt - 1.9) / 0.6)
    return (f'<g opacity="{op:.2f}"><defs><linearGradient id="tc{n}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#tc{n})"/>'
            f'<g transform="translate({-900 * (1 - min(a, 1)):.0f},0)"><circle cx="380" cy="470" r="150" fill="#FFF6EA" stroke="{INK}" stroke-width="10"/>'
            f'<text x="380" y="530" font-family="{FONT}" font-weight="bold" font-size="190" fill="#D8343A" text-anchor="middle">{n}</text></g>'
            f'<g transform="translate({-900 * (1 - min(b, 1)):.0f},0)"><text x="620" y="440" font-family="{FONT}" font-weight="bold" font-size="76" fill="#FFF6EA" '
            f'stroke="{INK}" stroke-width="3">Arte {n}</text>'
            f'<text x="620" y="570" font-family="{FONT}" font-weight="bold" font-size="120" fill="#FFFFFF" stroke="{INK}" stroke-width="5">{name}</text></g>'
            f'<g transform="translate(1560,520) scale({max(ic, 0.001):.2f})">{icon}</g></g>')


def icon_palette():
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="24" fill="{c}" stroke="{INK}" stroke-width="5"/>'
                   for x, y, c in ((-70, -30, COLS[0]), (-20, -78, COLS[2]), (50, -62, COLS[1]), (80, 0, COLS[3])))
    return (f'<g><path d="M-120 10 Q-130 -110 0 -120 Q130 -120 130 -20 Q130 40 60 30 Q10 24 30 80 Q40 120 -20 118 Q-110 110 -120 10 Z" '
            f'fill="#F3D9B8" stroke="{INK}" stroke-width="8"/>{dots}</g>')


def icon_note():
    return (f'<g transform="scale(1.3)"><ellipse cx="-30" cy="60" rx="46" ry="34" fill="{INK}" transform="rotate(-20 -30 60)"/>'
            f'<rect x="4" y="-110" width="16" height="170" fill="{INK}"/><path d="M20 -110 Q90 -80 80 -10 Q60 -60 20 -60 Z" fill="{INK}"/></g>')


def icon_clay():
    return (f'<g><ellipse cx="0" cy="70" rx="130" ry="50" fill="#8A5B2E" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M-100 60 Q-90 -60 0 -80 Q90 -60 100 60 Z" fill="{CLAY}" stroke="{INK}" stroke-width="8"/>'
            f'<ellipse cx="-30" cy="-5" rx="22" ry="12" fill="#C28F5A"/></g>')


# ---------- casa ----------
def easel_painting():
    out = (f'<g transform="translate(0,0)"><line x1="330" y1="720" x2="260" y2="940" stroke="{INK}" stroke-width="14"/>'
           f'<line x1="470" y1="720" x2="540" y2="940" stroke="{INK}" stroke-width="14"/><line x1="400" y1="700" x2="400" y2="940" stroke="{INK}" stroke-width="12"/>'
           f'<rect x="220" y="260" width="360" height="460" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>')
    out += (f'<path d="M240 520 Q320 340 400 480 T560 400" fill="none" stroke="{COLS[1]}" stroke-width="22" stroke-linecap="round"/>'
            f'<circle cx="480" cy="340" r="44" fill="{COLS[2]}"/><circle cx="300" cy="620" r="40" fill="{COLS[0]}"/>'
            f'<path d="M260 680 Q400 600 540 680" fill="none" stroke="{COLS[3]}" stroke-width="20" stroke-linecap="round"/></g>')
    return out


def s_casa(lt):
    x = 1050.0
    if lt >= 8.0:
        x = lerp(1050, 2250, ease((lt - 8.0) / 2.0))
    moving = lt >= 8.0
    bob, rot = walk_bob(lt, 3.6, 16) if moving else (0, 0)
    hop = 0.0
    if A_BULB <= lt < A_BULB + 0.6:
        hop = -90 * math.sin(math.pi * (lt - A_BULB) / 0.6)
    expr = "happy" if lt >= A_BULB else "normal"
    out = room_bg() + easel_painting()
    if lt >= 3.0:
        out += sparkle(300, 300, 1.0 + 0.2 * math.sin(lt * 6), 0.9) + sparkle(540, 560, 0.9, 0.8)
    out += M(lt, x, 935 + bob + hop, 1.6, expr, rot=rot, mouth=meow(lt), flip=-1 if lt < 8.0 else 1)
    if A_BULB <= lt < A_BULB + 3.0:
        out += bulb(x, 330, 1.0, ease((lt - A_BULB) / 0.2) * (1 - ease((lt - (A_BULB + 2.5)) / 0.5)))
    out += caption(fade(lt, 6.0, 9.4), "Vou ser artista!")
    return out


# ---------- atelier (pintura e barro) ----------
def atelier(lt, wall="#FBEFD9"):
    out = f'<rect width="{W}" height="{H}" fill="{wall}"/><rect y="860" width="{W}" height="{H - 860}" fill="#D9B48B"/><rect y="850" width="{W}" height="16" fill="#B8864F"/>'
    out += (f'<rect x="1380" y="140" width="320" height="380" fill="#CFE8F5" stroke="{INK}" stroke-width="8"/>'
            f'<line x1="1540" y1="140" x2="1540" y2="520" stroke="{INK}" stroke-width="6"/><line x1="1380" y1="330" x2="1700" y2="330" stroke="{INK}" stroke-width="6"/>')
    return out


def can(x, col):
    return (f'<g transform="translate({x},945)"><rect x="-46" y="-84" width="92" height="84" rx="8" fill="#E9E9EE" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="-46" y="-56" width="92" height="30" fill="{col}" opacity="0.9"/><ellipse cx="0" cy="-84" rx="46" ry="14" fill="{col}" stroke="{INK}" stroke-width="4"/></g>')


def mx_paint(lt):
    if lt < 2.5:
        return lerp(-150, 800, ease(lt / 2.5))
    if lt < P_WALK[0]:
        return 800.0
    if lt < P_WALK[1]:
        return lerp(800, 1600, ease((lt - P_WALK[0]) / (P_WALK[1] - P_WALK[0])))
    return 1600.0


def s_e1(lt):
    out = atelier(lt)
    out += '<polygon points="1090,880 1800,880 1860,1040 1020,1040" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="6"/>'
    out += can(960, COLS[0]) + can(1020, COLS[1])
    # pegadas persistentes (na tela e no chão)
    for k in range(15):
        tk = P_WALK[0] + 0.55 * k
        if lt >= tk:
            xk = mx_paint(tk)
            out += paw(xk + (22 if k % 2 else -22), 975 + (k % 2) * 22, COLS[k % 4], 1.1)
    for j in range(8):
        tj = P_SPIN[0] + 0.2 * j
        if lt >= tj:
            a = j * 0.9
            out += paw(1400 + 150 * math.cos(a), 960 + 38 * math.sin(a), COLS[(j + 1) % 4], 1.2)
    x, y, rot, expr = mx_paint(lt), 935.0, 0.0, "normal"
    if lt < 2.5:
        bob, rot = walk_bob(lt, 3.4, 14)
        y += bob
    elif P_WALK[0] <= lt < P_WALK[1]:
        bob, rot = walk_bob(lt, 3.4, 12)
        y += bob
        expr = "happy"
    if P_DIP <= lt < P_DIP + 1.2:
        rot = 10 * math.sin(math.pi * (lt - P_DIP) / 1.2)
    if P_SPIN[0] <= lt < P_SPIN[1]:
        u = ease((lt - P_SPIN[0]) / (P_SPIN[1] - P_SPIN[0]))
        rot = 360 * u
        y -= 30 * math.sin(math.pi * u)
        expr = "shock"
    if lt >= P_SPIN[1]:
        expr = "sad"
    out += M(lt, x, y, 1.6, expr, rot=rot, mouth=meow(T["e1"] + lt))
    if lt >= P_DIP + 0.9:   # patas pintadas
        c = COLS[int(max(0, lt - P_WALK[0]) / 2) % 4] if lt >= P_WALK[0] else COLS[0]
        out += (f'<ellipse cx="{x - 62:.0f}" cy="{y - 6:.0f}" rx="40" ry="20" fill="{c}" opacity="0.9"/>'
                f'<ellipse cx="{x + 62:.0f}" cy="{y - 6:.0f}" rx="40" ry="20" fill="{c}" opacity="0.9"/>') if not (P_SPIN[0] <= lt < P_SPIN[1]) else ""
    out += burst(fade(lt, P_DIP + 0.9, P_DIP + 1.8, 0.05, 0.4), 900, 620, "PLOP!", 90, color="#3F6FB0", r=140, rot=-6)
    out += caption(fade(lt, P_DIP + 1.2, P_WALK[0] + 4.0), "Pintar com as patas")
    out += caption(fade(lt, 13.6, P_STAMP - 0.4), "Pegadas. Muitas pegadas.")
    out += stamp(lt, P_STAMP, "SÓ PEGADAS", 960, 420, 118)
    out += title_card(lt, 1, "Pintura", "#F7B6C8", "#D8657F", icon_palette())
    return out


# ---------- música ----------
def piano(pressed):
    out = (f'<rect x="560" y="300" width="1000" height="540" rx="34" fill="#3B2A2F" stroke="{INK}" stroke-width="8"/>'
           f'<rect x="600" y="340" width="920" height="440" rx="20" fill="#4A353B"/>'
           f'<rect x="900" y="380" width="320" height="220" rx="10" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>')
    for i in range(5):
        out += f'<line x1="925" y1="{420 + i * 30}" x2="1195" y2="{420 + i * 30}" stroke="#8A8FA3" stroke-width="3"/>'
    out += f'<circle cx="980" cy="{412 + 30}" r="9" fill="{INK}"/><circle cx="1060" cy="{412 + 60}" r="9" fill="{INK}"/><circle cx="1140" cy="{412 + 30}" r="9" fill="{INK}"/>'
    out += f'<rect x="580" y="820" width="960" height="40" rx="10" fill="#2B1D21"/>'
    return out


def keys(pressed):
    out = ""
    for i in range(13):
        dy = 8 if i == pressed else 0
        out += (f'<rect x="{610 + i * 70}" y="{846 + dy}" width="66" height="{120 - dy}" rx="8" fill="{"#D8D8E4" if i == pressed else "#FFFFFF"}" stroke="{INK}" stroke-width="4"/>')
    for i in (0, 1, 3, 4, 5, 7, 8, 10, 11):
        out += f'<rect x="{610 + i * 70 + 48}" y="846" width="42" height="70" rx="6" fill="{INK}"/>'
    return out


def mx_piano(lt):
    if lt < 2.5:
        return lerp(-150, 700, ease(lt / 2.5))
    if lt < M_WALK[0]:
        return 700.0
    if lt < M_WALK[1]:
        return lerp(700, 1440, (lt - M_WALK[0]) / (M_WALK[1] - M_WALK[0]))
    if lt < M_BACK[0]:
        return 1440.0
    if lt < M_BACK[1]:
        return lerp(1440, 1100, ease((lt - M_BACK[0]) / (M_BACK[1] - M_BACK[0])))
    return 1100.0


def s_e2(lt):
    out = f'<rect width="{W}" height="{H}" fill="#E9E0F5"/><rect y="900" width="{W}" height="{H - 900}" fill="#BBA9D8"/>'
    out += (f'<rect x="140" y="160" width="320" height="380" fill="#CFE8F5" stroke="{INK}" stroke-width="8"/><line x1="300" y1="160" x2="300" y2="540" stroke="{INK}" stroke-width="6"/>')
    x = mx_piano(lt)
    y, rot, expr, sx, sy = 848.0, 0.0, "normal", 1.0, 1.0
    if lt < 2.5:
        y = 945
        bob, rot = walk_bob(lt, 3.4, 14)
        y += bob
    elif lt < M_WALK[0]:
        y = 848 - 160 * (1 - ease((lt - 2.5) / 1.0)) * 0 + 0
        y = lerp(945, 848, ease((lt - 2.7) / 0.8))
    elif lt < M_WALK[1]:
        bob, rot = walk_bob(lt, 2.0, 16)
        y += bob
        expr = "happy"
    elif lt < M_LIE:
        expr = "sad"
    else:
        u = ease((lt - M_LIE) / 1.0)
        sy, sx = lerp(1.0, 0.72, u), lerp(1.0, 1.15, u)
        expr = "sleep" if lt >= M_SLEEP else "normal"
    pressed = -1
    if M_WALK[0] <= lt < M_WALK[1]:
        pressed = int((x - 610) / 70)
    out += piano(pressed) + keys(pressed)
    out += M(lt, x, y, 1.6, expr, rot=rot, sx=sx, sy=sy, mouth=meow(T["e2"] + lt))
    if M_WALK[0] <= lt < M_WALK[1]:   # notas a saltar
        i = int((lt - M_WALK[0]) / 0.5)
        u = ((lt - M_WALK[0]) % 0.5) / 0.5
        out += (f'<text x="{x + 120:.0f}" y="{700 - 120 * u:.0f}" font-family="{FONT}" font-weight="bold" font-size="70" fill="{COLS[i % 4]}" '
                f'opacity="{1 - u:.2f}" stroke="{INK}" stroke-width="2">{"♪♫"[i % 2]}</text>')
    if lt >= M_SLEEP:
        out += zzz(lt, x + 110, y - 300)
    out += burst(fade(lt, M_WALK[1], M_WALK[1] + 1.0, 0.05, 0.4), 1330, 520, "BLONC!", 90, color="#6B4FB5", r=150, rot=6)
    out += caption(fade(lt, 3.2, 6.5), "Vou tocar piano")
    out += caption(fade(lt, M_WALK[1] + 0.2, M_BACK[1] + 0.2), "Isto não soa bem")
    out += caption(fade(lt, 13.6, M_STAMP - 0.4), "Mas é uma ótima cama")
    out += stamp(lt, M_STAMP, "SÓ RUÍDO", 960, 420, 118)
    out += title_card(lt, 2, "Música", "#B7A2E0", "#6B4FB5", icon_note())
    return out


# ---------- barro ----------
SPLATS = [(260, 250), (540, 180), (760, 340), (430, 470), (150, 520), (680, 560), (900, 220), (330, 380), (820, 480), (1040, 300)]


def s_e3(lt):
    out = atelier(lt, "#EDE6DA")
    # mesa
    out += (f'<rect x="1100" y="700" width="480" height="28" rx="8" fill="#B8864F" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="1130" y="728" width="26" height="212" fill="#8A6A3A"/><rect x="1524" y="728" width="26" height="212" fill="#8A6A3A"/>')
    # salpicos na parede (persistentes)
    for j, (sx_, sy_) in enumerate(SPLATS):
        t0 = C_FLY + 0.35 * j + 0.5
        if lt >= t0:
            out += f'<ellipse cx="{sx_}" cy="{sy_}" rx="{34 + (j % 3) * 8}" ry="{26 + (j % 2) * 8}" fill="{CLAY}" stroke="#7A4F26" stroke-width="3"/>'
    # barro na mesa
    n = sum(1 for q in C_SQ if lt >= q)
    wx, wy = 1.0 + 0.28 * n, 1.0 - 0.2 * n
    for q in C_SQ:
        if q <= lt < q + 0.3:
            k = (lt - q) / 0.3
            wx += 0.12 * math.sin(math.pi * k)
            wy -= 0.15 * math.sin(math.pi * k)
    out += f'<ellipse cx="1340" cy="{700 - 70 * wy:.0f}" rx="{90 * wx:.0f}" ry="{70 * wy:.0f}" fill="{CLAY}" stroke="#7A4F26" stroke-width="6"/>'
    x, y, rot, expr = 1000.0, 935.0, 0.0, "normal"
    if lt < 2.5:
        x = lerp(-150, 1000, ease(lt / 2.5))
        bob, rot = walk_bob(lt, 3.4, 14)
        y += bob
    for q in C_SQ:
        if q - 0.3 <= lt < q + 0.4:
            rot = 16 * math.sin(math.pi * (lt - (q - 0.3)) / 0.7)
            expr = "angry"
    if lt >= C_SQ[-1] + 0.5 and lt < C_FLY + 4.0:
        rot = 10 * math.sin(lt * 18) if lt >= C_FLY else rot
        expr = "shock"
    if lt >= C_FLY + 4.0:
        expr = "sad"
    out += M(lt, x, y, 1.6, expr, rot=rot, mouth=meow(T["e3"] + lt),
             extra="".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{CLAY}" stroke="#7A4F26" stroke-width="3"/>'
                           for cx, cy, rx, ry in ((120, 170, 26, 20), (250, 160, 22, 18), (190, 300, 30, 22), (110, 300, 22, 18), (265, 290, 24, 20)))
             if lt >= C_FLY + 3.0 else "")
    if lt >= C_SQ[-1] + 0.6:   # barro colado às patas
        out += (f'<ellipse cx="{x + 92:.0f}" cy="{y - 205:.0f}" rx="40" ry="30" fill="{CLAY}" stroke="#7A4F26" stroke-width="4"/>'
                f'<ellipse cx="{x + 50:.0f}" cy="{y - 175:.0f}" rx="30" ry="24" fill="{CLAY}" stroke="#7A4F26" stroke-width="4"/>')
    for j, (sx_, sy_) in enumerate(SPLATS):   # barro a voar
        t0 = C_FLY + 0.35 * j
        if t0 <= lt < t0 + 0.5:
            u = (lt - t0) / 0.5
            fx = lerp(x + 90, sx_, u)
            fy = lerp(y - 200, sy_, u) - 120 * math.sin(math.pi * u)
            out += f'<ellipse cx="{fx:.0f}" cy="{fy:.0f}" rx="30" ry="24" fill="{CLAY}" stroke="#7A4F26" stroke-width="4"/>'
    for q, word in zip(C_SQ, ("PAF!", "PLOF!", "SPLAT!")):
        out += burst(fade(lt, q, q + 0.9, 0.05, 0.4), 1340, 420, word, 84, color="#7A4F26", r=140, rot=-5)
    out += caption(fade(lt, 2.8, C_SQ[0] + 1.0), "Escultura em barro")
    out += caption(fade(lt, C_FLY + 3.6, C_STAMP - 0.4), "O barro colou-se a tudo")
    out += stamp(lt, C_STAMP, "SÓ BARRO", 960, 420, 118)
    out += title_card(lt, 3, "Barro", "#E0B58A", "#A8723F", icon_clay())
    return out


# ---------- final ----------
def framed(cx, cy, scale=1.0):
    out = (f'<g transform="translate({cx:.0f},{cy:.0f}) scale({scale})"><rect x="-230" y="-290" width="460" height="580" rx="10" fill="#E0A82E" stroke="{INK}" stroke-width="8"/>'
           f'<rect x="-200" y="-260" width="400" height="520" fill="#FFFFFF" stroke="#B8862A" stroke-width="5"/>')
    for k in range(14):
        out += paw(-140 + (k % 4) * 90 + (k // 4) * 14, -190 + (k // 4) * 120 + (k % 2) * 20, COLS[k % 4], 1.4)
    return out + '</g>'


def s_fim(lt):
    t = T["fim"] + lt
    out = room_bg() + petals(lt, 10, 0.5)
    fy = None
    if lt >= F_FRAME:
        u = clamp((lt - F_FRAME) / 1.0)
        fy = lerp(-320, 330, ease_out(u))
        out += framed(960, fy)
        if u >= 1:
            out += sparkle(720, 120, 1.2 + 0.3 * math.sin(lt * 6), 0.9) + sparkle(1220, 160, 1.0, 0.8) + sparkle(1180, 520, 0.8, 0.7)
    if lt >= F_SOLD:
        u = ease((lt - F_SOLD) / 0.3)
        out += (f'<g transform="translate(1160,150) rotate(-10) scale({0.4 + 0.6 * u:.2f})"><rect x="-130" y="-42" width="260" height="84" rx="42" fill="#D8343A" stroke="{INK}" stroke-width="6"/>'
                f'<text x="0" y="16" font-family="{FONT}" font-weight="bold" font-size="52" fill="#FFFFFF" text-anchor="middle">VENDIDO</text></g>')
    expr = "sad"
    hop = 0.0
    sy, sx = 1.0, 1.0
    if lt >= F_FRAME:
        expr = "normal"
    if lt >= F_SOLD - 0.2:
        expr = "happy"
        if lt < F_SOLD + 0.6:
            hop = -80 * math.sin(math.pi * (lt - (F_SOLD - 0.2)) / 0.8) if lt < F_SOLD + 0.6 else 0
    if lt >= F_SLEEP:
        expr = "sleep"
        u = ease((lt - F_SLEEP) / 1.0)
        sy, sx = lerp(1.0, 0.76, u), lerp(1.0, 1.15, u)
    out += f'<ellipse cx="960" cy="948" rx="330" ry="26" fill="#C8553D" opacity="0.5"/>'
    out += M(t, 960, 940 + hop, 1.6, expr, sx=sx, sy=sy, mouth=meow(t))
    if lt >= F_SLEEP:
        out += zzz(lt, 1080, 640)
    out += burst(fade(lt, F_SOLD, F_SOLD + 1.2, 0.05, 0.5), 1500, 360, "VENDIDO!", 84, color="#D8343A", r=150, rot=8)
    out += caption(fade(lt, 1.2, 5.4), "3 artes. 0 obras.")
    out += caption(fade(lt, F_FRAME + 0.6, F_SOLD - 0.1), "Obra-prima!")
    out += caption(fade(lt, F_SLEEP + 0.8, 13.8), "E o Mochi nem percebeu")
    if t >= T["cartao"]:
        op = ease((t - T["cartao"]) / 0.6)
        out += (f'<g opacity="{op:.2f}"><rect width="{W}" height="{H}" fill="#1E1B2E" opacity="0.88"/>'
                f'<text x="960" y="360" font-family="{FONT}" font-weight="bold" font-size="96" fill="#FFF6EA" text-anchor="middle">Ajuda o Mochi</text>'
                f'<text x="960" y="470" font-family="{FONT}" font-weight="bold" font-size="80" fill="#F6C343" text-anchor="middle">a chegar ao Japão</text>'
                f'<rect x="560" y="550" width="800" height="112" rx="56" fill="#D8343A"/>'
                f'<text x="960" y="628" font-family="{FONT}" font-weight="bold" font-size="58" fill="#FFFFFF" text-anchor="middle">{VAQUINHA}</text>'
                f'<text x="960" y="760" font-family="{FONT}" font-size="50" fill="#FFF6EA" text-anchor="middle">Link na descrição</text></g>')
        out += M(t, 1650, 1040, 1.1, "happy", op=op, mouth=meow(t))
    return out


def frame_svg(t):
    if t < T["e1"]:
        body = s_casa(t)
    elif t < T["e2"]:
        body = s_e1(t - T["e1"])
    elif t < T["e3"]:
        body = s_e2(t - T["e2"])
    elif t < T["fim"]:
        body = s_e3(t - T["e3"])
    else:
        body = s_fim(t - T["fim"])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="#FDE7D3"/>{body}{dip(t)}</svg>')


DIR = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(DIR, "frames_artes")


def render_one(n):
    p = os.path.join(FRAMES, f"f{n:05d}.png")
    if not os.path.exists(p):
        cairosvg.svg2png(bytestring=frame_svg(n / FPS).encode(), write_to=p)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "render":
        for s in sys.argv[1:]:
            cairosvg.svg2png(bytestring=frame_svg(float(s)).encode(), write_to=os.path.join(DIR, f"prev_art_{s}.png"))
        sys.exit()
    os.makedirs(FRAMES, exist_ok=True)
    with Pool(2) as pool:
        pool.map(render_one, range(int(FPS * TOTAL)), chunksize=48)
    out = os.path.join(DIR, "mochi_artes.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(FRAMES, "f%05d.png"),
                    "-i", os.path.join(DIR, "musica_artes.wav"), "-vf", MOCHI_VF, "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out)
