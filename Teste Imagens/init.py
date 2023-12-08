import cv2 
import numpy as np 
import matplotlib.pyplot as plt
import timeit
import time

#Imagem Original (Colorida)
img_rgb = cv2.imread(r'C:\Users\debor\OneDrive\Documentos\VSPython\Area\piso_direcional.jpg') 

#Imagem Escala de Cinza
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) 

#Equalização da Imagem
img_equal = cv2.equalizeHist(img_gray)


#Suavização(blur) da Imagem
ksize = (20, 20)
img_blur = cv2.blur (img_equal,ksize)
cv2.imshow('Imagem Suavizada', img_blur)

#Segmentação da Imagem
ret,th1 = cv2.threshold (img_blur,130,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold (img_blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,13,3)
th3 = cv2.adaptiveThreshold (img_blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,13,3)
ret2,th4 = cv2.threshold(img_blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

titles = ['Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding', 'Otsus Thresholding']
images = [th1, th2, th3, th4]
for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

#Contornos da Imagem
contours, hierarchies = cv2.findContours(th4, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #Desenhar os cortornos
blank = np.zeros(th4.shape[:2],dtype='uint8')
cv2.drawContours(blank, contours, -1,(255, 0, 0), 1)
cv2.imshow('Imagem com Contornos', blank)

# Inicialize contadores de pixels brancos e pretos
pixels_brancos = 0
pixels_pretos = 0

# Percorra cada contorno e calcule o número de pixels brancos e pretos
for contorno in contours:
    area_contorno = cv2.contourArea(contorno)
    pixels_brancos_contorno = cv2.countNonZero(th4) - area_contorno
    pixels_brancos += pixels_brancos_contorno
    pixels_pretos += area_contorno

print(f"Número de pixels brancos: {pixels_brancos}")
print(f"Número de pixels pretos: {pixels_pretos}")

#number_of_white_pix = np.sum (blank == 255) # extraindo apenas pixels brancos 
#print('Number of white pixels:', number_of_white_pix)

cv2.waitKey()