"""Som de 'Caixa pequena' (10 s, 120 BPM, Sol menor, escala In em Ré). Estilo suave: piano, cordas e graves.

0-0.9   título, a caixa aparece (pizzicato) | 0.9-2.6 'Eu: cabe.' o Mochi anda até à caixa
2.6-4.0 a patinha | 4.0-5.6 a cabeça bate: nota grave + miado de susto 4.5
5.6-6.4 senta-se na caixa (PLOF) | 6.4-9.3 cabe sim: miado feliz 6.7, melodia calma | 9.3-10 volta ao início (loop)
"""
import os

from mochi_audio import (Mix, bed, celesta, cello, deg, harp_gliss, midi, piano, pizz, render_soft, sfx_meow,
                         soft_hit, strings)

TOTAL = 10.0
MEOWS = [4.5, 6.7]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 62]
ARP_G = [55, 62, 65, 70, 69, 65]
ARP_EB = [51, 58, 62, 67, 65, 62]
ARP_D = [50, 57, 62, 67, 69, 62]

# 0-2.6: a caixa aparece, o Mochi vai até ela
bed(m, 0.0, 2.6, GM9, 43, ARP_G)
m.add(pizz(midi(deg(15)), 0.25), 0.35, 0.10, "sfx")
for t, d in [(1.0, 12), (1.5, 13), (2.0, 15)]:
    m.add(pizz(midi(deg(d)), 0.2), t, 0.06, "sfx")

# 2.6-4.0: a patinha (tentativa tímida)
bed(m, 2.6, 4.0, EBMAJ7, 39, ARP_EB, gain=0.9)
m.add(strings([63, 67, 70], 1.6, 1800), 2.6, 0.10)
m.add(pizz(midi(deg(10)), 0.25), 3.1, 0.08, "sfx")

# 4.0-5.6: a cabeça bate na caixa
m.add(soft_hit(), 4.4, 0.25, "sfx")
m.add(sfx_meow(), MEOWS[0], 0.5, "sfx")
m.add(strings([50, 57, 62], 1.6, 900), 4.0, 0.16)
m.add(cello(midi(38), 1.6), 4.0, 0.22)

# 5.6-6.4: PLOF (senta-se)
m.add(soft_hit(), 5.95, 0.22, "sfx")
m.add(harp_gliss([62, 65, 69, 74], 0.06, 1.2), 6.0, 0.18)

# 6.4-9.3: cabe sim
bed(m, 6.4, 9.3, DSUS, 38, ARP_D, step=2.0)
m.add(celesta(midi(deg(15)), 1.0), 6.45, 0.12, "sfx")
m.add(sfx_meow(), MEOWS[1], 0.42, "sfx")
for t, d, dur in [(7.0, 8, 1.0), (8.0, 10, 1.0), (8.8, 12, 1.0)]:
    m.add(piano(midi(deg(d)), dur + 0.8, 0.7), t, 0.26)

# 9.3-10: volta ao início (loop)
bed(m, 9.3, 10.0, GM9, 43, ARP_G)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_caixa.wav")
    render_soft(m, out, TOTAL)
    print(out)
