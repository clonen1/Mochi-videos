"""'O Mochi procura emprego' (1920x1080, 24 fps, 102 s). Sem falas: conta-se com animação.

casa (0-14) | emprego 1 entregador (14-36) | emprego 2 barista (36-54) | emprego 3 segurança (54-74)
final: 3 empregos, 0€ -> pedir ajuda -> vaquinha (74-90) | Japão (90-96) | cartão (96-102)
"""
import math
import os
import subprocess
import sys
from multiprocessing import Pool

import cairosvg

from mochi_longo import (LANG, tr, APRON, CAP, GUARD_CAP, H, W, FPS, FONT, INK, M, bubble, bulb, burst, caption, clamp, clock, coin,
                         cam, delivery_box, drool, ease, ease_out, fade, fish_icon, lerp, mug, pay, person, petals, phone,
                         piggy_svg, poster, smell, spring, sparkle, stamp, steam, sunrise_sky, torii, trophy, walk_bob, zzz)
from mochi_props import moth
from tempos_trabalhos import *  # noqa: F401,F403

VAQUINHA = "gofund.me/5d9e87b27"


def meow(t):
    for t0 in MEOWS:
        if t0 <= t <= t0 + 0.55:
            return math.sin(math.pi * (t - t0) / 0.55) ** 0.8
    return 0.0


# ---------- cartões de título ----------
def icon_box():
    return f'<g transform="scale(1.5)">{delivery_box()}</g>'


def icon_cup():
    return f'<g transform="translate(0,60) scale(2.0)">{mug(1.0)}</g>'


def icon_torch():
    return ('<g transform="rotate(-35) scale(1.6)"><rect x="-26" y="-110" width="52" height="120" rx="12" fill="#5A6B8C" stroke="#2B2B2B" stroke-width="6"/>'
            '<rect x="-40" y="-150" width="80" height="50" rx="10" fill="#8A97B5" stroke="#2B2B2B" stroke-width="6"/>'
            '<path d="M-40 -150 L-90 -230 L90 -230 L40 -150 Z" fill="#FFE98A" opacity="0.6"/></g>')


def title_card(lt, n, name, c1, c2, icon):
    """Cartão de título que desliza e sai com fade (0 a 2.5 s)."""
    if lt > 2.5:
        return ""
    out_op = 1 - ease((lt - 2.0) / 0.5)
    a = spring(lt - 0.1)
    b = spring(lt - 0.35)
    ic = spring(lt - 0.55)
    return (f'<g opacity="{out_op:.2f}"><defs><linearGradient id="tc{n}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#tc{n})"/>'
            f'<g transform="translate({-900 * (1 - min(a, 1)):.0f},0)"><circle cx="380" cy="470" r="150" fill="#FFF6EA" stroke="{INK}" stroke-width="10"/>'
            f'<text x="380" y="530" font-family="{FONT}" font-weight="bold" font-size="190" fill="#D8343A" text-anchor="middle">{n}</text></g>'
            f'<g transform="translate({-900 * (1 - min(b, 1)):.0f},0)"><text x="620" y="440" font-family="{FONT}" font-weight="bold" font-size="76" fill="#FFF6EA" '
            f'stroke="{INK}" stroke-width="3">{"工作" + str(n) if LANG == "zh" else "Emprego " + str(n)}</text>'
            f'<text x="620" y="570" font-family="{FONT}" font-weight="bold" font-size="120" fill="#FFFFFF" stroke="{INK}" stroke-width="5">{tr(name)}</text></g>'
            f'<g transform="translate(1560,520) scale({max(ic, 0.001):.2f})">{icon}</g></g>')


# ---------- 1. casa ----------
def room_bg():
    out = (f'<rect width="{W}" height="{H}" fill="#FFE9CF"/><rect y="800" width="{W}" height="280" fill="#D9A27A"/>'
           '<rect y="790" width="1920" height="22" fill="#B8774A"/>')
    for i in range(8):
        out += f'<line x1="{i * 300 - 100}" y1="812" x2="{i * 300 - 380}" y2="1080" stroke="#C48A5C" stroke-width="4"/>'
    out += ('<rect x="1320" y="150" width="300" height="360" fill="#9ED3F0" stroke="#2B2B2B" stroke-width="10"/>'
            '<line x1="1470" y1="150" x2="1470" y2="510" stroke="#2B2B2B" stroke-width="8"/><line x1="1320" y1="330" x2="1620" y2="330" stroke="#2B2B2B" stroke-width="8"/>'
            '<ellipse cx="1420" cy="250" rx="60" ry="26" fill="#FFFFFF" opacity="0.9"/>'
            '<rect x="1290" y="130" width="40" height="400" fill="#F2A14A"/><rect x="1610" y="130" width="40" height="400" fill="#F2A14A"/>'
            '<ellipse cx="960" cy="930" rx="520" ry="80" fill="#E8B0A0" opacity="0.7"/>')
    return out


def s_casa(t):
    lt = t
    x = 820.0
    if lt >= 3.5:
        x = lerp(820, 1120, ease((lt - 3.5) / 1.1))
    if lt >= 11.6:
        x = lerp(1120, 2250, ease((lt - 11.6) / 2.0))
    moving = (3.5 <= lt < 4.6) or lt >= 11.6
    bob, rot = walk_bob(lt, 3.6, 16) if moving else (0, 0)
    hop = 0.0
    if BULB <= lt < BULB + 0.6:
        hop = -90 * math.sin(math.pi * (lt - BULB) / 0.6)
    expr = "normal"
    if 6.2 <= lt < BULB:
        expr = "sad"
    elif lt >= BULB:
        expr = "happy"
    shake = 0.0
    if SHAKE[0] <= lt < SHAKE[1]:
        shake = 9 * math.sin(lt * 32) * (1 - 0.4 * (lt - SHAKE[0]) / (SHAKE[1] - SHAKE[0]))
    out = room_bg()
    out += poster(300, 170)
    if lt < 4:  # sonha: pétalas a sair do poster
        for i in range(8):
            u = (lt * 0.3 + i / 8) % 1
            out += (f'<ellipse cx="{420 + 130 * math.sin(i * 2 + lt)  + 280 * u:.0f}" cy="{600 - 320 * u:.0f}" rx="11" ry="7" fill="#F7B6C8" '
                    f'opacity="{math.sin(math.pi * u):.2f}"/>')
    out += f'<g transform="translate(1480,860) scale(1.0)">{piggy_svg(shake)}</g>'
    out += M(lt, x, 935 + bob + hop, 1.6, expr, rot=rot + (shake * 0.15), mouth=meow(lt))
    if lt < 3.5:
        out += sparkle(500, 190, 1.2 + 0.2 * math.sin(lt * 5), 0.9) + sparkle(640, 260, 0.9, 0.8)
    if MOTH <= lt < MOTH + 4:  # a traça sai da ranhura
        u = (lt - MOTH) / 4
        mx = 1440 - 780 * u + 60 * math.sin(u * 14)
        my = 760 - 420 * u + 40 * math.sin(u * 9)
        out += f'<g transform="translate({mx:.0f},{my:.0f}) scale(0.9)">{moth(lt)}</g>'
    if BULB <= lt < BULB + 3.2:
        out += bulb(x, 330, 1.0, ease((lt - BULB) / 0.2) * (1 - ease((lt - (BULB + 2.7)) / 0.5)))
    out += caption(fade(lt, 5.0, 8.2), "O mealheiro está vazio")
    out += caption(fade(lt, 9.0, 12.6), "Vou arranjar um emprego!")
    return out


# ---------- 2. emprego 1: entregador ----------
DOOR_X = 2700
GROUND = 860


def street(off, lt):
    out = f'<rect width="{W}" height="{H}" fill="#CDE8F5"/><circle cx="1500" cy="190" r="90" fill="#FFF3B0"/>'
    for k, c in enumerate(["#E8C5A0", "#D9A27A", "#E5D3B3", "#CFA88A", "#E8C5A0", "#D9A27A", "#E5D3B3"]):
        bx = (k * 330 - off * 0.25) % 2310 - 330
        h = [520, 640, 460, 600, 500, 620, 480][k]
        out += f'<rect x="{bx:.0f}" y="{GROUND - h}" width="300" height="{h}" fill="{c}"/>'
        for r in range(3):
            out += f'<rect x="{bx + 50:.0f}" y="{GROUND - h + 60 + r * 130}" width="60" height="80" fill="#9ED3F0"/><rect x="{bx + 180:.0f}" y="{GROUND - h + 60 + r * 130}" width="60" height="80" fill="#9ED3F0"/>'
    out += f'<rect y="{GROUND}" width="{W}" height="{H - GROUND}" fill="#B8B8C0"/><rect y="{GROUND}" width="{W}" height="22" fill="#9A9AA4"/>'
    for i in range(14):
        sx = (i * 240 - off) % 3360 - 240
        out += f'<rect x="{sx:.0f}" y="{GROUND + 160}" width="120" height="14" rx="7" fill="#E9E9EE"/>'
    for i in range(4):  # candeeiros
        lx = (i * 820 - off * 0.8) % 3280 - 200
        out += f'<rect x="{lx:.0f}" y="{GROUND - 360}" width="14" height="360" fill="#5A5F73"/><circle cx="{lx + 7:.0f}" cy="{GROUND - 372}" r="26" fill="#FFE98A" stroke="#2B2B2B" stroke-width="4"/>'
    return out


def house(off, door_open):
    x = DOOR_X - off
    if x < -700 or x > 2600:
        return ""
    out = (f'<rect x="{x - 420:.0f}" y="{GROUND - 620}" width="840" height="620" fill="#F2D6B3" stroke="{INK}" stroke-width="6"/>'
           f'<polygon points="{x - 460:.0f},{GROUND - 620} {x:.0f},{GROUND - 760} {x + 460:.0f},{GROUND - 620}" fill="#C9553F" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
           f'<rect x="{x - 360:.0f}" y="{GROUND - 480}" width="150" height="170" fill="#9ED3F0" stroke="{INK}" stroke-width="6"/>'
           f'<rect x="{x + 210:.0f}" y="{GROUND - 480}" width="150" height="170" fill="#9ED3F0" stroke="{INK}" stroke-width="6"/>'
           f'<rect x="{x - 110:.0f}" y="{GROUND - 400}" width="220" height="400" fill="#6B4630" stroke="{INK}" stroke-width="6"/>')
    if door_open > 0:
        out += (f'<rect x="{x - 100:.0f}" y="{GROUND - 390}" width="200" height="390" fill="#3A2A3E"/>'
                f'<rect x="{x - 110:.0f}" y="{GROUND - 400}" width="{220 * (1 - door_open) + 30:.0f}" height="400" fill="#6B4630" stroke="{INK}" stroke-width="6"/>')
    else:
        out += f'<circle cx="{x + 70:.0f}" cy="{GROUND - 200}" r="12" fill="#F6C343" stroke="{INK}" stroke-width="3"/>'
    out += f'<rect x="{x - 140:.0f}" y="{GROUND - 14}" width="280" height="22" rx="8" fill="#8A6A8E"/>'
    return out


def s_e1(lt):
    t = T["e1"] + lt
    off = 1450 * ease((lt - 2.5) / 7.5) if lt >= 2.5 else 0
    door_open = ease((lt - E1_DOOR) / 0.4) if lt >= E1_DOOR else 0
    out = street(off, lt) + house(off, door_open)
    walking = 2.5 <= lt < 10.0
    bob, rot = walk_bob(lt, 3.8, 15) if walking else (0, 0)
    mx = 640.0
    flip = 1
    expr = "normal"
    extra = CAP
    box_open = 0.0
    bites = sum(1 for b in E1_BITES if lt >= b)
    if 7.0 <= lt < 11.0:
        expr = "eat"
        extra += drool(lt)
    if lt >= 10.0:
        mx = lerp(640, 800, ease((lt - 10.0) / 1.0))
    if 11.6 <= lt < 13.6:
        flip = 1 if int((lt - 11.6) / 0.7) % 2 == 1 else -1
        expr = "normal"
    if lt >= E1_OPEN:
        box_open = ease((lt - E1_OPEN) / 0.4)
    my = GROUND + 40
    sx = 1 + 0.025 * bites
    dip = 0.0
    if lt >= E1_OPEN and lt < E1_BURP:
        expr = "eat"
        for b in E1_BITES:
            if b <= lt < b + 0.5:
                dip = 30 * math.sin(math.pi * (lt - b) / 0.5)
    if lt >= E1_BURP:
        expr = "happy"
    if lt >= E1_DOOR + 0.6:
        expr = "normal"
        extra = CAP
    # caixa: às costas -> chão
    if lt < 10.5:
        bx, by, brot = mx - 120, my - 170 + bob * 0.5, -6 + rot
    elif lt < 11.4:
        u = ease((lt - 10.5) / 0.9)
        bx, by, brot = lerp(mx - 120, 1010, u), lerp(my - 170, my + 30, u) - 120 * math.sin(math.pi * u), 0
    else:
        bx, by, brot = 1010, my + 30, 0
    if lt >= 2.0:
        if lt < 10.5:
            out += f'<g transform="translate({bx:.0f},{by:.0f}) rotate({brot:.1f}) scale(0.95)">{delivery_box()}</g>'
        if 5.0 <= lt < 10.5:
            out += smell(lt, bx, by - 190, ease((lt - 5) / 1.5))
    out += M(lt, mx, my + bob - dip * 0.4, 1.5, expr, flip=flip, sx=sx, rot=rot, mouth=meow(t), extra=extra)
    if lt >= 10.5:
        content = 1 - bites / 5.0
        out += f'<g transform="translate({bx:.0f},{by:.0f}) scale(1.1)">{delivery_box(box_open, content)}</g>'
        if lt >= E1_OPEN + 0.4 and lt < E1_BURP:
            out += smell(lt, bx, by - 220, 0.6 * content)
        for b in E1_BITES:  # migalhas
            if b <= lt < b + 0.7:
                u = (lt - b) / 0.7
                for k in range(5):
                    out += f'<circle cx="{bx - 20 + k * 22 - 30 * u * (k - 2):.0f}" cy="{by - 130 + 70 * u * u + k * 4:.0f}" r="5" fill="#7FB5D8" opacity="{1 - u:.2f}"/>'
    if lt >= E1_BURP and lt < E1_BURP + 1.2:
        u = (lt - E1_BURP) / 1.2
        out += burst(1 - u, int(mx + 150), int(my - 330), "buurp", 44, 80, "#7A4A2A")
    # cliente à porta
    if lt >= E1_DOOR:
        dx = DOOR_X - off
        c_mood = "shock" if lt < E1_DOOR + 1.0 else "angry"
        out += person(dx, GROUND + 6, 1.15, c_mood, 1, "#E86A5C", "#2B2B2B", "#3D4B6B", arms=1 if c_mood == "shock" else 0.3)
        if lt >= E1_DOOR + 0.5:
            out += bubble(dx - 240, GROUND - 560, 330, 150,
                          f'<text x="-90" y="26" font-family="{FONT}" font-weight="bold" font-size="90" fill="#D8343A" text-anchor="middle">?!</text>'
                          f'<g transform="translate(70,6) scale(1.0)"><rect x="-55" y="-34" width="110" height="68" rx="8" fill="none" stroke="{INK}" stroke-width="6" stroke-dasharray="14 10"/></g>',
                          (90, 70), fade(lt, E1_DOOR + 0.5, E1_STAMP + 0.4, 0.2, 0.3))
    out += caption(fade(lt, 7.0, 10.0), "Que cheirinho...")
    out += caption(fade(lt, 11.7, 13.4), "Ninguém está a ver...")
    out += caption(fade(lt, E1_DOOR + 0.8, E1_STAMP, 0.25, 0.3), "A encomenda sumiu")
    out += stamp(lt, E1_STAMP) + pay(lt, E1_STAMP + 0.4)
    return out + title_card(lt, 1, "Entregador", "#F6C343", "#F2A14A", icon_box())


# ---------- 3. emprego 2: barista ----------
FLOOR2 = 1030


def cafe_bg(lt):
    out = (f'<rect width="{W}" height="{H}" fill="#F3D9B8"/>'
           '<rect y="150" width="1920" height="30" fill="#B8774A"/><rect y="330" width="1920" height="30" fill="#B8774A"/>')
    for i in range(9):
        out += (f'<g transform="translate({140 + i * 200},{150})">{mug(1.0, 0.5)}</g>' if i % 2 == 0 else
                f'<g transform="translate({140 + i * 200},{330})">{mug(0.0, 0.5)}</g>')
    out += (f'<rect y="{FLOOR2 - 90}" width="{W}" height="{H - FLOOR2 + 90}" fill="#C7A27C"/><rect x="1500" y="440" width="260" height="190" rx="14" fill="#6F4E37" stroke="{INK}" stroke-width="6"/>'
            f'<text x="1630" y="560" font-family="{FONT}" font-weight="bold" font-size="76" fill="#FFF6EA" text-anchor="middle">{tr("CAFÉ")}</text>')
    return out


def s_e2(lt):
    t = T["e2"] + lt
    my = 770
    mx = 1010
    out = cafe_bg(lt)
    # Mochi atrás do balcão
    expr = "normal"
    if lt >= 11.4:
        expr = "happy"
    push = clamp((lt - E2_PUSH) / 0.7) if lt < E2_PUSH + 1.4 else clamp(1 - (lt - (E2_PUSH + 1.4)) / 0.5)
    out += M(lt, mx, my + 6, 1.65, expr, mouth=meow(t), extra=APRON, shadow=False)
    # balcão
    out += (f'<rect x="-20" y="700" width="1420" height="{H - 700}" fill="#8A5A34" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="-20" y="678" width="1440" height="34" rx="8" fill="#D9A27A" stroke="{INK}" stroke-width="6"/>')
    for i in range(6):
        out += f'<rect x="{40 + i * 230}" y="760" width="190" height="220" rx="10" fill="#A06E40" stroke="#6F4824" stroke-width="4"/>'
    # máquina de café
    out += (f'<rect x="250" y="470" width="260" height="210" rx="22" fill="#9AA4B8" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="290" y="500" width="100" height="60" rx="10" fill="#2B2B2B"/><circle cx="450" cy="530" r="20" fill="#D8343A"/>'
            f'<rect x="395" y="612" width="30" height="40" rx="6" fill="#5A6074" stroke="{INK}" stroke-width="4"/>')
    # caneca
    mug_x, mug_y, mug_rot, mug_fill = 395, 678, 0.0, 0.0
    if lt >= E2_POUR[0]:
        mug_fill = clamp((lt - E2_POUR[0]) / (E2_POUR[1] - E2_POUR[0]))
    if E2_POUR[0] <= lt < E2_POUR[1]:
        out += f'<rect x="407" y="650" width="6" height="{678 - 650}" fill="#7A4A2A"/>'
    if lt >= E2_SLIDE[0]:
        mug_x = lerp(410, 1230, ease((lt - E2_SLIDE[0]) / (E2_SLIDE[1] - E2_SLIDE[0])))
    else:
        mug_x = 410
    falling = lt >= E2_FALL
    if lt >= E2_PUSH and not falling:
        mug_x = 1230 + 190 * ease((lt - E2_PUSH) / (E2_FALL - E2_PUSH))
        mug_rot = 14 * ease((lt - (E2_FALL - 0.4)) / 0.4)
    if falling:
        d = lt - E2_FALL
        mug_x = 1420 + 150 * d
        mug_y = 678 + 420 * d * d * 1.35 + 40 * d
        mug_rot = 14 + 380 * d
    crashed = lt >= E2_CRASH
    if not crashed:
        out += f'<g transform="translate({mug_x:.0f},{min(mug_y, 1010):.0f}) rotate({mug_rot:.0f})">{mug(mug_fill if not falling else 1.0)}</g>'
        if 6 <= lt < E2_PUSH + 0.8:
            out += steam(lt, mug_x, mug_y - 90)
    # pata a empurrar
    if lt >= E2_PUSH - 0.2 and lt < E2_PUSH + 2:
        u = push
        px = lerp(1060, mug_x - 60, ease(u)) if lt < E2_FALL else lerp(1060, 1380, ease(clamp(1 - (lt - E2_FALL) / 0.6)))
        out += (f'<line x1="1090" y1="610" x2="{px:.0f}" y2="{678 - 46:.0f}" stroke="#F2A14A" stroke-width="64" stroke-linecap="round"/>'
                f'<circle cx="{px:.0f}" cy="{678 - 46:.0f}" r="36" fill="#FFF6EA"/>')
    # estrago
    if crashed:
        d = lt - E2_CRASH
        wide = 200 * ease(d / 0.6)
        out += f'<ellipse cx="1560" cy="1020" rx="{wide:.0f}" ry="{wide * 0.18:.0f}" fill="#7A4A2A" opacity="0.92"/>'
        for k in range(7):
            ang = -2.6 + k * 0.5
            dd = min(d, 0.7)
            out += f'<circle cx="{1570 + math.cos(ang) * 260 * dd:.0f}" cy="{1010 + math.sin(ang) * 380 * dd + 600 * dd * dd:.0f}" r="9" fill="#7A4A2A" opacity="{1 - d / 0.9 if d < 0.9 else 0:.2f}"/>'
        for k in range(5):
            out += (f'<polygon points="0,0 30,10 14,34" transform="translate({1480 + k * 38 + 30 * min(d, 0.4) * (k - 2):.0f},{1010 + (k % 2) * 14}) rotate({k * 60})" '
                    f'fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>')
    # cliente à direita
    c_mood = "neutral"
    cb = 0.0
    arms = 0.0
    if lt < E2_FALL - 0.2:
        cb = -6 * abs(math.sin(lt * 5))  # impaciente
    elif lt < 13.4:
        c_mood, arms = "shock", 1
    else:
        c_mood, arms = "angry", 0.4
    out += person(1700, 1060, 1.2, c_mood, -1, "#6CB58E", "#2B2B2B", "#3D4B6B", bob=cb, arms=arms)
    if lt >= 13.4:
        out += bubble(1480, 360 + 220, 280, 140,
                      f'<text x="0" y="24" font-family="{FONT}" font-weight="bold" font-size="86" fill="#D8343A" text-anchor="middle">!!!</text>', (90, 60),
                      fade(lt, 13.4, E2_STAMP + 1.0, 0.2, 0.4))
    out += caption(fade(lt, 3.0, 6.0), "Um café a sair...")
    out += caption(fade(lt, 8.2, 10.4), "Gatos e canecas...")
    out += stamp(lt, E2_STAMP) + pay(lt, E2_STAMP + 0.4)
    return out + title_card(lt, 2, "Barista", "#9CC9A6", "#4E9A6E", icon_cup())


# ---------- 4. emprego 3: segurança ----------
def shop_bg(lt):
    dawn = ease((lt - 12.0) / 4.0)
    sky = f'rgb({int(27 + 215 * dawn)},{int(34 + 130 * dawn)},{int(64 + 50 * dawn)})'
    wall = f'rgb({int(36 + 150 * dawn)},{int(42 + 120 * dawn)},{int(78 + 70 * dawn)})'
    moon_u = ease((lt - 6.0) / 10.0)
    out = (f'<rect width="{W}" height="{H}" fill="{wall}"/><rect y="880" width="{W}" height="200" fill="#{"2A2F52" if dawn < 0.5 else "7A6A60"}"/>'
           f'<rect x="150" y="120" width="440" height="470" fill="{sky}" stroke="{INK}" stroke-width="10"/>'
           f'<circle cx="{200 + 340 * moon_u:.0f}" cy="{210 + 90 * math.sin(moon_u * 3.1):.0f}" r="52" fill="{"#FFF3C4" if dawn < 0.6 else "#FFD070"}"/>'
           f'<line x1="370" y1="120" x2="370" y2="590" stroke="{INK}" stroke-width="8"/><line x1="150" y1="355" x2="590" y2="355" stroke="{INK}" stroke-width="8"/>')
    if dawn < 0.7:
        for i in range(7):
            out += f'<circle cx="{190 + i * 61}" cy="{150 + (i * 47) % 160}" r="3.5" fill="#FFFFFF" opacity="{0.9 * (1 - dawn):.2f}"/>'
    # estantes com caixas
    for k in range(4):
        out += (f'<rect x="{1500}" y="{250 + k * 170}" width="380" height="16" fill="#6B4630"/>'
                f'<rect x="{1520 + (k * 37) % 40}" y="{190 + k * 170}" width="90" height="60" fill="#B98A5A" stroke="{INK}" stroke-width="4"/>'
                f'<rect x="{1650 - (k * 23) % 30}" y="{200 + k * 170}" width="110" height="50" fill="#8FA9C9" stroke="{INK}" stroke-width="4"/>')
    return out


def s_e3(lt):
    t = T["e3"] + lt
    dawn = ease((lt - 12.0) / 4.0)
    out = shop_bg(lt)
    hours = 22 + 8 * ease((lt - 8.0) / 8.0) if lt >= 8 else 22
    out += clock(hours, 960, 230)
    # pedestal e troféu
    glass_op = 0.25
    taken = lt >= E3_GRAB
    out += (f'<g transform="translate(1260,{880})"><rect x="-90" y="-80" width="180" height="80" fill="#4A4F6E" stroke="{INK}" stroke-width="6"/>'
            f'{"" if taken else trophy(0.8 + 0.2 * math.sin(lt * 4))}'
            f'<rect x="-84" y="-250" width="168" height="170" fill="#BFE6FF" opacity="{glass_op}" stroke="{INK}" stroke-width="4"/></g>')
    # Mochi
    asleep = lt >= E3_SLEEP
    if lt < E3_PATROL[0]:
        mx, expr, flip = 330.0, "normal", 1
    elif lt < E3_PATROL[1]:
        u = ease((lt - E3_PATROL[0]) / (E3_PATROL[1] - E3_PATROL[0]))
        mx, expr, flip = lerp(330, 760, u), "normal", 1
    else:
        mx, expr, flip = lerp(760, 900, ease((lt - 6.0) / 0.8)), "normal", 1
    moving = E3_PATROL[0] <= lt < 6.8
    bob, rot = walk_bob(lt, 3.2, 12) if moving else (0, 0)
    sit = ease((lt - 6.6) / 0.5)
    my = 930 - 40 * sit
    sy = 1 - 0.12 * sit
    mouth = 0.0
    if 6.9 <= lt < 7.5:
        mouth = 1.0
    if asleep:
        expr = "sleep"
    wake = lt >= E3_WAKE
    if wake:
        expr = "shock"
    # lanterna (feixe) enquanto patrulha
    if lt < 6.6 and lt >= 2.0:
        sweep = 18 * math.sin(lt * 1.6)
        out += (f'<g transform="translate({mx + 150:.0f},{my - 190:.0f}) rotate({sweep + 14:.0f})"><polygon points="0,0 720,-170 720,170" fill="#FFF3B0" opacity="0.30"/>'
                f'<rect x="-6" y="-16" width="64" height="32" rx="8" fill="#5A6B8C" stroke="{INK}" stroke-width="4"/></g>')
    # cadeira
    out += (f'<rect x="{760}" y="880" width="260" height="22" rx="8" fill="#7A5A3A" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="780" y="900" width="18" height="90" fill="#5A3E26"/><rect x="982" y="900" width="18" height="90" fill="#5A3E26"/>')
    head_dip = 0.0
    if asleep and not wake:
        head_dip = 6 * math.sin(lt * 2.4) + 10
    out += M(lt, mx, my + bob + (head_dip * 0.2 if asleep else 0), 1.55, expr, sy=sy, rot=rot + (head_dip * 0.4 if asleep and not wake else 0),
             mouth=mouth if not asleep else 0.0, extra=GUARD_CAP, scarf=True)
    if asleep and not wake:
        out += zzz(lt, mx + 60, my - 380, 3, 64)
        if lt >= 12.0:  # bolha do nariz
            r = 12 + 34 * (0.5 + 0.5 * math.sin(lt * 2.6))
            out += f'<circle cx="{mx + 6:.0f}" cy="{my - 275:.0f}" r="{r:.0f}" fill="#BFE6FF" opacity="0.7" stroke="{INK}" stroke-width="3"/>'
    # ladrão
    if E3_ROBBER[0] <= lt < 14.6:
        if lt < 11.0:
            rx = lerp(-150, 1160, clamp((lt - 8.5) / 2.5)); rflip = 1
        elif lt < 11.6:
            rx, rflip = 1160, 1
        elif lt < 13.0:
            rx, rflip = lerp(1160, 520, ease((lt - 11.6) / 1.4)), -1
        elif lt < 13.8:
            rx, rflip = 520, -1
        else:
            rx, rflip = lerp(520, -200, ease((lt - 13.8) / 0.8)), -1
        rb = -8 * abs(math.sin(lt * 7)) if (lt < 11.0 or 11.6 <= lt < 13.0 or lt >= 13.8) else 0
        sack = taken
        out += person(rx, 1010, 1.15, "mask", rflip, "#4A4A55", "#2B2B2B", "#2B2B2B", bob=rb, arms=0.0)
        if sack:
            out += (f'<g transform="translate({rx - 70 * rflip:.0f},{1010 - 150 + rb:.0f})"><circle r="60" fill="#B98A5A" stroke="{INK}" stroke-width="5"/>'
                    f'<path d="M-20 -52 Q0 -86 20 -52" fill="#B98A5A" stroke="{INK}" stroke-width="5"/></g>')
        if 13.0 <= lt < 13.8:
            out += bubble(rx + 40, 590, 190, 110,
                          f'<text x="0" y="22" font-family="{FONT}" font-weight="bold" font-size="64" fill="{INK}" text-anchor="middle">shh</text>', (-30, 50), 1.0)
    if dawn > 0:
        out += f'<rect width="{W}" height="{H}" fill="#FFB86B" opacity="{0.20 * dawn:.2f}"/>'
    if wake:
        out += burst(fade(lt, E3_WAKE, E3_WAKE + 1.6, 0.1, 0.4), int(mx + 190), int(my - 440), "!?", 90, 120)
    out += caption(fade(lt, 3.0, 6.0), "Noite tranquila...")
    out += caption(fade(lt, 7.8, 11.0), "Só uma sonequinha...")
    out += caption(fade(lt, E3_WAKE + 0.6, E3_STAMP, 0.2, 0.3), "O troféu sumiu!")
    out += stamp(lt, E3_STAMP) + pay(lt, E3_STAMP + 0.4)
    return out + title_card(lt, 3, "Segurança", "#8A97B5", "#2D4A7C", icon_torch())


# ---------- 5. final ----------
def mini_card(x, y, op, kind):
    icon = {"box": f'<g transform="translate(0,52) scale(0.46)">{delivery_box()}</g>',
            "cup": f'<g transform="translate(0,48) scale(0.8)">{mug(1.0)}</g>',
            "torch": '<g transform="translate(0,6) rotate(-35) scale(0.6)"><rect x="-26" y="-60" width="52" height="120" rx="12" fill="#5A6B8C" stroke="#2B2B2B" stroke-width="6"/><rect x="-40" y="-100" width="80" height="50" rx="10" fill="#8A97B5" stroke="#2B2B2B" stroke-width="6"/></g>'}[kind]
    return (f'<g opacity="{op:.2f}" transform="translate({x},{y + (1 - op) * 40:.0f})"><rect x="-130" y="-120" width="260" height="240" rx="26" fill="#FFF6EA" stroke="{INK}" stroke-width="6"/>'
            f'{icon}<path d="M-100 -90 L100 90 M100 -90 L-100 90" stroke="#D8343A" stroke-width="12" stroke-linecap="round" opacity="0.8"/>'
            f'<text x="0" y="104" font-family="{FONT}" font-weight="bold" font-size="52" fill="#D8343A" text-anchor="middle">0€</text></g>')


def s_fim(lt):
    t = T["fim"] + lt
    if lt < 9.0:
        out = (f'<rect width="{W}" height="{H}" fill="#34304F"/><rect y="860" width="{W}" height="220" fill="#4A4768"/><rect y="850" width="{W}" height="22" fill="#6B6890"/>')
        for i in range(36):  # chuva
            rx = (i * 67 + lt * 160) % 2000 - 40
            ry = (i * 131 + lt * 900) % 1100
            out += f'<line x1="{rx:.0f}" y1="{ry:.0f}" x2="{rx - 20:.0f}" y2="{ry + 50:.0f}" stroke="#9FB7E3" stroke-width="3" opacity="0.55"/>'
        out += mini_card(560, 230, ease((lt - 0.4) / 0.5), "box") + mini_card(960, 230, ease((lt - 1.1) / 0.5), "cup") + mini_card(1360, 230, ease((lt - 1.8) / 0.5), "torch")
        sy = 0.9
        expr = "sad" if lt < FIM_BULB else "happy"
        if lt >= FIM_PHONE:
            expr = "normal" if lt < FIM_BULB else "happy"
        hop = 0.0
        if FIM_BULB <= lt < FIM_BULB + 0.6:
            hop = -80 * math.sin(math.pi * (lt - FIM_BULB) / 0.6)
        out += M(lt, 960, 880 + hop, 1.55, expr, sy=sy if lt < FIM_BULB else 1.0, mouth=meow(t))
        if lt >= FIM_PHONE:
            u = ease((lt - FIM_PHONE) / 0.7)
            out += f'<g transform="translate(1200,{lerp(1100, 760, u):.0f}) rotate(-10) scale(0.95)">{phone(0.6 + 0.4 * math.sin(lt * 5))}</g>'
        if FIM_BULB <= lt < FIM_BULB + 2.0:
            out += bulb(960, 340, 1.0, ease((lt - FIM_BULB) / 0.2) * (1 - ease((lt - (FIM_BULB + 1.5)) / 0.5)))
        out += caption(fade(lt, 2.4, FIM_PHONE - 0.2, 0.3, 0.3), "3 empregos. 0€.")
        out += caption(fade(lt, FIM_PHONE + 0.8, 8.9, 0.3, 0.3), "E se eu pedisse ajuda?")
        return out
    # moedas para o mealheiro
    if t < T["japao"]:
        n = sum(1 for c in FIM_COINS if lt >= c + 0.6)
        out = f'<rect width="{W}" height="{H}" fill="#FDE7D3"/>'
        out += ('<rect x="560" y="90" width="800" height="62" rx="31" fill="#2B2B2B"/><rect x="568" y="98" width="784" height="46" rx="23" fill="#FFF6EA"/>'
                f'<rect x="572" y="102" width="{776 * n / len(FIM_COINS):.0f}" height="38" rx="19" fill="#4CAF50"/>')
        squash = 0.0
        for c in FIM_COINS:
            if c + 0.6 <= lt < c + 0.9:
                squash = math.sin(math.pi * (lt - c - 0.6) / 0.3) * 0.08
        out += f'<g transform="translate(1280,{800}) scale({1.5 * (1 + squash):.3f},{1.5 * (1 - squash):.3f})">{piggy_svg()}</g>'
        for i, c in enumerate(FIM_COINS):
            if c <= lt < c + 0.6:
                u = (lt - c) / 0.6
                sx0 = 300 + (i * 211) % 1300
                out += coin(lerp(sx0, 1240, u), -60 + 700 * u * u + 40 * u, 32, lt * 9 + i)
            if c + 0.6 <= lt < c + 1.4:
                u = (lt - c - 0.6) / 0.8
                out += f'<g transform="translate({1240 + 70 * (i % 3 - 1)},{600 - 200 * u:.0f}) scale({0.7 + 0.5 * u:.2f})" opacity="{1 - u:.2f}"><path d="M0 -10 C -20 -35 -45 -10 0 25 C 45 -10 20 -35 0 -10 Z" fill="#D8343A"/></g>'
        hop = abs(math.sin(lt * 5)) * 44 * (1 if n else 0.3)
        out += M(lt, 640, 1000 - hop, 1.6, "happy", mouth=meow(t))
        if n == len(FIM_COINS):
            for k in range(12):
                out += sparkle(900 + (k * 97) % 700, 200 + (k * 61) % 500, 1.3, 0.8)
        out += caption(fade(lt, 9.2, 15.7, 0.3, 0.4), "Cada ajuda conta")
        return out
    # Japão e cartão final
    ju = (t - T["japao"])
    out = sunrise_sky(ju / 6) + torii(450, 840, 0.75) + petals(t, 24)
    out += M(t, 1150, 1010, 1.5 + 0.08 * ease((ju - 1) / 4), "happy", mouth=meow(t))
    if 2.0 < ju < 6.0:
        p = 1 + 0.12 * math.sin(ju * 8)
        out += f'<g transform="translate(1150,{860:.0f}) scale({p:.2f})"><path d="M0 -10 C -20 -35 -45 -10 0 25 C 45 -10 20 -35 0 -10 Z" fill="#D8343A" stroke="#2B2B2B" stroke-width="3"/></g>'
    out = cam(out, t, T["japao"], T["cartao"], 1.0, 1.1, 1150, 700)
    out += caption(fade(ju, 0.6, 5.6, 0.4, 0.4), "E o Japão fica mais perto")
    if t >= T["cartao"]:
        op = ease((t - T["cartao"]) / 0.6)
        out += (f'<g opacity="{op:.2f}"><rect width="{W}" height="{H}" fill="#1E1B2E" opacity="0.86"/>'
                f'<text x="960" y="360" font-family="{FONT}" font-weight="bold" font-size="96" fill="#FFF6EA" text-anchor="middle">{tr("Ajuda o Mochi")}</text>'
                f'<text x="960" y="470" font-family="{FONT}" font-weight="bold" font-size="80" fill="#F6C343" text-anchor="middle">{tr("a chegar ao Japão")}</text>'
                f'<rect x="560" y="550" width="800" height="112" rx="56" fill="#D8343A"/>'
                f'<text x="960" y="628" font-family="{FONT}" font-weight="bold" font-size="58" fill="#FFFFFF" text-anchor="middle">{tr(VAQUINHA)}</text>'
                f'<text x="960" y="760" font-family="{FONT}" font-size="50" fill="#FFF6EA" text-anchor="middle">{tr("Link na descrição")}</text></g>')
        out += M(t, 1650, 1040, 1.1, "happy", op=op, mouth=meow(t))
    return out


# ---------- composição ----------
CUTS = [T["e1"], T["e2"], T["e3"], T["fim"], T["japao"]]


def dip(t):
    op = 0.0
    for c in CUTS:
        if c - 0.3 <= t < c + 0.3:
            op = max(op, 1 - abs(t - c) / 0.3)
    if t < 0.6:
        op = max(op, 1 - t / 0.6)
    if t > TOTAL - 1.2:
        op = max(op, ease((t - (TOTAL - 1.2)) / 1.2))
    return f'<rect width="{W}" height="{H}" fill="#000" opacity="{op:.2f}"/>' if op > 0.01 else ""


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
FRAMES = os.path.join(DIR, "frames_trabalhos" + SUF)


def render_one(n):
    p = os.path.join(FRAMES, f"f{n:05d}.png")
    if not os.path.exists(p):
        cairosvg.svg2png(bytestring=frame_svg(n / FPS).encode(), write_to=p)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "render":
        for s in sys.argv[1:]:
            cairosvg.svg2png(bytestring=frame_svg(float(s)).encode(), write_to=os.path.join(DIR, f"prev_trab_{s}.png"))
        sys.exit()
    os.makedirs(FRAMES, exist_ok=True)
    with Pool(2) as pool:
        pool.map(render_one, range(int(FPS * TOTAL)), chunksize=48)
    out = os.path.join(DIR, "mochi_trabalhos" + SUF + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(FRAMES, "f%05d.png"),
                    "-i", os.path.join(DIR, "musica_trabalhos.wav"), "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out)
