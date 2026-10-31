"""Som do 'Dia 5: o Mochi treina os pauzinhos' (10 s, 120 BPM, Sol menor, escala In em Ré).

0-0.35  groove a abrir, pauzinhos a mergulhar | 0.35 FLIP: a massa voa (apito a subir)
1.3     PLAF na cabeça + miado de susto | 2.2-2.9 pauzinhos a tremer (cliques)
3.0     TOING: um pauzinho foge | 4.1 plano B: cara na taça, slurps em groove
6.7     miado feliz 'aprovado' | 8.4 tema | 9.3 a massa volta para a taça (loop)
"""
import os

import numpy as np

from mochi_audio import (SR, Mix, bass, bell, deg, downer, flute, hat, kick, koto, midi, pad, riser, sfx_coin,
                         sfx_meow, sfx_pop, snare)

TOTAL = 10.0
MEOWS = [1.4, 6.7]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 63]


def slide(f0, f1, dur, g=1.0):
    t = np.arange(int(dur * SR)) / SR
    f = f0 + (f1 - f0) * t / dur
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / dur) * g


def groove(t0, t1, root=43):
    t = t0
    while t < t1 - 0.01:
        m.add(bass(midi(root), 0.42), t, 0.34)
        m.add(kick(0.7), t, 0.5, bus="drums")
        m.add(hat(), t + 0.25, 0.07, bus="drums")
        t += 0.5


# ---- 0-2: a primeira tentativa ----
groove(0, 1.0)
m.add(pad(GM9, 2.2), 0, 0.2)
for t, d in [(0.0, 7), (0.12, 8), (0.25, 10)]:
    m.add(koto(midi(deg(d)), 0.4), t, 0.34)
m.add(sfx_pop(deg(10)), 0.35, 0.45, "sfx")
m.add(slide(midi(deg(7)), midi(deg(15)), 0.5), 0.38, 0.22, "sfx")      # a massa sobe
m.add(slide(midi(deg(15)), midi(deg(8)), 0.4), 0.9, 0.18, "sfx")       # e desce
m.add(snare(), 1.3, 0.7, bus="drums")
m.add(sfx_pop(deg(0)), 1.3, 0.5, "sfx")                                # PLAF
m.add(sfx_meow(), MEOWS[0], 0.55, "sfx")
m.add(downer(0.6), 1.5, 0.08)

# ---- 2-4: tentativa 2 ----
groove(2.0, 3.0, 39)
m.add(pad(EBMAJ7, 2.0), 2.0, 0.15)
for k in range(10):
    m.add(bell(midi(deg(12 + k % 2)), 0.08, 0.2), 2.2 + k * 0.075, 0.12, "sfx")   # clic clic
m.add(slide(midi(deg(10)), midi(deg(17)), 0.25), 3.0, 0.3, "sfx")      # TOING
m.add(slide(midi(deg(17)), midi(deg(12)), 0.35), 3.25, 0.18, "sfx")
m.add(kick(0.9), 3.0, 0.7, bus="drums")
for t, d in [(3.4, 5), (3.65, 4)]:
    m.add(bass(midi(deg(d, 38)), 0.25), t, 0.35)

# ---- 4-6.5: plano B, cara na taça ----
m.add(riser(0.4), 3.7, 0.09)
m.add(snare(), 4.1, 0.5, bus="drums")
groove(4.0, 6.5)
m.add(pad(GM9, 2.6), 4.0, 0.18)
for t in np.arange(4.45, 6.3, 0.5):
    m.add(slide(midi(deg(3)), midi(deg(9)), 0.22), t, 0.2, "sfx")      # slurp
    m.add(hat(), t + 0.12, 0.05, bus="drums")
for t, d in [(4.5, 5), (4.75, 7), (5.0, 8), (5.25, 10), (5.5, 8), (5.75, 7), (6.0, 5)]:
    m.add(koto(midi(deg(d)), 0.45), t, 0.3)

# ---- 6.5-9: aprovado ----
m.add(sfx_coin(), 6.5, 0.32, "sfx")
m.add(sfx_meow(), MEOWS[1], 0.5, "sfx")
groove(6.5, 9.0)
m.add(pad(DSUS, 2.5), 6.5, 0.16)
for t, d, dur in [(7.0, 8, 0.25), (7.25, 10, 0.25), (7.5, 12, 0.5), (8.0, 10, 0.25), (8.25, 8, 0.25),
                  (8.5, 7, 0.5)]:
    m.add(flute(midi(deg(d)), dur), t, 0.2)

# ---- 9-10: a massa volta para a taça (liga ao início) ----
groove(9.0, 10.0)
m.add(pad(GM9, 1.2), 9.0, 0.18)
m.add(slide(midi(deg(12)), midi(deg(5)), 0.4), 9.3, 0.16, "sfx")
m.add(sfx_pop(deg(7)), 9.7, 0.25, "sfx")
for t, d in [(9.5, 5), (9.75, 7)]:
    m.add(koto(midi(deg(d)), 0.4), t, 0.3)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_dia5.wav")
    m.render(out, TOTAL, fade=0.2)
    print(out)
