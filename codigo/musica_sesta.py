"""Som de 'Eu quando me acordam da sesta' (10 s, 120 BPM, Sol menor, escala In em Ré).

0-0.3    canção de embalar (sinos suaves)
0.3-2.0  despertador: trilo Lá6/Si bemol6 (as duas notas são da escala)
2.0      o Mochi acorda zangado: pancada e miado
3.0      PAF: o despertador voa para fora (pop a subir)
3.4-5.6  groove rabugento no grave
5.8      a taça de comida chega (moeda), miado feliz, nham nham em koto
8.3-10   canção de embalar outra vez + ressonar (liga ao início)
"""
import os

from mochi_audio import (Mix, bass, bell, deg, downer, hat, kick, koto, midi, pad, sfx_coin, sfx_meow,
                         sfx_pop, sfx_snore, snare)

TOTAL = 10.0
MEOWS = [2.1, 6.3]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 63]


def lullaby(t0, dur, gain=0.16):
    m.add(pad(EBMAJ7, dur, 1100), t0, 0.2)
    for i, d in enumerate([7, 5, 6, 4]):
        if i * 0.5 < dur - 0.3:
            m.add(bell(midi(deg(d)), 1.0, 0.2), t0 + i * 0.5, gain)


# ---- 0-2: embalar + despertador ----
lullaby(0, 2.2)
for i in range(int(1.7 / 0.06)):
    m.add(bell(midi(deg(13 + i % 2)), 0.08, 0.6), 0.3 + i * 0.06, 0.12, "sfx")

# ---- 2.0: acorda zangado ----
m.add(kick(), 2.0, 0.9, bus="drums")
m.add(snare(), 2.0, 0.5, bus="drums")
m.add(bass(midi(38), 0.9), 2.0, 0.55)
m.add(sfx_meow(), MEOWS[0], 0.5, "sfx")
m.add(pad(DSUS, 1.4), 2.0, 0.22)

# ---- 3.0: PAF ----
m.add(kick(), 3.0, 1.0, bus="drums")
m.add(snare(), 3.0, 0.7, bus="drums")
m.add(sfx_pop(deg(10)), 3.05, 0.45, "sfx")
m.add(downer(0.6), 3.1, 0.12)

# ---- 3.4-5.6: rabugento ----
m.add(pad(DSUS, 2.4), 3.3, 0.18)
for b in range(5):
    t = 3.5 + b * 0.5
    m.add(bass(midi(38 if b % 2 == 0 else 39), 0.4), t, 0.45)
    m.add(kick(0.7), t, 0.5, bus="drums")
    m.add(hat(), t + 0.25, 0.07, bus="drums")
for t, d in [(3.75, 2), (4.25, 1), (4.75, 2), (5.25, 0)]:
    m.add(koto(midi(deg(d)), 0.6), t, 0.4)

# ---- 5.8-8.2: comida! ----
m.add(sfx_coin(), 5.8, 0.4, "sfx")
m.add(sfx_meow(), MEOWS[1], 0.45, "sfx")
m.add(pad(GM9, 2.6), 5.8, 0.22)
m.add(bass(midi(43), 1.0), 6.0, 0.4)
m.add(bass(midi(43), 1.0), 7.0, 0.35)
for k in range(10):
    t = 6.8 + k * 0.12
    m.add(koto(midi(deg(8 if k % 2 else 7)), 0.25), t, 0.35)   # nham nham
for k in range(5):
    m.add(hat(), 6.0 + k * 0.5, 0.07, bus="drums")

# ---- 8.3-10: de volta à sesta ----
lullaby(8.2, 1.8)
m.add(sfx_snore(1.3), 8.6, 0.35, "sfx")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_sesta.wav")
    m.render(out, TOTAL, fade=0.2)
    print(out)
