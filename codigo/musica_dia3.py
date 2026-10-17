"""Som do 'Dia 3: o Mochi aprende japonês' (10 s, 120 BPM, Sol menor, escala In em Ré).

0.25    'Miaugatô!' (miado) | 0.95 ERRADO: buzina grave
2.5     'Konni-MIAU!' (miado) | 3.2 'quase': sinos a descer
4.8     'Ramen kudasai!' (miado) | 5.4 PERFEITO: moeda e sinos a subir
6.9     bilhete de avião = ?: pancada e miado de susto | 7.4 0€: apito a descer
9.0-10  tema do início (loop)
"""
import os

import numpy as np

from mochi_audio import (SR, Mix, bass, bell, deg, downer, flute, hat, kick, koto, midi, pad, sfx_coin,
                         sfx_meow, sfx_pop, snare)

TOTAL = 10.0
MEOWS = [0.25, 2.5, 4.8, 6.95]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 63]


def buzz(f, dur):
    t = np.arange(int(dur * SR)) / SR
    x = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * f * t)
    return x * np.minimum(t / 0.01, 1) * np.clip((dur - t) / 0.03, 0, 1)


# ---- groove contínuo (2 compassos de Sol menor, 1 de Mi bemol, volta) ----
for b in range(18):
    t = b * 0.5
    if t >= 9.0:
        break
    root = 39 if 4.5 <= t < 6.5 else (38 if 6.5 <= t < 8.5 else 43)
    m.add(bass(midi(root), 0.45), t, 0.36)
    m.add(kick(0.7), t, 0.5, bus="drums")
    m.add(hat(), t + 0.25, 0.07, bus="drums")
m.add(pad(GM9, 4.6), 0, 0.2)
m.add(pad(EBMAJ7, 2.2), 4.5, 0.2)
m.add(pad(DSUS, 2.6), 6.5, 0.2)

# ---- 0.25: Miaugatô! ----
m.add(sfx_pop(deg(7)), 0.0, 0.35, "sfx")
m.add(sfx_meow(), MEOWS[0], 0.5, "sfx")
m.add(buzz(midi(50), 0.2), 0.95, 0.12, "sfx")
m.add(buzz(midi(51), 0.35), 1.18, 0.12, "sfx")
m.add(snare(), 0.95, 0.5, bus="drums")
for t, d in [(1.5, 5), (1.75, 4)]:
    m.add(koto(midi(deg(d)), 0.6), t, 0.35)

# ---- 2.5: Konni-MIAU ----
for t, d in [(2.2, 5), (2.35, 7)]:
    m.add(koto(midi(deg(d)), 0.5), t, 0.4)
m.add(sfx_meow(), MEOWS[1], 0.5, "sfx")
for t, d in [(3.2, 8), (3.45, 7), (3.7, 5)]:
    m.add(bell(midi(deg(d)), 0.7, 0.3), t, 0.18)

# ---- 4.8: Ramen kudasai! / PERFEITO ----
for t, d, dur in [(4.5, 7, 0.25), (4.75, 8, 0.25)]:
    m.add(flute(midi(deg(d)), dur), t, 0.22)
m.add(sfx_meow(), MEOWS[2], 0.5, "sfx")
m.add(sfx_coin(), 5.4, 0.4, "sfx")
m.add(snare(), 5.4, 0.5, bus="drums")
for i in range(6):
    m.add(bell(midi(deg(8 + i)), 0.4, 0.5), 5.5 + i * 0.08, 0.15)
for t, d, dur in [(5.75, 10, 0.4), (6.0, 8, 0.4)]:
    m.add(flute(midi(deg(d)), dur), t, 0.2)

# ---- 6.9: bilhete de avião = ? ----
m.add(kick(), 6.9, 1.0, bus="drums")
m.add(snare(), 6.9, 0.55, bus="drums")
m.add(bass(midi(38), 1.0), 6.9, 0.5)
m.add(sfx_meow(), MEOWS[3], 0.45, "sfx")
m.add(downer(0.8), 7.4, 0.15)
for t, d in [(7.6, 4), (8.0, 3), (8.4, 2)]:
    m.add(bell(midi(deg(d)), 0.9, 0.3), t, 0.16)

# ---- 9.0-10: tema (liga ao início) ----
m.add(pad(GM9, 1.1), 8.9, 0.2)
m.add(bass(midi(43), 0.9), 9.0, 0.35)
for t, d in [(9.0, 5), (9.25, 7), (9.5, 8), (9.75, 7)]:
    m.add(koto(midi(deg(d)), 0.6), t, 0.38)
for k in range(4):
    m.add(hat(), 9.0 + k * 0.25, 0.06, bus="drums")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_dia3.wav")
    m.render(out, TOTAL, fade=0.2)
    print(out)
