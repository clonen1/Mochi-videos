"""Tempos partilhados entre o vídeo e a música de 'O Mochi procura emprego' (102 s). Sem síntese aqui."""
TOTAL = 102.0
T = dict(casa=0, e1=14.0, e2=36.0, e3=54.0, fim=74.0, japao=90.0, cartao=96.0)

# casa
SHAKE = (4.6, 6.4)         # o mealheiro abana
MOTH = 6.0                  # sai uma traça
BULB = 8.4                  # ideia
# emprego 1 (t = T["e1"] + ...)
E1_WALK = (2.5, 10.0)
E1_BITES = [14.2, 15.0, 15.8, 16.6, 17.4]
E1_OPEN = 13.6
E1_BURP = 18.2
E1_DOOR = 19.0
E1_STAMP = 20.8
# emprego 2
E2_POUR = (2.8, 6.0)
E2_SLIDE = (6.0, 8.0)
E2_PUSH = 9.8
E2_FALL = 10.7
E2_CRASH = 11.4
E2_STAMP = 15.0
# emprego 3
E3_PATROL = (2.5, 6.0)
E3_SLEEP = 7.5
E3_ROBBER = (8.5, 13.5)
E3_GRAB = 11.0
E3_WAKE = 16.3
E3_STAMP = 18.3
# final
FIM_PHONE = 5.0
FIM_BULB = 7.6
FIM_COINS = [9.0 + 0.7 * i for i in range(10)]

MEOWS = [8.6, 18.9, 33.5, 47.0, 71.0, 83.0, 91.5]
for _k in (T["e1"] + E1_STAMP, T["e2"] + E2_STAMP, T["e3"] + E3_STAMP):
    pass
STAMPS = [T["e1"] + E1_STAMP, T["e2"] + E2_STAMP, T["e3"] + E3_STAMP]
