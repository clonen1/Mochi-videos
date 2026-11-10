"""Som de 'O Mochi desapareceu' (96 s, 80 BPM). Instrumentos reais pelo mochi_real.py; efeitos pelo mochi_audio.py.

casa: piano calmo | caixa: pizzicato misterioso | cesto: cordas e susto | site: guitarra e celesta, cliques
cortina: piano e flauta, final cómico | cartões: tema do Mochi
"""
import os

import numpy as np

from mochi_audio import SR, Mix, RNG, hp, lp, sfx_meow, sfx_pop, sfx_snore
from mochi_real import Real, mix_down
from tempos_desaparecido import *  # noqa: F401,F403

BEAT = 0.75
BAR = 3.0
AM = dict(b=45, c=[57, 60, 64], t=[57, 60, 64, 69])
F = dict(b=41, c=[53, 57, 60], t=[53, 57, 60, 65])
C = dict(b=48, c=[55, 60, 64], t=[55, 60, 64, 67])
G = dict(b=43, c=[55, 59, 62], t=[55, 59, 62, 67])
DM = dict(b=38, c=[53, 57, 62], t=[53, 57, 62, 65])

m = Mix(TOTAL)
r = Real(TOTAL)


def each(t0, t1, chords, bar=BAR):
    t, i = t0, 0
    while t < t1 - 0.01:
        yield t, min(t1, t + bar), chords[i % len(chords)]
        t += bar
        i += 1


def pad(t0, t1, c, vel=55, inst="slow"):
    r.chord(t0, c["c"], t1 - t0 + 0.4, inst, vel)


def low(t0, t1, c, vel=70, cello=True):
    r.note(t0, c["b"], t1 - t0 + 0.2, "bassbow", vel)
    if cello:
        r.note(t0, c["b"] + 12, t1 - t0 + 0.2, "cello", vel - 10)


def arp(t0, t1, c, step=BEAT, vel=52, inst="piano", pat=(0, 1, 2, 3, 2, 1)):
    t, i = t0, 0
    while t < t1 - 0.05:
        r.note(t, c["t"][pat[i % len(pat)]], 2.0, inst, vel)
        t += step
        i += 1


def sfx(x, t, g=0.4):
    m.add(x, t, g, "sfx")


def thud():
    t = np.arange(int(0.3 * SR)) / SR
    return np.sin(2 * np.pi * 70 * t) * np.exp(-t * 14) + 0.3 * lp(RNG.normal(0, 1, len(t)), 400) * np.exp(-t * 30)


def click():
    t = np.arange(int(0.05 * SR)) / SR
    return hp(RNG.normal(0, 1, len(t)), 1500) * np.exp(-t * 90)


def printer(d=2.4):
    t = np.arange(int(d * SR)) / SR
    return lp(RNG.normal(0, 1, len(t)), 2200) * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * t)) * 0.35 * np.minimum(1, t * 8) * np.minimum(1, (d - t) * 8)


def yawn():
    t = np.arange(int(1.2 * SR)) / SR
    f = 380 - 140 * t / 1.2
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 1.2) ** 1.5 * 0.5


# ======== casa (0-10) ========
for a, b, c in each(0, 9, [C, AM, F, G]):
    pad(a, b, c, 46)
    low(a, b, c, 58)
    arp(a, b, c, BEAT, 48)
pad(9, 10, C, 46); low(9, 10, C, 52)
r.chord(C_SHOCK, [52, 58, 64], 1.2, "strings", 85)
sfx(sfx_pop(), C_SHOCK, 0.3)
sfx(sfx_meow(), MEOWS[0], 0.40)
for i, tt in enumerate((7.8, 8.4, 9.0)):
    r.note(tt, [60, 58, 55][i], 0.4, "pizz", 70)
# ======== caixa (10-28) ========
e = T["e1"]
r.chord(e, [48, 55, 64], 2.6, "strings", 62)
for a, b, c in each(e + 2.5, e + 17, [AM, DM, AM, G]):
    pad(a, b, c, 40, "strings")
    low(a, b, c, 52)
    arp(a, b, c, BEAT / 2, 40, "pizz", pat=(0, 2, 1, 3, 1, 2))
sfx(thud(), e + B_NOT, 0.3)
r.note(e + B_NOT, 57, 0.6, "cello", 82)
r.chord(e + B_PEEK, [76, 79, 83], 1.6, "celesta", 70, roll=0.05)
sfx(sfx_meow(), MEOWS[1], 0.40)
# ======== cesto (28-46) ========
e = T["e2"]
r.chord(e, [48, 55, 64], 2.6, "strings", 62)
for a, b, c in each(e + 2.5, e + 17, [C, F, G, AM]):
    pad(a, b, c, 42, "strings")
    low(a, b, c, 54)
    arp(a, b, c, BEAT, 44, "harp")
r.chord(e + K_TAIL, [53, 59, 65], 1.2, "strings", 90)
sfx(sfx_pop(), e + K_TAIL, 0.28)
for i, tt in enumerate((e + K_REACH, e + K_REACH + 0.25, e + K_REACH + 0.5)):
    r.note(tt, [57, 59, 61][i], 0.3, "pizz", 74)
sfx(sfx_meow(), MEOWS[2], 0.40)
r.chord(e + K_SOCK + 0.8, [57, 60, 63], 1.2, "strings", 72)
r.note(e + K_SOCK + 1.4, 45, 0.7, "cello", 80)
# ======== site e cartaz (46-66) ========
e = T["site"]
r.chord(e, [48, 55, 64], 2.4, "strings", 60)
for a, b, c in each(e + 2.5, e + 19, [C, G, AM, F]):
    for bt in np.arange(a, b - 0.01, BEAT):
        r.note(bt, c["b"] + 12, 0.5, "bass", 70)
    t2 = a + BEAT * 0.5
    while t2 < b - 0.01:
        r.chord(t2, c["c"], 0.5, "guitar", 54, roll=0.015)
        t2 += BEAT
    pad(a, b, c, 34, "strings")
sfx(click(), e + S_CLICK1, 0.5)
r.note(e + S_CLICK1, 84, 0.4, "celesta", 74)
for i in range(5):
    sfx(click(), e + S_TYPE0 + 0.4 * i, 0.35)
r.chord(e + S_PHOTO, [72, 76, 79], 1.4, "celesta", 74, roll=0.04)
sfx(sfx_pop(), e + S_PHOTO, 0.25)
sfx(click(), e + S_PRINT, 0.5)
r.chord(e + S_PRINT, [60, 64, 67, 72], 1.6, "harp", 74, roll=0.05)
sfx(printer(), e + P_OUT, 0.4)
r.chord(e + P_TAKE, [60, 64, 67, 72], 2.5, "harp", 78, roll=0.06)
# ======== cortina (66-84) ========
e = T["e3"]
r.chord(e, [48, 55, 64], 2.4, "strings", 58)
for a, b, c in each(e + 2.5, e + 11, [C, AM]):
    pad(a, b, c, 40, "strings")
    low(a, b, c, 52)
    arp(a, b, c, BEAT, 40, "pizz", pat=(0, 2, 1, 3, 1, 2))
sfx(thud(), e + W_STICK, 0.18)
r.note(e + W_STICK, 72, 0.3, "pizz", 70)
for i in range(6):
    r.note(e + W_BULGE[0] + 0.35 * i, [57, 58, 57, 56, 57, 58][i], 0.3, "pizz", 66)
sfx(yawn(), e + W_OUT + 1.6, 0.45)
r.chord(e + W_OUT + 1.6, [57, 60, 64], 1.4, "slow", 52)
sfx(sfx_meow(), MEOWS[3], 0.30)
r.chord(e + W_SEE, [51, 57, 63], 0.8, "strings", 92)
sfx(sfx_pop(), e + W_SEE, 0.25)
sfx(sfx_meow(), MEOWS[4], 0.40)
for i, tt in enumerate((e + W_ANGRY, e + W_ANGRY + 0.3, e + W_ANGRY + 0.6)):
    r.note(tt, [45, 45, 43][i], 0.4, "bass", 88)
sfx(sfx_meow(), MEOWS[5], 0.35)
r.chord(e + 16.2, [57, 60, 64], 1.8, "cello", 62)
r.chord(e + 16.2, [69, 72, 76], 1.8, "flute", 54)
# ======== cartões (84-96) ========
tema = [(64, 0.75), (67, 0.75), (69, 1.5), (67, 0.75), (64, 0.75), (62, 1.5)]
tt = T["cartaoA"] + 0.2
for nt, d in tema:
    r.note(tt, nt + 12, d * 1.05, "flute", 72)
    r.note(tt, nt, d, "piano", 66)
    tt += d
r.chord(T["cartaoA"] + 5.2, [48, 55, 64, 72], 2.0, "strings", 62)
r.chord(T["cartaoB"], [48, 55, 64, 72], 6.0, "strings", 62)
r.chord(T["cartaoB"], [48, 52, 55, 60, 64], 6.0, "piano", 66, roll=0.06)
tt = T["cartaoB"] + 0.2
for nt, d in tema:
    r.note(tt, nt + 12, d * 1.05, "flute", 70)
    tt += d

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_desaparecido.wav")
    music = r.render()
    n = int(TOTAL * SR)
    sf = m.bus["sfx"][:n]
    print("rms musica", float(np.sqrt((music ** 2).mean())), "| rms sfx", float(np.sqrt((sf ** 2).mean())))
    mix_down(music * 2.6, sf, out, TOTAL, sfx_gain=0.5)
    print(out)
