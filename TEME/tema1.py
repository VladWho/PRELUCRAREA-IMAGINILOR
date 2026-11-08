import time
import cv2
import matplotlib.pyplot as plt

# Calea catre imagine
image_path = "../Laboratoare/images/Flower.bmp"

# Citim imaginea si o transformam in tonuri de gri
img = cv2.imread(image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Imagine gri', gray)
key = cv2.waitKey()
if key == 27:  # ESC
    cv2.destroyAllWindows()

# 1. PRAGURI MULTIPLE
# Histograma = cati pixeli sunt din fiecare nuanta de gri (0..255).
# Cautam "varfurile" histogramei (nuantele care apar cel mai des).
# Aceste varfuri vor fi singurele nuante folosite in imaginea finala.

# Calculam histograma
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

# impartim la numarul total de pixeli
nr_pixeli = gray.shape[0] * gray.shape[1]
h = []
for i in range(256):
    h.append(hist[i] / nr_pixeli)

# Setari
WH = 5        # 5 nuante in stanga si 5 in dreapta
TH = 0.0003   # cat de mult trebuie sa depaseasca media ca sa fie varf

# Lista cu varfurile gasite
maxime = [0]  # incepem cu 0 (negru)

# Verificam fiecare nuanta de gri (fara margini)
for k in range(WH, 256 - WH):
    # Calculam media valorilor din jurul lui k
    suma = 0
    for i in range(k - WH, k + WH + 1):
        suma = suma + h[i]
    media = suma / (2 * WH + 1)

    # Aflam cea mai mare valoare din jurul lui k
    maxim_local = 0
    for i in range(k - WH, k + WH + 1):
        if h[i] > maxim_local:
            maxim_local = h[i]

    # k este varf daca: depaseste media + TH si e cea mai mare din jurul lui
    if h[k] > media + TH and h[k] == maxim_local:
        maxime.append(k)

maxime.append(255)  # terminam cu 255 (alb)

print("Valorile pragurilor (maximelor):", maxime)

# Afisam histograma, cu linii rosii in dreptul varfurilor
plt.plot(h)
for m in maxime:
    plt.axvline(m, color='r')
plt.title("Histograma si maximele gasite")
plt.show()


# returneaza cel mai apropiat maxim
def closest(valoare):
    best = maxime[0]
    for m in maxime:
        # daca m este mai aproape de valoare decat best, il retinem
        if abs(int(m) - int(valoare)) < abs(int(best) - int(valoare)):
            best = m
    return best

start1 = time.time()

# Cuantizare: fiecare pixel devine cel mai apropiat maxim
cuantizata = gray.copy()
for i in range(gray.shape[0]):
    for j in range(gray.shape[1]):
        cuantizata[i, j] = closest(gray[i, j])

timp1 = time.time() - start1

cv2.imshow('Imagine cuantizata', cuantizata)
key = cv2.waitKey()
if key == 27:
    cv2.destroyAllWindows()

# 2. FLOYD-STEINBERG
# Cand schimbam un pixel (ex: din 100 in 128) facem o "eroare" (28).
# In loc sa o ignoram, o trimitem vecinilor care nu au fost inca
# parcursi (dreapta si cei de jos), ca sa se compenseze.
# Vecinii primesc:   dreapta: 7/16
#                    stanga-jos: 3/16, jos: 5/16, dreapta-jos: 1/16

# Copie cu numere zecimale (erorile pot fi cu virgula)
fs = gray.astype(float)

inaltime = gray.shape[0]
latime = gray.shape[1]

start2 = time.time()

for i in range(inaltime):
    for j in range(latime):
        vechi = fs[i, j]               # valoarea pixelului acum
        nou = closest(vechi)           # cel mai apropiat maxim
        fs[i, j] = nou                 # punem noua valoare
        eroare = vechi - nou           # cat am gresit

        # Trimitem eroarea vecinilor (verificam sa nu iesim din imagine)
        if j + 1 < latime:
            fs[i, j + 1] = fs[i, j + 1] + eroare * 7 / 16
        if i + 1 < inaltime and j - 1 >= 0:
            fs[i + 1, j - 1] = fs[i + 1, j - 1] + eroare * 3 / 16
        if i + 1 < inaltime:
            fs[i + 1, j] = fs[i + 1, j] + eroare * 5 / 16
        if i + 1 < inaltime and j + 1 < latime:
            fs[i + 1, j + 1] = fs[i + 1, j + 1] + eroare * 1 / 16

timp2 = time.time() - start2

# Revenim la numere intregi (0..255) ca sa putem afisa imaginea
rezultat_fs = fs.astype('uint8')

cv2.imshow('Imagine Floyd-Steinberg', rezultat_fs)
key = cv2.waitKey()
if key == 27:
    cv2.destroyAllWindows()

print("Timp praguri multiple (cuantizare):", round(timp1, 2), "secunde")
print("Timp Floyd-Steinberg:", round(timp2, 2), "secunde")
print("Timp total de calcul:", round(timp1 + timp2, 2), "secunde")
