"""Som de 'O Mochi procura emprego' (102 s, 80 BPM). Música com instrumentos reais (piano, cordas, guitarra, harpa,
flauta) pelo mochi_real.py; os efeitos (miados, moedas, ressonar) vêm do mochi_audio.py.

casa: piano calmo | emprego 1: brincalhão (guitarra, baixo, pizzicato) | emprego 2: café, jazz leve
emprego 3: noite misteriosa (cordas lentas, celesta) | final: tristeza, ideia, esperança, tema do Mochi
"""
import os

import numpy as np

from mochi_audio import (SR, Mix, RNG, bell, lp, hp, sfx_coin, sfx_meow, sfx_pop, sfx_snore)
from mochi_real import Real, mix_down
from tempos_trabalhos import *  # noqa: F401,F403

BEAT = 0.75
BAR = 3.0

AM = dict(b=45, c=[57, 60, 64], t=[57, 60, 64, 69])
F = dict(b=41, c=[53, 57, 60], t=[53, 57, 60, 65])
C = dict(b=48, c=[55, 60, 64], t=[55, 60, 64, 67])
G = dict(b=43, c=[55, 59, 62], t=[55, 59, 62, 67])
DM = dict(b=38, c=[53, 57, 62], t=[53, 57, 62, 65])
EM = dict(b=40, c=[55, 59, 64], t=[55, 59, 64, 67])
E7 = dict(b=40, c=[56, 59, 62], t=[56, 59, 62, 64])
DM7 = dict(b=38, c=[53, 57, 60, 64], t=[57, 60, 64, 65])
G7 = dict(b=43, c=[53, 59, 62], t=[53, 59, 62, 67])
CM7 = dict(b=48, c=[55, 59, 64], t=[55, 59, 64, 67])
A7 = dict(b=45, c=[55, 61, 64], t=[55, 61, 64, 69])

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
    x = hp(RNG.normal(0, 1, len(t)), 900) * np.exp(-t * 90)
    return lp(x, 4500) * n


def chomp():
    t = np.arange(int(0.12 * SR)) / SR
    return lp(RNG.normal(0, 1, len(t)), 900) * np.exp(-t * 35)


def crash():
    t = np.arange(int(0.9 * SR)) / SR
    x = hp(RNG.normal(0, 1, len(t)), 2500) * np.exp(-t * 7)
    for f, d in ((2300, 0.0), (3100, 0.05), (1700, 0.11), (3900, 0.18)):
        a = np.sin(2 * np.pi * f * np.clip(t - d, 0, None)) * np.exp(-np.clip(t - d, 0, None) * 12) * (t >= d)
        x = x + 0.4 * a
    return x


def thud():
    t = np.arange(int(0.3 * SR)) / SR
    return np.sin(2 * np.pi * 70 * t) * np.exp(-t * 14) + 0.3 * lp(RNG.normal(0, 1, len(t)), 400) * np.exp(-t * 30)


# ======== casa (0-14) ========
for a, b, c in each(0, 12, [AM, F, C, G]):
    pad(a, b, c, 48)
    low(a, b, c, 62)
    arp(a, b, c, BEAT, 50)
pad(12, 14, AM, 48); low(12, 14, AM, 55)
r.note(0.2, 76, 2.5, "celesta", 55)       # o sonho: celesta no poster
r.note(1.0, 72, 2.5, "celesta", 50)
r.note(2.2, 76, 2.5, "celesta", 50)
for tt in (4.6, 5.0, 5.4, 5.8, 6.2):
    sfx(thud(), tt, 0.10)                 # moedas "a faltar" no mealheiro
sfx(sfx_pop(), MOTH, 0.25)
sfx(sfx_meow(), MEOWS[0], 0.40)
r.note(BULB, 84, 2.5, "celesta", 80)      # ideia
r.chord(BULB, [60, 64, 67, 72], 3.0, "harp", 70, roll=0.07)
for i, tt in enumerate((11.6, 12.1, 12.6, 13.1)):
    r.note(tt, [60, 64, 67, 72][i], 0.4, "pizz", 70)
# ======== emprego 1: entregador (14-36) ========
e = T["e1"]
r.chord(e, [48, 55, 64], 2.6, "strings", 70)
r.note(e, 36, 2.5, "bassbow", 80)
prog1 = [C, G, AM, F]
for a, b, c in each(e + 2.5, e + 22, prog1):
    bt = a
    while bt < b - 0.01:
        r.note(bt, c["b"] + 12, 0.5, "bass", 82)
        r.note(bt + BEAT * 2, c["b"] + 19, 0.5, "bass", 74)
        bt += BEAT * 4
    t2 = a + BEAT * 0.5
    while t2 < b - 0.01:   # guitarra nos contratempos
        r.chord(t2, c["c"], 0.5, "guitar", 62, roll=0.015)
        t2 += BEAT
    pad(a, b, c, 38, "strings")
# melodia pizzicato enquanto caminha (e+2.5 .. e+10)
mel = [(64, 0.75), (67, 0.75), (69, 0.75), (67, 0.75), (64, 1.5), (62, 0.75), (64, 0.75),
       (67, 1.5), (62, 1.5), (60, 0.75), (62, 0.75), (64, 1.5), (60, 1.5)]
tt = e + 2.5
for nt, d in mel:
    r.note(tt, nt, d * 0.9, "pizz", 78)
    r.note(tt, nt + 12, d * 0.9, "celesta", 40)
    tt += d
for i in range(int(7.5 / 0.75)):
    sfx(tick(0.5), e + 2.5 + i * 0.75, 0.15)    # passos
# cheira (e+7): flauta curiosa; come (e+13.6..e+17.4): pizz staccato
for tt2, nt in [(e + 7.2, 72), (e + 7.7, 74), (e + 8.2, 76), (e + 9.0, 74)]:
    r.note(tt2, nt, 0.4, "flute", 62)
for i, bt in enumerate(E1_BITES):
    tt3 = e + bt
    sfx(chomp(), tt3, 0.40)
    r.note(tt3 + 0.05, [60, 64, 67, 72, 76][i], 0.25, "pizz", 85)
sfx(sfx_meow(), MEOWS[1] - 2.0, 0.0)
sfx(thud(), e + E1_BURP, 0.35)
r.note(e + E1_BURP, 36, 0.8, "cello", 85)
r.note(e + E1_DOOR, 38, 1.2, "cello", 90)
r.note(e + E1_DOOR + 0.8, 37, 1.5, "cello", 90)
sfx(thud(), e + E1_DOOR, 0.3)
sfx(sfx_meow(), MEOWS[1], 0.40)
r.chord(e + E1_STAMP, [38, 45, 50, 53], 2.0, "piano", 95)
sfx(thud(), e + E1_STAMP, 0.45)
# ======== emprego 2: barista (36-54) ========
e = T["e2"]
r.chord(e, [50, 57, 62], 2.6, "strings", 65)
r.note(e, 38, 2.5, "bassbow", 75)
prog2 = [DM7, G7, CM7, A7]
for a, b, c in each(e + 2.5, e + 9.4, prog2):
    q = a
    while q < min(b, e + 9.4) - 0.01:   # baixo a andar
        r.note(q, c["b"] + 12 if q == a else c["b"] + 19, 0.6, "bass", 80)
        q += BEAT
    r.chord(a + BEAT * 0.5, c["c"], 0.4, "piano", 58)
    r.chord(a + BEAT * 2.5, c["c"], 0.4, "piano", 58)
    t2 = a
    while t2 < min(b, e + 9.4) - 0.01:
        r.note(t2 + BEAT * 0.5, c["t"][1] + 12, 0.3, "guitar", 60)
        t2 += BEAT * 2
# suspense: o gato olha para a caneca
r.note(e + 9.4, 45, 0.6, "pizz", 70)
for i, tt in enumerate((e + 9.6, e + 9.9, e + 10.2)):
    r.note(tt, 57 + i * 2, 0.35, "pizz", 62)
r.note(e + 10.5, 69, 0.3, "pizz", 60)
sfx(tick(0.7), e + E2_PUSH, 0.2)
sfx(thud(), e + E2_FALL - 0.3, 0.1)
sfx(crash(), e + E2_CRASH, 0.42)
r.chord(e + E2_CRASH, [50, 53, 56, 62], 1.4, "strings", 100)  # acorde de susto
r.note(e + E2_CRASH + 0.4, 38, 1.2, "bassbow", 90)
for i, tt in enumerate((e + 12.2, e + 12.6, e + 13.0)):
    r.note(tt, [57, 55, 53][i], 0.35, "pizz", 78)      # wah-wah triste, em pizz
sfx(sfx_meow(), MEOWS[2], 0.4)
for tt in (e + 13.4, e + 13.9, e + 14.4):
    r.note(tt, 45, 0.3, "bass", 88)
r.chord(e + E2_STAMP, [38, 45, 50, 53], 2.5, "piano", 95)
sfx(thud(), e + E2_STAMP, 0.45)
# ======== emprego 3: segurança (54-74) ========
e = T["e3"]
for a, b, c in each(e, e + 14, [AM, F, DM, E7]):
    pad(a, b, c, 52, "slow")
    low(a, b, c, 66)
    if a >= e + 2.5:
        r.note(a + BEAT, c["t"][3] + 12, 2.4, "celesta", 52)
        r.note(a + BEAT * 3, c["t"][2] + 12, 2.4, "celesta", 46)
for a, b, c in each(e + 14, e + 20, [AM, F]):
    pad(a, b, c, 55, "slow"); low(a, b, c, 62)
for i in range(int(3.5 / 0.7)):
    sfx(tick(0.5), e + 2.5 + i * 0.7, 0.14)           # passos de guarda
for i, tt in enumerate((e + 7.5, e + 10.0, e + 12.5, e + 15.0)):
    sfx(sfx_snore(1.6), tt, 0.4)
for i in range(30):                                      # relógio acelera
    u = i / 30
    sfx(tick(0.7), e + 8.0 + 8.0 * (u ** 1.3), 0.12)
# o ladrão: pizzicato furtivo
sneak = [57, 60, 64, 60, 57, 55, 57, 60]
tt = e + 8.6
for i in range(10):
    r.note(tt, sneak[i % len(sneak)] - 12, 0.25, "pizz", 62)
    tt += 0.5
r.chord(e + E3_GRAB, [76, 79, 83], 2.0, "celesta", 82, roll=0.05)
r.chord(e + E3_GRAB, [60, 64, 67, 72], 2.0, "harp", 70, roll=0.06)
sfx(sfx_pop(), e + E3_GRAB, 0.25)
for i, tt in enumerate((e + 12.0, e + 12.4, e + 12.8, e + 13.2)):
    r.note(tt, [64, 62, 60, 59][i] - 12, 0.28, "pizz", 62)
# amanhecer: flauta e harpa
r.chord(e + 14.0, [64, 67, 72, 76], 3.0, "harp", 60, roll=0.12)
for tt, nt in [(e + 14.5, 79), (e + 15.0, 81), (e + 15.5, 79)]:
    r.note(tt, nt, 0.4, "flute", 50)
r.chord(e + E3_WAKE, [57, 60, 63, 69], 1.4, "strings", 105)     # susto
r.note(e + E3_WAKE, 33, 1.2, "bassbow", 95)
sfx(thud(), e + E3_WAKE, 0.35)
sfx(sfx_pop(), e + E3_WAKE - 0.05, 0.3)
sfx(sfx_meow(), MEOWS[3], 0.4)
r.chord(e + E3_STAMP, [38, 45, 50, 53], 2.0, "piano", 95)
sfx(thud(), e + E3_STAMP, 0.45)
# ======== final (74-102) ========
e = T["fim"]
for a, b, c in each(e, e + 5, [AM, F]):
    pad(a, b, c, 48, "slow")
    low(a, b, c, 62)
    r.note(a + 0.4, c["t"][3], 2.5, "piano", 55)
    r.note(a + BEAT * 2, c["t"][1], 2.5, "piano", 48)
pad(e + 5, e + FIM_BULB, DM, 50, "slow"); low(e + 5, e + FIM_BULB, DM, 60)
r.note(e + FIM_PHONE, 84, 2.5, "celesta", 62)
r.note(e + FIM_PHONE + 0.75, 79, 2.5, "celesta", 55)
r.note(e + FIM_PHONE + 1.5, 76, 2.5, "celesta", 55)
r.chord(e + FIM_BULB, [60, 64, 67, 72, 76], 3.0, "harp", 80, roll=0.08)
r.note(e + FIM_BULB, 84, 3.0, "celesta", 85)
sfx(sfx_meow(), MEOWS[4], 0.4)
# esperança: Dó, Sol, Lá menor, Fá (coins)
prog3 = [C, G, AM, F]
for a, b, c in each(e + 7.6, e + 16, prog3):
    pad(a, b, c, 58, "strings")
    low(a, b, c, 72)
    arp(a, b, c, BEAT / 2, 54, "guitar", pat=(0, 1, 2, 3, 2, 1))
    r.note(a, c["t"][3] + 12, 2.5, "piano", 62)
for i, cc in enumerate(FIM_COINS):
    sfx(sfx_coin(), T["fim"] + cc + 0.6, 0.30)
    r.note(T["fim"] + cc + 0.6, [84, 86, 88][i % 3], 1.5, "celesta", 55)
# Japão: tema do Mochi
tema = [(64, 0.75), (67, 0.75), (69, 1.5), (67, 0.75), (64, 0.75), (62, 1.5),
        (64, 0.75), (67, 0.75), (72, 1.5), (71, 0.75), (69, 0.75), (67, 1.5)]
ja = T["japao"]
for a, b, c in each(ja, ja + 12, [C, G, AM, F]):
    pad(a, b, c, 66, "strings")
    low(a, b, c, 78)
    arp(a, b, c, BEAT / 2, 52, "harp", pat=(0, 1, 2, 3, 2, 1))
tt = ja + 0.2
for nt, d in tema:
    r.note(tt, nt + 12, d * 1.05, "flute", 78)
    r.note(tt, nt, d * 1.0, "piano", 72)
    tt += d
sfx(sfx_meow(), MEOWS[5], 0.4)
sfx(sfx_meow(), MEOWS[6], 0.35)
# fim: acorde final
r.chord(T["cartao"] + 4.5, [48, 55, 64, 72], 4.0, "strings", 70)
r.chord(T["cartao"] + 4.5, [48, 52, 55, 60, 64], 4.0, "piano", 70, roll=0.06)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_trabalhos.wav")
    music = r.render()
    n = int(TOTAL * SR)
    sf = m.bus["sfx"][:n]
    print("rms musica", float(np.sqrt((music ** 2).mean())), "pico", float(np.abs(music).max()), "| rms sfx", float(np.sqrt((sf ** 2).mean())), "pico", float(np.abs(sf).max()))
    mix_down(music * 2.6, sf, out, TOTAL, sfx_gain=0.5)
    print(out)
