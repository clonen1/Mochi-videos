"""Vídeo grande 'O sonho do Mochi' (1920x1080, 24 fps, ~4 min). Sem falas: conta-se com animação.

1 casa (0-20) | 2 sonho: sushi, templo, arcade, Fuji (20-80) | 3 choque: mealheiro (80-110)
4 planos 1-3 (110-180) | 5 solução: vaquinha (180-210) | 6 final + cartões (210-246)
"""
import math
import os
import subprocess
import sys
from multiprocessing import Pool

import cairosvg

from mochi_kit import mochi, RED, RED_DARK
from musica_grande import COINS, CUPCAKES, MEOWS, SUSHI_BITES, T, TOTAL

W, H, FPS = 1920, 1080, 24
FONT = "DejaVu Sans"
DIR = os.path.dirname(os.path.abspath(__file__))
INK = "#2B2B2B"
VAQUINHA = "gofund.me/696fddb27"
SCARF = f'<rect x="112" y="228" width="156" height="24" rx="12" fill="{RED}"/><rect x="200" y="240" width="22" height="48" rx="8" fill="{RED_DARK}"/>'


# ---------- utilitários ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def spring(t):
    return 0 if t < 0 else 1 - math.exp(-t * 7) * math.cos(t * 16)


def fade(t, a, b, fin=0.4, fout=0.4):
    return ease((t - a) / fin) * (1 - ease((t - (b - fout)) / fout))


def meow_open(t):
    for t0 in MEOWS:
        if t0 <= t <= t0 + 0.55:
            return math.sin(math.pi * (t - t0) / 0.55) ** 0.8
    return 0.0


def auto_blink(t):
    return (t % 3.7) < 0.12


def M(t, x, y, s=1.3, expr="normal", flip=1, sx=1.0, rot=0, scarf=True, blink=None, headphones=False, op=1):
    """Mochi com os pés em (x, y)."""
    if blink is None:
        blink = auto_blink(t) and expr in ("normal", "angry", "eat")
    svg = mochi(expr, blink, headphones=headphones, mouth_open=meow_open(t) if expr not in ("eat", "sleep") else 0)
    if not scarf:
        svg = svg.replace(SCARF, "")
    return (f'<g opacity="{op:.2f}" transform="translate({x:.1f},{y:.1f}) rotate({rot:.1f}) scale({s * sx * flip:.3f},{s:.3f})">'
            f'<g transform="translate(-190,-378)">{svg}</g></g>')


def caption(op, txt, y=930, size=64):
    if op <= 0:
        return ""
    w = max(520, len(txt) * size * 0.62 + 120)
    return (f'<g opacity="{op:.2f}"><rect x="{(W - w) / 2:.0f}" y="{y - size - 18}" width="{w:.0f}" height="{size + 56}" rx="26" fill="#1E1B2E" opacity="0.88"/>'
            f'<rect x="{(W - w) / 2 + 10:.0f}" y="{y - size - 8}" width="{w - 20:.0f}" height="{size + 36}" rx="20" fill="none" stroke="#F6C343" stroke-width="3"/>'
            f'<text x="{W / 2}" y="{y + 8}" font-family="{FONT}" font-weight="bold" font-size="{size}" fill="#FFF6EA" text-anchor="middle">{txt}</text></g>')


def burst(op, x, y, word, size=80, r=130, color="#D8343A"):
    if op <= 0:
        return ""
    pts = []
    for i in range(24):
        rr = (r if i % 2 == 0 else r * 0.66) * (0.6 + 0.4 * op)
        a = math.pi * 2 * i / 24
        pts.append(f"{x + math.cos(a) * rr * 1.35:.0f},{y + math.sin(a) * rr:.0f}")
    return (f'<g opacity="{op:.2f}"><polygon points="{" ".join(pts)}" fill="#F6C343" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<text x="{x}" y="{y + size * 0.36:.0f}" font-family="{FONT}" font-weight="bold" font-size="{size}" fill="{color}" text-anchor="middle">{word}</text></g>')


def cam(inner, t, a, b, z0=1.0, z1=1.08, fx=960, fy=560):
    u = ease((t - a) / (b - a))
    z = z0 + (z1 - z0) * u
    return f'<g transform="translate({fx},{fy}) scale({z:.4f}) translate({-fx},{-fy})">{inner}</g>'


def sparkle(x, y, s, op=1):
    return (f'<path transform="translate({x:.0f},{y:.0f}) scale({s:.2f})" opacity="{op:.2f}" d="M0 -20 Q3 -3 20 0 Q3 3 0 20 Q-3 3 -20 0 Q-3 -3 0 -20Z" fill="#FFF3B0"/>')


def petals(t, n=18, op=1):
    out = ""
    for i in range(n):
        ph = i * 1.7
        x = (i * 113 + t * 60 + 40 * math.sin(t + ph)) % (W + 100) - 50
        y = (i * 71 + t * 90) % (H + 100) - 50
        out += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="11" ry="7" fill="#F7B6C8" opacity="{0.85 * op:.2f}" transform="rotate({(t * 80 + i * 40) % 360:.0f},{x:.0f},{y:.0f})"/>'
    return out


# ---------- cenários ----------
def fuji(x, y, w, h, snow=True):
    out = f'<polygon points="{x},{y + h} {x + w * 0.42},{y} {x + w * 0.58},{y} {x + w},{y + h}" fill="#5B6FA8"/>'
    if snow:
        out += (f'<polygon points="{x + w * 0.32},{y + h * 0.24} {x + w * 0.42},{y} {x + w * 0.58},{y} {x + w * 0.68},{y + h * 0.24} '
                f'{x + w * 0.6},{y + h * 0.2} {x + w * 0.54},{y + h * 0.28} {x + w * 0.47},{y + h * 0.2} {x + w * 0.4},{y + h * 0.28}" fill="#FFFFFF"/>')
    return out


def sunrise_sky(t0, t):
    u = ease((t - t0) / 10)
    sun_y = 760 - 330 * u
    return (f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6C5CE7"/>'
            f'<stop offset="0.6" stop-color="#FD9A8C"/><stop offset="1" stop-color="#FFD39A"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
            f'<circle cx="1300" cy="{sun_y:.0f}" r="120" fill="#FFE8A3" opacity="0.95"/>'
            + fuji(380, 330, 1160, 520) +
            '<rect x="0" y="830" width="1920" height="250" fill="#3E7D5A"/><rect x="0" y="830" width="1920" height="20" fill="#4E9A6E"/>')


def torii(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<rect x="-230" y="-380" width="460" height="40" rx="10" fill="#2B2B2B"/>'
            '<rect x="-210" y="-345" width="420" height="34" fill="#D8343A"/>'
            '<rect x="-190" y="-280" width="380" height="26" fill="#D8343A"/>'
            '<rect x="-170" y="-345" width="40" height="345" fill="#D8343A"/><rect x="130" y="-345" width="40" height="345" fill="#D8343A"/>'
            '<rect x="-180" y="-20" width="60" height="20" fill="#2B2B2B"/><rect x="120" y="-20" width="60" height="20" fill="#2B2B2B"/></g>')


def room(t, tv_on=False, night=False):
    out = (f'<rect width="{W}" height="{H}" fill="#FDE7D3"/>'
           '<rect x="0" y="820" width="1920" height="260" fill="#C98B52"/><rect x="0" y="810" width="1920" height="16" fill="#B5713A"/>'
           # janela
           '<rect x="180" y="150" width="380" height="300" rx="16" fill="#9ED3F0" stroke="#FFFFFF" stroke-width="16"/>'
           '<line x1="370" y1="150" x2="370" y2="450" stroke="#FFFFFF" stroke-width="12"/>'
           '<line x1="180" y1="300" x2="560" y2="300" stroke="#FFFFFF" stroke-width="12"/>'
           # sofá
           '<rect x="520" y="560" width="760" height="260" rx="60" fill="#7C8DB5"/>'
           '<rect x="480" y="640" width="120" height="200" rx="40" fill="#6A7AA0"/><rect x="1200" y="640" width="120" height="200" rx="40" fill="#6A7AA0"/>'
           '<rect x="590" y="690" width="620" height="110" rx="30" fill="#8FA0C8"/>'
           # TV
           '<rect x="1400" y="640" width="380" height="180" fill="#8A5A34"/>'
           '<rect x="1410" y="330" width="360" height="240" rx="18" fill="#2B2B2B"/><rect x="1570" y="570" width="40" height="70" fill="#2B2B2B"/>')
    if tv_on:
        out += ('<svg x="1428" y="348" width="324" height="204" viewBox="0 0 1920 1080">' + sunrise_sky(-20, 0)
                + torii(1500, 830, 0.8) + '</svg>')
    else:
        out += '<rect x="1428" y="348" width="324" height="204" fill="#3A3A48"/>'
    if night:
        out = out.replace("#9ED3F0", "#1F2A4A")
        out += f'<rect width="{W}" height="{H}" fill="#101530" opacity="0.55"/><circle cx="470" cy="230" r="34" fill="#FFF3C4" opacity="0.9"/>'
    return out


def bubble_frame(inner, op, cx=960, cy=540, r=None):
    """Bolha de pensamento que se abre até encher o ecrã."""
    if r is None:
        r = 1200
    return (f'<defs><clipPath id="bub"><circle cx="{cx}" cy="{cy}" r="{r:.0f}"/></clipPath></defs>'
            f'<g clip-path="url(#bub)" opacity="{op:.2f}">{inner}</g>'
            f'<circle cx="{cx}" cy="{cy}" r="{r:.0f}" fill="none" stroke="#FFFFFF" stroke-width="18" opacity="{op:.2f}"/>')


# ---------- cenas ----------
def s1_casa(t):
    tv = t >= 9
    out = room(t, tv_on=tv)
    eating = t < 10.6
    expr = "eat" if eating else ("shock" if t < 12.2 else "happy")
    bob = 6 * math.sin(t * 5) if eating else 0
    out += M(t, 880, 800 - bob, 1.25, expr)
    # taça de comida
    fy = 690 if t < 10.6 else 690 + 260 * clamp((t - 10.6) / 0.4) ** 2
    if t < 11.4:
        out += (f'<g transform="translate(1040,{fy:.0f})"><ellipse cx="0" cy="0" rx="70" ry="22" fill="#F6C343"/>'
                '<path d="M-70 0 Q0 70 70 0 Z" fill="#E28B2E"/></g>')
    if t >= 11.0:
        out += '<g transform="translate(1040,815)"><ellipse cx="0" cy="0" rx="70" ry="14" fill="#E28B2E" opacity="0.8"/></g>'
    if t >= 12.2:  # olhos a brilhar e baba
        for i, (x, y) in enumerate([(780, 520), (990, 500), (720, 600), (1050, 590)]):
            out += sparkle(x, y, 1 + 0.3 * math.sin(t * 6 + i), 0.9)
        d = clamp((t - 13) / 1.5)
        out += f'<ellipse cx="895" cy="{640 + 40 * d:.0f}" rx="9" ry="{12 + 18 * d:.0f}" fill="#9ED3F0" opacity="0.9"/>'
    if 9 <= t < 10.5:
        out += burst(ease((t - 9) / 0.3) * (1 - ease((t - 10.2) / 0.3)), 1590, 300, "!", 90, 70)
    out = cam(out, t, 0, 20, 1.0, 1.18, 1200, 520)
    out += caption(fade(t, 14, 19.6), "O Mochi tem um sonho.")
    return out


def s2_sonho(t):
    # base: o Mochi na sala a sonhar, com bolhas pequenas a subir
    keys = ["sushi", "templo", "arcade", "fuji"]
    idx = min(3, int((t - 20) // 15))
    k = keys[idx]
    a = T[k]
    lt = t - a
    r = 60 + 1300 * ease((lt - 0.2) / 1.6) if lt < 1.8 else 1400
    base = room(t) + M(t, 900, 800, 1.25, "sleep")
    for i in range(3):
        base += f'<circle cx="{1010 + i * 50}" cy="{460 - i * 70}" r="{16 + i * 10}" fill="#FFFFFF" opacity="0.9"/>'
    inner = {"sushi": sushi, "templo": templo, "arcade": arcade, "fuji": fuji_scene}[k](t, lt)
    out = base + bubble_frame(inner, 1.0, 1140, 320 if lt < 1.8 else 540, r)
    words = {"sushi": "Comer.", "templo": "Passear.", "arcade": "Jogar.", "fuji": "Ver o Fuji."}
    out += caption(fade(t, a + 1.8, a + 5.0), words[k])
    return out


def sushi(t, lt):
    out = (f'<rect width="{W}" height="{H}" fill="#F3D9B1"/>'
           '<rect x="0" y="0" width="1920" height="120" fill="#7A3B2E"/>'
           + "".join(f'<rect x="{80 + i * 300}" y="20" width="180" height="80" rx="10" fill="#FFF6EA"/>'
                     f'<rect x="{80 + i * 300}" y="40" width="180" height="10" fill="#D8343A"/>' for i in range(7)) +
           '<rect x="0" y="760" width="1920" height="320" fill="#A0643A"/><rect x="0" y="700" width="1920" height="70" fill="#8C8C96"/>')
    for i in range(9):  # tapete rolante
        x = (i * 240 - lt * 160) % 2160 - 120
        out += (f'<g transform="translate({x:.0f},690)"><ellipse cx="0" cy="0" rx="80" ry="18" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="3"/>'
                '<rect x="-46" y="-40" width="92" height="38" rx="16" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="3"/>'
                f'<rect x="-46" y="-52" width="92" height="22" rx="10" fill="{"#F28C6B" if i % 2 else "#F6C343"}"/></g>')
    bites = sum(1 for b in SUSHI_BITES if t >= b)
    grow = 1 + 0.06 * bites
    chewing = any(b <= t < b + 0.5 for b in SUSHI_BITES)
    out += M(t, 960, 1000, 1.4, "eat" if chewing else "happy", sx=grow)
    out += f'<g transform="translate(1250,940)">' + "".join(f'<rect x="{-60}" y="{-i * 16}" width="120" height="14" rx="6" fill="#{"E9E3D8" if i % 2 else "D7CFC2"}" stroke="#2B2B2B" stroke-width="2"/>' for i in range(bites)) + '</g>'
    return out


def templo(t, lt):
    out = (f'<rect width="{W}" height="{H}" fill="#BFE3F2"/>' + fuji(1150, 260, 700, 420) +
           '<rect x="0" y="820" width="1920" height="260" fill="#D8C7A4"/>'
           # templo
           '<rect x="300" y="460" width="520" height="360" fill="#8E3B2E"/>'
           '<polygon points="240,470 560,330 880,470" fill="#3B3B46"/>'
           '<rect x="460" y="620" width="200" height="200" fill="#5B2A22"/>')
    out += torii(1300, 830, 0.9)
    swing = math.sin((t - 40) * 6) * 18 * math.exp(-max(0, t - 40) * 0.6) if t >= 40 else 0
    out += (f'<g transform="translate(980,360) rotate({swing:.1f})"><line x1="0" y1="0" x2="0" y2="120" stroke="#8B5A2B" stroke-width="8"/>'
            '<path d="M-55 120 Q-55 60 0 60 Q55 60 55 120 L65 190 L-65 190 Z" fill="#E1B23C" stroke="#2B2B2B" stroke-width="5"/>'
            '<line x1="0" y1="190" x2="0" y2="330" stroke="#D8343A" stroke-width="10"/></g>')
    hop = abs(math.sin((t - 36) * 3)) * 40 if t < 39.5 else 0
    x = 300 + 640 * ease((t - 35.5) / 3.5)
    expr = "happy" if t < 39.5 or t > 44 else ("shock" if t < 41 else "normal")
    out += M(t, x, 1000 - hop, 1.2, expr)
    out += burst(fade(t, 40, 42, 0.15, 0.4), 1250, 330, "DONG!", 70, 110)
    out += petals(t, 12)
    return out


def arcade(t, lt):
    out = (f'<rect width="{W}" height="{H}" fill="#24183F"/>'
           + "".join(f'<circle cx="{(i * 237) % 1920}" cy="{(i * 151) % 600}" r="4" fill="#{"4FD1C5" if i % 2 else "F7A9D8"}" opacity="{0.4 + 0.4 * math.sin(t * 3 + i):.2f}"/>' for i in range(30)) +
           '<rect x="0" y="860" width="1920" height="220" fill="#3A2A5E"/>')
    # máquina
    out += ('<rect x="1180" y="240" width="460" height="640" rx="30" fill="#3F6FB0" stroke="#2B2B2B" stroke-width="6"/>'
            '<rect x="1230" y="300" width="360" height="270" rx="12" fill="#111"/>'
            '<rect x="1220" y="620" width="380" height="80" rx="16" fill="#2B4E80"/>'
            '<circle cx="1300" cy="660" r="20" fill="#D8343A"/><circle cx="1380" cy="660" r="20" fill="#F6C343"/><circle cx="1460" cy="660" r="20" fill="#4FD1C5"/>')
    # ecrã: blocos a cair
    for i in range(6):
        y = 300 + ((lt * 140 + i * 47) % 260)
        out += f'<rect x="{1250 + i * 55}" y="{y:.0f}" width="44" height="44" fill="#{["F6C343", "4FD1C5", "F7A9D8", "8FD14F", "F28C6B", "9B6BCB"][i]}"/>'
    win = t >= 60
    expr = "happy" if win else ("angry" if lt > 2 else "normal")
    shake = math.sin(t * 40) * 6 if 52 <= t < 60 else 0
    out += M(t, 900 + shake, 1000, 1.35, expr, headphones=True)
    out += burst(fade(t, 60, 64, 0.2, 0.5), 1410, 430, "GANHEI!", 64, 120)
    if win:
        for i in range(10):
            out += sparkle(700 + i * 110, 200 + 80 * math.sin(i + t * 4), 1.2, 0.9)
    return out


def fuji_scene(t, lt):
    out = sunrise_sky(65, t) + torii(400, 840, 0.75)
    x = 1160 + 15 * math.sin(t)
    out += M(t, x, 1010, 1.2, "happy" if lt > 3 else "normal", flip=-1 if lt < 3 else 1)
    out += petals(t, 20)
    return out


def s3_choque(t):
    out = room(t)
    pop = 1 - ease((t - 80) / 0.3)
    if pop > 0:
        out += burst(pop, 1140, 360, "POP!", 80, 120)
    # mealheiro
    shaking = 88 <= t < 92.5
    hold = t >= 85
    pig_x = 1380 if not hold else 1380 - 260 * ease((t - 85) / 1.5)
    pig_y = 760 if not shaking else 600 + math.sin(t * 50) * 30
    if t >= 92.5:
        pig_y = 640
    pig_rot = 180 * ease((t - 92) / 0.5) if t >= 92 else 0
    if t < 103.5:
        out += (f'<g transform="translate({pig_x:.0f},{pig_y:.0f}) rotate({pig_rot:.0f})">'
                '<ellipse cx="0" cy="0" rx="110" ry="80" fill="#F7A9C0" stroke="#2B2B2B" stroke-width="5"/>'
                '<ellipse cx="100" cy="0" rx="28" ry="24" fill="#F28AAA" stroke="#2B2B2B" stroke-width="4"/>'
                '<circle cx="95" cy="-4" r="4" fill="#2B2B2B"/><circle cx="108" cy="-4" r="4" fill="#2B2B2B"/>'
                '<circle cx="55" cy="-30" r="7" fill="#2B2B2B"/><rect x="-30" y="-82" width="50" height="10" rx="4" fill="#2B2B2B"/>'
                '<polygon points="30,-70 50,-110 70,-60" fill="#F7A9C0" stroke="#2B2B2B" stroke-width="4"/>'
                '<rect x="-80" y="60" width="26" height="40" fill="#F7A9C0" stroke="#2B2B2B" stroke-width="4"/>'
                '<rect x="40" y="60" width="26" height="40" fill="#F7A9C0" stroke="#2B2B2B" stroke-width="4"/></g>')
    if t >= 93:  # moeda cai
        u = clamp((t - 93) / 0.5)
        cy = 700 + 110 * u * u
        if t > 93.5:
            cy = 810 - 20 * abs(math.sin((t - 93.5) * 8)) * math.exp(-(t - 93.5) * 3)
        out += f'<g transform="translate(1120,{cy:.0f})"><ellipse cx="0" cy="0" rx="30" ry="30" fill="#F6C343" stroke="#B88A1B" stroke-width="5"/><text x="0" y="12" font-family="{FONT}" font-weight="bold" font-size="32" fill="#B88A1B" text-anchor="middle">1</text></g>'
    if t >= 95:  # aranha
        sy = 560 + 120 * ease((t - 95) / 2) + 10 * math.sin(t * 3)
        out += (f'<line x1="1250" y1="440" x2="1250" y2="{sy:.0f}" stroke="#555" stroke-width="2"/>'
                f'<g transform="translate(1250,{sy:.0f})"><circle r="16" fill="#2B2B2B"/>'
                + "".join(f'<path d="M0 0 L{s * 30} {k * 10 - 10} L{s * 36} {k * 12}" stroke="#2B2B2B" stroke-width="3" fill="none"/>' for s in (-1, 1) for k in range(3)) +
                '<circle cx="-5" cy="-4" r="3" fill="#fff"/><circle cx="5" cy="-4" r="3" fill="#fff"/></g>')
    if t < 88:
        expr = "happy"
    elif t < 93:
        expr = "normal"
    elif t < 103.5:
        expr = "shock"
    else:
        expr = "ko"
    rot = -90 * ease((t - 103.5) / 0.5) if t >= 103.5 else 0
    hop = 30 * abs(math.sin(t * 9)) if shaking else 0
    out += M(t, 760, 800 - hop, 1.25, expr, rot=rot)
    out = cam(out, t, 92, 104, 1.0, 1.25, 1000, 600)
    out += caption(fade(t, 98, 103), "Só falta uma coisa...")
    return out


def plano_card(t, s, n):
    op = fade(t, s, s + 2.4, 0.2, 0.4)
    if op <= 0:
        return ""
    return (f'<g opacity="{op:.2f}"><rect width="{W}" height="{H}" fill="#1E1B2E"/>'
            f'<rect x="560" y="390" width="800" height="300" rx="30" fill="none" stroke="#F6C343" stroke-width="8"/>'
            f'<text x="960" y="580" font-family="{FONT}" font-weight="bold" font-size="130" fill="#FFF6EA" text-anchor="middle">Plano {n}</text></g>')


def street_bg(t):
    out = f'<rect width="{W}" height="{H}" fill="#CDE8F5"/>'
    for i, (x, w, h, c) in enumerate([(0, 300, 520, "#E8C5A0"), (320, 260, 640, "#D9A27A"), (600, 340, 460, "#E5D3B3"),
                                      (960, 280, 600, "#CFA88A"), (1260, 320, 500, "#E8C5A0"), (1600, 320, 620, "#D9A27A")]):
        out += f'<rect x="{x}" y="{820 - h}" width="{w}" height="{h}" fill="{c}"/>'
        for r in range(3):
            for k in range(2):
                out += f'<rect x="{x + 50 + k * (w - 160)}" y="{820 - h + 60 + r * 140}" width="60" height="80" fill="#9ED3F0"/>'
    return out + '<rect x="0" y="820" width="1920" height="260" fill="#B8B8C0"/><rect x="0" y="820" width="1920" height="20" fill="#9A9AA4"/>'


def pigeon(x, y, flip=1, peck=0):
    return (f'<g transform="translate({x:.0f},{y:.0f}) scale({flip},1)"><ellipse cx="0" cy="-50" rx="55" ry="40" fill="#9AA0B5"/>'
            f'<g transform="rotate({peck:.0f},40,-80)"><circle cx="40" cy="-90" r="28" fill="#8A90A8"/><circle cx="50" cy="-95" r="5" fill="#2B2B2B"/>'
            '<polygon points="66,-90 86,-84 66,-80" fill="#F6C343"/></g>'
            '<path d="M-55 -50 L-90 -70 L-80 -40 Z" fill="#7A8098"/><line x1="-10" y1="-12" x2="-10" y2="0" stroke="#E77C8A" stroke-width="5"/>'
            '<line x1="15" y1="-12" x2="15" y2="0" stroke="#E77C8A" stroke-width="5"/></g>')


def p1(t):
    s = T["p1"]
    lt = t - s
    out = street_bg(t)
    # banca com o lenço
    out += ('<rect x="1050" y="640" width="360" height="30" fill="#8A5A34"/><rect x="1070" y="670" width="20" height="160" fill="#8A5A34"/>'
            '<rect x="1370" y="670" width="20" height="160" fill="#8A5A34"/>')
    if t < 124:
        sc_x, sc_y, sc_r = 1230, 620, 0
    else:
        u = clamp((t - 124) / 2.2)
        sc_x, sc_y, sc_r = 1230 + 900 * u, 620 - 500 * u + 300 * u * u * 0, 720 * u
    if t < 126.5:
        out += (f'<g transform="translate({sc_x:.0f},{sc_y:.0f}) rotate({sc_r:.0f})"><rect x="-90" y="-16" width="180" height="32" rx="14" fill="{RED}"/>'
                f'<rect x="20" y="0" width="30" height="60" rx="10" fill="{RED_DARK}"/></g>')
    out += f'<g transform="translate(1230,560)"><rect x="-70" y="-50" width="140" height="70" rx="10" fill="#FFF6EA" stroke="#2B2B2B" stroke-width="4"/><text x="0" y="5" font-family="{FONT}" font-weight="bold" font-size="40" fill="{RED}" text-anchor="middle">?</text></g>' if t < 124 else ""
    # pombos que passam e ignoram
    for k, (a, b) in enumerate([(114, 119), (118.5, 123.5)]):
        if a <= t < b:
            u = (t - a) / (b - a)
            x = -150 + 2200 * u if k == 0 else 2050 - 2200 * u
            stop = 0.45 < u < 0.6
            out += pigeon(x, 960, 1 if k == 0 else -1, 25 * math.sin(t * 12) if stop else 0)
    if 123.6 <= t < 127:  # vento
        for i in range(5):
            x = ((t - 123.6) * 1400 + i * 300) % 2300 - 300
            out += f'<path d="M{x:.0f} {380 + i * 90} q 120 -30 240 0" stroke="#FFFFFF" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.8"/>'
    expr = "happy" if t < 116 else ("normal" if t < 124 else ("shock" if t < 127.5 else "angry"))
    out += M(t, 860, 1000, 1.3, expr, scarf=False)
    out += plano_card(t, s, 1)
    return cam(out, t, s + 2, s + 23, 1.0, 1.06, 1000, 600)


def p2(t):
    s = T["p2"]
    out = (f'<rect width="{W}" height="{H}" fill="#E9DCC4"/><rect x="0" y="850" width="1920" height="230" fill="#9C7A54"/>')
    for i in range(4):
        for j in range(3 - (i % 2)):
            out += f'<rect x="{100 + i * 160}" y="{690 - j * 150}" width="150" height="150" fill="#C99A5E" stroke="#8A6A3E" stroke-width="5"/><rect x="{100 + i * 160}" y="{750 - j * 150}" width="150" height="16" fill="#E5C17E"/>'
    # relógio que gira depressa quando ele dorme
    spin = (t - s) * 40 if t < 142 else (t - s) * 40 + (t - 142) * 720
    out += (f'<circle cx="1500" cy="250" r="110" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="8"/>'
            f'<line x1="1500" y1="250" x2="{1500 + 70 * math.sin(math.radians(spin)):.0f}" y2="{250 - 70 * math.cos(math.radians(spin)):.0f}" stroke="#2B2B2B" stroke-width="8" stroke-linecap="round"/>'
            f'<line x1="1500" y1="250" x2="{1500 + 50 * math.sin(math.radians(spin / 12)):.0f}" y2="{250 - 50 * math.cos(math.radians(spin / 12)):.0f}" stroke="#D8343A" stroke-width="10" stroke-linecap="round"/>')
    # caixa e Mochi
    if t < 141:
        x = 1500 - 500 * ease((t - (s + 3)) / 6)
        hop = abs(math.sin(t * 6)) * 30 if t < s + 9 else 0
        out += M(t, x, 1000 - hop, 1.25, "happy" if t < 139 else "normal")
        out += f'<rect x="{x - 110:.0f}" y="{770 - hop:.0f}" width="220" height="170" fill="#C99A5E" stroke="#8A6A3E" stroke-width="6"/><rect x="{x - 110:.0f}" y="{830 - hop:.0f}" width="220" height="18" fill="#E5C17E"/>'
        if 139 <= t < 141:  # bocejo
            out += f'<ellipse cx="{x:.0f}" cy="{790:.0f}" rx="22" ry="{10 + 14 * math.sin(math.pi * (t - 139) / 2):.0f}" fill="#2B2B2B" opacity="0.0"/>'
    else:
        out += '<rect x="890" y="780" width="220" height="170" fill="#C99A5E" stroke="#8A6A3E" stroke-width="6"/><rect x="890" y="840" width="220" height="18" fill="#E5C17E"/>'
        wake = t >= 153
        out += M(t, 1000, 800 - (40 * spring(t - 153) if wake else 0), 1.2, "shock" if wake else "sleep")
        if not wake:
            for i in range(3):
                ph = ((t - 141) * 0.6 + i / 3) % 1
                out += f'<text x="{1120 + 80 * ph:.0f}" y="{560 - 200 * ph:.0f}" font-family="{FONT}" font-weight="bold" font-size="{50 + 30 * ph:.0f}" fill="#3F6FB0" opacity="{1 - ph:.2f}">Z</text>'
    if 141 <= t < 153:
        out += f'<rect width="{W}" height="{H}" fill="#101530" opacity="{0.35 * fade(t, 141, 153, 1.5, 1):.2f}"/>'
    out += plano_card(t, s, 2)
    return out


def cupcake(x, y):
    return (f'<g transform="translate({x},{y})"><path d="M-35 0 L35 0 L26 50 L-26 50 Z" fill="#E28B2E" stroke="#2B2B2B" stroke-width="3"/>'
            '<ellipse cx="0" cy="-6" rx="42" ry="26" fill="#F7A9C0" stroke="#2B2B2B" stroke-width="3"/><circle cx="0" cy="-30" r="9" fill="#D8343A"/></g>')


def p3(t):
    s = T["p3"]
    out = (f'<rect width="{W}" height="{H}" fill="#FCE3E8"/>'
           '<rect x="100" y="260" width="380" height="440" rx="20" fill="#B8B8C0" stroke="#2B2B2B" stroke-width="6"/>'
           f'<rect x="150" y="380" width="280" height="200" rx="14" fill="{"#F28C3B" if t < 161 else "#4A4A55"}" opacity="0.9"/>'
           '<rect x="0" y="760" width="1920" height="320" fill="#C98B52"/><rect x="0" y="740" width="1920" height="40" fill="#E5C17E"/>')
    # tabuleiro
    out += '<rect x="1050" y="720" width="560" height="24" rx="10" fill="#8C8C96"/>'
    eaten = sum(1 for c in CUPCAKES if t >= c)
    if t >= 160:
        for i in range(eaten, 6):
            out += cupcake(1110 + i * 88, 690)
    if t >= CUPCAKES[-1] + 0.6:
        for i in range(12):
            out += f'<circle cx="{1080 + i * 42}" cy="{714 - (i % 3) * 4}" r="5" fill="#E28B2E"/>'
    chewing = any(c <= t < c + 0.6 for c in CUPCAKES)
    grow = 1 + 0.05 * eaten
    if t < 160:
        expr = "happy"
    elif t < CUPCAKES[0]:
        expr = "normal"
    elif t < 174:
        expr = "eat" if chewing else "happy"
    else:
        expr = "shock" if t < 176 else "happy"
    x = 700 if t < 162.5 else 700 + 260 * ease((t - 162.5) / 0.5)
    out += M(t, x, 1000, 1.3, expr, sx=grow)
    if t >= 174:  # o pombo cliente chega e não há nada
        u = ease((t - 174) / 1.2)
        out += pigeon(2050 - 420 * u, 980, -1)
        out += burst(fade(t, 175, 178, 0.2, 0.4), 1560, 560, "?", 90, 70)
    out += plano_card(t, s, 3)
    return cam(out, t, s + 2, s + 23, 1.0, 1.07, 1200, 650)


def s5_solucao(t):
    out = room(t, night=True)
    lit = t >= 186
    glow = 0.5 + 0.2 * math.sin(t * 4) if lit else 0
    zoom = ease((t - 194) / 3)
    # telemóvel no chão
    px, py = 1180, 870
    if lit:
        out += f'<ellipse cx="{px}" cy="{py - 40}" rx="200" ry="120" fill="#9ED3F0" opacity="{glow * 0.35:.2f}"/>'
    out += M(t, 880, 880, 1.2, "ko" if t < 186 else ("normal" if t < 192 else "happy"), rot=0)
    out += (f'<g transform="translate({px},{py}) rotate(-8)"><rect x="-55" y="-100" width="110" height="190" rx="18" fill="#2B2B2B"/>'
            f'<rect x="-45" y="-88" width="90" height="160" rx="8" fill="{"#FFF6EA" if lit else "#3A3A48"}"/>')
    if lit:
        out += ('<path d="M0 -20 C -30 -55 -50 -15 0 15 C 50 -15 30 -55 0 -20 Z" fill="#D8343A"/>'
                '<rect x="-35" y="35" width="70" height="12" rx="6" fill="#DDD"/>')
    out += '</g>'
    if t >= 192:  # lâmpada
        s = spring(t - 192)
        out += (f'<g transform="translate(880,{360 - 20 * s:.0f}) scale({s:.2f})"><circle r="60" fill="#FFE066" stroke="#2B2B2B" stroke-width="5"/>'
                '<rect x="-25" y="55" width="50" height="34" rx="6" fill="#999" stroke="#2B2B2B" stroke-width="4"/>'
                + "".join(f'<line x1="{90 * math.cos(a):.0f}" y1="{90 * math.sin(a):.0f}" x2="{120 * math.cos(a):.0f}" y2="{120 * math.sin(a):.0f}" stroke="#F6C343" stroke-width="8" stroke-linecap="round"/>'
                          for a in [math.pi * (1.1 + 0.2 * i) for i in range(5)]) + '</g>')
    if zoom > 0:  # ecrã do telemóvel em grande: coração e barra vazia
        out += (f'<g opacity="{zoom:.2f}"><rect width="{W}" height="{H}" fill="#1E1B2E" opacity="0.6"/>'
                '<rect x="660" y="120" width="600" height="860" rx="60" fill="#2B2B2B"/><rect x="690" y="160" width="540" height="780" rx="30" fill="#FFF6EA"/>'
                '<path d="M960 400 C 860 280 740 400 960 560 C 1180 400 1060 280 960 400 Z" fill="#D8343A"/>'
                '<rect x="760" y="640" width="400" height="44" rx="22" fill="#E6DCCB" stroke="#2B2B2B" stroke-width="4"/>'
                f'<text x="960" y="780" font-family="{FONT}" font-weight="bold" font-size="44" fill="#2B2B2B" text-anchor="middle">Ajuda o Mochi</text>'
                + M(t, 960 + 230, 960, 0.55, "happy") + '</g>')
    out += caption(fade(t, 199, 206), "E se pedisse ajuda?", y=1040 if zoom > 0.5 else 930)
    return out


def s6_final(t):
    if t < T["japao"]:
        # a barra enche com moedas
        filled = sum(1 for c in COINS if t >= c) / len(COINS)
        out = (f'<rect width="{W}" height="{H}" fill="#FDE7D3"/>'
               '<rect x="660" y="120" width="600" height="860" rx="60" fill="#2B2B2B"/><rect x="690" y="160" width="540" height="780" rx="30" fill="#FFF6EA"/>'
               f'<g transform="translate(960,480) scale({1 + 0.08 * math.sin(t * 6) * filled:.3f})"><path d="M0 -80 C -100 -200 -220 -80 0 80 C 220 -80 100 -200 0 -80 Z" fill="#D8343A"/></g>'
               '<rect x="760" y="640" width="400" height="44" rx="22" fill="#E6DCCB" stroke="#2B2B2B" stroke-width="4"/>'
               f'<rect x="764" y="644" width="{392 * filled:.0f}" height="36" rx="18" fill="#4CAF50"/>')
        for c in COINS:
            if c - 0.6 <= t < c:
                u = (t - (c - 0.6)) / 0.6
                out += f'<circle cx="{960 + 200 * math.sin(c * 3):.0f}" cy="{-60 + 700 * u * u:.0f}" r="28" fill="#F6C343" stroke="#B88A1B" stroke-width="5"/>'
        hop = abs(math.sin(t * 5)) * 40
        out += M(t, 420, 1000 - hop, 1.2, "happy") + M(t, 1500, 1000 - abs(math.sin(t * 5 + 1)) * 40, 1.2, "happy", flip=-1)
        if filled >= 1:
            for i in range(12):
                out += sparkle(720 + (i * 97) % 480, 200 + (i * 61) % 400, 1.4, 0.8)
        return out
    # Japão
    out = sunrise_sky(T["japao"] - 10, t) + torii(450, 840, 0.75) + petals(t, 24)
    lt = t - T["japao"]
    look = lt > 2.5
    out += M(t, 1150, 1010, 1.45 + 0.1 * ease((lt - 2) / 4), "happy" if not look else ("normal" if lt < 4 else "happy"))
    if look and lt < 8:  # mão no peito: coração a pulsar
        p = 1 + 0.12 * math.sin(lt * 8)
        out += f'<g transform="translate(1150,{880:.0f}) scale({p:.2f})"><path d="M0 -10 C -20 -35 -45 -10 0 25 C 45 -10 20 -35 0 -10 Z" fill="#D8343A" stroke="#2B2B2B" stroke-width="3"/></g>'
    out = cam(out, t, T["japao"], T["cartao"], 1.0, 1.12, 1150, 700)
    if t >= T["cartao"]:
        op = ease((t - T["cartao"]) / 0.6) * (1 - ease((t - (T["jogo"] - 0.4)) / 0.4))
        out += (f'<g opacity="{op:.2f}"><rect width="{W}" height="{H}" fill="#1E1B2E" opacity="0.72"/>'
                f'<text x="960" y="380" font-family="{FONT}" font-weight="bold" font-size="92" fill="#FFF6EA" text-anchor="middle">Ajuda o Mochi</text>'
                f'<text x="960" y="490" font-family="{FONT}" font-weight="bold" font-size="76" fill="#F6C343" text-anchor="middle">a chegar ao Japão</text>'
                f'<rect x="560" y="570" width="800" height="110" rx="55" fill="#D8343A"/>'
                f'<text x="960" y="645" font-family="{FONT}" font-weight="bold" font-size="56" fill="#FFFFFF" text-anchor="middle">{VAQUINHA}</text>'
                f'<text x="960" y="780" font-family="{FONT}" font-size="48" fill="#FFF6EA" text-anchor="middle">Link na descrição</text></g>')
    return out


def s7_jogo(t):
    op = ease((t - T["jogo"]) / 0.5)
    out = room(t) + f'<rect width="{W}" height="{H}" fill="#1E1B2E" opacity="{0.75 * op:.2f}"/>'
    # mini ecrã com blocos (estilo Terrabloco, sem copiar o jogo)
    out += f'<g opacity="{op:.2f}">'
    for i in range(6):
        for j in range(3):
            c = ["#6BBF59", "#8A5A34", "#7A7A86"][j]
            out += f'<rect x="{1180 + i * 90}" y="{420 + j * 90}" width="88" height="88" fill="{c}" stroke="#2B2B2B" stroke-width="3"/>'
    out += (f'<text x="620" y="400" font-family="{FONT}" font-weight="bold" font-size="56" fill="#F6C343" text-anchor="middle">O Mochi recomenda:</text>'
            f'<text x="620" y="520" font-family="{FONT}" font-weight="bold" font-size="104" fill="#FFF6EA" text-anchor="middle">Terrabloco</text>'
            f'<text x="620" y="610" font-family="{FONT}" font-size="46" fill="#FFF6EA" text-anchor="middle">grátis no CrazyGames</text>'
            f'<text x="620" y="700" font-family="{FONT}" font-size="42" fill="#FFF6EA" text-anchor="middle">Link na descrição</text></g>')
    out += M(t, 1450, 1050, 0.9, "happy", headphones=True, op=op)
    return out


def black_transition(t):
    """Fade a preto curto nos cortes entre cenas."""
    cuts = [T["planos"], T["solucao"], T["final"], T["japao"], T["jogo"]]
    op = 0
    for c in cuts:
        if c - 0.35 <= t < c + 0.35:
            op = max(op, 1 - abs(t - c) / 0.35)
    if t < 0.5:
        op = max(op, 1 - t / 0.5)
    if t > TOTAL - 1.5:
        op = max(op, ease((t - (TOTAL - 1.5)) / 1.5))
    return f'<rect width="{W}" height="{H}" fill="#000" opacity="{op:.2f}"/>' if op > 0 else ""


def frame_svg(t):
    if t < T["sonho"]:
        body = s1_casa(t)
    elif t < T["choque"]:
        body = s2_sonho(t)
    elif t < T["planos"]:
        body = s3_choque(t)
    elif t < T["p2"]:
        body = p1(t)
    elif t < T["p3"]:
        body = p2(t)
    elif t < T["solucao"]:
        body = p3(t)
    elif t < T["final"]:
        body = s5_solucao(t)
    elif t < T["jogo"]:
        body = s6_final(t)
    else:
        body = s7_jogo(t)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="#FDE7D3"/>{body}{black_transition(t)}</svg>')


FRAMES = os.path.join(DIR, "frames_grande")


def render_one(n):
    p = os.path.join(FRAMES, f"f{n:05d}.png")
    if not os.path.exists(p):
        cairosvg.svg2png(bytestring=frame_svg(n / FPS).encode(), write_to=p)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for s in sys.argv[1:]:
            cairosvg.svg2png(bytestring=frame_svg(float(s)).encode(), write_to=os.path.join(DIR, f"prev_grande_{s}.png"))
        sys.exit()
    os.makedirs(FRAMES, exist_ok=True)
    with Pool(2) as pool:
        pool.map(render_one, range(int(FPS * TOTAL)), chunksize=48)
    out = os.path.join(DIR, "mochi_grande.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(FRAMES, "f%05d.png"),
                    "-i", os.path.join(DIR, "musica_grande.wav"), "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out)
