"""Som de 'Mochi e o cartaz' (10 s, Sol menor, escala In em Ré). Suave e lento: piano, cordas e baixo.

0-2.6   Mochi a dormir (bed calmo + ressonar) | 2.7 o cartaz cola-se à parede (pancada suave)
4.4     o Mochi acorda (cordas em tensão) | 5.8 e 7.0 miados | 7.6-9.4 cartão final calmo
9.4-10  volta a dormir (liga ao início)
"""
import os

from mochi_audio import (Mix, bed, celesta, cello, deg, harp_gliss, midi, piano, pizz, render_soft, sfx_meow, sfx_snore,
                         soft_hit, strings)

TOTAL = 10.0
MEOWS = [5.8, 7.0]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
CM = [48, 55, 58, 63]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 62]
ARP_G = [55, 62, 65, 70, 69, 65]
ARP_C = [48, 55, 58, 63, 62, 58]
ARP_EB = [51, 58, 62, 67, 65, 62]
ARP_D = [50, 57, 62, 67, 69, 62]

bed(m, 0.0, 2.6, GM9, 43, ARP_G, step=1.2, gain=0.7)
m.add(sfx_snore(1.1), 0.4, 0.5, "sfx")
m.add(sfx_snore(1.0), 1.5, 0.5, "sfx")

m.add(soft_hit(), 2.7, 0.3, "sfx")                      # cartaz cola-se
m.add(piano(midi(deg(8)), 1.0, 0.6), 2.75, 0.22)
bed(m, 2.7, 4.4, CM, 36, ARP_C, step=1.1, gain=0.8)

m.add(strings([63, 67, 70], 1.2, 1500), 4.3, 0.14)     # acorda
m.add(cello(midi(39), 1.2), 4.3, 0.18)
m.add(pizz(midi(deg(13)), 0.3), 4.55, 0.2, "sfx")
bed(m, 4.4, 7.5, EBMAJ7, 39, ARP_EB, step=1.0, gain=0.9)
m.add(sfx_meow(), MEOWS[0], 0.5, "sfx")
m.add(sfx_meow(), MEOWS[1], 0.5, "sfx")

bed(m, 7.5, 9.4, DSUS, 38, ARP_D, step=2.0, gain=0.8)  # cartão final
for t, d in [(7.6, 12), (8.1, 10), (8.8, 8)]:
    m.add(piano(midi(deg(d)), 1.2, 0.6), t, 0.26)
m.add(harp_gliss([67, 70, 74, 79], 0.05, 1.0), 7.55, 0.16)
m.add(celesta(midi(deg(6)), 1.2), 8.8, 0.10, "sfx")

bed(m, 9.4, 10.0, GM9, 43, ARP_G, step=1.2, gain=0.7)  # loop
m.add(sfx_snore(0.6), 9.5, 0.4, "sfx")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_cartaz.wav")
    render_soft(m, out, TOTAL)
    print(out)
