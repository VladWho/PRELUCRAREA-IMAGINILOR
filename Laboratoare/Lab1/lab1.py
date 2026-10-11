import cv2
import os

# Image path
image_path = "Flower.bmp"
# Image directory
directory = "./"

# Image read
img = cv2.imread(image_path)
try:
    cv2.imshow('Image',img)
except:
    print("Image not exist")
key = cv2.waitKey()
if key == 27: #if ESC is pressed, exit
    cv2.destroyAllWindows()

# Image print
os.chdir(directory)
print("Before saving image:")
print(os.listdir(directory))

# Save new Image
filename = 'SavedFlower2.jpg'
cv2.imwrite(filename,img)
print("After saving image:")
print(os.listdir(directory))
print('Successfully saved')