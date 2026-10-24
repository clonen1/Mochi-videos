"""Som do 'Dia 4: o Mochi conta a vaquinha' (10 s, 120 BPM, Sol menor, escala In em Ré).

0.0     mealheiro cai: apito a descer | 0.45 PUM (apanha) | 0.6 miado feliz
2.2-3.3 abana o mealheiro: chocalho sem moedas (só hat) | 3.4 sai uma traça: flauta a tremer
4.5     painel do total: sino | 4.75 miado de susto + apito a descer | 5.5 sinos tristes
7.0     'ainda dá tempo': groove volta, moeda | 7.4 miado feliz
9.0     atira o mealheiro ao ar: subida | 9.5-10 tema (loop)
"""
import os

import numpy as np

from mochi_audio import (SR, Mix, bass, bell, deg, downer, flute, hat, kick, koto, midi, pad, riser, sfx_coin,
                         sfx_meow, sfx_pop, snare)

TOTAL = 10.0
MEOWS = [0.6, 4.75, 7.4]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 63]


def whistle_down(dur):
    t = np.arange(int(dur * SR)) / SR
    f = midi(deg(12)) * (1 - 0.5 * t / dur)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(t / 0.02, 1) * 0.6


# ---- groove (pára durante o abanar e o susto) ----
for b in range(20):
    t = b * 0.5
    if 2.2 <= t < 4.5 or 4.5 <= t < 7.0 and t not in (4.5, 5.5, 6.5):
        continue
    root = 43 if t < 4.5 else (39 if t < 8.5 else 43)
    m.add(bass(midi(root), 0.45), t, 0.36)
    m.add(kick(0.7), t, 0.5, bus="drums")
    m.add(hat(), t + 0.25, 0.07, bus="drums")
m.add(pad(GM9, 2.3), 0, 0.2)
m.add(pad(DSUS, 2.4), 4.5, 0.14)
m.add(pad(EBMAJ7, 2.0), 7.0, 0.2)
m.add(pad(GM9, 1.1), 9.0, 0.2)

# ---- 0.0: o mealheiro cai e o Mochi apanha ----
m.add(whistle_down(0.45), 0.0, 0.25, "sfx")
m.add(kick(1.0), 0.45, 0.9, bus="drums")
m.add(snare(), 0.45, 0.5, bus="drums")
m.add(sfx_pop(deg(3)), 0.45, 0.4, "sfx")
m.add(sfx_meow(), MEOWS[0], 0.5, "sfx")
for t, d in [(1.0, 5), (1.25, 7), (1.5, 8), (1.75, 7)]:
    m.add(koto(midi(deg(d)), 0.6), t, 0.38)

# ---- 2.2-3.3: abana, abana... nada ----
for k in range(9):
    m.add(hat(), 2.2 + k * 0.125, 0.12, bus="drums")
m.add(bell(midi(deg(2)), 0.5, 0.2), 3.3, 0.1)
for k in range(10):  # traça: flauta curta a tremer
    m.add(flute(midi(deg(5 + (k % 2))), 0.08), 3.4 + k * 0.08, 0.12)

# ---- 4.5: total = 0€ ----
m.add(bell(midi(deg(10)), 0.8, 0.5), 4.5, 0.2)
m.add(sfx_meow(), MEOWS[1], 0.5, "sfx")
m.add(downer(0.9), 4.9, 0.16)
m.add(bass(midi(38), 1.2), 4.75, 0.45)
for t, d in [(5.5, 7), (5.9, 5), (6.3, 3), (6.7, 2)]:
    m.add(bell(midi(deg(d)), 0.9, 0.3), t, 0.16)

# ---- 7.0: ainda dá tempo ----
m.add(sfx_coin(), 7.0, 0.35, "sfx")
m.add(snare(), 7.0, 0.5, bus="drums")
m.add(sfx_meow(), MEOWS[2], 0.5, "sfx")
for t, d, dur in [(7.75, 8, 0.25), (8.0, 10, 0.4), (8.5, 8, 0.25), (8.75, 7, 0.25)]:
    m.add(flute(midi(deg(d)), dur), t, 0.2)

# ---- 9.0: atira o mealheiro e volta o tema ----
m.add(riser(0.5), 9.0, 0.12)
for t, d in [(9.5, 5), (9.75, 7)]:
    m.add(koto(midi(deg(d)), 0.5), t, 0.38)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_dia4.wav")
    m.render(out, TOTAL, fade=0.2)
    print(out)
