"""'O Mochi tenta cozinhar' (1920x1080, 24 fps, 90 s). Sem falas: conta-se com animação.

casa (0-8) | panquecas (8-30) | sopa (30-52) | bolo (52-74) | prato final (74-84) | cartão (84-90)
"""
import math
import os
import subprocess
import sys
from multiprocessing import Pool

import cairosvg

from mochi_kit import MOCHI_VF
from mochi_longo import (H, W, FPS, FONT, INK, M, APRON, bulb, burst, caption, clamp, ease, ease_out, fade, lerp, sparkle,
                         spring, stamp, walk_bob, zzz)
from mochi_props import bowl, smoke
from mochi_props_cozinha import (CHEF, SOOT, cake, carrot, cookbook, fish, flame, foam, kitchen_bg, oven, pan, pancake, pot, spoon,
                                 stove, timer)
from tempos_cozinha import *  # noqa: F401,F403

VAQUINHA = "gofund.me/5d9e87b27"
CUTS = [T["e1"], T["e2"], T["e3"], T["fim"]]
HAT = CHEF + APRON
HAT_SOOT = CHEF + APRON + SOOT


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


def icon_pan():
    return f'<g transform="scale(1.5) translate(0,60)">{pan(1.0)}</g>'


def icon_pot():
    return f'<g transform="scale(1.1) translate(0,110)">{pot(True)}</g>'


def icon_cake():
    return f'<g transform="scale(1.6) translate(0,60)">{cake(0, True, 0)}</g>'


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
            f'stroke="{INK}" stroke-width="3">Receita {n}</text>'
            f'<text x="620" y="570" font-family="{FONT}" font-weight="bold" font-size="120" fill="#FFFFFF" stroke="{INK}" stroke-width="5">{name}</text></g>'
            f'<g transform="translate(1560,520) scale({max(ic, 0.001):.2f})">{icon}</g></g>')


def puff(t, x, y, n=4, op=1.0, r=50, speed=0.45):
    out = ""
    for i in range(n):
        u = (t * speed + i / n) % 1
        out += smoke(op * math.sin(math.pi * u) * 0.9, x + 30 * math.sin(i * 2 + t * 2) + 40 * u, y - 260 * u, r * (0.6 + 0.9 * u))
    return out


# ---------- casa ----------
def s_casa(lt):
    x = lerp(-150, 960, ease(lt / 2.2)) if lt < 2.2 else 960.0
    bob, rot = walk_bob(lt, 3.4, 14) if lt < 2.2 else (0, 0)
    hop = -80 * math.sin(math.pi * (lt - C_IDEA) / 0.6) if C_IDEA <= lt < C_IDEA + 0.6 else 0
    out = kitchen_bg()
    out += f'<g transform="translate(300,690)">{cookbook()}</g>'
    out += f'<g transform="translate(1560,690)"><ellipse cx="0" cy="-8" rx="110" ry="14" fill="#B8BCC6" stroke="{INK}" stroke-width="5"/></g>'
    out += M(lt, x, 940 + bob + hop, 1.6, "happy" if lt >= C_IDEA else "normal", rot=rot, extra=HAT, mouth=meow(lt))
    if C_IDEA <= lt < C_IDEA + 3.0:
        out += bulb(x, 270, 1.0, ease((lt - C_IDEA) / 0.2) * (1 - ease((lt - (C_IDEA + 2.5)) / 0.5)))
    out += caption(fade(lt, 4.2, 7.6), "Hoje cozinho eu!")
    return out


# ---------- 1. panquecas ----------
PAN_X, PAN_Y = 1550, 674
MX1 = 1000


def s_e1(lt):
    out = kitchen_bg() + stove()
    # Mochi
    x, y, rot, expr, flip = 700.0, 940.0, 0.0, "normal", 1
    if lt < 2.5:
        x = lerp(-150, 700, ease(lt / 2.5))
        bob, rot = walk_bob(lt, 3.4, 14)
        y += bob
    elif lt < 5.8:
        x = lerp(700, MX1, ease((lt - 4.6) / 1.0))
        if 4.6 <= lt < 5.6:
            bob, rot = walk_bob(lt, 3.4, 10)
            y += bob
    else:
        x = MX1
    if P_FLIP <= lt < P_FLIP + 0.5:
        y -= 70 * math.sin(math.pi * (lt - P_FLIP) / 0.5)
        expr = "happy"
    elif P_FLIP + 0.5 <= lt < P_LAND:
        expr = "shock" if lt < P_STICK + 2.0 else "sad"
        flip = 1
    elif P_LAND <= lt < P_LAND + 2.4:
        rot = 7 * math.sin((lt - P_LAND) * 8)
        expr = "sad"
    elif lt >= P_LAND + 2.4:
        expr = "sad"
    # frigideira e panqueca
    burnt = clamp((lt - P_FLIP - 3) / 6)
    batter = ease((lt - P_POUR) / 0.8) if lt >= P_POUR else 0.0
    if lt >= P_FLIP:
        batter = 0.0
    out += f'<g transform="translate({PAN_X},{PAN_Y})">{pan(batter, 0)}</g>'
    if lt >= P_FLIP - 0.1 and lt < P_FLIP + 0.1:
        pass
    flame_on = lt >= P_POUR - 0.5
    if flame_on:
        out += flame(lt, PAN_X, PAN_Y + 6, 1.4 if lt < P_SMOKE else 2.0)
    out += M(lt, x, y, 1.6, expr, rot=rot, extra=HAT, mouth=meow(T["e1"] + lt), flip=flip)
    # panqueca em voo / teto / queda
    if P_FLIP <= lt < P_STICK:
        u = (lt - P_FLIP) / (P_STICK - P_FLIP)
        px = lerp(PAN_X, MX1, ease(u))
        py = lerp(PAN_Y - 60, 70, ease_out(u))
        out += f'<g transform="translate({px:.0f},{py:.0f}) rotate({u * 540:.0f})">{pancake(110)}</g>'
    elif P_STICK <= lt < P_FALL:
        wob = 4 * math.sin(lt * 3)
        out += f'<g transform="translate({MX1},{58 + wob * 0.3:.0f}) scale(1,0.8)">{pancake(120, 0)}</g>'
        for i in range(2):
            u = ((lt * 0.6) + i * 0.5) % 1
            out += f'<ellipse cx="{MX1 - 50 + i * 90}" cy="{100 + 700 * u * u:.0f}" rx="9" ry="14" fill="#F6D77A" stroke="{INK}" stroke-width="3" opacity="{1 - u * 0.5:.2f}"/>'
        out += burst(fade(lt, P_STICK, P_STICK + 1.0, 0.05, 0.4), 1330, 330, "SPLAT!", 88, r=150, rot=-6)
    elif P_FALL <= lt < P_LAND:
        u = (lt - P_FALL) / (P_LAND - P_FALL)
        out += f'<g transform="translate({MX1},{lerp(60, 680, u * u):.0f}) rotate({u * 20:.0f})">{pancake(130)}</g>'
    elif P_LAND <= lt < P_LAND + 2.6:
        sq = 1 + 0.06 * math.sin((lt - P_LAND) * 14) * math.exp(-(lt - P_LAND) * 2)
        out += f'<g transform="translate({MX1 + 6 * math.sin((lt - P_LAND) * 8):.0f},690) scale({sq:.2f},1.2)">{pancake(150)}</g>'
        out += burst(fade(lt, P_LAND, P_LAND + 1.0, 0.05, 0.4), 700, 330, "PLOF!", 88, r=145, rot=5)
    elif lt >= P_LAND + 2.6:
        u = clamp((lt - (P_LAND + 2.6)) / 0.6)
        out += f'<g transform="translate({lerp(MX1, 1180, u):.0f},{lerp(690, 925, u * u):.0f}) rotate({u * 12:.0f}) scale(1,{lerp(1.2, 1, u):.2f})">{pancake(130 if u < 1 else 120, 0.0)}</g>'
    # fumo
    if lt >= P_SMOKE:
        out += puff(lt, PAN_X, PAN_Y - 120, 4, min(1, (lt - P_SMOKE) / 1.0), 55)
    out += caption(fade(lt, 5.8, 8.6), "Vira, panqueca!")
    out += caption(fade(lt, P_LAND + 0.4, P_STAMP - 0.6), "Panqueca na cabeça")
    out += stamp(lt, P_STAMP, "FALHOU", 960, 420, 118)
    out += title_card(lt, 1, "Panquecas", "#F6C86A", "#D9822B", icon_pan())
    return out


# ---------- 2. sopa ----------
def s_e2(lt):
    out = kitchen_bg() + stove()
    x, y, rot, expr = 880.0, 940.0, 0.0, "normal"
    if lt < 2.5:
        x = lerp(-150, 880, ease(lt / 2.5))
        bob, rot = walk_bob(lt, 3.4, 14)
        y += bob
    if S_ADD[0] - 0.8 <= lt < S_ADD[-1] + 1.0:
        x = 880
        expr = "happy"
    if S_TASTE - 0.4 <= lt < S_SHOCK:
        x = lerp(880, 1000, ease((lt - (S_TASTE - 0.4)) / 0.9))
    if S_SHOCK <= lt < S_FLOOD:
        x = 1000
    if S_SHOCK <= lt < S_SHOCK + 0.5:
        expr = "shock"
        y -= 90 * math.sin(math.pi * (lt - S_SHOCK) / 0.5)
    elif S_SHOCK + 0.5 <= lt < S_FLOOD - 2:
        expr = "shock"
    elif lt >= S_FLOOD - 2:
        expr = "sad"
        x = lerp(1000, 780, ease((lt - (S_FLOOD - 2)) / 1.5))
    # panela
    lid_on = lt >= S_BOIL and lt < S_TASTE
    lid_dy = -10 * abs(math.sin(lt * 14)) if S_BOIL + 0.6 < lt < S_TASTE else 0
    out += f'<g transform="translate({PAN_X},{PAN_Y})">{pot(lid_on, lid_dy, 3 * math.sin(lt * 20) if lid_dy else 0)}</g>'
    out += flame(lt, PAN_X, PAN_Y + 6, 1.6) if lt >= 2.8 else ""
    out += M(lt, x, y, 1.6, expr, rot=rot, extra=HAT, mouth=meow(T["e2"] + lt))
    # ingredientes a voar
    for i, t0 in enumerate(S_ADD):
        u = (lt - t0) / 0.9
        if 0 <= u < 1:
            ix = lerp(1050, PAN_X, u)
            iy = lerp(560, PAN_Y - 230, u) - 260 * math.sin(math.pi * u)
            out += f'<g transform="translate({ix:.0f},{iy:.0f})">{carrot(u * 300) if i == 0 else fish(u * 360)}</g>'
        if 0.9 <= (lt - t0) < 1.5 and lt < S_BOIL:
            v = (lt - t0 - 0.9) / 0.6
            out += f'<circle cx="{PAN_X - 40 + i * 25}" cy="{PAN_Y - 250 - 50 * v:.0f}" r="{16 + 10 * v:.0f}" fill="#FFFFFF" stroke="#CFE3EE" stroke-width="4" opacity="{1 - v:.2f}"/>'
    # tampa fora
    if lt >= S_TASTE:
        pass
    # colher
    if S_TASTE <= lt < S_FLOOD - 2:
        u = ease((lt - S_TASTE) / 1.0)
        sx_, sy_ = lerp(PAN_X - 20, x + 190, u), lerp(PAN_Y - 230, 560, u)
        out += f'<g transform="translate({sx_:.0f},{sy_ + 170:.0f}) rotate({lerp(-10, 25, u):.0f})">{spoon()}</g>'
    # vapor do susto
    if S_SHOCK <= lt < S_SHOCK + 1.6:
        k = (lt - S_SHOCK) / 1.6
        for i in range(3):
            out += smoke(0.8 * (1 - k), x + 180 + i * 60 + 80 * k, 560 - 150 * k - i * 30, 28)
        out += burst(fade(lt, S_SHOCK, S_SHOCK + 1.1, 0.05, 0.4), 760, 280, "QUENTE!", 78, color="#D8343A", r=160, rot=-7)
    # espuma da panela
    if lt >= S_OVER:
        g = ease((lt - S_OVER) / 3.2)
        out += foam(PAN_X, PAN_Y - 200, 340 + 160 * g, 80 + 480 * g, lt)
        if lt >= S_OVER + 1.5:
            f2 = ease((lt - S_OVER - 1.5) / 2.5)
            out += f'<rect x="{PAN_X - 160}" y="{PAN_Y - 120}" width="{320 + 80 * f2:.0f}" height="{(900 - PAN_Y + 100) * f2:.0f}" rx="20" fill="#FFFFFF"/>'
    if lt >= S_FLOOD - 1:
        w = 300 + 1500 * ease((lt - (S_FLOOD - 1)) / 3.0)
        out += foam(W - w / 2 + 20, 1010, w, 170, lt)
    out += caption(fade(lt, 3.0, 8.0), "Receita secreta")
    out += caption(fade(lt, S_FLOOD + 0.6, S_STAMP - 0.5), "Sopa de... espuma")
    out += stamp(lt, S_STAMP, "FALHOU", 960, 420, 118)
    out += title_card(lt, 2, "Sopa", "#9ED98F", "#3F9A6F", icon_pot())
    return out


# ---------- 3. bolo ----------
OV = dict(x=1340, y=500, w=460, h=400)


def s_e3(lt):
    t = T["e3"] + lt
    out = kitchen_bg()
    x, y, rot, expr, sx, sy = 800.0, 940.0, 0.0, "normal", 1.0, 1.0
    if lt < 2.5:
        x = lerp(-150, 800, ease(lt / 2.5))
        bob, rot = walk_bob(lt, 3.4, 14)
        y += bob
    elif lt < B_SLEEP:
        x = lerp(800, 1000, ease((lt - B_IN + 0.8) / 0.8)) if lt >= B_IN - 0.8 else 800
        if lt >= B_IN + 1.0:
            x = lerp(1000, 760, ease((lt - B_IN - 1.0) / 1.0))
        expr = "happy" if lt > B_IN + 1.0 else "normal"
    elif lt < B_WAKE:
        x = 760
        u = ease((lt - B_SLEEP) / 1.0)
        expr = "sleep"
        sy, sx = lerp(1.0, 0.74, u), lerp(1.0, 1.14, u)
        y = 934
    else:
        sleepy = clamp((lt - B_WAKE) / 0.3)
        x = 760
        if B_WAKE <= lt < B_WAKE + 0.5:
            y -= 100 * math.sin(math.pi * (lt - B_WAKE) / 0.5)
            expr = "shock"
        elif lt < B_OPEN:
            expr = "shock"
            x = lerp(760, 1000, ease((lt - B_WAKE - 0.5) / 1.0))
        else:
            expr = "sad"
            x = lerp(1000, 700, ease((lt - B_OPEN - 1.2) / 1.2)) if lt > B_OPEN + 1.2 else 1000
    soot = lt >= B_OPEN + 0.5
    cake_g = ease((lt - B_IN - 1.0) / 4.0) if lt >= B_IN + 1.0 else 0.0
    burnt = clamp((lt - 9.0) / 3.0)
    opened = ease((lt - B_OPEN) / 0.4) if lt >= B_OPEN else 0.0
    out += oven(opened, 1.0 if lt >= B_IN + 1.0 else 0.0, cake_g, burnt, **OV)
    # timer na bancada
    ring = 1.0 if B_RING <= lt < B_WAKE + 1.2 else 0.0
    out += f'<g transform="translate(400,640)">{timer(lt, ring)}</g>'
    # massa a entrar
    if B_IN - 1.0 <= lt < B_IN + 1.0:
        u = (lt - (B_IN - 1.0)) / 2.0
        out += f'<g transform="translate({lerp(x + 150, 1500, ease(u)):.0f},{lerp(620, 790, ease(u)):.0f})"><path d="M-80 0 L-80 -50 Q0 -80 80 -50 L80 0 Z" fill="#F4B6C2" stroke="{INK}" stroke-width="5"/></g>' if u < 0.9 else ""
    out += M(lt, x, y, 1.6, expr, rot=rot, sx=sx, sy=sy, extra=HAT_SOOT if soot else HAT, mouth=meow(T["e3"] + lt))
    if B_SLEEP + 0.8 <= lt < B_WAKE:
        out += zzz(lt, x + 90, y - 330)
    if B_SMOKE <= lt < B_OPEN:
        out += puff(lt, OV["x"] + 230, OV["y"] - 20, 5, min(1, (lt - B_SMOKE) / 1.5), 60)
    # abre o forno: nuvem
    if B_OPEN <= lt < B_OPEN + 2.6:
        k = (lt - B_OPEN) / 2.6
        for i in range(6):
            out += smoke(0.95 * (1 - k * k), 1100 + i * 110 + 60 * k, 680 - 220 * k - (i % 3) * 60, 120 - 20 * (i % 2))
    if B_RING <= lt < B_WAKE + 0.4:
        out += burst(fade(lt, B_RING, B_WAKE + 0.4, 0.05, 0.3), 400, 440, "RIIING!", 70, r=150, rot=6)
    if lt >= B_OPEN + 0.3:
        u = clamp((lt - B_OPEN - 0.3) / 0.5)
        out += f'<g transform="translate(1190,{lerp(560, 686, u * u):.0f})">{cake(1.0, True, lt)}</g>'
    out += caption(fade(lt, 6.8, 10.4), "Só uma sonequinha...")
    out += caption(fade(lt, B_OPEN + 1.6, B_STAMP - 0.6), "Bolo de carvão")
    out += stamp(lt, B_STAMP, "FALHOU", 960, 420, 118)
    out += title_card(lt, 3, "Bolo", "#F2A6B8", "#C45A8E", icon_cake())
    return out


# ---------- final ----------
def s_fim(lt):
    t = T["fim"] + lt
    out = kitchen_bg()
    out += f'<g transform="translate(330,690) scale(0.9)">{pancake(110, 1.0)}</g>'
    out += f'<g transform="translate(1530,690) scale(0.8)">{cake(1.0, False)}</g>'
    out += f'<g transform="translate(1000,690) scale(0.55)">{pot(True)}</g>'
    eating = lt >= F_BOWL + 1.8
    expr = "eat" if eating and (lt * 2.2) % 1 < 0.6 else ("happy" if eating else "sad")
    out += f'<ellipse cx="960" cy="948" rx="260" ry="22" fill="#000" opacity="0.10"/>'
    out += M(t, 800, 940, 1.6, expr, extra=HAT, mouth=meow(t))
    if lt >= F_BOWL:
        u = ease_out((lt - F_BOWL) / 0.9)
        by = lerp(-100, 960, u)
        out += f'<g transform="translate(1180,{by:.0f}) scale(0.8)">{bowl(True)}</g>'
        if eating:
            out += sparkle(1000, 560, 1.0 + 0.3 * math.sin(lt * 6), 0.9) + sparkle(1260, 780, 0.8, 0.8)
    out += caption(fade(lt, 1.8, 5.8), "3 receitas. 0 pratos.")
    out += caption(fade(lt, 6.2, 9.6), "Ração: receita perfeita")
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
            f'<rect width="{W}" height="{H}" fill="#FFF1DA"/>{body}{dip(t)}</svg>')


DIR = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(DIR, "frames_cozinha")


def render_one(n):
    p = os.path.join(FRAMES, f"f{n:05d}.png")
    if not os.path.exists(p):
        cairosvg.svg2png(bytestring=frame_svg(n / FPS).encode(), write_to=p)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "render":
        for s in sys.argv[1:]:
            cairosvg.svg2png(bytestring=frame_svg(float(s)).encode(), write_to=os.path.join(DIR, f"prev_coz_{s}.png"))
        sys.exit()
    os.makedirs(FRAMES, exist_ok=True)
    with Pool(2) as pool:
        pool.map(render_one, range(int(FPS * TOTAL)), chunksize=48)
    out = os.path.abspath(os.path.join(DIR, "..", "videos", "mochi_cozinha.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(FRAMES, "f%05d.png"),
                    "-i", os.path.abspath(os.path.join(DIR, "..", "musica", "musica_cozinha.wav")), "-vf", MOCHI_VF, "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out)
