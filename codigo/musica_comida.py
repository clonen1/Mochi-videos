"""Som de 'Tipos de gato quando chega a comida' (10 s, 120 BPM, Sol menor, escala In em Ré).
Estilo suave: piano e cordas, sem bateria nem efeitos arcade.

0.25    a taça cai: nota grave suave | 0.3 patinhas: pizzicatos rápidos
1.6     o educado: piano delicado | 3.6 o dramático: cordas em Mib, 2 miados (4.0 e 4.8)
5.8     o ninja: harpa rápida e pizz (nham nham) | 7.9 'e tu?' melodia no piano
9.3     saem: harpa a subir (loop)
"""
import os

from mochi_audio import (Mix, bed, celesta, cello, deg, harp_gliss, midi, piano, pizz, render_soft, sfx_meow,
                         soft_hit, strings)

TOTAL = 10.0
MEOWS = [4.0, 4.8]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
CM7 = [48, 55, 58, 63]
DSUS = [50, 55, 57, 62]
ARP_G = [55, 62, 65, 70, 69, 65]
ARP_EB = [51, 58, 62, 67, 65, 62]
ARP_D = [50, 57, 62, 67, 69, 62]

# 0-1.6: chegada
bed(m, 0.0, 1.6, GM9, 43, ARP_G)
m.add(soft_hit(), 0.25, 0.2, "sfx")
for k in range(8):
    m.add(pizz(midi(deg(8 + k % 3)), 0.25), 0.3 + k * 0.07, 0.08, "sfx")
m.add(celesta(midi(deg(13)), 0.8), 0.9, 0.1, "sfx")

# 1.6-3.6: o educado
bed(m, 1.6, 3.6, GM9, 43, ARP_G)
for t, d in [(1.6, 10), (2.1, 12), (2.6, 10), (3.1, 8)]:
    m.add(piano(midi(deg(d)), 1.2, 0.6), t, 0.22)

# 3.6-5.8: o dramático
m.add(strings(EBMAJ7, 2.4, 1100), 3.6, 0.22)
m.add(cello(midi(39), 2.3), 3.6, 0.26)
for t, d in [(3.6, 7), (4.4, 6), (5.2, 5)]:
    m.add(piano(midi(deg(d)), 1.4, 0.6), t, 0.24)
for t0 in MEOWS:
    m.add(sfx_meow(), t0, 0.5, "sfx")

# 5.8-7.8: o ninja
bed(m, 5.8, 7.8, CM7, 36, [48, 55, 60, 63, 67, 63])
m.add(harp_gliss([deg(d) for d in range(14, 7, -1)], 0.03, 0.7), 5.85, 0.13, "sfx")
for k in range(6):
    m.add(pizz(midi(deg(9 + k % 2)), 0.2), 6.2 + k * 0.25, 0.08, "sfx")

# 7.9-9.3: e tu?
bed(m, 7.8, 9.3, DSUS, 38, ARP_D, step=1.0)
for t, d, dur in [(7.95, 10, 0.25), (8.2, 12, 0.25), (8.45, 13, 0.5), (8.95, 12, 0.4)]:
    m.add(piano(midi(deg(d)), dur + 0.8, 0.7), t, 0.28)

# 9.3-10: volta ao início
bed(m, 9.3, 10.0, GM9, 43, ARP_G)
m.add(harp_gliss([deg(d) for d in range(6, 13)], 0.05, 0.7), 9.35, 0.12, "sfx")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_comida.wav")
    render_soft(m, out, TOTAL)
    print(out)
