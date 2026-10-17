"""Vídeo 'Eu à segunda vs eu à sexta' (1080x1920, 10 s, 30 fps), ecrã dividido, em loop.

Em cima o Mochi de segunda, em baixo o Mochi de sexta (com auscultadores, a dançar).
0-2.1 despertador TRIM em cima, festa em baixo | 2.2-4.4 energia: 1% vs 100%
4.5-6.6 a mesma comida: zangado vs feliz | 6.7-8.8 domingo à noite: os dois em pânico
8.9-10 volta ao início
"""
import math

from mochi_cena import W, H, FONT, burst, card, clamp, ease, fade, main, meow_open, spring, svg_doc
from mochi_kit import mochi
from musica_semana import BOT_MEOWS, TOP_MEOWS, TOTAL

S = 1.45
TOP_FLOOR, BOT_FLOOR = 800, 1820
MX = 640


def mix_col(a, b, u):
    u = clamp(u)
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * u):02X}" for x, y in zip(ca, cb))


def panic(t):
    return fade(t, 6.85, 8.85, 0.2, 0.3)


def label(y, txt, fill):
    return (f'<rect x="60" y="{y}" width="{len(txt) * 46 + 70}" height="96" rx="48" fill="{fill}"/>'
            f'<text x="{60 + (len(txt) * 46 + 70) / 2:.0f}" y="{y + 68}" font-family="{FONT}" font-weight="bold" '
            f'font-size="60" fill="#FFFFFF" text-anchor="middle">{txt}</text>')


def clock(x, y, t):
    sh = math.sin(t * 80) * 10 if 0.12 <= t < 0.9 else 0
    return (f'<g transform="translate({x + sh:.0f},{y})">'
            '<circle cx="-45" cy="-70" r="24" fill="#D8343A" stroke="#2B2B2B" stroke-width="5"/>'
            '<circle cx="45" cy="-70" r="24" fill="#D8343A" stroke="#2B2B2B" stroke-width="5"/>'
            '<circle cx="0" cy="0" r="72" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="7"/>'
            '<line x1="0" y1="0" x2="0" y2="-45" stroke="#2B2B2B" stroke-width="7" stroke-linecap="round"/>'
            '<line x1="0" y1="0" x2="32" y2="10" stroke="#2B2B2B" stroke-width="7" stroke-linecap="round"/>'
            '<line x1="-40" y1="64" x2="-55" y2="88" stroke="#2B2B2B" stroke-width="7" stroke-linecap="round"/>'
            '<line x1="40" y1="64" x2="55" y2="88" stroke="#2B2B2B" stroke-width="7" stroke-linecap="round"/></g>')


def battery(x, y, level, color, txt, op):
    if op <= 0:
        return ""
    sc = 0.7 + 0.3 * op
    return (f'<g opacity="{op:.2f}" transform="translate({x},{y}) scale({sc:.2f})">'
            '<rect x="-110" y="-55" width="200" height="110" rx="18" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="8"/>'
            '<rect x="90" y="-22" width="22" height="44" rx="6" fill="#2B2B2B"/>'
            f'<rect x="-96" y="-41" width="{max(8, 172 * level):.0f}" height="82" rx="10" fill="{color}"/>'
            f'<text x="0" y="125" font-family="{FONT}" font-weight="bold" font-size="70" fill="{color}" '
            f'stroke="#FFFFFF" stroke-width="3" text-anchor="middle">{txt}</text></g>')


def bowl(x, y, op):
    if op <= 0:
        return ""
    kib = "".join(f'<circle cx="{cx}" cy="{cy}" r="13" fill="#9C5F2E"/>' for cx, cy in
                  [(-50, -28), (-20, -38), (12, -32), (44, -26), (-34, -14), (0, -18), (30, -12)])
    return (f'<g opacity="{op:.2f}" transform="translate({x},{y}) scale(1.6)">{kib}'
            '<path d="M-95 -20 L95 -20 Q85 50 0 55 Q-85 50 -95 -20 Z" fill="#3F6FB0" stroke="#2B2B2B" stroke-width="6" stroke-linejoin="round"/>'
            f'<text x="0" y="28" font-family="{FONT}" font-weight="bold" font-size="34" fill="#FFFFFF" text-anchor="middle">MOCHI</text></g>')


def top_expr(t):
    if panic(t) > 0.5:
        return "shock"
    if 0.15 <= t < 2.1:
        return "ko" if t < 0.9 else "angry"
    if 2.1 <= t < 4.45:
        return "sleep"
    if 4.45 <= t < 6.7:
        return "angry"
    return "sleep"


def bot_expr(t):
    if panic(t) > 0.5:
        return "shock"
    if 4.6 <= t < 6.7:
        return "eat" if (t * 4) % 1 < 0.5 else "happy"
    return "happy"


def frame_svg(t):
    p = panic(t)
    top_bg = mix_col("#C3CCD8", "#8E99A8", p)
    bot_bg = mix_col("#FFE08A", "#8E99A8", p)
    # Mochi de sexta: dança a tempo (2 saltos por segundo), pára no pânico
    dance = (1 - p)
    hop = 26 * abs(math.sin(2 * math.pi * t)) * dance
    sway = 6 * math.sin(2 * math.pi * t) * dance
    jolt = 0.0
    if 6.9 <= t < 7.25:
        jolt = 70 * math.sin(math.pi * (t - 6.9) / 0.35)
    top_jolt = jolt + (40 * math.sin(math.pi * (t - 0.15) / 0.3) if 0.15 <= t < 0.45 else 0)
    confetti = "".join(
        f'<rect x="{(97 * i + 108 * t * (1 if i % 2 else -1)) % 1080:.0f}" y="{1000 + (53 * i) % 760}" width="18" height="18" '
        f'rx="4" fill="{["#D8343A", "#3F6FB0", "#2E8B57", "#9B6BCB"][i % 4]}" opacity="{0.8 * (1 - p):.2f}" '
        f'transform="rotate({(37 * i + 72 * t) % 360:.0f},{(97 * i) % 1080},{1000 + (53 * i) % 760})"/>' for i in range(14))
    top_my = TOP_FLOOR - 378 * S - top_jolt
    bot_my = BOT_FLOOR - 378 * S - hop - jolt
    mx = MX - 190 * S
    title_op = 1 - ease((t - 2.0) / 0.25) if t < 5 else ease((t - 9.2) / 0.45)
    blink_b = 3.6 < t < 3.72
    parts = [
        f'<rect width="{W}" height="960" fill="{top_bg}"/>',
        f'<rect y="960" width="{W}" height="960" fill="{bot_bg}"/>',
        f'<rect y="{TOP_FLOOR - 30}" width="{W}" height="{960 - TOP_FLOOR + 30}" fill="#A9B3C0"/>',
        f'<rect y="{BOT_FLOOR - 30}" width="{W}" height="{H - BOT_FLOOR + 30}" fill="{mix_col("#F2B866", "#A9B3C0", p)}"/>',
        confetti,
        label(60, "SEGUNDA", "#5B6B80"),
        label(1080, "SEXTA", "#D9802C"),
        clock(200, TOP_FLOOR - 95, t) if t < 2.15 or t >= 8.85 else "",
        burst(fade(t, 0.12, 0.95, 0.06, 0.25), 240, 480, "TRIM!", 70, r=120),
        battery(220, TOP_FLOOR - 230, 0.03, "#D8343A", "1%", fade(t, 2.15, 4.45, 0.15, 0.2)),
        battery(220, BOT_FLOOR - 250, 1.0 if (t * 4) % 1 < 0.7 else 0.85, "#2E8B57", "100%", fade(t, 2.15, 4.45, 0.15, 0.2)),
        bowl(210, TOP_FLOOR - 95, fade(t, 4.45, 6.7, 0.15, 0.2)),
        bowl(210, BOT_FLOOR - 95, fade(t, 4.45, 6.7, 0.15, 0.2)),
        f'<g transform="translate({mx:.1f},{top_my:.1f}) scale({S})">'
        f'{mochi(top_expr(t), False, mouth_open=meow_open(t, TOP_MEOWS))}</g>',
        f'<g transform="translate({mx:.1f},{bot_my:.1f}) scale({S}) rotate({sway:.1f},190,375)">'
        f'{mochi(bot_expr(t), blink_b, headphones=p < 0.5, mouth_open=meow_open(t, BOT_MEOWS))}</g>',
        '<rect y="954" width="1080" height="12" fill="#2B2B2B"/>',
        card(title_op, "Eu à segunda", "vs eu à sexta", y=820, s1=74, s2=74, c1="#5B6B80"),
        card(fade(t, 2.2, 4.4), "Energia:", y=865, s1=80),
        card(fade(t, 4.55, 6.6), "A comida é a mesma.", y=865, s1=68),
        card(fade(t, 6.9, 9.1), "Domingo à noite:", "amanhã é segunda?!", y=820, s1=70, s2=62),
    ]
    return svg_doc(parts)


if __name__ == "__main__":
    main("semana", frame_svg, TOTAL)
