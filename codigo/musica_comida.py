"""Som de 'Tipos de gato quando chega a comida' (10 s, 120 BPM, Sol menor, escala In em Ré).

0.0     a taça cai: apito a descer | 0.25 PUM + 3 gatos a correr (passos) | 0.9 groove
1.6     o educado: koto delicado | 3.6 o dramático: acordes tristes, 2 miados (4.0 e 4.8)
5.8     o ninja: PUF + golpe de flauta, a mastigar | 7.9 'e tu?' tema com flauta
9.3     saem a correr, a taça sobe (loop)
"""
import os

import numpy as np

from mochi_audio import (SR, Mix, bass, bell, deg, downer, flute, hat, kick, koto, midi, pad, riser, sfx_coin,
                         sfx_meow, sfx_pop, snare)

TOTAL = 10.0
MEOWS = [4.0, 4.8]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 63]


def slide(f0, f1, dur, g=1.0):
    t = np.arange(int(dur * SR)) / SR
    f = f0 + (f1 - f0) * t / dur
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / dur) * g


def groove(t0, t1, root=43, kg=0.7):
    t = t0
    while t < t1 - 0.01:
        m.add(bass(midi(root), 0.42), t, 0.34)
        m.add(kick(kg), t, 0.5, bus="drums")
        m.add(hat(), t + 0.25, 0.07, bus="drums")
        t += 0.5


# ---- 0-1.6: a taça cai e chegam os três ----
m.add(slide(midi(deg(14)), midi(deg(6)), 0.25), 0.0, 0.25, "sfx")
m.add(kick(1.0), 0.25, 0.9, bus="drums")
m.add(snare(), 0.25, 0.6, bus="drums")
m.add(sfx_pop(deg(3)), 0.25, 0.4, "sfx")
for k in range(8):
    m.add(sfx_pop(deg(8 + k % 3)), 0.3 + k * 0.07, 0.14, "sfx")       # patinhas a correr
m.add(sfx_coin(), 0.9, 0.25, "sfx")
groove(1.0, 1.5)
m.add(pad(GM9, 1.6), 0.2, 0.18)

# ---- 1.6-3.6: o educado ----
groove(1.5, 3.5)
m.add(pad(GM9, 2.0), 1.6, 0.16)
for t, d in [(1.6, 10), (1.85, 12), (2.1, 10), (2.35, 8), (2.6, 7), (2.85, 8), (3.1, 10), (3.35, 7)]:
    m.add(koto(midi(deg(d)), 0.5), t, 0.3)
m.add(bell(midi(deg(15)), 0.6), 2.0, 0.12, "sfx")                       # piscadela

# ---- 3.6-5.8: o dramático ----
m.add(snare(), 3.6, 0.5, bus="drums")
m.add(pad(EBMAJ7, 2.2), 3.6, 0.22)
m.add(downer(0.8), 3.7, 0.12)
for k, t in enumerate([3.6, 4.1, 4.6, 5.1]):
    m.add(bass(midi(39 if k % 2 == 0 else 38), 0.45), t, 0.4)
    m.add(kick(0.5), t, 0.4, bus="drums")
for t, d, dur in [(4.3, 8, 0.4), (5.3, 7, 0.45)]:
    m.add(flute(midi(deg(d)), dur), t, 0.15)
for t0 in MEOWS:
    m.add(sfx_meow(), t0, 0.6, "sfx")

# ---- 5.8-7.8: o ninja ----
m.add(sfx_pop(deg(1)), 5.85, 0.5, "sfx")
m.add(downer(0.4), 5.85, 0.15)
m.add(slide(midi(deg(15)), midi(deg(10)), 0.15), 6.0, 0.25, "sfx")       # zás
m.add(flute(midi(deg(12)), 0.15), 6.05, 0.22)
groove(6.0, 7.9, 43, 0.6)
for t in np.arange(6.2, 7.7, 0.25):
    m.add(sfx_pop(deg(9 + int(t * 4) % 2)), t, 0.1, "sfx")              # nham nham
for t, d in [(6.5, 5), (6.75, 7), (7.0, 8), (7.25, 7)]:
    m.add(koto(midi(deg(d)), 0.4), t, 0.3)

# ---- 7.9-9.3: e tu? ----
m.add(riser(0.3), 7.6, 0.08)
groove(7.9, 9.4)
m.add(pad(DSUS, 1.6), 7.9, 0.16)
for t, d, dur in [(7.95, 10, 0.25), (8.2, 12, 0.25), (8.45, 13, 0.5), (8.95, 12, 0.3)]:
    m.add(flute(midi(deg(d)), dur), t, 0.2)

# ---- 9.3-10: saem, a taça sobe (liga ao início) ----
for k in range(6):
    m.add(sfx_pop(deg(10 - k % 3)), 9.3 + k * 0.07, 0.12, "sfx")
m.add(slide(midi(deg(6)), midi(deg(14)), 0.4), 9.4, 0.2, "sfx")
m.add(pad(GM9, 0.8), 9.3, 0.14)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_comida.wav")
    m.render(out, TOTAL, fade=0.2)
    print(out)
