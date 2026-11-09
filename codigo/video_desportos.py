"""'O Mochi tentou 3 desportos' (1920x1080, 24 fps, 90 s). Sem falas: conta-se com animação.

casa (0-10) | natação (10-30) | futebol (30-50) | ginásio (50-70) | medalha de sesta (70-84) | cartão (84-90)
Versão em chinês: MOCHI_LANG=zh python3 video_desportos.py render  ->  mochi_desportos_zh.mp4
"""
import math
import os
import subprocess
import sys
from multiprocessing import Pool

import cairosvg

from mochi_longo import (LANG, tr, H, W, FPS, FONT, INK, M, bulb, burst, caption, clamp, ease, ease_out, fade, lerp, sparkle,
                         spring, stamp, walk_bob, zzz, petals)
from mochi_props import moth
from tempos_desportos import *  # noqa: F401,F403
from video_trabalhos import room_bg

VAQUINHA = "gofund.me/5d9e87b27"
CUTS = [T["e1"], T["e2"], T["e3"], T["fim"]]
SWIM_CAP = ('<path d="M104 130 Q190 30 276 130 Q190 112 104 130 Z" fill="#4FA3D9" stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round"/>'
            '<path d="M150 60 Q190 40 230 60" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>')


def meow(t):
    for t0 in MEOWS:
        if t0 <= t <= t0 + 0.55:
            return max(0.0, math.sin(math.pi * (t - t0) / 0.55)) ** 0.8
    return 0.0


def medal(s=1.0, glow=1.0):
    return (f'<g transform="scale({s})"><circle cx="0" cy="0" r="{90 * glow:.0f}" fill="#FFF3B0" opacity="0.25"/>'
            f'<polygon points="-42,-130 -10,-130 16,-30 -18,-30" fill="#D8343A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<polygon points="42,-130 10,-130 -16,-30 18,-30" fill="#3F6FB0" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<circle cx="0" cy="0" r="50" fill="#F6C343" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="0" cy="0" r="36" fill="none" stroke="#E0A82E" stroke-width="5"/>'
            f'<text x="0" y="20" font-family="{FONT}" font-weight="bold" font-size="56" fill="#B8862A" text-anchor="middle">1</text></g>')


def title_card(lt, n, name, c1, c2, icon):
    """Cartão de título que desliza e sai com fade (0 a 2.5 s)."""
    if lt >= 2.5:
        return ""
    a = ease(lt / 0.5)
    b = ease((lt - 0.15) / 0.5)
    ic = spring((lt - 0.4) / 1.0) if lt > 0.4 else 0
    op = 1 - ease((lt - 1.9) / 0.6)
    label = ("运动" + str(n)) if LANG == "zh" else ("Desporto " + str(n))
    return (f'<g opacity="{op:.2f}"><defs><linearGradient id="tc{n}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#tc{n})"/>'
            f'<g transform="translate({-900 * (1 - min(a, 1)):.0f},0)"><circle cx="380" cy="470" r="150" fill="#FFF6EA" stroke="{INK}" stroke-width="10"/>'
            f'<text x="380" y="530" font-family="{FONT}" font-weight="bold" font-size="190" fill="#D8343A" text-anchor="middle">{n}</text></g>'
            f'<g transform="translate({-900 * (1 - min(b, 1)):.0f},0)"><text x="620" y="440" font-family="{FONT}" font-weight="bold" font-size="76" fill="#FFF6EA" '
            f'stroke="{INK}" stroke-width="3">{label}</text>'
            f'<text x="620" y="570" font-family="{FONT}" font-weight="bold" font-size="120" fill="#FFFFFF" stroke="{INK}" stroke-width="5">{tr(name)}</text></g>'
            f'<g transform="translate(1560,520) scale({max(ic, 0.001):.2f})">{icon}</g></g>')


def icon_swim():
    return ('<g><circle cx="0" cy="0" r="90" fill="#FFF6EA" stroke="#2B2B2B" stroke-width="10"/><circle cx="0" cy="0" r="48" fill="#4FA3D9" stroke="#2B2B2B" stroke-width="8"/>'
            '<path d="M-150 120 Q-110 90 -70 120 T10 120 T90 120 T170 120" fill="none" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round"/></g>')


def ball(rot=0.0, r=48):
    pts = ""
    for i in range(5):
        a = math.radians(i * 72 - 90)
        pts += f"{math.cos(a) * r * 0.42:.1f},{math.sin(a) * r * 0.42:.1f} "
    return (f'<g transform="rotate({rot:.0f})"><circle r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
            f'<polygon points="{pts}" fill="{INK}"/>'
            + "".join(f'<line x1="{math.cos(math.radians(i * 72 - 90)) * r * 0.42:.1f}" y1="{math.sin(math.radians(i * 72 - 90)) * r * 0.42:.1f}" '
                      f'x2="{math.cos(math.radians(i * 72 - 90)) * r * 0.95:.1f}" y2="{math.sin(math.radians(i * 72 - 90)) * r * 0.95:.1f}" stroke="{INK}" stroke-width="4"/>'
                      for i in range(5)) + '</g>')


def icon_ball():
    return f'<g transform="scale(3.2)">{ball(0, 48)}</g>'


def dumbbell(w=330, plate=90):
    return (f'<rect x="{-w / 2:.0f}" y="-14" width="{w}" height="28" rx="8" fill="#8A8FA3" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{-w / 2 - 14:.0f}" y="{-plate:.0f}" width="36" height="{plate * 2}" rx="12" fill="#3B3F54" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{w / 2 - 22:.0f}" y="{-plate:.0f}" width="36" height="{plate * 2}" rx="12" fill="#3B3F54" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{-w / 2 + 28:.0f}" y="{-plate * 0.7:.0f}" width="26" height="{plate * 1.4:.0f}" rx="10" fill="#555A73" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{w / 2 - 54:.0f}" y="{-plate * 0.7:.0f}" width="26" height="{plate * 1.4:.0f}" rx="10" fill="#555A73" stroke="{INK}" stroke-width="5"/>')


def icon_dumb():
    return f'<g transform="translate(0,0) scale(1.2) rotate(-20)">{dumbbell(260, 80)}</g>'


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


# ---------- casa ----------
def tv(lt):
    out = ('<rect x="230" y="260" width="520" height="330" rx="22" fill="#2B2B2B"/><rect x="254" y="284" width="472" height="282" rx="10" fill="#9CC9E8"/>'
           '<rect x="440" y="590" width="100" height="60" fill="#2B2B2B"/><rect x="380" y="640" width="220" height="24" rx="10" fill="#2B2B2B"/>')
    if lt >= D_MEDAL:
        u = spring((lt - D_MEDAL) / 1.2)
        out += f'<g transform="translate(490,420) scale({max(u, 0.01) * 0.9:.2f})">{medal()}</g>'
        out += sparkle(330, 330, 1.0 + 0.2 * math.sin(lt * 6), 0.9) + sparkle(660, 500, 0.9, 0.8)
    else:
        out += ('<path d="M254 500 Q380 430 480 500 T726 470 L726 566 L254 566 Z" fill="#7FC28F"/>'
                '<circle cx="640" cy="350" r="34" fill="#FFF3B0"/>')
    return out


def s_casa(lt):
    x = 1050.0
    if lt >= 8.0:
        x = lerp(1050, 2250, ease((lt - 8.0) / 2.0))
    moving = lt >= 8.0
    bob, rot = walk_bob(lt, 3.6, 16) if moving else (0, 0)
    hop = 0.0
    if D_BULB <= lt < D_BULB + 0.6:
        hop = -90 * math.sin(math.pi * (lt - D_BULB) / 0.6)
    expr = "happy" if lt >= D_BULB else "normal"
    out = room_bg() + tv(lt)
    out += M(lt, x, 935 + bob + hop, 1.6, expr, rot=rot, mouth=meow(lt), flip=-1 if lt < 8.0 else 1)
    if D_BULB <= lt < D_BULB + 3.0:
        out += bulb(x, 330, 1.0, ease((lt - D_BULB) / 0.2) * (1 - ease((lt - (D_BULB + 2.5)) / 0.5)))
    out += caption(fade(lt, 6.0, 9.4), "Vou ser campeão!")
    return out


# ---------- natação ----------
WATER_X = 880


def pool_bg(lt):
    out = f'<rect width="{W}" height="{H}" fill="#D8F0F7"/>'
    for i in range(0, W, 120):
        out += f'<line x1="{i}" y1="0" x2="{i}" y2="700" stroke="#BFE3EE" stroke-width="3"/>'
    for j in range(0, 700, 120):
        out += f'<line x1="0" y1="{j}" x2="{W}" y2="{j}" stroke="#BFE3EE" stroke-width="3"/>'
    out += (f'<rect y="860" width="{WATER_X}" height="{H - 860}" fill="#EBDDC8"/><rect y="850" width="{WATER_X}" height="16" fill="#CDB896"/>'
            f'<rect x="{WATER_X}" y="740" width="{W - WATER_X}" height="{H - 740}" fill="#5BB8E8"/>'
            f'<rect x="{WATER_X - 24}" y="740" width="30" height="{H - 740}" fill="#F4F1EA" stroke="{INK}" stroke-width="4"/>')
    for k in range(7):
        wx = WATER_X + 60 + k * 150 + 20 * math.sin(lt * 2 + k)
        out += f'<path d="M{wx:.0f} {800 + (k % 2) * 90} q30 -18 60 0 t60 0" fill="none" stroke="#B4E3FA" stroke-width="7" stroke-linecap="round"/>'
    out += f'<rect x="{WATER_X}" y="736" width="{W - WATER_X}" height="10" fill="#9ADBF8"/>'
    return out


def droplets(lt, t0, x, y, n=14, power=520):
    u = lt - t0
    if not 0 <= u < 1.4:
        return ""
    out = ""
    for i in range(n):
        a = math.radians(200 + i * (140 / (n - 1)))
        vx, vy = math.cos(a) * power * (0.5 + (i % 3) * 0.25), math.sin(a) * power * (0.7 + (i % 4) * 0.2)
        px, py = x + vx * u, y + vy * u + 900 * u * u
        out += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{10 - 4 * u:.1f}" fill="#9ADBF8" stroke="#3F8FBF" stroke-width="2" opacity="{1 - u / 1.4:.2f}"/>'
    return out


def s_e1(lt):
    out = pool_bg(lt)
    y0 = 905
    x, y, rot, expr, sx, sy = 640.0, y0, 0.0, "normal", 1.0, 1.0
    wet = False
    flip = 1
    if lt < 2.5:
        x = lerp(-150, 640, ease(lt / 2.5))
        bob, rot = walk_bob(lt, 3.4, 14)
        y += bob
    elif lt < N_PAW + 1.4:
        if lt >= N_PAW:
            rot = 9 * math.sin(math.pi * (lt - N_PAW) / 1.4)
    elif lt < N_JUMP - 3.0:   # recua
        u = ease((lt - (N_BRR + 0.6)) / 1.0)
        x = lerp(640, 500, u)
        expr = "sad"
    if N_BRR <= lt < N_BRR + 0.9:
        expr = "shock"
        y -= 50 * math.sin(math.pi * (lt - N_BRR) / 0.5) if lt - N_BRR < 0.5 else 0
        x = 640
        rot = -6
    if N_BRR + 0.9 <= lt < N_JUMP - 1.0:
        expr = "sad"
        x = lerp(640, 500, ease((lt - (N_BRR + 0.9)) / 0.8))
    if N_JUMP - 1.0 <= lt < N_JUMP:
        expr = "angry"
        x = 500 + 6 * math.sin(lt * 40)
    if N_JUMP <= lt < N_SPLASH:
        u = (lt - N_JUMP) / (N_SPLASH - N_JUMP)
        x = lerp(500, 1300, u)
        y = lerp(y0, 960, u) - 380 * math.sin(math.pi * u)
        expr = "shock"
        rot = 25 * u
    inwater = N_SPLASH <= lt < N_OUT
    if inwater:
        x = 1300 + 15 * math.sin(lt * 5)
        y = 965 + 14 * math.sin(lt * 7)
        rot = 16 * math.sin(lt * 13)
        expr = "shock"
    if N_OUT <= lt < N_OUT + 1.4:
        u = (lt - N_OUT) / 1.4
        x = lerp(1300, 560, u)
        y = lerp(965, y0, u) - 330 * math.sin(math.pi * u)
        expr = "sad"
        rot = -20 * math.sin(math.pi * u)
    if lt >= N_OUT + 1.4:
        x, y = 560, y0
        expr = "sad"
        wet = True
        sy = 1.0 + 0.03 * math.sin(lt * 30) * max(0, 1 - (lt - N_OUT - 1.4) / 2)
        sx = 1.0 + 0.04 * math.sin(lt * 30 + 1) * max(0, 1 - (lt - N_OUT - 1.4) / 2)
    out += M(lt, x, y, 1.6, expr, rot=rot, sx=sx, sy=sy, extra=SWIM_CAP, mouth=meow(T["e1"] + lt), flip=flip,
             op=1.0 if not inwater else 1.0)
    if inwater:
        out += f'<rect x="{WATER_X}" y="880" width="{W - WATER_X}" height="{H - 880}" fill="#5BB8E8" opacity="0.62"/>'
        for i in range(6):
            u = ((lt * 0.8) + i / 6) % 1
            out += f'<circle cx="{1180 + i * 45 + 14 * math.sin(lt * 4 + i):.0f}" cy="{950 - 260 * u:.0f}" r="{8 + 5 * (i % 3)}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="{math.sin(math.pi * u):.2f}"/>'
    # ondas quando toca na água
    if N_PAW <= lt < N_PAW + 1.4:
        u = (lt - N_PAW) / 1.4
        for k in range(3):
            uu = (u * 1.4 + k * 0.3) % 1
            out += f'<ellipse cx="930" cy="760" rx="{20 + 90 * uu:.0f}" ry="{6 + 20 * uu:.0f}" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="{1 - uu:.2f}"/>'
    out += droplets(lt, N_SPLASH, 1300, 860)
    if wet and lt < N_OUT + 5:
        for i in range(5):
            u = ((lt * 1.6) + i / 5) % 1
            out += f'<circle cx="{x - 110 + i * 55:.0f}" cy="{y - 340 + 330 * u:.0f}" r="9" fill="#9ADBF8" stroke="#3F8FBF" stroke-width="2" opacity="{1 - u:.2f}"/>'
    out += burst(fade(lt, N_BRR, N_BRR + 1.0, 0.1, 0.4), 1080, 330, "BRRR!", 90, color="#3F8FBF", r=150, rot=-8)
    out += burst(fade(lt, N_SPLASH, N_SPLASH + 1.1, 0.1, 0.5), 1300, 620, "SPLASH!", 84, color="#3F8FBF", r=160, rot=6)
    out += caption(fade(lt, N_BRR + 0.9, N_JUMP - 1.2), "Água?!")
    out += caption(fade(lt, N_SPLASH + 0.8, N_OUT - 0.3), "O Mochi não gosta de água")
    out += stamp(lt, N_STAMP, tr("ELIMINADO"), 960, 420, 118)
    out += title_card(lt, 1, "Natação", "#6EC6F0", "#2F7FB8", icon_swim())
    return out


# ---------- futebol ----------
def field_bg(lt):
    out = f'<rect width="{W}" height="{H}" fill="#BEE5F7"/><circle cx="260" cy="170" r="90" fill="#FFF3B0"/>'
    out += '<ellipse cx="1000" cy="200" rx="160" ry="48" fill="#FFFFFF" opacity="0.9"/><ellipse cx="1100" cy="170" rx="100" ry="36" fill="#FFFFFF" opacity="0.9"/>'
    out += f'<rect y="700" width="{W}" height="{H - 700}" fill="#6DBE6A"/>'
    for i in range(8):
        out += f'<rect x="{i * 240}" y="700" width="120" height="{H - 700}" fill="#63B460"/>'
    out += '<rect y="1010" width="1920" height="14" fill="#FFFFFF" opacity="0.7"/>'
    # baliza
    out += (f'<rect x="1560" y="560" width="300" height="320" fill="#FFFFFF" opacity="0.18"/>')
    for i in range(1, 6):
        out += f'<line x1="{1560 + i * 50}" y1="560" x2="{1560 + i * 50}" y2="880" stroke="#FFFFFF" stroke-width="2" opacity="0.7"/>'
    for j in range(1, 6):
        out += f'<line x1="1560" y1="{560 + j * 53}" x2="1860" y2="{560 + j * 53}" stroke="#FFFFFF" stroke-width="2" opacity="0.7"/>'
    out += f'<rect x="1550" y="548" width="320" height="16" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/><rect x="1550" y="548" width="16" height="344" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/><rect x="1854" y="548" width="16" height="344" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
    return out


def moth_pos(lt):
    """Traça: entra por cima, faz uma volta e sai."""
    u = lt - F_MOTH
    if u < 0 or u > 6.0:
        return None
    k = u / 6.0
    mx = 1100 + 380 * math.sin(k * 7.0) - 200 * k
    my = 230 + 420 * ease(min(1, k * 1.2)) * (1 - ease((k - 0.8) / 0.2)) + 60 * math.sin(k * 11) - 300 * ease((k - 0.85) / 0.15)
    return mx, my


def s_e2(lt):
    out = field_bg(lt)
    ground_y = 940
    bx, by = 640.0, 905.0
    ball_rot = 0.0
    if lt >= F_KICK:
        u = clamp((lt - F_KICK) / (F_GOAL - F_KICK))
        bx = lerp(640, 1640, u)
        by = 905 - 120 * abs(math.sin(u * 3 * math.pi)) * (1 - u) ** 1.2
        ball_rot = u * 1500
    mp = moth_pos(lt)
    # Mochi
    x, y, rot, expr, flip = 420.0, ground_y, 0.0, "normal", 1
    if lt < 2.5:
        x = lerp(-150, 420, ease(lt / 2.5))
        bob, rot = walk_bob(lt, 3.4, 14)
        y += bob
    elif lt < F_KICK:
        rot = -10 * ((lt - 2.5) / 0.5)
    elif lt < F_MOTH:
        x = lerp(420, 900, ease((lt - F_KICK) / 3.4))
        bob, rot = walk_bob(lt, 3.2, 12)
        y += bob
        expr = "happy"
    elif lt < F_MOTH + 6.0:
        k = (lt - F_MOTH) / 6.0
        x = 900 + 300 * math.sin(k * 7.0 + 0.6)
        y = ground_y - abs(math.sin(k * 20)) * 40 - (150 * math.sin(math.pi * clamp((k - 0.3) / 0.4)) if 0.3 < k < 0.7 else 0)
        rot = 10 * math.sin(k * 20)
        expr = "normal" if k < 0.4 else "happy"
        flip = 1 if math.cos(k * 7.0 + 0.6) >= 0 else -1
    else:
        x = 900 + 300 * math.sin(7.0 + 0.6) if False else 1150
        expr = "normal" if lt < F_MOTH + 7.2 else "sad"
        flip = -1 if lt < F_MOTH + 8.0 else 1
    if lt >= F_MOTH + 6.0:
        x = 1150
    out += f'<g transform="translate({bx:.0f},{by:.0f})">{ball(ball_rot)}</g>'
    out += M(lt, x, y, 1.6, expr, rot=rot, mouth=meow(T["e2"] + lt), flip=flip)
    if mp:
        out += f'<g transform="translate({mp[0]:.0f},{mp[1]:.0f}) scale(1.0)">{moth(lt)}</g>'
    out += burst(fade(lt, F_GOAL, F_GOAL + 1.2, 0.1, 0.5), 1500, 360, "GOLO!", 100, color="#2E8B57", r=170, rot=-6)
    out += caption(fade(lt, F_MOTH + 0.3, F_GOAL - 0.2), "Algo a voar...")
    out += caption(fade(lt, F_GOAL + 0.6, F_STAMP - 0.4), "Golo! ...não viu.")
    out += stamp(lt, F_STAMP, tr("ELIMINADO"), 960, 420, 118)
    out += title_card(lt, 2, "Futebol", "#8ED08A", "#3F9A4F", icon_ball())
    return out


# ---------- ginásio ----------
MAT_X = 1500


def gym_bg(lt):
    out = f'<rect width="{W}" height="{H}" fill="#E8E3F4"/><rect y="860" width="{W}" height="{H - 860}" fill="#BBA9D8"/><rect y="850" width="{W}" height="16" fill="#9D88C0"/>'
    out += f'<rect x="1260" y="150" width="500" height="420" fill="#CFE8F5" stroke="{INK}" stroke-width="8"/><line x1="1510" y1="150" x2="1510" y2="570" stroke="{INK}" stroke-width="6"/>'
    out += f'<rect x="120" y="220" width="400" height="60" rx="14" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
    out += f'<text x="320" y="264" font-family="{FONT}" font-weight="bold" font-size="40" fill="#8A7BB0" text-anchor="middle">GYM</text>'
    for i in range(5):  # halteres pequenos na parede
        out += f'<g transform="translate({180 + i * 80},520) scale(0.35)">{dumbbell(120, 50)}</g>'
    out += f'<rect x="130" y="500" width="440" height="14" rx="6" fill="#8A8FA3"/>'
    return out


def s_e3(lt):
    out = gym_bg(lt)
    ground_y = 940
    x, y, rot, expr, sx, sy = 700.0, ground_y, 0.0, "normal", 1.0, 1.0
    dx, dy, drot = 1050.0, 880.0, 0.0
    flip = 1
    if lt < 2.5:
        x = lerp(-150, 700, ease(lt / 2.5))
        bob, rot = walk_bob(lt, 3.4, 14)
        y += bob
    elif lt < G_FALL:
        x = 780
        k = (lt - 2.5)
        expr = "angry"
        rot = 6 * math.sin(k * 9) * min(1, k / 2)
        y = ground_y + 4 * math.sin(k * 30)
        dy = 880 - (18 * clamp((lt - 5.0) / 3.0)) + 3 * math.sin(k * 30)
    elif lt < G_FALL + 3.2:
        u = (lt - G_FALL)
        fall = ease(u / 0.5)
        rot = -88 * fall
        x = 780 - 100 * fall
        y = ground_y - 10 - 50 * fall
        expr = "ko"
        dy = 880 + 30 * ease(u / 0.5)
    elif lt < G_MAT:
        u = ease((lt - (G_FALL + 3.2)) / 1.0)
        rot = -88 * (1 - u)
        x = 680 + 0 * u
        y = ground_y + 30 * (1 - u)
        expr = "sad" if u < 0.9 else "normal"
        dy = 910
        if lt >= G_FALL + 4.4:
            v = ease((lt - (G_FALL + 4.4)) / (G_MAT - G_FALL - 4.4))
            x = lerp(680, MAT_X - 60, v)
            bob, rot = walk_bob(lt, 3.4, 10)
            y += bob
            expr = "normal"
    else:
        dy = 910
        x = MAT_X - 60
        y = ground_y
        u = ease((lt - G_MAT) / 1.4)
        expr = "sleep" if lt >= G_SLEEP else "normal"
        sy = lerp(1.0, 0.72, u)
        sx = lerp(1.0, 1.15, u)
        y = ground_y - 6
    # tapete de yoga
    out += f'<rect x="{MAT_X - 260}" y="{ground_y - 10}" width="520" height="34" rx="14" fill="#8E6FC9" stroke="{INK}" stroke-width="5"/>'
    out += f'<g transform="translate({dx},{dy}) rotate({drot})">{dumbbell(330, 100)}</g>'
    out += M(lt, x, y, 1.6, expr, rot=rot, sx=sx, sy=sy, mouth=meow(T["e3"] + lt), flip=flip)
    if 3.0 <= lt < G_FALL:   # vapor de esforço
        for i in range(3):
            u = ((lt * 1.2) + i / 3) % 1
            out += f'<circle cx="{660 + i * 40:.0f}" cy="{ground_y - 520 - 100 * u:.0f}" r="{14 + 10 * u:.0f}" fill="#FFFFFF" opacity="{0.8 * (1 - u):.2f}" stroke="#CFC6E3" stroke-width="3"/>'
    if lt >= G_SLEEP:
        out += zzz(lt, x + 100, y - 340)
    out += burst(fade(lt, G_FALL, G_FALL + 1.0, 0.05, 0.4), 1000, 560, "PAF!", 96, r=155, rot=-6)
    out += caption(fade(lt, G_FALL + 0.5, G_MAT - 0.3), "Muito pesado")
    out += caption(fade(lt, G_SLEEP + 0.5, G_STAMP - 0.5), "Isto sim é desporto")
    out += stamp(lt, G_STAMP, tr("ELIMINADO"), 960, 420, 118)
    out += title_card(lt, 3, "Ginásio", "#B7A2E0", "#6B4FB5", icon_dumb())
    return out


# ---------- final ----------
def s_fim(lt):
    t = T["fim"] + lt
    out = room_bg()
    out += petals(lt, 10, 0.5)
    out += f'<ellipse cx="960" cy="948" rx="330" ry="26" fill="#C8553D" opacity="0.5"/>'
    out += M(t, 960, 940, 1.6, "sleep", sx=1.15, sy=0.76, mouth=meow(t))
    out += zzz(lt, 1080, 640)
    if lt >= M_MEDAL:
        u = clamp((lt - M_MEDAL) / 1.2)
        my = lerp(-140, 780, ease_out(u))
        out += f'<g transform="translate(960,{my:.0f}) scale(1.0)">{medal(1.0, 1.0 if u >= 1 else 0.5)}</g>'
        if u >= 1:
            out += sparkle(800, 700, 1.2 + 0.3 * math.sin(lt * 6), 0.9) + sparkle(1130, 740, 1.0, 0.8) + sparkle(900, 600, 0.8, 0.7)
    out += caption(fade(lt, 1.2, 5.4), "3 desportos. 0 medalhas.")
    out += caption(fade(lt, 8.0, 13.8), "Campeão de sesta")
    if t >= T["cartao"]:
        op = ease((t - T["cartao"]) / 0.6)
        out += (f'<g opacity="{op:.2f}"><rect width="{W}" height="{H}" fill="#1E1B2E" opacity="0.88"/>'
                f'<text x="960" y="360" font-family="{FONT}" font-weight="bold" font-size="96" fill="#FFF6EA" text-anchor="middle">{tr("Ajuda o Mochi")}</text>'
                f'<text x="960" y="470" font-family="{FONT}" font-weight="bold" font-size="80" fill="#F6C343" text-anchor="middle">{tr("a chegar ao Japão")}</text>'
                f'<rect x="560" y="550" width="800" height="112" rx="56" fill="#D8343A"/>'
                f'<text x="960" y="628" font-family="{FONT}" font-weight="bold" font-size="58" fill="#FFFFFF" text-anchor="middle">{tr(VAQUINHA)}</text>'
                f'<text x="960" y="760" font-family="{FONT}" font-size="50" fill="#FFF6EA" text-anchor="middle">{tr("Link na descrição")}</text></g>')
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
SUF = "_zh" if LANG == "zh" else ""
FRAMES = os.path.join(DIR, "frames_desportos" + SUF)


def render_one(n):
    p = os.path.join(FRAMES, f"f{n:05d}.png")
    if not os.path.exists(p):
        cairosvg.svg2png(bytestring=frame_svg(n / FPS).encode(), write_to=p)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "render":
        for s in sys.argv[1:]:
            cairosvg.svg2png(bytestring=frame_svg(float(s)).encode(), write_to=os.path.join(DIR, f"prev_desp_{s}.png"))
        sys.exit()
    os.makedirs(FRAMES, exist_ok=True)
    with Pool(2) as pool:
        pool.map(render_one, range(int(FPS * TOTAL)), chunksize=48)
    out = os.path.join(DIR, "mochi_desportos" + SUF + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(FRAMES, "f%05d.png"),
                    "-i", os.path.join(DIR, "musica_desportos.wav"), "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out)
