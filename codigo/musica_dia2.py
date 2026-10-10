"""Som do 'Dia 2: o Mochi faz as malas' (10 s, 120 BPM, Sol menor, escala In em Ré).

0.35    a mala rebenta: POP, miado de susto, sinos a subir (ramens a voar)
1.5-7.4 groove de koto (inventário da mala); 5.3 susto com o preço do bilhete
7.5-8.9 ideia (moeda) e os ramens voltam para a mala (sinos a descer), mala fecha
9-10    tema do início, para ligar ao loop
"""
import os

from mochi_audio import (Mix, bass, bell, deg, downer, hat, kick, koto, midi, pad, sfx_coin, sfx_meow,
                         sfx_pop, snare)

TOTAL = 10.0
MEOWS = [0.4, 7.6]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 63]

# ---- 0-0.35: tensão (mala a abanar) ----
m.add(pad(DSUS, 0.6), 0, 0.22)
for k, d in enumerate([5, 6, 7]):
    m.add(koto(midi(deg(d)), 0.4), k * 0.11, 0.35)

# ---- 0.35: POP ----
m.add(kick(), 0.35, 1.0, bus="drums")
m.add(snare(), 0.35, 0.5, bus="drums")
m.add(sfx_pop(deg(7)), 0.35, 0.6, "sfx")
m.add(sfx_meow(), MEOWS[0], 0.45, "sfx")
for i in range(8):
    m.add(bell(midi(deg(6 + i)), 0.3, 0.5), 0.45 + i * 0.07, 0.15)
for i in range(4):
    m.add(koto(midi(deg(3 + i % 2)), 0.3), 1.1 + i * 0.09, 0.25)   # ramens a aterrar

# ---- 1.5-7.4: groove ----
m.add(pad(GM9, 3.6), 1.4, 0.22)
m.add(pad(EBMAJ7, 2.4), 5.2, 0.22)
for b in range(12):
    t = 1.5 + b * 0.5
    if t >= 7.4:
        break
    root = 43 if t < 5.3 else 39
    m.add(bass(midi(root), 0.45), t, 0.38)
    m.add(kick(0.8), t, 0.55, bus="drums")
    m.add(hat(), t + 0.25, 0.08, bus="drums")
mel = [(2.5, 5), (2.75, 7), (3.0, 8), (3.5, 7), (3.75, 5), (4.0, 4), (4.5, 5), (4.75, 7),
       (6.5, 3), (6.75, 2), (7.0, 1)]
for t, d in mel:
    m.add(koto(midi(deg(d)), 0.9), t, 0.45)
# 5.3: susto com o preço
m.add(snare(), 5.3, 0.55, bus="drums")
m.add(bass(midi(38), 0.9), 5.3, 0.6)
m.add(downer(0.7), 5.35, 0.15)
for t, d in [(5.6, 8), (5.85, 7), (6.1, 6)]:
    m.add(bell(midi(deg(d)), 0.8, 0.3), t, 0.18)

# ---- 7.5-8.9: ideia e regresso dos ramens ----
m.add(sfx_coin(), 7.5, 0.35, "sfx")
m.add(sfx_meow(), MEOWS[1], 0.4, "sfx")
m.add(pad(DSUS, 1.6), 7.4, 0.22)
for i in range(8):
    m.add(bell(midi(deg(13 - i)), 0.3, 0.5), 7.7 + i * 0.11, 0.14)
m.add(kick(), 8.9, 0.9, bus="drums")          # a mala fecha
m.add(sfx_pop(deg(5)), 8.9, 0.35, "sfx")

# ---- 9-10: tema do início ----
m.add(pad(GM9, 1.3), 8.9, 0.22)
m.add(bass(midi(43), 1.0), 9.0, 0.35)
for t, d in [(9.0, 5), (9.25, 7), (9.5, 8), (9.75, 7)]:
    m.add(koto(midi(deg(d)), 0.7), t, 0.4)
for k in range(4):
    m.add(hat(), 9.0 + k * 0.25, 0.06, bus="drums")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_dia2.wav")
    m.render(out, TOTAL, fade=0.2)
    print(out)
