"""Tempos partilhados entre o vídeo e a música de 'O Mochi tentou 3 desportos' (90 s). Sem síntese aqui."""
TOTAL = 90.0
T = dict(casa=0, e1=10.0, e2=30.0, e3=50.0, fim=70.0, cartao=84.0)

# casa
D_MEDAL = 3.0       # aparece a medalha na TV
D_BULB = 5.2        # ideia
# natação (t = T["e1"] + ...)
N_PAW = 3.0         # patinha na água
N_BRR = 4.4         # susto
N_JUMP = 9.0        # salta
N_SPLASH = 10.0
N_OUT = 13.0        # sai da água
N_STAMP = 17.0
# futebol
F_KICK = 3.0
F_GOAL = 8.6        # a bola entra na baliza
F_MOTH = 7.0        # entra a mosca/traça
F_STAMP = 17.0
# ginásio
G_FALL = 8.2
G_MAT = 12.4
G_SLEEP = 14.0
G_STAMP = 17.5
# final
M_MEDAL = 6.0

MEOWS = [5.3, 14.6, 24.0, 43.6, 58.4, 78.0]
STAMPS = [T["e1"] + N_STAMP, T["e2"] + F_STAMP, T["e3"] + G_STAMP]
