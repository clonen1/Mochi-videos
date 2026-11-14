"""Som de 'O Mochi tenta cozinhar' (90 s, 80 BPM). Instrumentos reais pelo mochi_real.py; efeitos pelo mochi_audio.py.

casa: piano e guitarra | panquecas: pizzicato e flauta | sopa: violoncelo e harpa | bolo: celesta, ninar | final: tema do Mochi
"""
import os

import numpy as np

from mochi_audio import SR, Mix, RNG, hp, lp, sfx_meow, sfx_pop, sfx_snore
from mochi_real import Real, mix_down
from tempos_cozinha import *  # noqa: F401,F403

BEAT = 0.75
BAR = 3.0
C = dict(b=48, c=[55, 60, 64], t=[55, 60, 64, 67])
G = dict(b=43, c=[55, 59, 62], t=[55, 59, 62, 67])
AM = dict(b=45, c=[57, 60, 64], t=[57, 60, 64, 69])
F = dict(b=41, c=[53, 57, 60], t=[53, 57, 60, 65])
DM = dict(b=38, c=[53, 57, 62], t=[53, 57, 62, 65])

m = Mix(TOTAL)
r = Real(TOTAL)


def each(t0, t1, chords, bar=BAR):
    t, i = t0, 0
    while t < t1 - 0.01:
        yield t, min(t1, t + bar), chords[i % len(chords)]
        t += bar
        i += 1


def pad(t0, t1, c, vel=50, inst="slow"):
    r.chord(t0, c["c"], t1 - t0 + 0.4, inst, vel)


def low(t0, t1, c, vel=62, cello=True):
    r.note(t0, c["b"], t1 - t0 + 0.2, "bassbow", vel)
    if cello:
        r.note(t0, c["b"] + 12, t1 - t0 + 0.2, "cello", vel - 10)


def arp(t0, t1, c, step=BEAT, vel=50, inst="piano", pat=(0, 1, 2, 3, 2, 1)):
    t, i = t0, 0
    while t < t1 - 0.05:
        r.note(t, c["t"][pat[i % len(pat)]], 2.0, inst, vel)
        t += step
        i += 1


def sfx(x, t, g=0.4):
    m.add(x, t, g, "sfx")


def env(n, k):
    t = np.arange(int(n * SR)) / SR
    return t, np.exp(-t * k)


def thud():
    t, e = env(0.3, 14)
    return np.sin(2 * np.pi * 70 * t) * e + 0.3 * lp(RNG.normal(0, 1, len(t)), 400) * np.exp(-t * 30)


def sizzle(d=1.2):
    t = np.arange(int(d * SR)) / SR
    return hp(RNG.normal(0, 1, len(t)), 3500) * np.sin(np.pi * t / d) * 0.4


def plop():
    t, e = env(0.2, 25)
    return np.sin(2 * np.pi * (300 + 500 * np.exp(-t * 25)) * t) * e


def ding(d=1.4):
    t = np.arange(int(d * SR)) / SR
    return (np.sin(2 * np.pi * 2300 * t) * (np.sin(2 * np.pi * 14 * t) > 0) * 0.5) * np.exp(-t * 1.2)


def whoosh():
    t = np.arange(int(0.5 * SR)) / SR
    return lp(RNG.normal(0, 1, len(t)), 1800) * np.sin(np.pi * t / 0.5) * 0.5


# casa
for a, b, c in each(0, 8, [C, G, AM]):
    pad(a, b, c, 46)
    low(a, b, c, 58)
    arp(a, b, c, BEAT, 52)
    r.chord(a + BEAT / 2, c["c"], 0.5, "guitar", 54, roll=0.015)
r.note(C_IDEA, 84, 2.0, "celesta", 80)
r.chord(C_IDEA, [60, 64, 67, 72], 2.5, "harp", 70, roll=0.07)
# panquecas
e = T["e1"]
for a, b, c in each(e + 2.5, e + 21, [C, F, G, AM]):
    pad(a, b, c, 44, "strings")
    low(a, b, c, 56)
    arp(a, b, c, BEAT, 46, "harp")
    for k in range(4):
        r.note(a + k * BEAT, c["b"] + 12, 0.4, "pizz", 62)
sfx(sizzle(), e + P_POUR, 0.25)
for i in range(5):
    r.note(e + P_FLIP - 0.6 + i * 0.15, 72 + i * 2, 0.2, "flute", 64)
sfx(whoosh(), e + P_FLIP, 0.35)
sfx(plop(), e + P_STICK, 0.4)
pass
sfx(plop(), e + P_LAND, 0.45)
for i, tt in enumerate((e + 15.0, e + 15.4, e + 15.8)):
    r.note(tt, [57, 55, 53][i], 0.35, "pizz", 78)
r.chord(e + P_STAMP, [38, 45, 50, 53], 2.0, "piano", 90)
sfx(thud(), e + P_STAMP, 0.45)
# sopa
e = T["e2"]
for a, b, c in each(e + 2.5, e + 19.5, [AM, F, C, G]):
    pad(a, b, c, 44, "slow")
    low(a, b, c, 60)
    arp(a, b, c, BEAT / 2, 44, "harp", pat=(0, 1, 2, 3, 2, 1))
for i, t0 in enumerate(S_ADD):
    sfx(plop(), e + t0 + 0.9, 0.35)
    r.note(e + t0 + 0.9, [76, 79, 81, 84][i], 0.4, "celesta", 66)
sfx(sizzle(2.5), e + S_BOIL, 0.22)
for i in range(6):
    r.note(e + S_BOIL + i * 0.25, 50 + (i % 2) * 7, 0.15, "pizz", 60)
r.chord(e + S_SHOCK, [57, 60, 63, 69], 1.2, "strings", 100)
sfx(sfx_meow(), MEOWS[2], 0.4)
for i in range(10):
    r.note(e + S_OVER + i * 0.3, 60 + i, 0.3, "bassbow", 62 + i * 3)
for tt in (e + 17.0, e + 17.4, e + 17.8):
    r.note(tt, 45 - (tt > e + 17.5) * 2, 0.35, "pizz", 78)
r.chord(e + S_STAMP, [38, 45, 50, 53], 2.0, "piano", 90)
sfx(thud(), e + S_STAMP, 0.45)
# bolo
e = T["e3"]
for a, b, c in each(e + 2.5, e + B_SLEEP, [C, G], 3.0):
    pad(a, b, c, 44, "strings")
    arp(a, b, c, BEAT, 46, "harp")
r.note(e + B_IN, 76, 0.5, "celesta", 66)
sfx(sizzle(1.0), e + B_IN + 1.0, 0.18)
for a, b, c in each(e + B_SLEEP, e + B_RING, [AM, F, C], 3.0):          # embalar
    pad(a, b, c, 42, "slow")
    low(a, b, c, 46, cello=False)
    arp(a, b, c, BEAT, 40, "celesta", pat=(0, 1, 2, 3, 2, 1))
for tt in (e + 8.4, e + 10.0):
    sfx(sfx_snore(1.6), tt, 0.3)
sfx(ding(1.4), e + B_RING, 0.28)
r.chord(e + B_WAKE, [57, 60, 63, 69], 1.2, "strings", 100)
sfx(sfx_meow(), MEOWS[3], 0.4)
sfx(whoosh(), e + B_OPEN, 0.35)
for i, tt in enumerate((e + 17.4, e + 17.8, e + 18.2)):
    r.note(tt, [57, 55, 53][i], 0.35, "pizz", 78)
r.chord(e + B_STAMP, [38, 45, 50, 53], 2.0, "piano", 90)
sfx(thud(), e + B_STAMP, 0.45)
# final
e = T["fim"]
for a, b, c in each(e, e + 10, [C, AM, F, G]):
    pad(a, b, c, 48, "strings")
    low(a, b, c, 58)
    arp(a, b, c, BEAT, 46, "harp")
sfx(sfx_pop(), e + F_BOWL + 0.8, 0.25)
r.chord(e + F_BOWL + 1.8, [76, 79, 83, 88], 2.5, "celesta", 80, roll=0.04)
sfx(sfx_meow(), MEOWS[4], 0.35)
tema = [(64, 0.75), (67, 0.75), (69, 1.5), (67, 0.75), (64, 0.75), (62, 1.5)]
tt = T["cartao"] + 0.2
for nt, d in tema:
    r.note(tt, nt + 12, d * 1.05, "flute", 74)
    r.note(tt, nt, d, "piano", 68)
    tt += d
r.chord(T["cartao"] + 4.4, [48, 55, 64, 72], 4.0, "strings", 70)
r.chord(T["cartao"] + 4.4, [48, 52, 55, 60, 64], 4.0, "piano", 70, roll=0.06)
sfx(sfx_meow(), MEOWS[0], 0.4)
sfx(sfx_meow(), MEOWS[1], 0.4)

if __name__ == "__main__":
    out = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "musica", "musica_cozinha.wav"))
    music = r.render()
    n = int(TOTAL * SR)
    sf = m.bus["sfx"][:n]
    mix_down(music * 2.6, sf, out, TOTAL, sfx_gain=0.5)
    print(out)
