"""Vídeo 'Dia 2: o Mochi faz as malas' (1080x1920, 10 s, 30 fps), em loop.

0-0.35 mala a abanar | 0.35 POP, ramens voam | 2.4-4.9 o que está na mala
5.0-7.4 bilhete 1400€ / vaquinha 0€ de 3000€ | 7.5-9 'Plano B: viajar como bagagem', ramens voltam
9.3-10 volta ao início
"""
import math

from mochi_cena import W, H, FONT, card, clamp, ease, fade, main, meow_open, spring, burst, svg_doc
from mochi_kit import mochi
from musica_dia2 import MEOWS, TOTAL

PRICE, META, ANGARIADO = 1400, 3000, 0
S = 1.3
CASE_L, CASE_R, CASE_TOP, CASE_BOT = 250, 830, 1330, 1620
LID_H = 60
POP_T, CLOSE_T = 0.35, 8.9
CUPS = [(95, 1745), (205, 1700), (880, 1700), (990, 1750), (150, 1830), (935, 1835), (300, 1800), (785, 1800)]


def lid_angle(t):
    """0 = fechada; 100 = aberta (roda à volta da dobradiça direita)."""
    if t < POP_T or t >= CLOSE_T:
        return 0.0
    if t < 8.5:
        return 100 * clamp(spring((t - POP_T) * 1.4))
    return 100 * (1 - ease((t - 8.5) / 0.4))


def suitcase_svg(t):
    ang = lid_angle(t)
    wob = 0.0
    if t < POP_T:
        wob = math.sin(t * 60) * 0.04 * (t / POP_T)
    elif t >= CLOSE_T:
        wob = math.sin((t - CLOSE_T) * 40) * 0.05 * math.exp(-(t - CLOSE_T) * 6)
    sy = 1 + wob
    base = (f'<g transform="translate(540,{CASE_BOT}) scale({1 - wob / 2:.3f},{sy:.3f}) translate(-540,-{CASE_BOT})">'
            f'<rect x="{CASE_L}" y="{CASE_TOP}" width="{CASE_R - CASE_L}" height="{CASE_BOT - CASE_TOP}" rx="34" fill="#3A9C9B"/>'
            f'<rect x="{CASE_L + 120}" y="{CASE_TOP}" width="40" height="{CASE_BOT - CASE_TOP}" fill="#2D7C7B"/>'
            f'<rect x="{CASE_R - 160}" y="{CASE_TOP}" width="40" height="{CASE_BOT - CASE_TOP}" fill="#2D7C7B"/>'
            f'<circle cx="{CASE_L + 60}" cy="{CASE_BOT + 8}" r="16" fill="#2B2B2B"/><circle cx="{CASE_R - 60}" cy="{CASE_BOT + 8}" r="16" fill="#2B2B2B"/>'
            '</g>')
    inside = ""
    if ang > 1:   # interior visível com ramens
        inside = (f'<rect x="{CASE_L + 20}" y="{CASE_TOP - 6}" width="{CASE_R - CASE_L - 40}" height="22" rx="10" fill="#21605F"/>')
    lid = (f'<g transform="rotate({ang:.2f},{CASE_R},{CASE_TOP}) translate(0,{-wob * 300:.1f})">'
           f'<rect x="{CASE_L}" y="{CASE_TOP - LID_H}" width="{CASE_R - CASE_L}" height="{LID_H + 6}" rx="26" fill="#47B3B2"/>'
           f'<rect x="{CASE_L + 120}" y="{CASE_TOP - LID_H}" width="40" height="{LID_H + 6}" fill="#3A9C9B"/>'
           f'<rect x="{CASE_R - 160}" y="{CASE_TOP - LID_H}" width="40" height="{LID_H + 6}" fill="#3A9C9B"/>'
           f'<rect x="490" y="{CASE_TOP - LID_H - 34}" width="100" height="40" rx="16" fill="none" stroke="#2B2B2B" stroke-width="12"/>'
           '</g>')
    return base, inside + lid


def cup(x, y, rot=0, sc=1.0):
    return (f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot:.0f}) scale({sc:.2f})">'
            '<polygon points="-40,-50 40,-50 30,40 -30,40" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round"/>'
            '<rect x="-38" y="-30" width="76" height="26" fill="#D8343A"/>'
            '<rect x="-44" y="-60" width="88" height="14" rx="6" fill="#F6C343" stroke="#2B2B2B" stroke-width="4"/>'
            '<path d="M-22 -5 Q-11 6 0 -5 Q11 6 22 -5" fill="none" stroke="#FFFFFF" stroke-width="4"/>'
            '</g>')


def cups_svg(t):
    out = ""
    for i, (x1, y1) in enumerate(CUPS):
        x0, y0 = 540, CASE_TOP - 20
        peak = 520 + 60 * (i % 3)
        t_out = POP_T + 0.05 + i * 0.04
        t_back = 7.65 + i * 0.1
        if t < t_out or t >= t_back + 0.55:
            continue
        if t < t_out + 0.7:
            u = (t - t_out) / 0.7
        elif t < t_back:
            u = 1.0
        else:
            u = 1 - (t - t_back) / 0.55
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u - peak * 4 * u * (1 - u)
        rot = (1 - u) * 0 + u * (8 if i % 2 else -8) + (360 * u if 0 < u < 1 else 0)
        out += cup(x, y, rot, 0.6 + 0.4 * min(1, u * 1.5))
    return out


def mochi_expr(t):
    for a, b, e in [(0.35, 1.6, "shock"), (2.4, 5.0, "happy"), (5.3, 6.6, "shock"), (7.5, 8.95, "happy")]:
        if a <= t < b:
            return e
    return "normal"


def frame_svg(t):
    ang = lid_angle(t)
    seat = CASE_TOP - LID_H * (1 - clamp(ang / 30))       # senta na tampa ou dentro da mala
    jump = 0.0
    if POP_T <= t < POP_T + 0.75:
        u = (t - POP_T) / 0.75
        jump = 330 * 4 * u * (1 - u)
    if CLOSE_T <= t < CLOSE_T + 0.35:
        u = (t - CLOSE_T) / 0.35
        jump = 60 * 4 * u * (1 - u)
    mx = 540 - 190 * S - 20
    my = seat - 372 * S - jump
    tilt = -12 * math.sin(math.pi * clamp((t - POP_T) / 0.75)) if POP_T <= t < POP_T + 0.75 else 0
    blink = 1.9 < t < 2.02 or 6.9 < t < 7.02
    base, lid = suitcase_svg(t)
    title_op = 1 - ease((t - 2.05) / 0.3) if t < 5 else ease((t - 9.35) / 0.4)
    parts = [
        f'<rect width="{W}" height="{H}" fill="#FDE7D3"/>',
        '<ellipse cx="540" cy="1720" rx="700" ry="230" fill="#E9C9A8"/>',
        '<ellipse cx="540" cy="1630" rx="330" ry="30" fill="#000" opacity="0.12"/>',
        base,
        lid if ang < 5 else "",
        f'<g transform="translate({mx:.1f},{my:.1f}) scale({S}) rotate({tilt:.1f},190,375)">{mochi(mochi_expr(t), blink, mouth_open=meow_open(t, MEOWS))}</g>',
        lid if ang >= 5 else "",
        cups_svg(t),
        burst(fade(t, POP_T, 1.15, 0.08, 0.3), 215, 600, "POP!", 88, r=150),
        card(title_op, "Dia 2", "O Mochi faz as malas", s1=84),
        card(fade(t, 2.4, 4.95), "Na mala do Mochi:", "8 ramens e 0 meias", s1=64),
        card(fade(t, 5.0, 7.45), f"Bilhete: {PRICE}€", f"Vaquinha: {ANGARIADO}€ de {META}€", s1=72),
        card(fade(t, 7.5, 9.3), "Plano B:", "viajar como bagagem", s1=80, s2=60),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("dia2", frame_svg, TOTAL)
