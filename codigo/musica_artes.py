"""Som de 'O Mochi tentou 3 artes' (90 s, 80 BPM). Instrumentos reais pelo mochi_real.py; efeitos pelo mochi_audio.py.

casa: piano alegre | pintura: pizzicato e flauta, gotas | música: piano desafinado a cada passo, depois ninar
barro: baixo brincalhão e chapadas | quadro: celesta e cordas | cartão: tema do Mochi
"""
import os

import numpy as np

from mochi_audio import SR, Mix, RNG, hp, lp, sfx_meow, sfx_pop, sfx_snore
from mochi_real import Real, mix_down
from tempos_artes import *  # noqa: F401,F403

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


def drip():
    t = np.arange(int(0.18 * SR)) / SR
    return np.sin(2 * np.pi * (900 + 1400 * np.exp(-t * 30)) * t) * np.exp(-t * 28)


def splat():
    t = np.arange(int(0.35 * SR)) / SR
    return lp(RNG.normal(0, 1, len(t)), 1200) * np.exp(-t * 14) * (1 - np.exp(-t * 120))


# ======== casa (0-10) ========
for a, b, c in each(0, 9, [C, G, AM, F]):
    pad(a, b, c, 48)
    low(a, b, c, 60)
    arp(a, b, c, BEAT, 50)
pad(9, 10, C, 48); low(9, 10, C, 55)
r.chord(3.0, [76, 79, 83], 2.0, "celesta", 70, roll=0.05)
r.chord(A_BULB, [60, 64, 67, 72], 3.0, "harp", 70, roll=0.07)
r.note(A_BULB, 84, 2.5, "celesta", 80)
sfx(sfx_meow(), MEOWS[0], 0.40)
for i, tt in enumerate((8.0, 8.5, 9.0, 9.5)):
    r.note(tt, [60, 64, 67, 72][i], 0.4, "pizz", 70)
# ======== pintura (10-30) ========
e = T["e1"]
r.chord(e, [48, 55, 64], 2.6, "strings", 68)
r.note(e, 36, 2.5, "bassbow", 78)
for a, b, c in each(e + 2.5, e + 20, [C, F, G, AM]):
    pad(a, b, c, 44, "strings")
    low(a, b, c, 58)
    arp(a, b, c, BEAT / 2, 46, "harp", pat=(0, 1, 2, 3, 2, 1))
sfx(drip(), e + P_DIP + 0.9, 0.35)
r.note(e + P_DIP + 0.9, 86, 0.4, "celesta", 70)
mel = [72, 74, 76, 74, 72, 69, 72, 76, 79, 76, 74, 72, 69, 72]
for i in range(14):                                               # as pegadas: pizzicato a andar
    tt = e + P_WALK[0] + 0.55 * i
    r.note(tt, mel[i], 0.4, "pizz", 78)
    sfx(drip(), tt, 0.10)
for i in range(8):
    r.note(e + P_SPIN[0] + 0.2 * i, 72 + (i * 2) % 12, 0.25, "flute", 66)
sfx(sfx_meow(), MEOWS[1], 0.40)
for i, tt in enumerate((e + 14.6, e + 15.0, e + 15.4)):
    r.note(tt, [57, 55, 53][i], 0.35, "pizz", 78)
r.chord(e + P_STAMP, [38, 45, 50, 53], 2.0, "piano", 95)
sfx(thud(), e + P_STAMP, 0.45)
# ======== música (30-50) ========
e = T["e2"]
r.chord(e, [48, 55, 64], 2.6, "strings", 62)
r.note(e + 3.0, 36, 0.6, "pizz", 60)
for i, tt in enumerate(PIANO_STEPS):                              # piano clunky: um acorde estranho por passo
    n = PIANO_NOTES[i]
    r.chord(e + tt, [n, n + 6 if i % 2 else n + 1], 0.5, "piano", 88)
    r.note(e + tt, n - 12, 0.5, "pizz", 60)
r.chord(e + M_WALK[1], [40, 41, 46, 52], 1.6, "piano", 105)       # BLONC
r.chord(e + M_WALK[1], [50, 53, 56, 62], 1.2, "strings", 80)
sfx(thud(), e + M_WALK[1], 0.4)
sfx(sfx_meow(), MEOWS[2], 0.40)
for i, tt in enumerate((e + 10.4, e + 10.8, e + 11.2)):
    r.note(tt, [57, 55, 53][i], 0.35, "pizz", 78)
r.chord(e + M_LIE, [36, 43, 48, 52, 55], 3.5, "piano", 70, roll=0.12)   # deita-se nas teclas: acorde calmo
for a, b, c in each(e + M_SLEEP, e + 20, [C, AM]):
    pad(a, b, c, 42, "slow")
    low(a, b, c, 50, cello=False)
    arp(a, b, c, BEAT, 40, "celesta", pat=(0, 1, 2, 3, 2, 1))
for tt in (e + 14.5, e + 16.0):
    sfx(sfx_snore(1.6), tt, 0.35)
r.chord(e + M_STAMP, [38, 45, 50, 53], 2.0, "piano", 95)
sfx(thud(), e + M_STAMP, 0.45)
# ======== barro (50-70) ========
e = T["e3"]
r.chord(e, [48, 55, 64], 2.6, "strings", 68)
for a, b, c in each(e + 2.5, e + 16, [C, G, AM, F]):
    bt = a
    while bt < b - 0.01:
        r.note(bt, c["b"] + 12, 0.5, "bass", 82)
        r.note(bt + BEAT * 2, c["b"] + 19, 0.5, "bass", 74)
        bt += BEAT * 4
    t2 = a + BEAT * 0.5
    while t2 < b - 0.01:
        r.chord(t2, c["c"], 0.5, "guitar", 60, roll=0.015)
        t2 += BEAT
    pad(a, b, c, 34, "strings")
for q, nn in zip(C_SQ, (52, 48, 43)):
    sfx(splat(), e + q, 0.5)
    sfx(thud(), e + q, 0.25)
    r.note(e + q, nn, 0.6, "cello", 95)
r.chord(e + 8.6, [57, 60, 63, 69], 1.2, "strings", 90)              # fica colado
for j in range(10):
    tt = e + C_FLY + 0.35 * j + 0.5
    sfx(splat(), tt, 0.30)
    r.note(tt, 60 + (j * 3) % 12, 0.25, "pizz", 72)
sfx(sfx_meow(), MEOWS[3], 0.40)
for tt in (e + 14.0, e + 14.6, e + 15.2):
    r.note(tt, 45, 0.3, "bass", 88)
r.chord(e + C_STAMP, [38, 45, 50, 53], 2.0, "piano", 95)
sfx(thud(), e + C_STAMP, 0.45)
# ======== quadro (70-84) e cartão (84-90) ========
e = T["fim"]
for a, b, c in each(e, e + 14, [C, AM, F, G]):
    pad(a, b, c, 50, "strings")
    low(a, b, c, 62)
    arp(a, b, c, BEAT, 46, "harp", pat=(0, 1, 2, 3, 2, 1))
r.chord(e + F_FRAME + 0.8, [76, 79, 83, 88], 2.5, "celesta", 85, roll=0.04)      # a moldura chega
r.chord(e + F_SOLD, [60, 64, 67, 72], 3.0, "harp", 76, roll=0.06)                 # vendido
r.chord(e + F_SOLD, [48, 55, 64, 72], 3.0, "strings", 85)
sfx(sfx_pop(), e + F_SOLD, 0.30)
sfx(sfx_meow(), MEOWS[4], 0.35)
sfx(sfx_snore(1.6), e + 11.5, 0.3)
tema = [(64, 0.75), (67, 0.75), (69, 1.5), (67, 0.75), (64, 0.75), (62, 1.5)]
tt = T["cartao"] + 0.2
for nt, d in tema:
    r.note(tt, nt + 12, d * 1.05, "flute", 74)
    r.note(tt, nt, d, "piano", 68)
    tt += d
r.chord(T["cartao"] + 4.4, [48, 55, 64, 72], 4.0, "strings", 70)
r.chord(T["cartao"] + 4.4, [48, 52, 55, 60, 64], 4.0, "piano", 70, roll=0.06)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_artes.wav")
    music = r.render()
    n = int(TOTAL * SR)
    sf = m.bus["sfx"][:n]
    print("rms musica", float(np.sqrt((music ** 2).mean())), "pico", float(np.abs(music).max()), "| rms sfx", float(np.sqrt((sf ** 2).mean())), "pico", float(np.abs(sf).max()))
    mix_down(music * 2.6, sf, out, TOTAL, sfx_gain=0.5)
    print(out)
