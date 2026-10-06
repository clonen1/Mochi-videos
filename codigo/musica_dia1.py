"""Banda sonora v2 do 'Dia 1': faixa contínua de 14 s, 120 BPM (1 compasso = 2 s), centro Sol menor.

Estrutura (alinhada com as cenas do vídeo):
  c1-2  intro   koto + pad + grave; hats entram, subida de ruído prepara a bateria
  c3-4  plano   groove com bateria, linha de baixo e flauta; moedas no tempo
  c5-6  noite   bateria sai, a música "escurece" (filtro fecha), caixinha de música + ronco
  c7    fim     o filtro reabre e o tema do início volta e resolve em Sol menor
"""
import os

import numpy as np

from mochi_audio import (SR, Mix, bass, bell, deg, downer, flute, hat, kick, koto, lp, midi, pad, riser,
                         sfx_blink, sfx_coin, sfx_meow, sfx_pop, sfx_snore, snare)

BAR = 2.0
TOTAL = 14.0
m = Mix(TOTAL)

GM9 = [55, 58, 62, 69]       # G Bb D A
EBMAJ7 = [51, 55, 58, 62]    # Eb G Bb D
BB6 = [50, 55, 58, 62]       # D G Bb D (Bb6 sem fundamental, o baixo dá o Bb)
DSUS = [50, 55, 57, 63]      # D G A Eb (tensão que pede resolução)
chords = [(GM9, 43), (EBMAJ7, 39), (GM9, 43), (EBMAJ7, 39), (BB6, 46), (DSUS, 38), (GM9, 43)]

# Pad e grave longo em todos os compassos, ligados (sem cortes entre cenas)
for i, (ch, root) in enumerate(chords):
    t = i * BAR
    m.add(pad(ch, BAR + 0.6), t, 0.28 if i < 6 else 0.32)
    if i not in (2, 3):  # nos compassos do groove o baixo é rítmico
        m.add(bass(midi(root), BAR - 0.05), t, 0.5 if i < 4 else 0.42)

# ---- c1-2: tema do koto ----
motif1 = [(0, 2), (0.25, 4), (0.5, 5), (1.0, 3), (1.25, 4), (1.5, 2)]
motif2 = [(0, 4), (0.25, 5), (0.5, 7), (1.0, 6), (1.25, 5), (1.5, 4)]
for base, motif in ((0.0, motif1), (BAR, motif2)):
    for t, d in motif:
        m.add(koto(midi(deg(d)), 1.2), base + t, 0.5)
for k in range(4):                                   # hats entram na 2.ª metade do c2
    m.add(hat(), 3.0 + k * 0.25, 0.08 + 0.03 * k)
m.add(riser(1.0), 3.0, 0.16)
for k, t in enumerate([3.5, 3.625, 3.75, 3.875]):   # rufo curto para entrar no groove
    m.add(snare(), t, 0.12 + 0.07 * k, bus="drums")

# ---- c3-4: groove ----
G = 2 * BAR
for b in range(2):
    s = G + b * BAR
    for t, g in [(0, 0.9), (0.75, 0.45), (1.0, 0.8)]:
        m.add(kick(), s + t, g, bus="drums")
    for t in (0.5, 1.5):
        m.add(snare(), s + t, 0.4, bus="drums")
    for k in range(8):
        is_open = b == 1 and k == 7
        m.add(hat(is_open), s + k * 0.25, 0.14 if k % 2 else 0.09, bus="drums")
groove_bass = [(0, 43, .4), (.75, 43, .2), (1.0, 46, .4), (1.5, 45, .2), (1.75, 50, .2),
               (2.0, 39, .4), (2.75, 39, .2), (3.0, 43, .4), (3.5, 46, .2), (3.75, 45, .2)]
for t, n, d in groove_bass:
    m.add(bass(midi(n), d), G + t, 0.62)
melody = [(0, 5, .5), (.5, 4, .25), (.75, 3, .25), (1.0, 2, .5), (1.5, 3, .25), (1.75, 4, .25),
          (2.0, 6, .75), (2.75, 5, .25), (3.0, 4, .5), (3.5, 7, .5)]
for t, d, dur in melody:
    m.add(flute(midi(deg(d)), dur + 0.05), G + t, 0.3)
for k in range(8):                                    # koto em contratempo, discreto
    m.add(koto(midi(deg(2 + (k % 3))), 0.4), G + 0.125 + k * 0.5, 0.18)
m.add(downer(1.0), 7.4, 0.12)

# ---- c5-6: noite, caixinha de música ----
N = 4 * BAR
m.add(kick(0.5), N, 0.6, bus="drums")                # último batimento, suave
lullaby = [(0, 10), (0.5, 9), (1.0, 7), (1.5, 9), (2.0, 8), (2.5, 7), (3.0, 5), (3.5, 8)]
for t, d in lullaby:
    m.add(bell(midi(deg(d)), 1.4, 0.35), N + t, 0.26)

# ---- c7: o tema volta e resolve ----
E = 6 * BAR
for t, d in [(0, 2), (0.25, 4), (0.5, 5), (1.0, 7)]:
    m.add(koto(midi(deg(d)), 1.8), E + t, 0.5)
m.add(bell(midi(deg(7)), 2.0, 0.3), E + 1.0, 0.18)

# ---- efeitos (no tom, alinhados com o vídeo) ----
m.add(sfx_pop(), 0.05, 0.45, "sfx")
m.add(sfx_meow(), 0.7, 0.4, "sfx")
m.add(sfx_blink(), 1.6, 0.5, "sfx")
m.add(sfx_pop(deg(7)), 4.0, 0.35, "sfx")
for t in np.arange(4.5, 7.6, 0.5):
    m.add(sfx_coin(), t, 0.16, "sfx")
m.add(sfx_snore(1.3), 9.0, 0.32, "sfx")
m.add(sfx_snore(1.3), 10.6, 0.28, "sfx")
m.add(sfx_pop(deg(7)), 12.0, 0.35, "sfx")
m.add(sfx_meow(), 12.5, 0.35, "sfx")


def night_filter(x):
    """Crossfade suave entre a mistura cheia e uma versão 'abafada' durante a noite."""
    t = np.arange(len(x)) / SR
    dark = lp(lp(x, 1300), 1300)
    w = np.interp(t, [0, 7.4, 8.6, 11.4, 12.4, TOTAL], [0, 0, 1, 1, 0, 0])
    w = 0.5 - 0.5 * np.cos(np.pi * w)  # curva suave
    return x * (1 - w) + dark * w * 1.15


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica_dia1.wav")
    m.render(out, TOTAL, music_fx=night_filter, fade=1.2)
    print(out)
