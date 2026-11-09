"""Som de 'Mochi e o saco de ração' (10 s, Sol menor, escala In em Ré).
Estilo suave e lento: piano, cordas e baixo; sem bateria nem sons arcade.

0-2.4   Mochi a dormir: bed muito calmo + ressonar | 2.4 o saco amachuca (CRRR), cordas em tensão
3.5     o Mochi aparece à taça: nota grave + harpa | 4.3 e 6.1 miados | 7.5 era o saco do pão: violoncelo cai
9.4-10  volta a dormir (liga ao início, loop)
"""
import os

import numpy as np

from mochi_audio import (RNG, SR, Mix, bed, celesta, cello, deg, harp_gliss, hp, lp, midi, piano, pizz, render_soft,
                         sfx_meow, sfx_snore, soft_hit, strings)

TOTAL = 10.0
MEOWS = [4.3, 6.1]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
CM = [48, 55, 58, 63]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 62]
ARP_G = [55, 62, 65, 70, 69, 65]
ARP_EB = [51, 58, 62, 67, 65, 62]
ARP_D = [50, 57, 62, 67, 69, 62]


def crinkle(dur=1.0):
    """Saco de papel a amachucar: estalidos curtos filtrados."""
    n = int(dur * SR)
    x = np.zeros(n)
    t = 0.0
    while t < dur - 0.05:
        i = int(t * SR)
        L = int(RNG.uniform(0.004, 0.02) * SR)
        x[i:i + L] += RNG.normal(0, 1, L) * np.linspace(1, 0, L) * RNG.uniform(0.3, 1.0)
        t += RNG.uniform(0.012, 0.07)
    env = np.sin(np.pi * np.arange(n) / n) ** 0.6
    return hp(lp(x, 7000), 1800) * env * 0.9


# 0-2.4: a dormir
bed(m, 0.0, 2.4, GM9, 43, ARP_G, step=1.2, gain=0.7)
m.add(sfx_snore(1.1), 0.4, 0.5, "sfx")
m.add(sfx_snore(1.0), 1.5, 0.5, "sfx")

# 2.4: CRRR! o saco
m.add(crinkle(1.0), 2.45, 0.6, "sfx")
m.add(strings([63, 67, 70], 1.3, 1500), 2.45, 0.14)
m.add(cello(midi(39), 1.2), 2.45, 0.18)
m.add(pizz(midi(deg(13)), 0.3), 3.25, 0.2, "sfx")

# 3.5: já estou aqui
m.add(soft_hit(), 3.5, 0.3, "sfx")
m.add(harp_gliss([67, 70, 74, 79], 0.05, 1.0), 3.55, 0.2)
bed(m, 3.5, 5.5, EBMAJ7, 39, ARP_EB, step=1.0, gain=0.9)
m.add(sfx_meow(), MEOWS[0], 0.5, "sfx")

# 5.5-7.5: onde está a ração?
bed(m, 5.5, 7.5, GM9, 43, ARP_G, step=1.0, gain=0.9)
m.add(sfx_meow(), MEOWS[1], 0.5, "sfx")

# 7.5: era o saco do pão
bed(m, 7.5, 9.4, DSUS, 38, ARP_D, step=2.0, gain=0.8)
for t, d in [(7.6, 12), (8.1, 10), (8.8, 8)]:
    m.add(piano(midi(deg(d)), 1.2, 0.6), t, 0.26)
m.add(celesta(midi(deg(6)), 1.2), 8.8, 0.10, "sfx")

# 9.4-10: volta a dormir (loop)
bed(m, 9.4, 10.0, GM9, 43, ARP_G, step=1.2, gain=0.7)
m.add(sfx_snore(0.6), 9.5, 0.4, "sfx")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_racao.wav")
    render_soft(m, out, TOTAL)
    print(out)
