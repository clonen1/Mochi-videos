"""Som de 'O meu plano para ir ao Japão' (10 s, 120 BPM, Sol menor, escala In em Ré).

0.15    a carteira abre: pop, sai uma traça (trilo de flauta) | 0.3 miado de susto
2.2-4.4 passo 1, o cartaz: groove de koto
4.5-6.6 passo 2, chuva de moedas: moedas a subir no tom | 4.8 miado feliz
6.7-8.0 passo 3, ramen no Japão: flauta alegre
8.0     o sonho rebenta: POP, miado, apito a descer; a traça volta para a carteira
9.0-10  tema do início (loop)
"""
import os

from mochi_audio import (Mix, bass, bell, deg, downer, flute, hat, kick, koto, midi, pad, sfx_coin, sfx_meow,
                         sfx_pop, snare)

TOTAL = 10.0
MEOWS = [0.3, 4.8, 8.1]
COIN_T = [4.55 + i * 0.16 for i in range(10)]
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 63]

# ---- 0-2.1: carteira vazia ----
m.add(pad(DSUS, 2.3), 0, 0.2)
m.add(sfx_pop(deg(6)), 0.15, 0.45, "sfx")
m.add(sfx_meow(), MEOWS[0], 0.45, "sfx")
for i in range(8):                                  # traça a esvoaçar: trilo
    m.add(flute(midi(deg(10 + i % 2)), 0.1), 0.35 + i * 0.1, 0.12)
m.add(bass(midi(38), 1.0), 0.15, 0.4)
for t, d in [(1.2, 4), (1.6, 3)]:
    m.add(bell(midi(deg(d)), 0.8, 0.3), t, 0.16)

# ---- 2.1-8.0: groove do plano ----
for b in range(12):
    t = 2.1 + b * 0.5
    if t >= 8.0:
        break
    root = 43 if t < 4.5 else (39 if t < 6.6 else 41 + 2)
    m.add(bass(midi(root), 0.45), t, 0.36)
    m.add(kick(0.75), t, 0.5, bus="drums")
    m.add(hat(), t + 0.25, 0.08, bus="drums")
    if b % 2 == 1:
        m.add(snare(), t, 0.25, bus="drums")
m.add(pad(GM9, 2.5), 2.1, 0.2)
m.add(pad(EBMAJ7, 2.2), 4.5, 0.2)
m.add(pad(GM9, 1.5), 6.6, 0.2)
for t, d in [(2.25, 5), (2.5, 7), (2.75, 8), (3.25, 7), (3.5, 5), (3.75, 7), (4.0, 8)]:
    m.add(koto(midi(deg(d)), 0.7), t, 0.4)

# ---- 4.5-6.6: chuva de moedas ----
for i, t in enumerate(COIN_T):
    m.add(bell(midi(deg(10 + i % 5)), 0.25, 0.5), t + 0.35, 0.16, "sfx")
m.add(sfx_coin(), 6.2, 0.35, "sfx")
m.add(sfx_meow(), MEOWS[1], 0.45, "sfx")

# ---- 6.7-8.0: ramen no Japão ----
for t, d, dur in [(6.75, 7, 0.25), (7.0, 8, 0.25), (7.25, 10, 0.5), (7.75, 12, 0.25)]:
    m.add(flute(midi(deg(d)), dur), t, 0.24)

# ---- 8.0: o sonho rebenta ----
m.add(kick(), 8.0, 1.0, bus="drums")
m.add(snare(), 8.0, 0.6, bus="drums")
m.add(sfx_pop(deg(8)), 8.0, 0.6, "sfx")
m.add(sfx_meow(), MEOWS[2], 0.45, "sfx")
m.add(downer(0.8), 8.1, 0.16)
m.add(bass(midi(38), 1.0), 8.0, 0.5)
m.add(pad(DSUS, 1.2), 8.0, 0.2)
for i in range(6):                                  # a traça volta
    m.add(flute(midi(deg(9 + i % 2)), 0.1), 8.3 + i * 0.1, 0.1)
m.add(sfx_pop(deg(4)), 9.05, 0.35, "sfx")           # a carteira fecha

# ---- 9.0-10: tema ----
m.add(pad(DSUS, 1.1), 9.0, 0.2)
m.add(bass(midi(38), 0.9), 9.1, 0.3)
for t, d in [(9.25, 5), (9.5, 6), (9.75, 7)]:
    m.add(koto(midi(deg(d)), 0.6), t, 0.36)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_plano.wav")
    m.render(out, TOTAL, fade=0.2)
    print(out)
