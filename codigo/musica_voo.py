"""Som do vídeo 'Eu a ver o preço do voo para o Japão' (10 s, 120 BPM, Sol menor, escala In em Ré).

0-2.5   tema alegre de koto (o Mochi está todo contente)
2.5-4   o preço sobe: notas a subir cada vez mais rápido + subida de ruído
4.0     o preço aparece: pancada, miado de susto, apito a descer (cai para trás)
4.5-8.8 tristeza cómica: sinos lentos e graves, 'Plano B' com um pop
8.8-10  o tema volta (liga ao início, para o vídeo dar a volta)
"""
import os

import numpy as np

from mochi_audio import (SR, Mix, bass, bell, deg, downer, hat, kick, koto, midi, pad, riser,
                         sfx_meow, sfx_pop, snare)

TOTAL = 10.0
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 63]

# ---- 0-2.5: tema alegre ----
m.add(pad(GM9, 2.6), 0, 0.26)
m.add(bass(midi(43), 1.9), 0, 0.45)
for t, d in [(0, 5), (0.25, 7), (0.5, 8), (0.75, 7), (1.0, 5), (1.5, 7), (1.75, 9), (2.0, 10)]:
    m.add(koto(midi(deg(d)), 1.0), t, 0.5)
for k in range(10):
    m.add(hat(), k * 0.25, 0.08 if k % 2 else 0.05, bus="drums")
m.add(kick(), 0, 0.7, bus="drums")
m.add(kick(), 1.0, 0.6, bus="drums")

# ---- 2.5-4: o preço a subir ----
m.add(pad(DSUS, 1.7), 2.4, 0.3)
m.add(riser(1.5), 2.5, 0.2)
ticks = np.cumsum([0.22, 0.18, 0.15, 0.12, 0.1, 0.09, 0.08, 0.07, 0.065, 0.06, 0.055, 0.05])
for i, dt in enumerate(ticks):
    t = 2.5 + dt - ticks[0]
    if t < 3.95:
        m.add(bell(midi(deg(5 + i)), 0.25, 0.5), t, 0.18)

# ---- 4.0: o preço aparece ----
m.add(kick(), 4.0, 1.0, bus="drums")
m.add(snare(), 4.0, 0.6, bus="drums")
m.add(bass(midi(38), 0.9), 4.0, 0.7)
m.add(downer(0.8), 4.05, 0.18)
m.add(sfx_meow(), 4.05, 0.5, "sfx")


def slide_down(dur=0.7):
    """Apito a descer (o Mochi cai para trás), de Ré6 a Ré4."""
    t = np.arange(int(dur * SR)) / SR
    f = midi(deg(10)) * (midi(deg(0)) / midi(deg(10))) ** (t / dur)
    vib = 1 + 0.01 * np.sin(2 * np.pi * 7 * t)
    return np.sin(2 * np.pi * np.cumsum(f * vib) / SR) * np.minimum(t / 0.02, 1) * (1 - t / dur) ** 0.5


m.add(slide_down(), 4.4, 0.32, "sfx")
m.add(kick(0.5), 5.1, 0.5, bus="drums")       # o Mochi bate no chão

# ---- 4.5-8.8: tristeza cómica ----
m.add(pad(EBMAJ7, 4.4), 4.6, 0.22)
m.add(bass(midi(39), 2.0), 5.0, 0.35)
m.add(bass(midi(38), 2.0), 7.0, 0.35)
for t, d in [(5.5, 4), (6.0, 3), (6.5, 2), (7.5, 3), (8.0, 1), (8.5, 2)]:
    m.add(bell(midi(deg(d)), 1.2, 0.3), t, 0.2)
m.add(sfx_pop(deg(7)), 6.8, 0.35, "sfx")      # 'Plano B'

# ---- 8.8-10: o tema volta ----
m.add(pad(GM9, 1.4), 8.7, 0.24)
m.add(bass(midi(43), 1.2), 8.8, 0.4)
for t, d in [(9.0, 5), (9.25, 7), (9.5, 8), (9.75, 7)]:
    m.add(koto(midi(deg(d)), 0.8), t, 0.45)
m.add(sfx_pop(), 9.0, 0.3, "sfx")             # o Mochi levanta-se

MEOWS = [4.05]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_voo.wav")
    m.render(out, TOTAL, fade=0.25)
    print(out)
