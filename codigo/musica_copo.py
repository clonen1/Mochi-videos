"""Som de 'Mochi e o copo' (10 s, Sol menor). Piano, cordas e baixo; lento e natural, sem sons arcade.

0-5.5   empurrões lentos: piano esparso, pizzicato a cada empurrão, tensão de cordas a subir
5.75    o copo cai: celesta a descer | 6.35 CRASH de vidro suave + nota grave
6.5-9.4 assobio inocente (flauta no piano) | miado 8.0
9.4-10  volta ao início (loop)
"""
import os

import numpy as np

from mochi_audio import (RNG, SR, Mix, bed, celesta, cello, deg, flute, harp_gliss, hp, lp, midi, piano, pizz,
                         render_soft, sfx_meow, soft_hit, strings)

TOTAL = 10.0
MEOWS = [8.0]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
CM = [48, 55, 58, 63]
DSUS = [50, 55, 57, 62]
ARP_G = [55, 62, 65, 70, 69, 65]
ARP_C = [48, 55, 58, 63, 62, 58]
ARP_D = [50, 57, 62, 67, 69, 62]


def vidro(dur=1.1):
    """Vidro a partir: estalido curto + tilintar agudo (filtrado, suave)."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = RNG.normal(0, 1, n) * np.exp(-t * 28)
    x = hp(lp(x, 8000), 1500)
    for f, d in [(2637, 0.0), (3136, 0.03), (3951, 0.07), (2093, 0.11), (3520, 0.16), (4186, 0.22)]:
        i = int(d * SR)
        tt = t[:n - i]
        x[i:] += 0.25 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 14)
    return x * 0.8


# 0-5.5: empurrões lentos
bed(m, 0.0, 2.6, GM9, 43, ARP_G, step=1.4, gain=0.7)
bed(m, 2.6, 5.5, CM, 36, ARP_C, step=1.3, gain=0.75)
for t0, n in [(0.0, 79), (1.0, 79), (1.9, 77), (2.9, 79), (3.9, 77), (4.8, 74)]:
    m.add(pizz(midi(n - 12), 0.4), t0 + 0.2, 0.2, "sfx")
for t0, n in [(0.5, 74), (2.4, 72), (3.4, 70), (4.4, 69)]:
    m.add(piano(midi(n), 1.4, 0.55), t0, 0.2)
m.add(strings([58, 62, 67], 3.0, 1300), 2.9, 0.10)
m.add(cello(midi(36), 2.4), 3.2, 0.14)

# 5.45-6.3: o último empurrão e a queda
m.add(piano(midi(55), 0.8, 0.5), 5.45, 0.2)
m.add(celesta(midi(91), 0.6), 5.8, 0.08, "sfx")
m.add(celesta(midi(86), 0.6), 5.95, 0.08, "sfx")
m.add(celesta(midi(79), 0.6), 6.1, 0.08, "sfx")
# 6.35: crash
m.add(vidro(), 6.35, 0.7, "sfx")
m.add(soft_hit(), 6.35, 0.3, "sfx")

# 6.5-9.4: assobio inocente
bed(m, 6.5, 9.4, DSUS, 38, ARP_D, step=1.8, gain=0.75)
for t0, n, d in [(6.9, 79, 0.5), (7.45, 81, 0.4), (7.9, 79, 0.6), (8.6, 77, 0.5), (9.1, 74, 0.5)]:
    m.add(flute(midi(n), d), t0, 0.16)
m.add(sfx_meow(), MEOWS[0], 0.35, "sfx")

# 9.4-10: volta (loop)
bed(m, 9.4, 10.0, GM9, 43, ARP_G, step=1.4, gain=0.7)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_copo.wav")
    render_soft(m, out, TOTAL)
    print(out)
