import cv2
import matplotlib.pyplot as plt

# Calea catre imagine
image_path = "../Laboratoare/images/Flower.bmp"

# Citim imaginea si o transformam in tonuri de gri
img = cv2.imread(image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Histograma = cati pixeli sunt din fiecare nuanta de gri (0..255)
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

inaltime = gray.shape[0]
latime = gray.shape[1]
nr_pixeli = inaltime * latime

# 1. BINARIZARE AUTOMATA GLOBALA
# Pornim de la un prag initial, impartim pixelii in doua grupuri
# (mai mici / mai mari decat pragul), calculam media fiecarui grup
# si noul prag este media celor doua medii. Repetam pana cand
# pragul nu se mai schimba semnificativ.

# Cea mai mica si cea mai mare nuanta care apare in imagine
i_min = 0
while hist[i_min] == 0:
    i_min = i_min + 1

i_max = 255
while hist[i_max] == 0:
    i_max = i_max - 1

# Pragul initial si eroarea acceptata
T = (i_min + i_max) / 2
eroare = 0.1

while True:
    t_int = int(T)

    # Grupul 1: nuante <= T
    n1 = 0
    s1 = 0
    for g in range(i_min, t_int + 1):
        n1 = n1 + hist[g]
        s1 = s1 + g * hist[g]

    # Grupul 2: nuante > T
    n2 = 0
    s2 = 0
    for g in range(t_int + 1, i_max + 1):
        n2 = n2 + hist[g]
        s2 = s2 + g * hist[g]

    # Mediile celor doua grupuri
    media1 = 0
    media2 = 0
    if n1 > 0:
        media1 = s1 / n1
    if n2 > 0:
        media2 = s2 / n2

    # Noul prag
    T_nou = (media1 + media2) / 2

    # Ne oprim cand pragul abia se mai schimba
    if abs(T_nou - T) < eroare:
        T = T_nou
        break
    T = T_nou

prag = int(T)
print("Prag final calculat:", prag)

# Binarizare: peste prag devine alb (255), restul negru (0)
binara = gray.copy()
for i in range(inaltime):
    for j in range(latime):
        if gray[i, j] > prag:
            binara[i, j] = 255
        else:
            binara[i, j] = 0

cv2.imshow('Imagine originala in tonuri de gri', gray)
cv2.imshow('Imagine binarizata', binara)
cv2.waitKey()
cv2.destroyAllWindows()

# 2. EGALIZAREA HISTOGRAMEI
# Fiecare nuanta de gri este inlocuita cu 255 * (suma probabilitatilor
# tuturor nuantelor pana la ea), ca nuantele sa se imprastie pe tot
# intervalul 0..255.

# Probabilitatea fiecarei nuante (impartim la numarul total de pixeli)
h = []
for i in range(256):
    h.append(hist[i] / nr_pixeli)

# Functia de repartitie cumulata si tabela de transformare
tabela = []
cumulat = 0
for i in range(256):
    cumulat = cumulat + h[i]
    tabela.append(int(round(255 * cumulat)))

# Aplicam transformarea fiecarui pixel
egalizata = gray.copy()
for i in range(inaltime):
    for j in range(latime):
        egalizata[i, j] = tabela[gray[i, j]]

# Histograma imaginii egalizate
hist_egalizata = cv2.calcHist([egalizata], [0], None, [256], [0, 256])

# Afisam cele doua histograme
plt.subplot(1, 2, 1)
plt.plot(hist)
plt.title("Histograma imaginii originale")

plt.subplot(1, 2, 2)
plt.plot(hist_egalizata)
plt.title("Histograma imaginii egalizate")

plt.show()