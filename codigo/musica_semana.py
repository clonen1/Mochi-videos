"""Som de 'Eu à segunda vs eu à sexta' (10 s, 120 BPM, Sol menor, escala In em Ré).

0.15    despertador TRIM (sinos rápidos no tom) | 0.2 miado zangado (Mochi de segunda)
0-6.6   groove alegre de sexta (koto + baixo + bateria)
2.2     bateria: 'tlim' grave (1%) e moeda aguda (100%) | 2.5 miado feliz (Mochi de sexta)
4.5     a mesma comida: pop da taça
6.9     domingo à noite: a música pára, pancada, dois miados de susto, apito a descer
9.0-10  groove volta (loop)
"""
import os

from mochi_audio import (Mix, bass, bell, deg, downer, flute, hat, kick, koto, midi, pad, sfx_coin, sfx_meow,
                         sfx_pop, snare)

TOTAL = 10.0
TOP_MEOWS = [0.2, 6.95]
BOT_MEOWS = [2.5, 6.95]
MEOWS = sorted(set(TOP_MEOWS + BOT_MEOWS))
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 63]


def groove(t0, t1):
    t = t0
    k = 0
    while t < t1 - 0.01:
        root = 43 if (k // 4) % 2 == 0 else 39
        m.add(bass(midi(root), 0.22), t, 0.36)
        m.add(bass(midi(root + 12), 0.2), t + 0.25, 0.18)
        m.add(kick(0.75), t, 0.5, bus="drums")
        if k % 2 == 1:
            m.add(snare(), t, 0.3, bus="drums")
        m.add(hat(), t + 0.25, 0.08, bus="drums")
        t += 0.5
        k += 1


groove(0.0, 6.9)
m.add(pad(GM9, 2.0), 0, 0.18)
m.add(pad(EBMAJ7, 2.0), 2.0, 0.18)
m.add(pad(GM9, 2.5), 4.0, 0.18)
riff = [(0.5, 5), (0.75, 7), (1.0, 8), (1.5, 7), (2.5, 8), (2.75, 10), (3.0, 9), (3.5, 8),
        (4.5, 5), (4.75, 7), (5.0, 8), (5.5, 10), (6.0, 9), (6.25, 8)]
for t, d in riff:
    m.add(koto(midi(deg(d)), 0.7), t, 0.38)

# ---- 0.15: despertador ----
for i in range(10):
    m.add(bell(midi(deg(13 if i % 2 else 12)), 0.12, 0.6), 0.12 + i * 0.06, 0.18, "sfx")
m.add(sfx_meow(), TOP_MEOWS[0], 0.45, "sfx")

# ---- 2.2: bateria ----
m.add(bell(midi(deg(2)), 0.6, 0.2), 2.2, 0.3, "sfx")
m.add(sfx_coin(), 2.35, 0.35, "sfx")
m.add(sfx_meow(), BOT_MEOWS[0], 0.45, "sfx")

# ---- 4.5: a mesma comida ----
m.add(sfx_pop(deg(6)), 4.5, 0.45, "sfx")
for t, d, dur in [(4.75, 10, 0.3), (5.1, 8, 0.4)]:
    m.add(flute(midi(deg(d)), dur), t, 0.2)

# ---- 6.9: domingo à noite ----
m.add(kick(), 6.9, 1.0, bus="drums")
m.add(snare(), 6.9, 0.6, bus="drums")
m.add(bass(midi(38), 1.6), 6.9, 0.55)
m.add(pad(DSUS, 2.1), 6.9, 0.22)
m.add(sfx_meow(), 6.95, 0.5, "sfx")
m.add(downer(0.9), 7.3, 0.16)
for t, d in [(7.6, 4), (8.0, 3), (8.4, 1)]:
    m.add(bell(midi(deg(d)), 0.9, 0.3), t, 0.16)

# ---- 9-10: groove volta ----
groove(9.0, 10.0)
m.add(pad(GM9, 1.2), 8.9, 0.18)
for t, d in [(9.0, 5), (9.25, 7), (9.5, 8), (9.75, 7)]:
    m.add(koto(midi(deg(d)), 0.6), t, 0.36)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_semana.wav")
    m.render(out, TOTAL, fade=0.2)
    print(out)
