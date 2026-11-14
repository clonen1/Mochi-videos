"""Som de 'Mochi finge que não ouve' (10 s, Sol menor). Piano, cordas, violoncelo e harpa; lento e natural.

0-0.5 1.6 3.3  o dono chama (duas notas descendentes ao piano) | 0.2 orelha (celesta)
5.0  a lata abre: toques suaves + harpa | 5.5 o Mochi aparece | miados 5.9 e 7.4
9.4-10 volta ao início (loop)
"""
import os

from mochi_audio import (Mix, bed, celesta, cello, deg, flute, harp_gliss, midi, piano, pizz, render_soft,
                         sfx_meow, soft_hit, strings)

TOTAL = 10.0
MEOWS = [5.9, 7.4]
m = Mix(TOTAL)

GM = [55, 58, 62, 69]
CM = [48, 55, 58, 63]
EB = [51, 55, 58, 62]
DS = [50, 55, 57, 62]
ARP_G = [55, 62, 65, 70, 69, 65]
ARP_EB = [51, 58, 62, 67, 65, 62]
ARP_D = [50, 57, 62, 67, 69, 62]

bed(m, 0.0, 2.6, GM, 43, ARP_G, step=1.0, gain=0.8)
bed(m, 2.6, 5.0, CM, 36, [48, 55, 58, 63], step=1.2, gain=0.8)
for t in (0.0, 1.6, 3.3):  # "Mo-chi"
    m.add(piano(midi(74), 1.0, 0.7), t, 0.24)
    m.add(piano(midi(69), 1.4, 0.7), t + 0.35, 0.22)
m.add(celesta(midi(86), 0.8), 0.25, 0.10, "sfx")
m.add(celesta(midi(86), 0.8), 1.85, 0.08, "sfx")
for t in (1.0, 2.2, 2.9, 3.9, 4.4):  # passinhos de quem finge
    m.add(pizz(midi(deg(2)), 0.3), t, 0.16, "sfx")
m.add(flute(midi(74), 1.2), 3.9, 0.07)

# 5.0 a lata
for t in (4.95, 5.1, 5.25):
    m.add(soft_hit(), t, 0.22, "sfx")
m.add(harp_gliss([67, 70, 74, 79, 82], 0.05, 1.2), 5.3, 0.22)
bed(m, 5.0, 7.5, EB, 39, ARP_EB, step=1.0, gain=0.9)
m.add(sfx_meow(), MEOWS[0], 0.5, "sfx")
m.add(sfx_meow(), MEOWS[1], 0.45, "sfx")
bed(m, 7.5, 10.0, GM, 43, ARP_G, step=1.2, gain=0.8)
m.add(strings([67, 70, 74], 2.0, 1500), 7.5, 0.10)
for t, d in [(7.8, 12), (8.4, 10), (9.0, 8)]:
    m.add(piano(midi(deg(d)), 1.2, 0.6), t, 0.2)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "musica", "musica_chamar.wav")
    render_soft(m, out, TOTAL)
    print(out)
