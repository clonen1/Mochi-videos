"""Som de 'O Mochi tentou 3 desportos' (90 s, 80 BPM). Instrumentos reais pelo mochi_real.py; efeitos pelo mochi_audio.py.

casa: piano alegre | natação: harpa e celesta, água | futebol: guitarra e pizzicato brincalhões
ginásio: baixo pesado e depois ninar | medalha: celesta e cordas | cartão: tema do Mochi
"""
import os

import numpy as np

from mochi_audio import SR, Mix, RNG, hp, lp, sfx_meow, sfx_pop, sfx_snore
from mochi_real import Real, mix_down
from tempos_desportos import *  # noqa: F401,F403

BEAT = 0.75
BAR = 3.0
AM = dict(b=45, c=[57, 60, 64], t=[57, 60, 64, 69])
F = dict(b=41, c=[53, 57, 60], t=[53, 57, 60, 65])
C = dict(b=48, c=[55, 60, 64], t=[55, 60, 64, 67])
G = dict(b=43, c=[55, 59, 62], t=[55, 59, 62, 67])
DM = dict(b=38, c=[53, 57, 62], t=[53, 57, 62, 65])
EM = dict(b=40, c=[55, 59, 64], t=[55, 59, 64, 67])

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


def tick(n=1):
    t = np.arange(int(0.05 * SR)) / SR
    return lp(hp(RNG.normal(0, 1, len(t)), 900) * np.exp(-t * 90), 4500) * n


def thud():
    t = np.arange(int(0.3 * SR)) / SR
    return np.sin(2 * np.pi * 70 * t) * np.exp(-t * 14) + 0.3 * lp(RNG.normal(0, 1, len(t)), 400) * np.exp(-t * 30)


def splash():
    t = np.arange(int(0.9 * SR)) / SR
    x = lp(RNG.normal(0, 1, len(t)), 3500) * np.exp(-t * 5) * (1 - np.exp(-t * 80))
    return x


def drip():
    t = np.arange(int(0.18 * SR)) / SR
    return np.sin(2 * np.pi * (900 + 1400 * np.exp(-t * 30)) * t) * np.exp(-t * 28)


def whistle():
    t = np.arange(int(0.5 * SR)) / SR
    f = 2600 + 120 * np.sin(2 * np.pi * 28 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3) * 0.6


# ======== casa (0-10) ========
for a, b, c in each(0, 9, [C, G, AM, F]):
    pad(a, b, c, 48)
    low(a, b, c, 60)
    arp(a, b, c, BEAT, 50)
pad(9, 10, C, 48); low(9, 10, C, 55)
r.chord(D_MEDAL, [76, 79, 83], 2.0, "celesta", 70, roll=0.05)
r.chord(D_BULB, [60, 64, 67, 72], 3.0, "harp", 70, roll=0.07)
r.note(D_BULB, 84, 2.5, "celesta", 80)
sfx(sfx_meow(), MEOWS[0], 0.40)
for i, tt in enumerate((8.0, 8.5, 9.0, 9.5)):
    r.note(tt, [60, 64, 67, 72][i], 0.4, "pizz", 70)
# ======== natação (10-30) ========
e = T["e1"]
r.chord(e, [48, 55, 64], 2.6, "strings", 68)
r.note(e, 36, 2.5, "bassbow", 78)
for a, b, c in each(e + 2.5, e + 20, [C, F, G, AM]):
    pad(a, b, c, 46, "strings")
    low(a, b, c, 60)
    arp(a, b, c, BEAT / 2, 48, "harp", pat=(0, 1, 2, 3, 2, 1))
for i in range(int(2.0 / 0.7)):
    sfx(tick(0.5), e + 0.4 + i * 0.7, 0.14)
for i in range(4):
    sfx(drip(), e + N_PAW + 0.2 + i * 0.4, 0.22)
    r.note(e + N_PAW + 0.2 + i * 0.4, [84, 86, 88, 90][i], 0.3, "celesta", 55)
r.chord(e + N_BRR, [57, 60, 63, 69], 1.2, "strings", 105)       # susto
r.note(e + N_BRR, 33, 1.0, "bassbow", 90)
sfx(sfx_meow(), MEOWS[1], 0.40)
for tt in (e + 6.0, e + 6.6, e + 7.2):
    r.note(tt, 45, 0.3, "pizz", 62)                              # a pensar
r.chord(e + N_JUMP - 0.5, [52, 59, 64], 1.0, "strings", 90)
sfx(splash(), e + N_SPLASH, 0.5)
r.note(e + N_SPLASH, 36, 1.0, "cello", 90)
for i in range(6):
    r.note(e + 10.6 + i * 0.35, [72, 70, 67, 70, 72, 74][i], 0.3, "pizz", 70)   # a debater-se
for i in range(5):
    sfx(drip(), e + 11.0 + i * 0.45, 0.2)
sfx(sfx_meow(), MEOWS[2], 0.40)
sfx(sfx_pop(), e + N_OUT, 0.25)
for i, tt in enumerate((e + 14.6, e + 15.0, e + 15.4)):
    r.note(tt, [57, 55, 53][i], 0.35, "pizz", 78)                # wah-wah triste
r.chord(e + N_STAMP, [38, 45, 50, 53], 2.0, "piano", 95)
sfx(thud(), e + N_STAMP, 0.45)
# ======== futebol (30-50) ========
e = T["e2"]
r.chord(e, [48, 55, 64], 2.6, "strings", 68)
for a, b, c in each(e + 2.5, e + 16, [C, G, AM, F]):
    bt = a
    while bt < b - 0.01:
        r.note(bt, c["b"] + 12, 0.5, "bass", 82)
        r.note(bt + BEAT * 2, c["b"] + 19, 0.5, "bass", 74)
        bt += BEAT * 4
    t2 = a + BEAT * 0.5
    while t2 < b - 0.01:
        r.chord(t2, c["c"], 0.5, "guitar", 62, roll=0.015)
        t2 += BEAT
    pad(a, b, c, 36, "strings")
sfx(whistle(), e + 2.4, 0.20)
sfx(thud(), e + F_KICK, 0.42)
for i in range(8):
    r.note(e + 3.2 + i * 0.5, [64, 67, 69, 67, 64, 62, 64, 67][i], 0.4, "pizz", 72)
for i in range(12):                                              # a traça: flauta curiosa
    r.note(e + F_MOTH + i * 0.4, [72, 76, 74, 77, 76, 79, 77, 81, 79, 76, 74, 72][i], 0.35, "flute", 60)
r.chord(e + F_GOAL, [76, 79, 83], 2.0, "celesta", 80, roll=0.05)
sfx(sfx_pop(), e + F_GOAL, 0.25)
sfx(sfx_meow(), MEOWS[3], 0.40)
for tt in (e + 14.0, e + 14.6, e + 15.2):
    r.note(tt, 45, 0.3, "bass", 88)
r.chord(e + F_STAMP, [38, 45, 50, 53], 2.0, "piano", 95)
sfx(thud(), e + F_STAMP, 0.45)
# ======== ginásio (50-70) ========
e = T["e3"]
for a, b, c in each(e, e + 8.2, [AM, F, DM, EM]):
    pad(a, b, c, 46, "slow")
    low(a, b, c, 70)
    bt = a
    while bt < b - 0.01:
        r.note(bt, c["b"] + 12, 0.45, "bass", 86)
        bt += BEAT
for i in range(int(2.0 / 0.7)):
    sfx(tick(0.5), e + 0.4 + i * 0.7, 0.14)
for i in range(10):                                              # esforço: nota que sobe
    r.note(e + 3.0 + i * 0.5, 45 + i, 0.4, "bassbow", 70 + i * 3)
sfx(thud(), e + G_FALL, 0.5)
r.chord(e + G_FALL, [50, 53, 56, 62], 1.4, "strings", 100)
r.note(e + G_FALL + 0.3, 33, 1.2, "bassbow", 90)
for i, tt in enumerate((e + 9.4, e + 9.8, e + 10.2)):
    r.note(tt, [57, 55, 53][i], 0.35, "pizz", 78)
sfx(sfx_meow(), MEOWS[4], 0.40)
for a, b, c in each(e + 12.4, e + 20, [C, AM]):                  # sesta: embalar
    pad(a, b, c, 44, "slow")
    low(a, b, c, 50, cello=False)
    arp(a, b, c, BEAT, 42, "celesta", pat=(0, 1, 2, 3, 2, 1))
for tt in (e + 14.5, e + 16.0):
    sfx(sfx_snore(1.6), tt, 0.35)
r.chord(e + G_STAMP, [38, 45, 50, 53], 2.0, "piano", 95)
sfx(thud(), e + G_STAMP, 0.45)
# ======== medalha (70-84) e cartão (84-90) ========
e = T["fim"]
for a, b, c in each(e, e + 14, [C, AM, F, G]):
    pad(a, b, c, 50, "strings")
    low(a, b, c, 62)
    arp(a, b, c, BEAT, 46, "harp", pat=(0, 1, 2, 3, 2, 1))
sfx(sfx_snore(1.6), e + 2.0, 0.3)
r.chord(e + M_MEDAL + 1.0, [76, 79, 83, 88], 2.5, "celesta", 85, roll=0.04)
r.chord(e + M_MEDAL + 1.0, [60, 64, 67, 72], 3.0, "harp", 72, roll=0.06)
r.note(e + M_MEDAL + 1.0, 36, 3.0, "cello", 80)
sfx(sfx_pop(), e + M_MEDAL + 1.0, 0.25)
sfx(sfx_meow(), MEOWS[5], 0.35)
tema = [(64, 0.75), (67, 0.75), (69, 1.5), (67, 0.75), (64, 0.75), (62, 1.5)]
tt = T["cartao"] + 0.2
for nt, d in tema:
    r.note(tt, nt + 12, d * 1.05, "flute", 74)
    r.note(tt, nt, d, "piano", 68)
    tt += d
r.chord(T["cartao"] + 4.4, [48, 55, 64, 72], 4.0, "strings", 70)
r.chord(T["cartao"] + 4.4, [48, 52, 55, 60, 64], 4.0, "piano", 70, roll=0.06)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_desportos.wav")
    music = r.render()
    n = int(TOTAL * SR)
    sf = m.bus["sfx"][:n]
    print("rms musica", float(np.sqrt((music ** 2).mean())), "pico", float(np.abs(music).max()), "| rms sfx", float(np.sqrt((sf ** 2).mean())), "pico", float(np.abs(sf).max()))
    mix_down(music * 2.6, sf, out, TOTAL, sfx_gain=0.5)
    print(out)
