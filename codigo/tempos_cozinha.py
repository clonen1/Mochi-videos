"""Tempos partilhados entre o vídeo e a música de 'O Mochi tenta cozinhar' (90 s). Sem síntese aqui."""
TOTAL = 90.0
T = dict(casa=0, e1=8.0, e2=30.0, e3=52.0, fim=74.0, cartao=84.0)

# casa (0-8)
C_IDEA = 3.0
# panquecas (t = T["e1"] + ...)
P_POUR = 3.8
P_FLIP = 7.0        # a panqueca sobe
P_STICK = 8.0       # cola-se ao teto
P_FALL = 12.5       # descola
P_LAND = 13.2       # cai na cabeça
P_SMOKE = 14.5
P_STAMP = 18.5
# sopa
S_ADD = [3.5, 4.6, 5.7, 6.8]   # cenoura, peixe, peixe, peixe
S_BOIL = 8.2
S_TASTE = 11.2
S_SHOCK = 12.3
S_OVER = 12.8       # espuma transborda
S_FLOOD = 16.0
S_STAMP = 19.5
# bolo
B_IN = 3.6
B_SLEEP = 6.0
B_SMOKE = 11.0
B_RING = 13.0
B_WAKE = 14.2
B_OPEN = 15.6
B_STAMP = 19.8
# final
F_BOWL = 1.0
F_CARD_AT = 10.0    # = cartao - fim

MEOWS = [5.5, 18.5, 42.3, 66.2, 77.5]
STAMPS = [T["e1"] + P_STAMP, T["e2"] + S_STAMP, T["e3"] + B_STAMP]
