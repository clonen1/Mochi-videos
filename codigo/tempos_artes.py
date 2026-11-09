"""Tempos partilhados entre o vídeo e a música de 'O Mochi tentou 3 artes' (90 s). Sem síntese aqui."""
TOTAL = 90.0
T = dict(casa=0, e1=10.0, e2=30.0, e3=50.0, fim=70.0, cartao=84.0)

A_BULB = 5.2                      # casa: ideia
# pintura (t = T["e1"] + ...)
P_DIP = 3.0                       # patas na tinta
P_WALK = (4.5, 12.5)              # passeia pela tela
P_SPIN = (12.5, 14.0)             # roda sobre si mesmo
P_STAMP = 17.0
# música
M_WALK = (3.5, 9.5)               # anda pelas teclas (2 passos por segundo)
M_BACK = (10.0, 11.6)
M_LIE = 11.8                      # deita-se nas teclas
M_SLEEP = 12.8
M_STAMP = 17.7
PIANO_STEPS = [3.5 + 0.5 * i for i in range(12)]
PIANO_NOTES = [48, 49, 55, 54, 60, 61, 50, 57, 64, 52, 58, 63]
# barro
C_SQ = [4.5, 6.2, 7.9]            # esmaga o barro
C_FLY = 9.4                       # o barro voa das patas
C_STAMP = 17.5
# final
F_FRAME = 6.0
F_SOLD = 8.5
F_SLEEP = 10.3

MEOWS = [5.3, 23.2, 39.7, 59.0, 78.0]
STAMPS = [T["e1"] + P_STAMP, T["e2"] + M_STAMP, T["e3"] + C_STAMP]
