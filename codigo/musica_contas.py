"""Som de 'Quantos ramens custa ir ao Japão?' (10 s, 120 BPM, Sol menor, escala In em Ré).
Estilo suave: piano e cordas, sem bateria, sem bips arcade.

0-2     teclas da calculadora = pizzicatos leves no tempo | 2-4 mais rápidos, cordas a crescer
4.0     a calculadora rebenta: nota grave + miado de susto | 5.6 'MUITOS ramens': cordas em Mib
7.4     o plano: melodia no piano, miado feliz 7.6 | 9.4-10 as contas recomeçam (loop)
"""
import os

from mochi_audio import (Mix, bed, celesta, cello, deg, harp_gliss, midi, piano, pizz, render_soft, sfx_meow,
                         soft_hit, strings)

TOTAL = 10.0
MEOWS = [4.1, 7.6]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 62]
ARP_G = [55, 62, 65, 70, 69, 65]
ARP_EB = [51, 58, 62, 67, 65, 62]
ARP_D = [50, 57, 62, 67, 69, 62]


def keys(t0, t1, step):
    t, k = t0, 0
    while t < t1 - 0.01:
        m.add(pizz(midi(deg([12, 13, 15, 13][k % 4])), 0.2), t, 0.06, "sfx")
        t += step
        k += 1


# 0-2: a fazer contas
bed(m, 0.0, 2.0, GM9, 43, ARP_G)
keys(0.0, 2.0, 1 / 6)

# 2-4: as contas fogem
bed(m, 2.0, 4.0, EBMAJ7, 39, ARP_EB, step=0.25, gain=0.9)
keys(2.0, 4.0, 1 / 10)
m.add(strings([63, 67, 70], 2.0, 2000), 2.0, 0.10)

# 4.0: a calculadora desiste
m.add(soft_hit(), 4.0, 0.25, "sfx")
m.add(sfx_meow(), MEOWS[0], 0.5, "sfx")
m.add(strings([50, 57, 62], 1.6, 900), 4.0, 0.16)
m.add(cello(midi(38), 1.6), 4.0, 0.22)

# 5.6-7.4: MUITOS ramens
m.add(strings(EBMAJ7, 1.9, 1100), 5.6, 0.2)
m.add(cello(midi(39), 1.8), 5.6, 0.24)
for t, d in [(5.8, 12), (6.3, 11), (6.8, 10)]:
    m.add(piano(midi(deg(d)), 1.2, 0.6), t, 0.24)

# 7.4-9.4: o plano
m.add(celesta(midi(deg(15)), 1.0), 7.4, 0.12, "sfx")
m.add(sfx_meow(), MEOWS[1], 0.45, "sfx")
bed(m, 7.4, 9.4, DSUS, 38, ARP_D, step=1.0)
for t, d, dur in [(7.75, 8, 0.25), (8.0, 10, 0.25), (8.25, 12, 0.5), (8.75, 10, 0.25), (9.0, 8, 0.4)]:
    m.add(piano(midi(deg(d)), dur + 0.8, 0.7), t, 0.28)

# 9.4-10: volta às contas (liga ao início)
bed(m, 9.4, 10.0, GM9, 43, ARP_G)
keys(9.5, 10.0, 1 / 6)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_contas.wav")
    render_soft(m, out, TOTAL)
    print(out)
