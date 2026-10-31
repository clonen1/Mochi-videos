"""Motor de som do Mochi v2: instrumentos afinados, efeitos no tom e mistura com reverb real.

Tudo sintetizado em código (sem samples): original e sem direitos de autor.
Regra de ouro: TODAS as notas (incluindo efeitos) saem do mesmo conjunto de notas,
a escala japonesa In em Ré: D Eb G A Bb. Centro tonal: Sol menor.
"""
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, lfilter, sosfilt

SR = 44100
RNG = np.random.default_rng(7)

IN_PCS = [2, 3, 7, 9, 10]  # D Eb G A Bb (classes de altura)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def deg(d, base=62):
    """Grau d da escala In a partir de Ré4 (62). Atravessa oitavas."""
    steps = [0, 1, 5, 7, 8]
    o, k = divmod(d, 5)
    return base + 12 * o + steps[k]


def adsr(n, a=0.01, d=0.1, s=0.7, r=0.15):
    t = np.arange(n) / SR
    dur = n / SR
    e = np.full(n, s)
    e[t < a] = t[t < a] / a
    m = (t >= a) & (t < a + d)
    e[m] = 1 - (1 - s) * (t[m] - a) / d
    tail = t > dur - r
    e[tail] *= np.clip((dur - t[tail]) / r, 0, 1)
    return e


def lp(x, cut, order=2):
    return lfilter(*butter(order, min(cut / (SR / 2), 0.99)), x)


def hp(x, cut, order=2):
    return lfilter(*butter(order, cut / (SR / 2), btype="high"), x)


def sweep_lp(x, cut_start, cut_end, steps=24):
    """Filtro passa-baixo que fecha/abre ao longo do tempo (transições suaves)."""
    out = np.zeros_like(x)
    edges = np.linspace(0, len(x), steps + 1).astype(int)
    cuts = np.geomspace(cut_start, cut_end, steps)
    win = np.zeros_like(x)
    for i, c in enumerate(cuts):
        a, b = max(0, edges[i] - 512), min(len(x), edges[i + 1] + 512)
        seg = sosfilt(butter(2, min(c / (SR / 2), 0.99), output="sos"), x[a:b])
        w = np.hanning(b - a)
        out[a:b] += seg * w
        win[a:b] += w
    return out / np.maximum(win, 1e-6)


# ---------- instrumentos (todos afinados) ----------

def koto(freq, dur):
    """Corda dedilhada aditiva: harmónicos com decaimentos diferentes, sempre afinada."""
    t = np.arange(int(dur * SR)) / SR
    x = np.zeros_like(t)
    for k in range(1, 9):
        f = freq * k * (1 + 0.0007 * k * k)  # ligeira inarmonicidade de corda
        if f > SR / 2.2:
            break
        x += np.sin(2 * np.pi * f * t) * (0.9 ** k) / k ** 0.6 * np.exp(-t * (2.2 + 1.6 * k))
    att = np.minimum(t / 0.003, 1)
    return x * att


def bell(freq, dur, bright=0.6):
    t = np.arange(int(dur * SR)) / SR
    mod = np.sin(2 * np.pi * freq * 3.5 * t) * bright * 2.2 * np.exp(-t * 7)
    return np.sin(2 * np.pi * freq * t + mod) * np.exp(-t * 3.5) * np.minimum(t / 0.002, 1)


def bass(freq, dur):
    t = np.arange(int(dur * SR)) / SR
    sub = np.sin(2 * np.pi * freq * t)
    saw = 2 * ((freq * t) % 1) - 1
    return (0.85 * sub + 0.3 * lp(saw, 420)) * adsr(len(t), 0.012, 0.18, 0.75, 0.06)


def pad(notes, dur, bright=1600):
    t = np.arange(int(dur * SR)) / SR
    x = np.zeros_like(t)
    for n in notes:
        f = midi(n)
        x += np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * f * 1.0025 * t + 1.3)
        x += 0.2 * np.sin(2 * np.pi * 2 * f * t)
    return lp(x / len(notes), bright) * adsr(len(t), 0.35, 0.4, 0.85, 0.5)


def flute(freq, dur):
    t = np.arange(int(dur * SR)) / SR
    vib = 1 + 0.005 * np.sin(2 * np.pi * 5.2 * t) * np.clip((t - 0.12) * 5, 0, 1)
    ph = 2 * np.pi * np.cumsum(freq * vib) / SR
    breath = lp(RNG.normal(0, 1, len(t)), 2600) * 0.06 * np.exp(-t * 8)
    x = np.sin(ph) + 0.22 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph) + breath
    return x * adsr(len(t), 0.05, 0.1, 0.8, 0.1)


def kick(g=1.0):
    t = np.arange(int(0.4 * SR)) / SR
    f = 110 * np.exp(-t * 28) + 46
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8) * g


def snare():
    t = np.arange(int(0.22 * SR)) / SR
    body = np.sin(2 * np.pi * 196 * t) * np.exp(-t * 30)  # Sol: no tom
    return hp(RNG.normal(0, 1, len(t)), 1800) * 0.55 * np.exp(-t * 20) + body * 0.45


def hat(open_=False):
    d = 0.18 if open_ else 0.05
    t = np.arange(int(d * SR)) / SR
    return hp(RNG.normal(0, 1, len(t)), 7500) * np.exp(-t * (14 if open_ else 70))


def riser(dur):
    """Subida de ruído filtrado que prepara a entrada da bateria."""
    t = np.arange(int(dur * SR)) / SR
    x = sweep_lp(RNG.normal(0, 1, len(t)), 300, 6000)
    return x * (t / dur) ** 2


def downer(dur):
    t = np.arange(int(dur * SR)) / SR
    x = sweep_lp(RNG.normal(0, 1, len(t)), 5000, 200)
    return x * (1 - t / dur) ** 1.5 * np.minimum(t / 0.05, 1)


# ---------- efeitos no tom ----------

def sfx_pop(target=deg(5)):
    t = np.arange(int(0.16 * SR)) / SR
    f = midi(target) * (0.45 + 0.55 * (1 - np.exp(-t * 35)))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 20)


def sfx_blink():
    return bell(midi(deg(13)), 0.35, 0.3) * 0.6        # Lá6


def sfx_coin():
    return np.concatenate([bell(midi(deg(13)), 0.06, 0.5), bell(midi(deg(15)), 0.4, 0.5)])  # Lá6 -> Ré7


def sfx_meow():
    t = np.arange(int(0.55 * SR)) / SR
    shape = np.sin(np.pi * t / 0.55)
    f0 = midi(deg(5)) * (1 + 0.12 * shape)               # à volta de Ré5
    ph = 2 * np.pi * np.cumsum(f0) / SR
    x = sum(np.sin(k * ph) / k for k in range(1, 6))
    return (lp(x, 1100) * (1 - shape) + lp(x, 2600) * shape) * shape ** 1.5


def sfx_snore(dur=1.3):
    t = np.arange(int(dur * SR)) / SR
    noise = lp(RNG.normal(0, 1, len(t)), 380)
    return noise * (1 + 0.8 * np.sin(2 * np.pi * 24 * t)) * np.sin(np.pi * t / dur) ** 2 * 0.5


# ---------- mistura ----------

def _reverb_ir(seconds=1.4):
    t = np.arange(int(seconds * SR)) / SR
    ir = RNG.normal(0, 1, len(t)) * np.exp(-t * 4.5)
    return lp(ir, 5000) / np.sqrt(np.sum(ir ** 2))


class Mix:
    """Buses separados para poder filtrar a música sem afetar a voz/efeitos."""

    def __init__(self, seconds):
        n = int(seconds * SR) + 2 * SR
        self.bus = {"music": np.zeros(n), "drums": np.zeros(n), "sfx": np.zeros(n)}

    def add(self, x, at, gain=1.0, bus="music"):
        b = self.bus[bus]
        i = int(at * SR)
        j = min(len(b), i + len(x))
        b[i:j] += x[: j - i] * gain

    def render(self, path, seconds, music_fx=None, fade=1.0):
        n = int(seconds * SR)
        music = self.bus["music"][:n] + self.bus["drums"][:n]
        if music_fx:
            music = music_fx(music)
        sfx = self.bus["sfx"][:n]
        ir = _reverb_ir()
        wet = fftconvolve(music, ir)[:n] * 0.22 + fftconvolve(sfx, ir)[:n] * 0.12
        y = music + sfx * 0.9 + wet
        y = np.tanh(y * 1.1)
        f = int(fade * SR)
        y[-f:] *= np.linspace(1, 0, f) ** 1.5
        y = y / (np.max(np.abs(y)) + 1e-9) * 0.89
        right = np.roll(y, 180) * 0.96 + np.roll(wet, 400) * 0.05
        wavfile.write(path, SR, (np.stack([y, right], 1) * 32767).astype(np.int16))


# ---------- estilo suave (a partir da semana de 02/11) ----------
# Regra nova: nada de som arcade. Fundo com piano e cordas, simples e calmo.
# Sem bateria, sem apitos nem ondas quadradas. Os efeitos ficam discretos.

def piano(freq, dur, vel=0.8):
    """Piano suave: harmónicos com inarmonicidade, martelo macio e duas fases de decaimento."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for k in range(1, 11):
        f = freq * k * np.sqrt(1 + 0.0004 * k * k)
        if f > SR / 2.3:
            break
        amp = (0.55 ** (k - 1)) * (0.6 + 0.4 * vel)
        dec = np.exp(-t * (0.9 + 0.55 * k)) * 0.7 + np.exp(-t * (4 + 2 * k)) * 0.3
        x += amp * dec * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 1.0007 * t + 0.4))
    hammer = lp(RNG.normal(0, 1, n), 1800) * np.exp(-t * 90) * 0.04
    rel = np.clip((dur - t) / 0.12, 0, 1)
    return lp((x + hammer) * np.minimum(t / 0.004, 1) * rel, 4200) * vel


def strings(notes, dur, bright=1400):
    """Naipe de cordas: dentes de serra desafinados, ataque lento e vibrato leve."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for nt in notes:
        f = midi(nt)
        for det, ph in ((0.997, 0.0), (1.0, 1.1), (1.0035, 2.3)):
            vib = 1 + 0.004 * np.sin(2 * np.pi * (5.0 + det) * t + ph) * np.clip(t / 0.6, 0, 1)
            p = np.cumsum(f * det * vib) / SR
            x += 2 * (p % 1) - 1
    x = lp(x / (3 * len(notes)), bright, order=3)
    return x * adsr(n, min(0.5, dur * 0.35), 0.3, 0.9, min(0.6, dur * 0.4))


def cello(freq, dur):
    """Violoncelo: nota grave arcada, quente."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    vib = 1 + 0.005 * np.sin(2 * np.pi * 5.3 * t) * np.clip((t - 0.15) * 3, 0, 1)
    p = np.cumsum(freq * vib) / SR
    x = lp(2 * (p % 1) - 1, 700, order=3) + 0.5 * np.sin(2 * np.pi * p)
    return x * adsr(n, min(0.25, dur * 0.3), 0.2, 0.85, min(0.35, dur * 0.4))


def pizz(freq, dur=0.6):
    """Pizzicato: corda beliscada, curta e redonda."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * freq * k * t) * np.exp(-t * (5 + 4 * k)) / k for k in range(1, 6))
    return lp(x * np.minimum(t / 0.003, 1), 2500)


def celesta(freq, dur=1.0):
    """Celesta/caixa de música, para brilhos discretos."""
    return bell(freq, dur, bright=0.25) * 0.7


def harp_gliss(notes, at_step=0.05, dur=1.2):
    """Glissando de harpa (pizz rápidos) para transições."""
    out = np.zeros(int((len(notes) * at_step + dur) * SR))
    for i, nt in enumerate(notes):
        x = pizz(midi(nt), dur)
        a = int(i * at_step * SR)
        out[a:a + len(x)] += x * (0.6 + 0.4 * i / max(1, len(notes) - 1))
    return out


def soft_hit():
    """Impacto suave (em vez de bombo/caixa): nota grave de piano + corda."""
    return piano(midi(43), 1.2, 0.9) + pizz(midi(31), 1.2) * 0.6


def sfx_soft_pop(target=deg(10)):
    """Pop discreto: pizzicato agudo."""
    return pizz(midi(target), 0.25) * 0.8


def bed(m, t0, t1, chord, root, arp=None, step=0.5, gain=1.0):
    """Fundo simples: cordas seguradas, violoncelo no baixo e piano em arpejo calmo."""
    d = t1 - t0
    m.add(strings(chord, d + 0.4), t0, 0.16 * gain)
    m.add(cello(midi(root), d + 0.3), t0, 0.22 * gain)
    arp = arp or sorted(chord)
    t, i = t0, 0
    while t < t1 - 0.05:
        m.add(piano(midi(arp[i % len(arp)] + 12), 1.4, 0.55), t, 0.30 * gain)
        t += step
        i += 1


def render_soft(m, path, seconds, fade=0.2):
    """Render com reverb mais longo e sem saturação: som de sala calmo."""
    n = int(seconds * SR)
    music = m.bus["music"][:n] + m.bus["drums"][:n]
    sfx = m.bus["sfx"][:n]
    ir = _reverb_ir(2.2)
    wet = fftconvolve(music, ir)[:n] * 0.32 + fftconvolve(sfx, ir)[:n] * 0.15
    y = music + sfx * 0.9 + wet
    f = int(fade * SR)
    y[-f:] *= np.linspace(1, 0, f) ** 1.5
    y = y / (np.max(np.abs(y)) + 1e-9) * 0.85
    right = np.roll(y, 220) * 0.95 + np.roll(wet, 500) * 0.06
    wavfile.write(path, SR, (np.stack([y, right], 1) * 32767).astype(np.int16))
