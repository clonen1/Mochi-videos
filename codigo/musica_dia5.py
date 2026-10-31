"""Som do 'Dia 5: o Mochi treina os pauzinhos' (10 s, 120 BPM, Sol menor, escala In em Ré).
Estilo suave e lento (uma nota de piano por segundo), com graves de contrabaixo e violoncelo: piano e cordas, sem bateria nem efeitos arcade.

0-2     piano em arpejo e cordas | 0.35 a massa voa: harpa a subir | 1.3 cai: nota grave + miado
2-4     acorde de Mib, pizzicatos (pauzinhos a tremer) | 3.0 um pauzinho foge: harpa
4-6.5   plano B: piano calmo, pizz graves (slurps) | 6.7 miado feliz | 7-9 melodia no piano
9.3     a massa volta à taça: harpa a descer (loop)
"""
import os

from mochi_audio import (Mix, bed, celesta, cello, deg, harp_gliss, midi, piano, pizz, render_soft, sfx_meow,
                         soft_hit)

TOTAL = 10.0
MEOWS = [1.4, 6.7]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 62]
ARP_G = [55, 62, 65, 70, 69, 65]
ARP_EB = [51, 58, 62, 67, 65, 62]
ARP_D = [50, 57, 62, 67, 69, 62]

# 0-2: primeira tentativa
bed(m, 0.0, 2.0, GM9, 43, ARP_G)
m.add(harp_gliss([deg(d) for d in range(5, 13)], 0.06, 1.0), 0.35, 0.16, "sfx")
m.add(soft_hit(), 1.3, 0.22, "sfx")
m.add(sfx_meow(), MEOWS[0], 0.5, "sfx")

# 2-4: tentativa 2
bed(m, 2.0, 4.0, EBMAJ7, 39, ARP_EB)
for k in range(4):
    m.add(pizz(midi(deg(11 + k % 2)), 0.3), 2.2 + k * 0.18, 0.08, "sfx")
m.add(harp_gliss([deg(d) for d in range(8, 16)], 0.04, 0.9), 3.0, 0.14, "sfx")

# 4-6.5: plano B, cara na taça
bed(m, 4.0, 6.5, GM9, 43, ARP_G)
for t in (4.5, 5.0, 5.5, 6.0):
    m.add(pizz(midi(deg(3)), 0.3), t, 0.12, "sfx")
    m.add(pizz(midi(deg(2)), 0.3), t + 0.12, 0.10, "sfx")

# 6.5-9: aprovado (melodia simples no piano)
bed(m, 6.5, 9.0, DSUS, 38, ARP_D, step=2.0)
m.add(celesta(midi(deg(15)), 1.0), 6.5, 0.12, "sfx")
m.add(sfx_meow(), MEOWS[1], 0.45, "sfx")
for t, d, dur in [(7.0, 8, 1.0), (8.0, 10, 1.5)]:
    m.add(piano(midi(deg(d)), dur + 0.8, 0.7), t, 0.28)

# 9-10: volta ao início
bed(m, 9.0, 10.0, GM9, 43, ARP_G)
m.add(harp_gliss([deg(d) for d in range(12, 5, -1)], 0.05, 0.8), 9.3, 0.13, "sfx")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_dia5.wav")
    render_soft(m, out, TOTAL)
    print(out)
