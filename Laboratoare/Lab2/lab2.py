import cv2
import os
import matplotlib.pyplot as plt

# Image path
image_path = "../images/Flower.bmp"
imageBW_path = "../images/flower_grey.jpeg"
# Image directory
directory = "./"

# # Image read
# imgBW = cv2.imread(imageBW_path)
# try:
#     cv2.imshow('Image',imgBW)
# except:
#     print("Image not exist")
# key = cv2.waitKey()
# if key == 27: #if ESC is pressed, exit
#     cv2.destroyAllWindows()

# # Grey Image to Color Image
# colorized = cv2.applyColorMap(imgBW,cv2.COLORMAP_JET)
# cv2.imshow('Colorized image', colorized)
# key = cv2.waitKey()
# if key == 27: #if ESC is pressed, exit
#     cv2.destroyAllWindows()

# Image read
img = cv2.imread(image_path)
try:
    cv2.imshow('Image',img)
except:
    print("Image not exist")
key = cv2.waitKey()
if key == 27: #if ESC is pressed, exit
    cv2.destroyAllWindows()

# Color Image to GrayScale Image
gray =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray image',gray)
key = cv2.waitKey()
if key == 27: #if ESC is pressed, exit
    cv2.destroyAllWindows()


# Black&white Image
(thresh,BlackAndWhiteImage) = cv2.threshold (gray,127,255,cv2.THRESH_BINARY)
cv2.imshow( 'Black white image ', BlackAndWhiteImage)
key = cv2.waitKey()
if key == 27: #if ESC is pressed, exit
    cv2.destroyAllWindows()

# HSV Image
hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('HSV image', hsvImage)
key = cv2.waitKey()
if key == 27: #if ESC is pressed, exit
    cv2.destroyAllWindows()

# Histograma imaginii gri
imgGray=cv2.imread(image_path,0)
plt.hist(imgGray.ravel(),256,[0,256])
plt.title("Histograma imaginii in tonuri de gri")
cv2.imshow('Gray image',gray )
plt.show()
key = cv2.waitKey()
# if key == 27: #if ESC is pressed, exit
#     cv2.destroyAllWindows()

# Histograma imaginii color
color=('b','g','r')
for i, col in enumerate (color):
    histr=cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color=col)
    plt.xlim([0,256])
plt.title("Histograma imaginii color")
cv2.imshow('Image',img)
plt.show()
key = cv2.waitKey()
# if key == 27: #if ESC is pressed, exit
#     cv2.destroyAllWindows()

# # Image print
# os.chdir(directory)
# print("Before saving image:")
# print(os.listdir(directory))

# # Save new Image
# filename = 'SavedFlower2.jpg'
# cv2.imwrite(filename,img)
# print("After saving image:")
# print(os.listdir(directory))
# print('Successfully saved')