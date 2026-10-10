"""Som de 'Eu a tentar pagar o voo para o Japão' (10 s, 120 BPM, Sol menor, escala In em Ré).

0.15-2.3 cada objeto cai no balcão: pop no tom + 'tlim' triste (vale 0€)
2.75     susto: faltam 1400€ (pancada, miado, apito a descer)
4.7-6.5  'Aceitam ronrons?': flauta doce e ronronar
6.6      RECUSADO: buzina grave (Ré e Mi bemol, da escala)
7.95-9   o Mochi atira tudo ao chão: pops a descer
9.2-10   tema do início (loop)
"""
import os

import numpy as np

from mochi_audio import (SR, Mix, bass, bell, deg, downer, flute, hat, kick, koto, midi, pad, sfx_blink,
                         sfx_meow, sfx_pop, sfx_snore, snare)

TOTAL = 10.0
MEOWS = [2.75, 5.0]
ITEM_T = [0.15, 0.85, 1.55, 2.25]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 63]

# ---- 0-2.6: objetos no balcão ----
m.add(pad(GM9, 2.8), 0, 0.22)
m.add(bass(midi(43), 1.3), 0, 0.4)
m.add(bass(midi(43), 1.2), 1.4, 0.35)
for k in range(11):
    m.add(hat(), k * 0.25, 0.06, bus="drums")
for i, t in enumerate(ITEM_T):
    m.add(kick(0.7), t, 0.6, bus="drums")
    m.add(sfx_pop(deg(5 + i)), t, 0.4, "sfx")
    m.add(sfx_blink(), t + 0.2, 0.25, "sfx")
    m.add(koto(midi(deg(7 + i)), 0.6), t + 0.1, 0.35)

# ---- 2.75: susto ----
m.add(kick(), 2.7, 1.0, bus="drums")
m.add(snare(), 2.7, 0.6, bus="drums")
m.add(bass(midi(38), 1.2), 2.7, 0.6)
m.add(sfx_meow(), MEOWS[0], 0.45, "sfx")
m.add(downer(0.8), 2.8, 0.15)
m.add(pad(DSUS, 2.0), 2.7, 0.22)
for t, d in [(3.3, 4), (3.8, 3), (4.3, 2)]:
    m.add(bell(midi(deg(d)), 1.0, 0.3), t, 0.18)

# ---- 4.7-6.5: ronrons ----
m.add(pad(EBMAJ7, 2.0), 4.6, 0.22)
m.add(sfx_meow(), MEOWS[1], 0.4, "sfx")
for t, d, dur in [(4.75, 7, 0.45), (5.25, 8, 0.25), (5.5, 10, 0.5), (6.0, 8, 0.5)]:
    m.add(flute(midi(deg(d)), dur), t, 0.22)
m.add(sfx_snore(1.0), 5.5, 0.3, "sfx")      # ronronar

# ---- 6.6: RECUSADO ----


def buzz(f, dur):
    t = np.arange(int(dur * SR)) / SR
    x = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * f * t)
    return x * np.minimum(t / 0.01, 1) * np.clip((dur - t) / 0.03, 0, 1)


m.add(buzz(midi(50), 0.22), 6.6, 0.12, "sfx")
m.add(buzz(midi(51), 0.4), 6.85, 0.12, "sfx")
m.add(snare(), 6.6, 0.5, bus="drums")
m.add(bass(midi(38), 1.2), 6.6, 0.5)
m.add(pad(DSUS, 1.4), 6.6, 0.2)

# ---- 7.95-9: tudo ao chão ----
for i in range(4):
    t = 7.95 + i * 0.28
    m.add(kick(0.6), t, 0.55, bus="drums")
    m.add(sfx_pop(deg(9 - i)), t, 0.4, "sfx")
m.add(bass(midi(39), 1.0), 8.0, 0.4)

# ---- 9.2-10: tema ----
m.add(pad(GM9, 1.0), 9.1, 0.22)
m.add(bass(midi(43), 0.8), 9.2, 0.35)
for t, d in [(9.25, 5), (9.5, 7), (9.75, 8)]:
    m.add(koto(midi(deg(d)), 0.6), t, 0.4)
for k in range(3):
    m.add(hat(), 9.25 + k * 0.25, 0.06, bus="drums")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_pagar.wav")
    m.render(out, TOTAL, fade=0.2)
    print(out)
