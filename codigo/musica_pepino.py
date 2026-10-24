"""Som de 'Eu vs o pepino' (10 s, 120 BPM, Sol menor, escala In em Ré).

0-1.6   groove calmo a comer (koto) | 1.0 pepino entra: deslizar grave
1.65    SALTO: pancada, miado de susto, apito a subir | 1.8-3.7 tremer lá em cima (hats rápidos)
3.8     aterra | 4.0-5.4 tensão: baixo pulsado | 5.5-7.1 cheirar: sinos curiosos
7.2     PLOC: o pepino voa, moeda | 7.4 miado feliz | 8.6-10 volta a comer (loop)
"""
import os

import numpy as np

from mochi_audio import (SR, Mix, bass, bell, deg, downer, flute, hat, kick, koto, midi, pad, riser, sfx_coin,
                         sfx_meow, sfx_pop, snare)

TOTAL = 10.0
MEOWS = [1.7, 7.45]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 63]


def slide(f0, f1, dur):
    t = np.arange(int(dur * SR)) / SR
    f = f0 + (f1 - f0) * t / dur
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / dur)


def chew_groove(t0, t1):
    t = t0
    while t < t1 - 0.01:
        m.add(bass(midi(43), 0.4), t, 0.3)
        m.add(kick(0.6), t, 0.45, bus="drums")
        m.add(hat(), t + 0.25, 0.06, bus="drums")
        t += 0.5


# ---- 0-1.6: a comer em paz ----
chew_groove(0, 1.5)
m.add(pad(GM9, 1.7), 0, 0.18)
for t, d in [(0.0, 5), (0.25, 7), (0.5, 8), (0.75, 7), (1.0, 5), (1.25, 7)]:
    m.add(koto(midi(deg(d)), 0.5), t, 0.34)
for t in (0.3, 0.8, 1.3):
    m.add(sfx_pop(deg(9)), t, 0.12, "sfx")      # nham
m.add(slide(midi(38), midi(43), 0.5), 1.0, 0.18, "sfx")

# ---- 1.65: SALTO ----
m.add(kick(1.0), 1.65, 1.0, bus="drums")
m.add(snare(), 1.65, 0.6, bus="drums")
m.add(slide(midi(deg(5)), midi(deg(15)), 0.3), 1.65, 0.22, "sfx")
m.add(sfx_meow(), MEOWS[0], 0.6, "sfx")
for k in range(16):
    m.add(hat(), 2.0 + k * 0.11, 0.09, bus="drums")
m.add(pad(DSUS, 2.0), 1.8, 0.16)

# ---- 3.8: aterra e enfrenta o inimigo ----
m.add(kick(0.9), 3.8, 0.8, bus="drums")
m.add(sfx_pop(deg(2)), 3.8, 0.3, "sfx")
for k in range(6):
    t = 4.0 + k * 0.25
    m.add(bass(midi(38 if k % 2 == 0 else 39), 0.2), t, 0.4)
m.add(pad(EBMAJ7, 1.6), 4.0, 0.14)

# ---- 5.5-7.1: cheirar ----
for t, d in [(5.6, 10), (5.9, 11), (6.3, 10), (6.6, 12)]:
    m.add(bell(midi(deg(d)), 0.4, 0.4), t, 0.13)
m.add(downer(0.5), 6.7, 0.08)

# ---- 7.2: PLOC ----
m.add(sfx_pop(deg(10)), 7.2, 0.5, "sfx")
m.add(snare(), 7.2, 0.5, bus="drums")
m.add(riser(0.3), 7.0, 0.08)
m.add(sfx_coin(), 7.35, 0.3, "sfx")
m.add(sfx_meow(), MEOWS[1], 0.5, "sfx")
for t, d, dur in [(7.75, 8, 0.25), (8.0, 10, 0.4), (8.5, 8, 0.25)]:
    m.add(flute(midi(deg(d)), dur), t, 0.2)

# ---- 8.6-10: volta a comer (liga ao início) ----
chew_groove(8.0, 10.0)
m.add(pad(GM9, 2.0), 8.0, 0.18)
for t, d in [(9.0, 5), (9.25, 7), (9.5, 8), (9.75, 7)]:
    m.add(koto(midi(deg(d)), 0.5), t, 0.34)
for t in (9.3, 9.8):
    m.add(sfx_pop(deg(9)), t, 0.12, "sfx")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_pepino.wav")
    m.render(out, TOTAL, fade=0.2)
    print(out)
