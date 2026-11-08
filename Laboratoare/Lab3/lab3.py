import cv2
import numpy as np

# Calea catre imagine
image_path = "../images/Flower.bmp"

img = cv2.imread(image_path)
gray =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

negative_img = 255 - gray

contrast_img1 = cv2.convertScaleAbs(img, alpha=2.0, beta=0)
contrast_img2 = cv2.convertScaleAbs(img, alpha=1.0, beta=0)
contrast_img3 = cv2.convertScaleAbs(img, alpha=0.3, beta=0)

gamma1=3
gamma2=5
gamma3=0.5

invGamma1 = 1.0 / gamma1
invGamma2 = 1.0 / gamma2
invGamma3 = 1.0 / gamma3


table1 = np.array([((i / 255.0) ** invGamma1) * 255 for i in np.arange(0, 256)]).astype("uint8")
table2 = np.array([((i / 255.0) ** invGamma2) * 255 for i in np.arange(0, 256)]).astype("uint8")
table3 = np.array([((i / 255.0) ** invGamma3) * 255 for i in np.arange(0, 256)]).astype("uint8")


gamma_img1 = cv2.LUT(img, table1)
gamma_img2 = cv2.LUT(img, table2)
gamma_img3 = cv2.LUT(img, table3)


brightness_img1 = cv2.convertScaleAbs(gray, alpha=1, beta=60)
brightness_img2 = cv2.convertScaleAbs(gray, alpha=1, beta=-60)

cv2.imshow("Imaginea originala", img)
cv2.imshow("Imaginea in tonuri de gri", gray)
cv2.imshow("Negativarea imaginii", negative_img)

cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("Imaginea originala gri", img)
cv2.imshow("Contrast x2", contrast_img1)
cv2.imshow("Contrast x1", contrast_img2)
cv2.imshow("Contrast x0.3", contrast_img3)

cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("Imaginea originala gri", gray)
cv2.imshow("Modificarea luminozitatii pozitiva", brightness_img1)
cv2.imshow("Modificarea luminozitatii negativa", brightness_img2)

cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("Imaginea originala gri", img)
cv2.imshow('Corectia gamma 1/3', gamma_img1)
cv2.imshow('Corectia gamma 1/5', gamma_img2)
cv2.imshow('Corectia gamma 1/0.5', gamma_img3)

cv2.waitKey(0)
cv2.destroyAllWindows()
