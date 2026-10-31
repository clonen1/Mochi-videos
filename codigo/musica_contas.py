"""Som de 'Quantos ramens custa ir ao Japão?' (10 s, 120 BPM, Sol menor, escala In em Ré).

0-2     groove de contas: BIPs da calculadora no tempo | 2-4 os BIPs aceleram, riser
4.0     PFFF: a calculadora rebenta (ruído + nota grave) | 4.1 miado de susto
5.6     'MUITOS ramens': acorde grave e sinos tristes | 7.4 plano: tema feliz, miado 7.6
9.2-10  BIPs voltam (loop)
"""
import os

import numpy as np

from mochi_audio import (SR, Mix, bass, bell, deg, downer, flute, hat, kick, koto, midi, pad, riser, sfx_coin,
                         sfx_meow, sfx_pop, snare, lp, RNG)

TOTAL = 10.0
MEOWS = [4.1, 7.6]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 63]


def beep(d, dur=0.07):
    t = np.arange(int(dur * SR)) / SR
    f = midi(deg(d))
    return np.sign(np.sin(2 * np.pi * f * t)) * 0.35 * np.minimum(1, (dur - t) / 0.01)


def groove(t0, t1, root=43):
    t = t0
    while t < t1 - 0.01:
        m.add(bass(midi(root), 0.42), t, 0.34)
        m.add(kick(0.7), t, 0.5, bus="drums")
        m.add(hat(), t + 0.25, 0.07, bus="drums")
        t += 0.5


def beeps(t0, t1, step):
    t, k = t0, 0
    while t < t1 - 0.01:
        m.add(beep([12, 13, 15, 13][k % 4]), t, 0.13, "sfx")
        t += step
        k += 1


# ---- 0-2: a fazer contas ----
groove(0, 2.0)
m.add(pad(GM9, 2.2), 0, 0.18)
beeps(0.0, 2.0, 1 / 6)
for t, d in [(0.5, 7), (1.0, 8), (1.5, 10)]:
    m.add(koto(midi(deg(d)), 0.5), t, 0.3)

# ---- 2-4: contas a fugir ----
groove(2.0, 4.0, 39)
m.add(pad(EBMAJ7, 2.0), 2.0, 0.16)
beeps(2.0, 4.0, 1 / 10)
for k in range(12):
    m.add(sfx_pop(deg(8 + k % 5)), 2.05 + k * 0.15, 0.12, "sfx")       # ramens a saltar do visor
m.add(riser(1.0), 3.0, 0.12)

# ---- 4.0: PFFF ----
t = np.arange(int(1.2 * SR)) / SR
hiss = lp(RNG.normal(0, 1, len(t)), 3000) * np.exp(-t * 2.5) * np.minimum(t / 0.01, 1)
m.add(hiss, 4.0, 0.3, "sfx")
m.add(kick(1.0), 4.0, 0.9, bus="drums")
m.add(bass(midi(38), 0.8), 4.0, 0.5)
m.add(sfx_meow(), MEOWS[0], 0.6, "sfx")
m.add(downer(1.0), 4.3, 0.1)

# ---- 5.6-7.4: MUITOS ramens ----
m.add(snare(), 5.6, 0.5, bus="drums")
m.add(pad(EBMAJ7, 1.9), 5.6, 0.22)
for k, tt in enumerate([5.6, 6.1, 6.6, 7.1]):
    m.add(bass(midi(39 if k % 2 == 0 else 38), 0.45), tt, 0.38)
for tt, d in [(5.8, 12), (6.3, 11), (6.8, 10)]:
    m.add(bell(midi(deg(d)), 0.5, 0.3), tt, 0.13)

# ---- 7.4-9.2: o plano ----
m.add(sfx_coin(), 7.4, 0.3, "sfx")
m.add(sfx_meow(), MEOWS[1], 0.5, "sfx")
groove(7.5, 9.5)
m.add(pad(DSUS, 2.0), 7.4, 0.16)
for tt, d, dur in [(7.75, 8, 0.25), (8.0, 10, 0.25), (8.25, 12, 0.5), (8.75, 10, 0.25), (9.0, 8, 0.25)]:
    m.add(flute(midi(deg(d)), dur), tt, 0.2)

# ---- 9.3-10: volta às contas (liga ao início) ----
groove(9.5, 10.0)
m.add(pad(GM9, 0.8), 9.3, 0.16)
beeps(9.5, 10.0, 1 / 6)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_contas.wav")
    m.render(out, TOTAL, fade=0.2)
    print(out)
