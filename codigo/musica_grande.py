"""Som do vídeo grande 'O sonho do Mochi' (~4 min, 100 BPM, escala In em Ré, tudo sintetizado).

Os tempos (T) são partilhados com video_grande.py.
"""
import os

import numpy as np

from mochi_audio import (SR, Mix, bass, bell, deg, downer, flute, hat, kick, koto, midi, pad, riser,
                         sfx_coin, sfx_meow, sfx_pop, sfx_snore, snare, lp, RNG)

BEAT = 0.6
BAR = 4 * BEAT
TOTAL = 246.0

# ---- linha temporal (segundos) ----
T = dict(
    sonho=20, sushi=20, templo=35, arcade=50, fuji=65,
    choque=80, planos=110, p1=110, p2=133.3, p3=156.6, solucao=180, final=210, japao=222, cartao=230, jogo=240,
)
MEOWS = [12.4, 37.0, 63.0, 87.0, 131.0, 183.0, 193.0, 226.0]
COINS = [211.0 + 0.9 * i for i in range(12)]
CUPCAKES = [163.0 + 1.4 * i for i in range(6)]
SUSHI_BITES = [24.0 + 1.6 * i for i in range(6)]

GM9 = [55, 58, 62, 69]
EBMAJ7 = [51, 55, 58, 62]
DSUS = [50, 55, 57, 63]
BBADD = [46, 50, 53, 58, 62]

THEME = [(5, 1), (7, 1), (8, 2), (7, 1), (5, 1), (4, 2), (5, 1), (7, 1), (8, 1), (10, 1), (9, 2), (7, 2)]

m = Mix(TOTAL)


def melody(seq, start, inst, gain, shift=0, stac=0.95):
    t = start
    for d, beats in seq:
        m.add(inst(midi(deg(d + shift)), beats * BEAT * stac), t, gain)
        t += beats * BEAT
    return t


def pads(chords, start, end, gain=0.2, bright=1600):
    t, i = start, 0
    while t < end - 0.5:
        d = min(2 * BAR, end - t)
        m.add(pad(chords[i % len(chords)], d + 0.4, bright), t, gain)
        t += d
        i += 1


def arps(start, end, gain, pattern=(0, 2, 4, 5, 4, 2), step=BEAT / 2, shift=5):
    t, i = start, 0
    while t < end:
        m.add(koto(midi(deg(pattern[i % len(pattern)] + shift)), 0.7), t, gain)
        t += step
        i += 1


def drums(start, end, full=True, gain=1.0):
    t, k = start, 0
    while t < end:
        b = k % 4
        if b in (0, 2) or full:
            if b in (0, 2):
                m.add(kick(0.8), t, 0.55 * gain, bus="drums")
        if full and b in (1, 3):
            m.add(snare(), t, 0.3 * gain, bus="drums")
        m.add(hat(), t, 0.05 * gain, bus="drums")
        m.add(hat(), t + BEAT / 2, 0.035 * gain, bus="drums")
        t += BEAT
        k += 1


def basses(notes, start, end, gain=0.35):
    t, i = start, 0
    while t < end:
        m.add(bass(midi(notes[i % len(notes)]), BAR * 0.95), t, gain)
        t += BAR
        i += 1


def pizz(start, end, gain=0.3):
    """Pizzicato cómico: notas curtas a saltar."""
    pat = [0, 4, 2, 5, 4, 7, 5, 2]
    t, i = start, 0
    while t < end:
        m.add(koto(midi(deg(pat[i % 8] + 5)), 0.18), t, gain)
        if i % 2 == 0:
            m.add(bass(midi(43 if (i // 8) % 2 == 0 else 46), 0.2), t, 0.3)
        t += BEAT / 2
        i += 1


def whoosh(dur=0.8):
    t = np.arange(int(dur * SR)) / SR
    from mochi_audio import sweep_lp
    return sweep_lp(RNG.normal(0, 1, len(t)), 400, 5000) * np.sin(np.pi * t / dur) ** 2


def boing(d=5):
    t = np.arange(int(0.5 * SR)) / SR
    f = midi(deg(d)) * (1 + 0.35 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 6))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6)


def chomp():
    t = np.arange(int(0.12 * SR)) / SR
    return lp(RNG.normal(0, 1, len(t)), 900) * np.exp(-t * 35)


def dong():
    return bell(midi(deg(-3)), 3.0, 0.8) + 0.5 * bell(midi(deg(2)), 3.0, 0.4)


# ---- 1. casa: tema leve e curioso ----
pads([GM9, EBMAJ7], 0, 20, 0.16)
arps(0, 20, 0.16, step=BEAT)
basses([43, 39], 0, 20, 0.25)
for t in [9.0]:
    m.add(bell(midi(deg(12)), 1.5, 0.4), t, 0.25, "sfx")       # o Fuji aparece na TV
m.add(sfx_pop(deg(3)), 11.0, 0.35, "sfx")                       # a comida cai
for t in np.arange(1.0, 9.0, 0.8):
    m.add(chomp(), t, 0.25, "sfx")
m.add(sfx_meow(), MEOWS[0], 0.4, "sfx")
m.add(riser(2.0), 18.0, 0.12)

# ---- 2. sonho: pentatónica, flauta ----
pads([EBMAJ7, GM9, BBADD, DSUS], 20, 80, 0.18, 2200)
basses([39, 43, 46, 38], 20, 80, 0.3)
drums(20, 80, full=False, gain=0.8)
t = 20.0
while t < 80 - 4:
    t = melody(THEME, t, flute, 0.2)
arps(20, 80, 0.1, pattern=(0, 4, 7, 9, 7, 4), shift=5)
for k in ("sushi", "templo", "arcade", "fuji"):
    m.add(sfx_pop(deg(7)), T[k] + 0.2, 0.35, "sfx")
    m.add(bell(midi(deg(12)), 1.2, 0.5), T[k] + 0.3, 0.2, "sfx")
for b in SUSHI_BITES:
    m.add(chomp(), b, 0.35, "sfx")
m.add(dong(), 40.0, 0.35, "sfx")
m.add(dong(), 43.0, 0.3, "sfx")
for i, b in enumerate(np.arange(52, 60, 0.3)):
    m.add(sfx_pop(deg(8 + (i % 5))), b, 0.12, "sfx")            # botões do arcade
m.add(sfx_coin(), 60.0, 0.4, "sfx")
for i in range(5):
    m.add(bell(midi(deg(10 + i)), 0.8, 0.3), 60.3 + i * 0.15, 0.2, "sfx")
for k in MEOWS[1:3]:
    m.add(sfx_meow(), k, 0.35, "sfx")

# ---- 3. choque ----
m.add(sfx_pop(deg(9)), 80.0, 0.5, "sfx")                        # a bolha rebenta
pads([GM9], 80, 88, 0.14)
arps(80, 88, 0.12, step=BEAT)
for i, t in enumerate(np.arange(88, 92.5, 0.18)):               # abana o mealheiro
    m.add(bell(midi(deg(11 + (i % 2))), 0.1, 0.2), t, 0.08, "sfx")
m.add(sfx_coin(), 93.0, 0.45, "sfx")
m.add(downer(2.0), 93.5, 0.15)
m.add(pad(DSUS, 16.0, 900), 94, 0.18)
for t, d in [(96, 4), (98, 3), (100, 2), (102, 1)]:
    m.add(bell(midi(deg(d)), 1.6, 0.3), t, 0.16)
m.add(kick(), 103.5, 1.0, "drums")
m.add(bass(midi(38), 2.0), 103.5, 0.5)
m.add(boing(2), 104.0, 0.3, "sfx")
m.add(sfx_meow(), MEOWS[3], 0.4, "sfx")

# ---- 4. planos: pizzicato cómico ----
for k in ("p1", "p2", "p3"):
    s = T[k]
    for i in range(6):
        m.add(snare(), s + i * 0.1, 0.18 + 0.04 * i, "drums")
    m.add(bell(midi(deg(10)), 1.0, 0.6), s + 0.6, 0.25, "sfx")
    pizz(s + 1.5, s + 21.5, 0.26)
    drums(s + 1.5, s + 21.5, full=True, gain=0.6)
    m.add(downer(1.2), s + 21.6, 0.14)
# plano 1: vento leva o lenço
m.add(whoosh(1.4), 124.0, 0.4, "sfx")
m.add(whoosh(1.0), 125.0, 0.3, "sfx")
m.add(boing(3), 127.5, 0.3, "sfx")
m.add(sfx_meow(), MEOWS[4], 0.4, "sfx")
# plano 2: adormece
for t in [143.0, 145.5, 148.0, 150.5]:
    m.add(sfx_snore(1.6), t, 0.45, "sfx")
m.add(boing(7), 153.0, 0.3, "sfx")
# plano 3: come os bolinhos
for t in CUPCAKES:
    m.add(chomp(), t, 0.4, "sfx")
    m.add(chomp(), t + 0.15, 0.3, "sfx")
m.add(sfx_pop(deg(3)), 174.0, 0.3, "sfx")
m.add(boing(4), 176.0, 0.3, "sfx")

# ---- 5. solução ----
m.add(pad(DSUS, 7.0, 700), 180, 0.16)
m.add(bell(midi(deg(13)), 1.2, 0.4), 186.0, 0.3, "sfx")         # o telemóvel acende
m.add(sfx_meow(), MEOWS[5], 0.35, "sfx")
m.add(bell(midi(deg(15)), 1.5, 0.6), 192.0, 0.35, "sfx")        # ideia!
m.add(sfx_meow(), MEOWS[6], 0.4, "sfx")
m.add(riser(3.0), 189.0, 0.12)
pads([GM9, EBMAJ7, BBADD], 192, 210, 0.2, 2400)
arps(192, 210, 0.14, pattern=(0, 2, 4, 7, 9, 7, 4, 2), shift=5)
basses([43, 39, 46], 194, 210, 0.3)
m.add(riser(3.0), 207.0, 0.15)

# ---- 6. final: tema do Mochi, completo ----
pads([GM9, EBMAJ7, BBADD, DSUS], 210, 240, 0.2, 2600)
basses([43, 39, 46, 38], 210, 240, 0.35)
drums(210, 230, full=True, gain=0.85)
t = 210.0
while t < 238:
    t = melody(THEME, t, flute, 0.24)
arps(210, 240, 0.1, pattern=(0, 4, 7, 9, 7, 4), shift=5)
for c in COINS:
    m.add(sfx_coin(), c, 0.3, "sfx")
m.add(hat(True), 222.0, 0.3, "drums")
m.add(sfx_meow(), MEOWS[7], 0.4, "sfx")
# cartão do jogo: calmo
pads([GM9], 240, 246, 0.16)
arps(240, 245, 0.12, step=BEAT)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_grande.wav")
    m.render(out, TOTAL, fade=2.5)
    print(out)
