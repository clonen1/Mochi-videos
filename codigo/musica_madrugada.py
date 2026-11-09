"""Som de 'Madrugada' (10 s, 120 BPM, Lá menor). Suave e lento: piano, cordas, contrabaixo e violoncelo; sem bateria nem som arcade.

0-2.4   quarto calmo: acorde de Lá menor, tique-taque do relógio muito discreto
2.4     o Mochi agacha: cordas a crescer | 2.8 miado curto de entusiasmo
3.0-6.4 a correria: piano em arpejo rápido sobre Ré menor, pizzicatos em colcheias, duas pancadas macias da almofada (4.1 e 5.3)
6.4-7.4 pára: acorde seguro, miado pequeno 7.5 | 7.4-9.4 'Eu: ...' calma outra vez | 9.4-10 liga ao início (loop)
"""
import os

from mochi_audio import (Mix, bed, celesta, cello, deg, harp_gliss, midi, piano, pizz, render_soft, sfx_meow,
                         soft_hit, strings)

TOTAL = 10.0
MEOWS = [2.8, 7.5]
m = Mix(TOTAL)

AM9 = [57, 60, 64, 71]
ARP_AM = [57, 64, 60, 71, 64, 60]
DM9 = [50, 57, 60, 64]
ARP_DM = [50, 57, 62, 65, 69, 65, 62, 57]
FMAJ7 = [53, 57, 60, 64]
ARP_F = [53, 60, 57, 64, 60, 57]


def tick(t0, t1, step=0.5, g=0.05):
    t = t0
    while t < t1 - 0.01:
        m.add(pizz(midi(96), 0.08), t, g, "sfx")
        t += step


# 0-2.4: quarto calmo, 3 da manhã
bed(m, 0.0, 2.4, AM9, 45, ARP_AM, gain=0.85)
tick(0.0, 2.4)

# 2.4: o Mochi agacha, algo vai acontecer
m.add(strings([57, 64, 69], 1.0, 900), 2.4, 0.16)
m.add(cello(midi(45), 1.0), 2.4, 0.22)
m.add(sfx_meow(), MEOWS[0], 0.42, "sfx")

# 3.0-6.4: a correria
bed(m, 3.0, 4.7, DM9, 38, ARP_DM, step=0.25, gain=0.95)
bed(m, 4.7, 6.4, FMAJ7, 41, ARP_F, step=0.25, gain=0.95)
for t in [3.0 + i / 6 for i in range(int(3.4 * 6))]:
    m.add(pizz(midi(deg([8, 10, 12, 10][int((t - 3.0) * 6) % 4])), 0.25), t, 0.07, "sfx")
for t in (4.1, 5.3):
    m.add(soft_hit(), t, 0.3, "sfx")
m.add(harp_gliss([62, 65, 69, 72, 77], 0.06, 1.2), 3.0, 0.14)

# 6.4-7.4: pára e senta-se
m.add(strings(AM9, 2.0, 1000), 6.4, 0.18)
m.add(cello(midi(45), 2.0), 6.4, 0.24)
m.add(piano(midi(57), 2.0, 0.6), 6.45, 0.28)
m.add(sfx_meow(), MEOWS[1], 0.3, "sfx")

# 7.4-9.4: 'Eu: ...' como se nada fosse
bed(m, 7.4, 9.4, AM9, 45, ARP_AM, step=1.0, gain=0.8)
m.add(celesta(midi(deg(15)), 1.0), 8.2, 0.1, "sfx")
tick(7.4, 9.4)

# 9.4-10: liga ao início (loop)
bed(m, 9.4, 10.0, AM9, 45, ARP_AM, gain=0.85)
tick(9.4, 10.0)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_madrugada.wav")
    render_soft(m, out, TOTAL)
    print(out)
