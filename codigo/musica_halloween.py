"""Som de 'Halloween: o maior susto é a minha conta' (10 s, 120 BPM, Sol menor, escala In em Ré).

0.15    VRUUM do aspirador (ruído grave) | 0.25 miado de susto
2.3     pepino: pancada | 2.4 miado de susto
4.0     '3. A minha conta': sinos de caixa de música
4.6     luzes apagam: trovão + baixo grave | 5.0 relâmpago e grito (miado)
7.0     luzes voltam: moeda | 7.6 miado feliz | 9.0-10 tema assustador do início (loop)
"""
import os

import numpy as np

from mochi_audio import (SR, RNG, Mix, bass, bell, deg, downer, flute, hat, kick, koto, lp, midi, pad, riser,
                         sfx_coin, sfx_meow, sfx_pop, snare)

TOTAL = 10.0
MEOWS = [0.25, 2.4, 5.0, 7.6]
m = Mix(TOTAL)

GM = [55, 58, 62]
EB = [51, 55, 58]
DSUS = [50, 55, 57, 63]


def vroom(dur):
    t = np.arange(int(dur * SR)) / SR
    x = lp(RNG.normal(0, 1, len(t)), 500) * (1 + 0.5 * np.sin(2 * np.pi * 30 * t))
    return x * np.minimum(t / 0.03, 1) * np.clip((dur - t) / 0.2, 0, 1)


def thunder(dur):
    t = np.arange(int(dur * SR)) / SR
    x = lp(RNG.normal(0, 1, len(t)), 220) * 3
    return x * np.exp(-t * 2.5) * np.minimum(t / 0.01, 1)


def spooky_groove(t0, t1):
    t = t0
    k = 0
    while t < t1 - 0.01:
        m.add(bass(midi(43 if k % 4 < 2 else 39), 0.4), t, 0.33)
        m.add(kick(0.6), t, 0.45, bus="drums")
        m.add(hat(), t + 0.25, 0.06, bus="drums")
        t += 0.5
        k += 1


def spooky_theme(t0):
    for i, d in enumerate([10, 8, 7, 8, 6, 5, 6, 3]):
        m.add(bell(midi(deg(d)), 0.5, 0.45), t0 + i * 0.25, 0.14)


# ---- 0-4: lista de sustos ----
spooky_groove(0, 4.5)
m.add(pad(GM, 2.0), 0, 0.18)
m.add(pad(EB, 2.5), 2.0, 0.18)
m.add(vroom(1.0), 0.1, 0.5, "sfx")
m.add(snare(), 0.15, 0.5, bus="drums")
m.add(sfx_meow(), MEOWS[0], 0.5, "sfx")
spooky_theme(0.75)
m.add(sfx_pop(deg(2)), 2.0, 0.3, "sfx")
m.add(kick(1.0), 2.3, 0.9, bus="drums")
m.add(snare(), 2.3, 0.5, bus="drums")
m.add(sfx_meow(), MEOWS[1], 0.5, "sfx")
for t, d in [(4.0, 12), (4.15, 10), (4.3, 11)]:
    m.add(bell(midi(deg(d)), 0.6, 0.3), t, 0.16)

# ---- 4.6: escuro ----
m.add(thunder(2.0), 4.6, 0.7, "sfx")
m.add(bass(midi(31), 2.2), 4.6, 0.5)
m.add(pad(DSUS, 2.3), 4.6, 0.12)
m.add(thunder(1.2), 5.0, 0.5, "sfx")
m.add(sfx_meow(), MEOWS[2], 0.65, "sfx")
for t, d in [(5.8, 4), (6.2, 3), (6.6, 2)]:
    m.add(bell(midi(deg(d)), 0.9, 0.25), t, 0.15)

# ---- 7.0: luzes voltam ----
m.add(sfx_coin(), 7.0, 0.35, "sfx")
m.add(snare(), 7.0, 0.5, bus="drums")
m.add(sfx_meow(), MEOWS[3], 0.5, "sfx")
spooky_groove(7.0, 10.0)
m.add(pad(EB, 2.0), 7.0, 0.18)
m.add(pad(GM, 1.1), 9.0, 0.18)
for t, d, dur in [(7.75, 8, 0.25), (8.0, 10, 0.4), (8.5, 8, 0.25)]:
    m.add(flute(midi(deg(d)), dur), t, 0.2)
spooky_theme(9.0)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_halloween.wav")
    m.render(out, TOTAL, fade=0.2)
    print(out)
