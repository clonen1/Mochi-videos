"""'O Mochi desapareceu' (1920x1080, 24 fps, 96 s). Sem falas: conta-se com animação. Divulga o PetPapers.

casa (0-10) | caixa (10-28) | cesto (28-46) | site e cartaz (46-66) | cortina e foto (66-84) | cartões (84-96)
"""
import math
import os
import subprocess
import sys
from multiprocessing import Pool

import cairosvg

from mochi_longo import (H, W, FPS, FONT, INK, M, burst, caption, clamp, ease, ease_out, fade, lerp, person, spring, walk_bob)
from tempos_desaparecido import *  # noqa: F401,F403
from video_trabalhos import room_bg

VAQUINHA = "gofund.me/5d9e87b27"
CUTS = [T["e1"], T["e2"], T["site"], T["e3"], T["cartaoA"]]
PS = 1.7          # escala da pessoa
FLOOR = 935


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
            f'stroke="{INK}" stroke-width="3">Procura {n}</text>'
            f'<text x="620" y="570" font-family="{FONT}" font-weight="bold" font-size="120" fill="#FFFFFF" stroke="{INK}" stroke-width="5">{name}</text></g>'
            f'<g transform="translate(1560,520) scale({max(ic, 0.001):.2f})">{icon}</g></g>')


def icon_box():
    return (f'<g><rect x="-110" y="-70" width="220" height="150" fill="#C9965B" stroke="{INK}" stroke-width="8"/>'
            f'<polygon points="-110,-70 -150,-120 -40,-120 -30,-70" fill="#D9A96B" stroke="{INK}" stroke-width="8"/>'
            f'<polygon points="110,-70 150,-120 40,-120 30,-70" fill="#D9A96B" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="-30" y="-70" width="60" height="30" fill="#E9D3A8"/></g>')


def icon_basket():
    return (f'<g><path d="M-120 -40 H120 L95 90 H-95 Z" fill="#C8A06A" stroke="{INK}" stroke-width="8"/>'
            f'<line x1="-108" y1="10" x2="108" y2="10" stroke="{INK}" stroke-width="5"/><line x1="-100" y1="50" x2="100" y2="50" stroke="{INK}" stroke-width="5"/>'
            f'<ellipse cx="-40" cy="-50" rx="60" ry="30" fill="#D8343A" stroke="{INK}" stroke-width="6"/><ellipse cx="50" cy="-55" rx="55" ry="28" fill="#3F6FB0" stroke="{INK}" stroke-width="6"/></g>')


def icon_curtain():
    return (f'<g><rect x="-120" y="-120" width="240" height="14" fill="{INK}"/><path d="M-110 -106 H110 V110 H-110 Z" fill="#E6794A" stroke="{INK}" stroke-width="8"/>'
            + "".join(f'<line x1="{x}" y1="-100" x2="{x}" y2="104" stroke="#B4532C" stroke-width="6"/>' for x in (-60, 0, 60)) + '</g>')


def bowl(x, y):
    return (f'<g transform="translate({x},{y})"><ellipse cx="0" cy="6" rx="110" ry="14" fill="#000" opacity="0.15"/>'
            f'<path d="M-95 -56 H95 L72 0 H-72 Z" fill="#3F6FB0" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<ellipse cx="-30" cy="-60" rx="26" ry="14" fill="#B8774A" stroke="{INK}" stroke-width="4"/><ellipse cx="22" cy="-64" rx="30" ry="16" fill="#C98A58" stroke="{INK}" stroke-width="4"/>'
            f'<ellipse cx="62" cy="-58" rx="22" ry="12" fill="#B8774A" stroke="{INK}" stroke-width="4"/></g>')


# ---------- cartaz ----------
def poster_art(t, uid, name="Mochi", photo=True, w=440, h=600):
    """Cartaz em coordenadas locais (0,0) a (w,h). A foto é o Mochi a meio de uma mordidela, nada favorável."""
    px, py, pw, ph = w * 0.1, h * 0.2, w * 0.8, h * 0.42
    out = (f'<rect width="{w}" height="{h}" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
           f'<rect x="8" y="8" width="{w - 16}" height="{h * 0.14:.0f}" fill="#D8343A"/>'
           f'<text x="{w / 2}" y="{h * 0.1:.0f}" font-family="{FONT}" font-weight="bold" font-size="{w * 0.125:.0f}" fill="#FFFFFF" text-anchor="middle">PROCURA-SE</text>'
           f'<defs><clipPath id="{uid}"><rect x="{px}" y="{py}" width="{pw}" height="{ph}"/></clipPath></defs>'
           f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="#CFE8F5" stroke="{INK}" stroke-width="5"/>')
    if photo:
        out += (f'<g clip-path="url(#{uid})">'
                + M(t, px + pw / 2, py + ph + 40, 0.66, "eat", rot=-9, mouth=0.9, shadow=False, blink=False, breathe=False) + '</g>')
    out += (f'<text x="{w / 2}" y="{h * 0.71:.0f}" font-family="{FONT}" font-weight="bold" font-size="{w * 0.12:.0f}" fill="{INK}" text-anchor="middle">{name}</text>'
            f'<text x="{w / 2}" y="{h * 0.77:.0f}" font-family="{FONT}" font-size="{w * 0.056:.0f}" fill="#555" text-anchor="middle">Gato laranja, muito guloso</text>'
            f'<rect x="{w * 0.2}" y="{h * 0.8:.0f}" width="{w * 0.6}" height="10" rx="5" fill="#BBB"/><rect x="{w * 0.28}" y="{h * 0.835:.0f}" width="{w * 0.44}" height="10" rx="5" fill="#BBB"/>')
    for i in range(6):
        out += f'<rect x="{8 + i * (w - 16) / 6:.0f}" y="{h * 0.88:.0f}" width="{(w - 16) / 6:.0f}" height="{h * 0.12 - 8:.0f}" fill="#FFF6EA" stroke="#999" stroke-width="2" stroke-dasharray="6 4"/>'
        out += f'<text x="{8 + (i + 0.5) * (w - 16) / 6:.0f}" y="{h * 0.9 + 10:.0f}" font-family="{FONT}" font-size="14" fill="#888" text-anchor="middle">Mochi</text>'
    return out


# ---------- ecrã do site ----------
def cursor(x, y, press=False):
    s = 0.92 if press else 1.0
    return (f'<g transform="translate({x:.0f},{y:.0f}) scale({s})"><polygon points="0,0 0,46 12,36 22,58 32,53 22,32 38,32" fill="#FFFFFF" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/></g>')


def paw_icon(x, y, s=1.0, col="#E8744A"):
    return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="14" rx="34" ry="28" fill="{col}"/>'
            f'<circle cx="-34" cy="-16" r="13" fill="{col}"/><circle cx="-12" cy="-34" r="13" fill="{col}"/><circle cx="14" cy="-34" r="13" fill="{col}"/><circle cx="36" cy="-16" r="13" fill="{col}"/></g>')


def tool_card(x, y, label, kind, hot=False):
    out = (f'<g transform="translate({x},{y})"><rect width="440" height="330" rx="26" fill="{"#FFE3D0" if hot else "#FFFFFF"}" stroke="{INK if hot else "#CFC8BC"}" stroke-width="{8 if hot else 5}"/>')
    if kind == 0:
        out += '<rect x="160" y="40" width="120" height="150" fill="#fff" stroke="#2B2B2B" stroke-width="5"/><rect x="160" y="40" width="120" height="30" fill="#D8343A"/><circle cx="220" cy="120" r="30" fill="#F2A14A"/>'
    elif kind == 1:
        out += '<rect x="160" y="40" width="120" height="150" rx="10" fill="#fff" stroke="#2B2B2B" stroke-width="5"/><rect x="180" y="70" width="80" height="10" rx="5" fill="#4EA66A"/><rect x="180" y="100" width="80" height="10" rx="5" fill="#4EA66A"/><rect x="180" y="130" width="50" height="10" rx="5" fill="#4EA66A"/>'
    else:
        out += '<rect x="145" y="70" width="150" height="100" rx="14" fill="#fff" stroke="#2B2B2B" stroke-width="5"/><circle cx="190" cy="115" r="24" fill="#F2A14A"/><rect x="225" y="100" width="55" height="10" rx="5" fill="#999"/><rect x="225" y="125" width="40" height="10" rx="5" fill="#999"/>'
    out += f'<text x="220" y="260" font-family="{FONT}" font-weight="bold" font-size="34" fill="{INK}" text-anchor="middle">{label}</text></g>'
    return out


def screen_view(u, t):
    """u: segundos desde o início do ecrã."""
    out = (f'<rect x="120" y="90" width="1680" height="880" rx="26" fill="#FFF8EF" stroke="{INK}" stroke-width="10"/>'
           f'<path d="M130 100 H1790 V170 H130 Z" fill="#E8EAF0"/>'
           f'<circle cx="180" cy="135" r="12" fill="#D8343A"/><circle cx="220" cy="135" r="12" fill="#F6C343"/><circle cx="260" cy="135" r="12" fill="#4EA66A"/>'
           f'<rect x="330" y="112" width="1000" height="46" rx="23" fill="#FFFFFF" stroke="#C9CCD6" stroke-width="3"/>'
           f'<text x="830" y="147" font-family="{FONT}" font-size="30" fill="#666" text-anchor="middle">petpapers</text>')
    c1 = S_CLICK1 - S_SCR[0]
    form = u >= c1 + 0.5
    if not form:
        out += paw_icon(270, 290, 1.5) + (f'<text x="360" y="300" font-family="{FONT}" font-weight="bold" font-size="96" fill="#E8744A">PetPapers</text>'
                                          f'<text x="210" y="380" font-family="{FONT}" font-size="42" fill="#555">Grátis, no navegador, sem conta</text>')
        hot = u >= c1 - 0.1
        out += tool_card(200, 450, "Cartaz de animal perdido", 0, hot) + tool_card(740, 450, "Ficha de cuidados", 1) + tool_card(1280, 450, "Cartão de identificação", 2)
        cx = lerp(1500, 420, ease(clamp((u - 0.4) / (c1 - 0.4)))) if u < c1 + 0.5 else 420
        cy = lerp(880, 640, ease(clamp((u - 0.4) / (c1 - 0.4))))
        out += cursor(cx, cy, press=c1 - 0.1 <= u < c1 + 0.15)
    else:
        v = u - (c1 + 0.5)
        typed = clamp(int(max(0, (u - (S_TYPE0 - S_SCR[0])) / 0.4)) , 0, 5)
        name = "Mochi"[:typed]
        photo = u >= S_PHOTO - S_SCR[0]
        out += paw_icon(210, 250, 0.8) + f'<text x="270" y="272" font-family="{FONT}" font-weight="bold" font-size="56" fill="#E8744A">PetPapers</text>'
        out += f'<text x="200" y="360" font-family="{FONT}" font-weight="bold" font-size="42" fill="{INK}">Cartaz de animal perdido</text>'
        out += (f'<text x="200" y="430" font-family="{FONT}" font-size="34" fill="#555">Nome</text>'
                f'<rect x="200" y="446" width="600" height="70" rx="14" fill="#fff" stroke="#8A8FA3" stroke-width="4"/>'
                f'<text x="224" y="496" font-family="{FONT}" font-size="42" fill="{INK}">{name}{"|" if int(u * 2) % 2 == 0 and typed < 5 else ""}</text>')
        out += (f'<text x="200" y="580" font-family="{FONT}" font-size="34" fill="#555">Foto</text>'
                f'<rect x="200" y="596" width="260" height="170" rx="14" fill="{"#CFE8F5" if photo else "#fff"}" stroke="#8A8FA3" stroke-width="4" stroke-dasharray="{"0" if photo else "12 8"}"/>')
        if photo:
            k = spring((u - (S_PHOTO - S_SCR[0])) / 0.5)
            out += (f'<defs><clipPath id="thumb"><rect x="200" y="596" width="260" height="170" rx="14"/></clipPath></defs><g clip-path="url(#thumb)">'
                    + M(t, 330, 800, 0.46 * max(k, 0.01), "eat", rot=-9, mouth=0.9, shadow=False, blink=False, breathe=False) + '</g>')
        else:
            out += f'<text x="330" y="696" font-family="{FONT}" font-size="30" fill="#999" text-anchor="middle">Escolher foto</text>'
        pr = u >= S_PRINT - S_SCR[0]
        out += (f'<rect x="520" y="620" width="280" height="70" rx="14" fill="#DDD"/><rect x="520" y="706" width="280" height="60" rx="14" fill="#DDD"/>'
                f'<rect x="200" y="830" width="300" height="84" rx="42" fill="{"#B4532C" if pr else "#E8744A"}"/>'
                f'<text x="350" y="887" font-family="{FONT}" font-weight="bold" font-size="42" fill="#fff" text-anchor="middle">Imprimir</text>')
        out += f'<g transform="translate(1050,200) scale(1.0)">' + poster_art(t, "pv", name or " ", photo) + '</g>'
        # cursor: segue para o botão
        a0 = S_PRINT - S_SCR[0] - 1.2
        if u >= a0:
            k = ease(clamp((u - a0) / 1.0))
            out += cursor(lerp(1000, 380, k), lerp(600, 880, k), press=pr and u < S_PRINT - S_SCR[0] + 0.3)
    return out


# ---------- cenas ----------
def s_casa(lt):
    out = room_bg() + bowl(1500, FLOOR + 6)
    mx, my, expr = 1100.0, FLOOR, "normal"
    if lt >= C_SHOCK:
        expr = "shock"
        mx = lerp(1100, 2400, ease((lt - (C_SHOCK + 0.2)) / 1.3))
        my = FLOOR - abs(math.sin((lt - C_SHOCK) * 9)) * 60 * (lt < C_SHOCK + 1.5)
    px = lerp(-250, 450, ease(lt / 3.0))
    walking = lt < 3.0
    bob, _ = walk_bob(lt, 3.4, 10) if walking else (0, 0)
    flip = 1
    if lt >= 4.8:
        flip = 1 if int((lt - 4.8) / 1.1) % 2 == 0 else -1
    mood = "shock" if lt >= 7.8 else "neutral"
    if mx < 2200:
        out += M(lt, mx, my, 1.6, expr, mouth=meow(lt), flip=1)
    out += person(px, FLOOR, PS, mood, flip, bob=bob)
    out += burst(fade(lt, C_SHOCK + 0.1, C_SHOCK + 1.1, 0.1, 0.4), 1100, 420, "!", 110, r=120, rot=-6)
    out += caption(fade(lt, C_CALL, 7.4), "Mochi? É hora do jantar!")
    out += caption(fade(lt, 7.6, 9.8), "Onde se meteu?")
    return out


def box_scene(lt):
    """Caixa de cartao com o Mochi la dentro: so se veem as orelhas."""
    peek = 0.0
    if lt >= B_PEEK:
        peek = ease((lt - B_PEEK) / 0.8) * (1 - ease((lt - (B_PEEK + 2.6)) / 0.6))
    my = 1062 - 70 * peek
    rot = 2.2 * math.sin(lt * 5.5) if 3.0 <= lt < 9.0 else 0
    out = (f'<polygon points="940,725 880,660 1010,660 1000,725" fill="#D9A96B" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
           f'<polygon points="1360,725 1420,660 1290,660 1300,725" fill="#D9A96B" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    out += '<defs><clipPath id="boxclip"><rect x="0" y="0" width="1920" height="945"/></clipPath></defs><g clip-path="url(#boxclip)">'
    out += M(lt, 1150, my, 1.2, "happy" if peek > 0.3 else "normal", rot=rot, shadow=False, mouth=meow(10 + lt))
    out += '</g>'
    out += (f'<rect x="960" y="725" width="400" height="220" fill="#C9965B" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="1100" y="725" width="120" height="60" fill="#E9D3A8" stroke="{INK}" stroke-width="4"/>')
    return out


def s_e1(lt):
    out = room_bg() + box_scene(lt)
    px, flip, bob = 450.0, 1, 0.0
    walking = False
    if B_WALK[0] <= lt < B_WALK[1]:
        px = lerp(450, 800, ease((lt - B_WALK[0]) / (B_WALK[1] - B_WALK[0])))
        walking = True
    elif lt >= B_WALK[1]:
        px = 800
    if lt >= 7.0 and lt < 8.4:
        flip = 1 if int((lt - 7.0) / 0.4) % 2 == 0 else -1
    if lt >= 10.6:
        k = ease((lt - 10.6) / 2.8)
        px = lerp(800, -250, k)
        flip = -1
        walking = True
    if walking:
        bob, _ = walk_bob(lt, 3.4, 10)
    out += person(px, FLOOR, PS, "neutral", flip, bob=bob)
    out += caption(fade(lt, B_NOT, 10.6), "Aqui não está.")
    out += title_card(lt, 1, "Caixa", "#D9A96B", "#8E6A3A", icon_box())
    return out


def sock(x, y, rot=0.0, s=1.0):
    return (f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot:.0f}) scale({s})"><path d="M-20 -60 H20 V10 Q20 40 50 40 Q70 52 60 70 H-10 Q-24 70 -24 50 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<rect x="-22" y="-60" width="44" height="18" fill="#D8343A" stroke="{INK}" stroke-width="4"/></g>')


def s_e2(lt):
    out = room_bg()
    bx = 1250
    out += (f'<ellipse cx="{bx}" cy="944" rx="210" ry="22" fill="#000" opacity="0.15"/>')
    # cauda do Mochi a sair do cesto
    tail = 0.0
    if K_TAIL <= lt < K_SOCK:
        tail = ease((lt - K_TAIL) / 0.6)
    if tail > 0 or (lt >= K_SOCK and lt < K_SOCK + 0.3):
        if lt >= K_SOCK:
            tail = max(0.0, 1 - (lt - K_SOCK) / 0.25)
        sw = 28 * math.sin(lt * 6)
        out += (f'<path d="M{bx + 150} 780 Q{bx + 230 + sw:.0f} 760 {bx + 210 + sw:.0f} {780 - 200 * tail:.0f} Q{bx + 190 + sw:.0f} {700 - 230 * tail:.0f} {bx + 240 + sw * 1.4:.0f} {620 - 250 * tail:.0f}" '
                f'fill="none" stroke="{INK}" stroke-width="58" stroke-linecap="round"/>'
                f'<path d="M{bx + 150} 780 Q{bx + 230 + sw:.0f} 760 {bx + 210 + sw:.0f} {780 - 200 * tail:.0f} Q{bx + 190 + sw:.0f} {700 - 230 * tail:.0f} {bx + 240 + sw * 1.4:.0f} {620 - 250 * tail:.0f}" '
                f'fill="none" stroke="#F2A14A" stroke-width="44" stroke-linecap="round"/>')
    out += (f'<path d="M{bx - 190} 700 H{bx + 190} L{bx + 160} 935 H{bx - 160} Z" fill="#C8A06A" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
            f'<line x1="{bx - 182}" y1="770" x2="{bx + 182}" y2="770" stroke="{INK}" stroke-width="5"/><line x1="{bx - 174}" y1="840" x2="{bx + 174}" y2="840" stroke="{INK}" stroke-width="5"/>'
            f'<ellipse cx="{bx - 80}" cy="690" rx="110" ry="46" fill="#D8343A" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="{bx + 40}" cy="672" rx="100" ry="44" fill="#3F6FB0" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="{bx + 120}" cy="696" rx="80" ry="38" fill="#F6C343" stroke="{INK}" stroke-width="6"/>')
    px, flip, bob, walking, mood = 400.0, 1, 0.0, False, "neutral"
    if lt < 2.5:
        px, walking = lerp(-250, 400, ease(lt / 2.5)), True
    elif lt < 6.5:
        px, walking = lerp(400, 860, ease((lt - 2.5) / 4.0)), True
    else:
        px = 860
    if lt >= K_TAIL:
        mood = "shock"
    if lt >= K_SOCK + 1.4:
        mood = "neutral"
    if walking:
        bob, _ = walk_bob(lt, 3.4, 10)
    out += person(px, FLOOR, PS, mood, flip, bob=bob, arms=1.0 if K_REACH <= lt < K_SOCK + 1.4 else 0.0)
    # a meia voa do cesto para a mão
    if K_SOCK <= lt < K_SOCK + 1.0:
        u = ease((lt - K_SOCK) / 1.0)
        sx_, sy_ = lerp(bx, px + 130, u), lerp(690, 880, u) - 330 * math.sin(math.pi * u)
        out += sock(sx_, sy_, rot=lerp(-30, 160, u), s=0.9)
    elif lt >= K_SOCK + 1.0:
        out += sock(px + 130, 880, rot=170, s=0.9)
    out += caption(fade(lt, K_SOCK + 1.3, 13.4), "Só uma meia.")
    out += title_card(lt, 2, "Cesto", "#C8A06A", "#8A6A3A", icon_basket())
    return out


def s_site(lt):
    out = room_bg()
    # mesa, portátil e impressora
    out += (f'<rect x="880" y="740" width="720" height="34" rx="8" fill="#8E5B34" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="920" y="774" width="30" height="170" fill="#7A4B28"/><rect x="1530" y="774" width="30" height="170" fill="#7A4B28"/>')
    out += (f'<path d="M1010 600 H1300 L1320 730 H990 Z" fill="#2B2B2B" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M1020 612 H1290 L1306 716 H1006 Z" fill="#CFE8F5"/>'
            f'<path d="M960 730 H1350 L1370 742 H940 Z" fill="#8A8FA3" stroke="{INK}" stroke-width="5"/>')
    out += (f'<rect x="1400" y="620" width="190" height="120" rx="16" fill="#E4E6EE" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="1430" y="640" width="130" height="14" rx="7" fill="#8A8FA3"/>')
    # papel a sair
    printing = P_OUT <= lt < P_TAKE
    px = 640.0
    flip = 1
    walking = False
    if lt >= S_SCR[1] + 0.2 and lt < P_TAKE - 1.6:
        px = lerp(640, 1250, ease((lt - (S_SCR[1] + 0.2)) / 2.8))
        walking = True
    elif lt >= P_TAKE - 1.6 and lt < P_TAKE + 0.4:
        px = 1250
    elif lt >= P_TAKE + 0.4:
        px = lerp(1250, -300, ease((lt - (P_TAKE + 0.4)) / 2.4))
        flip = -1
        walking = True
    bob, _ = walk_bob(lt, 3.4, 10) if walking else (0, 0)
    mood = "angry" if lt < 1.0 else "neutral"
    if lt >= P_TAKE - 0.5:
        mood = "neutral"
    out += person(px, FLOOR, PS, mood, flip, bob=bob)
    if P_OUT <= lt < P_TAKE:
        u = clamp((lt - P_OUT) / 2.4)
        shake = 3 * math.sin(lt * 40) if u < 1 else 0
        out += (f'<g transform="translate({1432 + shake:.0f},{640 - 170 * ease(u):.0f}) scale(0.32)">' + poster_art(lt, "pr") + '</g>')
        out += (f'<rect x="1400" y="620" width="190" height="120" rx="16" fill="none" stroke="{INK}" stroke-width="6"/>')
    if lt >= P_TAKE:
        k = clamp((lt - P_TAKE) / 0.6)
        hx, hy = lerp(1480, px + 120, k), lerp(450, 700, k)
        out += f'<g transform="translate({hx:.0f},{hy:.0f}) scale(0.4)">' + poster_art(lt, "ph") + '</g>'
    out += caption(fade(lt, 0.8, 3.6), "Hora de pedir ajuda.")
    out += caption(fade(lt, P_TAKE + 0.3, 19.8), "Já está.")
    if S_SCR[0] <= lt < S_SCR[1] + 0.4:
        op = ease((lt - S_SCR[0]) / 0.5) * (1 - ease((lt - (S_SCR[1] - 0.2)) / 0.5))
        out += f'<g opacity="{op:.2f}"><rect width="{W}" height="{H}" fill="#E7E2D8"/>' + screen_view(lt - S_SCR[0], lt) + '</g>'
    return out


def curtain(lt):
    sway = 4 * math.sin(lt * 1.3)
    out = (f'<rect x="1270" y="80" width="430" height="14" fill="{INK}"/>'
           f'<path d="M1280 94 H1690 V935 H1280 Z" fill="#E6794A" stroke="{INK}" stroke-width="8"/>')
    for i in range(1, 8):
        x = 1280 + i * 410 / 8 + sway * (i % 2 - 0.5) * 0.3
        out += f'<line x1="{x:.0f}" y1="100" x2="{x:.0f}" y2="930" stroke="#B4532C" stroke-width="6" opacity="0.7"/>'
    if W_BULGE[0] <= lt < W_BULGE[1]:
        u = (lt - W_BULGE[0]) / (W_BULGE[1] - W_BULGE[0])
        bx = 1480 + 60 * math.sin(u * 9)
        out += f'<ellipse cx="{bx:.0f}" cy="720" rx="90" ry="170" fill="#FFFFFF" opacity="{0.20 * math.sin(math.pi * u):.2f}"/>'
    return out


def s_e3(lt):
    out = room_bg()
    # cartaz na parede
    pos = (110, 190)
    if lt >= W_STICK:
        k = ease(clamp((lt - W_STICK) / 0.4))
        sc = 0.82
        out += f'<g transform="translate({pos[0]},{pos[1]}) scale({sc})">' + poster_art(lt, "pw") + '</g>'
        for cx, cy in ((pos[0], pos[1]), (pos[0] + 440 * sc, pos[1]), (pos[0], pos[1] + 600 * sc), (pos[0] + 440 * sc, pos[1] + 600 * sc)):
            out += f'<rect x="{cx - 22:.0f}" y="{cy - 12:.0f}" width="44" height="24" fill="#F6C343" opacity="{0.8 * k:.2f}" transform="rotate(-20 {cx:.0f} {cy:.0f})"/>'
    # Mochi (por trás da cortina até sair)
    mx, expr, flip, sx, sy = 1480.0, "normal", -1, 1.0, 1.0
    if lt >= W_OUT:
        u = ease((lt - W_OUT) / 2.2)
        mx = lerp(1480, 1060, u)
        if lt < W_OUT + 2.6:
            expr = "normal"
        mouth = 0.0
    yawn = W_OUT + 1.6 <= lt < W_OUT + 2.8
    mouth = 0.9 if yawn else 0.0
    if yawn:
        k = math.sin(math.pi * (lt - (W_OUT + 1.6)) / 1.2)
        sy, sx = 1 + 0.12 * k, 1 - 0.06 * k
    if lt >= W_SEE:
        expr = "shock"
    if lt >= W_ANGRY:
        expr = "angry"
    if lt >= 16.2:
        expr = "sad"
        flip = 1
    mb = walk_bob(lt, 3.4, 12)[0] if W_OUT <= lt < W_OUT + 2.2 else 0
    out += M(lt, mx, FLOOR + mb, 1.6, expr, flip=flip, sx=sx, sy=sy, mouth=mouth or meow(66 + lt))
    out += curtain(lt)
    # pessoa com o cartaz
    px, flip_p, bob, walking = 640.0, 1, 0.0, False
    if lt < 2.5:
        px, walking = lerp(-250, 640, ease(lt / 2.5)), True
    elif lt < 5.8 and lt >= 2.5:
        px = 640
    mood = "neutral" if lt < W_OUT else "shock"
    if lt >= W_OUT + 1.6:
        mood = "neutral"
    if walking:
        bob, _ = walk_bob(lt, 3.4, 10)
    out += person(px, FLOOR, PS, mood, flip_p, bob=bob)
    if lt < W_STICK:
        k = ease(clamp((lt - 2.0) / 3.0))
        out += f'<g transform="translate({lerp(px + 40, pos[0], k):.0f},{lerp(560, pos[1], k):.0f}) scale({lerp(0.4, 0.82, k):.2f})">' + poster_art(lt, "pc2") + '</g>'
    out += caption(fade(lt, 5.8, 8.2), "Agora vão encontrá-lo.")
    out += caption(fade(lt, 13.3, 15.8), "Essa foto?!")
    out += caption(fade(lt, 16.1, 18.0), "Não me favorece.")
    out += title_card(lt, 3, "Cortina", "#E6794A", "#A84A24", icon_curtain())
    return out


def card_a(t):
    lt = t - T["cartaoA"]
    op = ease(lt / 0.6)
    return (f'<g opacity="{op:.2f}"><defs><linearGradient id="ca" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2E8C8C"/><stop offset="1" stop-color="#1F5F70"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#ca)"/>'
            f'<g transform="translate(1330,230) rotate(5) scale(0.9)">' + poster_art(t, "pcard") + '</g>'
            f'<text x="120" y="330" font-family="{FONT}" font-weight="bold" font-size="104" fill="#FFF6EA">Perdeu um animal?</text>'
            f'<text x="120" y="450" font-family="{FONT}" font-weight="bold" font-size="84" fill="#F6C343">Faça um cartaz grátis</text>'
            f'<rect x="120" y="540" width="680" height="130" rx="65" fill="#E8744A"/>'
            + paw_icon(210, 606, 0.9, "#FFFFFF") +
            f'<text x="500" y="634" font-family="{FONT}" font-weight="bold" font-size="76" fill="#FFFFFF" text-anchor="middle">PetPapers</text>'
            f'<text x="120" y="790" font-family="{FONT}" font-size="56" fill="#FFF6EA">Link na descrição</text></g>')


def card_b(t):
    lt = t - T["cartaoB"]
    op = ease(lt / 0.6)
    return (f'<g opacity="{op:.2f}"><rect width="{W}" height="{H}" fill="#1E1B2E"/>'
            f'<text x="960" y="360" font-family="{FONT}" font-weight="bold" font-size="96" fill="#FFF6EA" text-anchor="middle">Ajuda o Mochi</text>'
            f'<text x="960" y="470" font-family="{FONT}" font-weight="bold" font-size="80" fill="#F6C343" text-anchor="middle">a chegar ao Japão</text>'
            f'<rect x="560" y="550" width="800" height="112" rx="56" fill="#D8343A"/>'
            f'<text x="960" y="628" font-family="{FONT}" font-weight="bold" font-size="58" fill="#FFFFFF" text-anchor="middle">{VAQUINHA}</text>'
            f'<text x="960" y="760" font-family="{FONT}" font-size="50" fill="#FFF6EA" text-anchor="middle">Link na descrição</text></g>'
            + M(t, 1650, 1040, 1.1, "happy", op=op, mouth=meow(t)))


def frame_svg(t):
    if t < T["e1"]:
        body = s_casa(t)
    elif t < T["e2"]:
        body = s_e1(t - T["e1"])
    elif t < T["site"]:
        body = s_e2(t - T["e2"])
    elif t < T["e3"]:
        body = s_site(t - T["site"])
    elif t < T["cartaoA"]:
        body = s_e3(t - T["e3"])
    elif t < T["cartaoB"]:
        body = card_a(t)
    else:
        body = card_b(t)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="#FDE7D3"/>{body}{dip(t)}</svg>')


DIR = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(DIR, "frames_desaparecido")


def render_one(n):
    p = os.path.join(FRAMES, f"f{n:05d}.png")
    if not os.path.exists(p):
        cairosvg.svg2png(bytestring=frame_svg(n / FPS).encode(), write_to=p)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "render":
        for s in sys.argv[1:]:
            cairosvg.svg2png(bytestring=frame_svg(float(s)).encode(), write_to=os.path.join(DIR, f"prev_desap_{s}.png"))
        sys.exit()
    os.makedirs(FRAMES, exist_ok=True)
    with Pool(2) as pool:
        pool.map(render_one, range(int(FPS * TOTAL)), chunksize=48)
    out = os.path.join(DIR, "mochi_desaparecido.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(FRAMES, "f%05d.png"),
                    "-i", os.path.join(DIR, "musica_desaparecido.wav"), "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out)
