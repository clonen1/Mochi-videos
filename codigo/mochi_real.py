"""Instrumentos reais (amostras de piano, cordas, guitarra, harpa) para a música dos vídeos longos.

Usa o tinysoundfont com o SoundFont TimGM6mb (sf/TimGM6mb.sf2). Os efeitos (miados, moedas, etc.)
continuam a vir do mochi_audio.py; aqui só se faz a música, com notas ligeiramente "humanizadas"
(tempo e força a variar um pouco) para soar menos a máquina.
"""
import os

import numpy as np
import tinysoundfont as tsf
from scipy.io import wavfile
from scipy.signal import fftconvolve

from mochi_audio import RNG, _reverb_ir, lp

SR = 44100
DIR = os.path.dirname(os.path.abspath(__file__))


def _find_sf():
    """SoundFont TimGM6mb: pasta sf/ local ou o que vem dentro do pacote pretty_midi (pip install pretty_midi --no-deps)."""
    p = os.path.join(DIR, "sf", "TimGM6mb.sf2")
    if os.path.exists(p):
        return p
    import importlib.util
    spec = importlib.util.find_spec("pretty_midi")
    if spec and spec.origin:
        q = os.path.join(os.path.dirname(spec.origin), "TimGM6mb.sf2")
        if os.path.exists(q):
            return q
    raise FileNotFoundError("Falta o SoundFont: pip install tinysoundfont pretty_midi --no-deps --break-system-packages")


SF = _find_sf()

# nome -> (programa GM, canal, volume 0-127, pan 0-127)
INST = {
    "piano": (0, 0, 110, 64),
    "celesta": (8, 1, 90, 80),
    "guitar": (24, 2, 105, 44),
    "harp": (46, 3, 95, 84),
    "strings": (48, 4, 80, 64),
    "slow": (49, 5, 80, 64),
    "cello": (42, 6, 105, 50),
    "bass": (32, 7, 105, 64),
    "pizz": (45, 8, 95, 70),
    "flute": (73, 10, 95, 60),
    "bassbow": (43, 11, 95, 64),
}


class Real:
    def __init__(self, seconds, humanize=0.012):
        self.seconds = seconds
        self.h = humanize
        self.ev = []  # (tempo, tipo, canal, nota, vel)

    def note(self, t, midi, dur, inst="piano", vel=80):
        ch = INST[inst][1]
        j = RNG.normal(0, self.h) if self.h else 0.0
        v = int(np.clip(vel + RNG.normal(0, 5), 20, 125))
        t0 = max(0.0, t + j)
        self.ev.append((t0, 1, ch, int(midi), v))
        self.ev.append((t0 + max(0.05, dur), 0, ch, int(midi), 0))

    def chord(self, t, notes, dur, inst="strings", vel=70, roll=0.0):
        for i, n in enumerate(notes):
            self.note(t + i * roll, n, dur - i * roll, inst, vel)

    def render(self):
        s = tsf.Synth(samplerate=SR, gain=-2)
        sf = s.sfload(SF)
        for name, (prog, ch, vol, pan) in INST.items():
            s.program_select(ch, sf, 0, prog)
            s.control_change(ch, 7, vol)
            s.control_change(ch, 10, pan)
        n = int(self.seconds * SR)
        out = np.zeros((n + SR, 2), dtype=np.float32)
        ev = sorted(self.ev, key=lambda e: (e[0], e[1]))
        blk, i, pos = 256, 0, 0
        while pos < n + SR - blk:
            while i < len(ev) and ev[i][0] * SR < pos + blk:
                _, kind, ch, nt, v = ev[i]
                (s.noteon(ch, nt, v) if kind else s.noteoff(ch, nt))
                i += 1
            out[pos:pos + blk] = np.frombuffer(s.generate(blk), dtype=np.float32).reshape(-1, 2)
            pos += blk
        return out[:n]


def mix_down(music, sfx_mono, path, seconds, wet=0.26, fade=2.0, sfx_gain=1.0):
    """music: (n,2) das amostras; sfx_mono: bus 'sfx' do Mix (efeitos sintetizados), ligeiros e centrados."""
    n = int(seconds * SR)
    L, R = music[:n, 0].astype(np.float64), music[:n, 1].astype(np.float64)
    sf = sfx_mono[:n]
    ir = _reverb_ir(2.4)
    wl, wr = fftconvolve(L, ir)[:n] * wet, fftconvolve(R, ir[::-1])[:n] * wet
    ws = fftconvolve(sf, ir)[:n] * 0.12
    left = L + wl + sf * sfx_gain + ws
    right = R + wr + sf * sfx_gain + ws
    y = np.stack([left, right], 1)
    f = int(fade * SR)
    y[-f:] *= np.linspace(1, 0, f)[:, None] ** 1.5
    y = y / (np.max(np.abs(y)) + 1e-9) * 0.86
    wavfile.write(path, SR, (y * 32767).astype(np.int16))
