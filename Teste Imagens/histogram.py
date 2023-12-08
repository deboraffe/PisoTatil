import cv2 
import numpy as np 
import matplotlib.pyplot as plt

#Imagem Original (Colorida)
img_rgb = cv2.imread(r'C:\Users\debor\OneDrive\Documentos\VSPython\Area\piso_area.jpg') 
cv2.imshow('Original', img_rgb)

#Imagem Escala de Cinza
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) 
cv2.imshow('Escala de Cinza', img_gray)

#Calculo e Plote Direto do Histograma
plt.hist(img_gray.ravel(),256,[0,256])
plt.show()

#Equalização da Imagem
img_equal = cv2.equalizeHist(img_gray)
cv2.imshow('Imagem Equalizada', img_equal)
cv2.imwrite(r'C:\Users\debor\OneDrive\Documentos\VSPython\Area\imagemeq.jpg', img_equal)

#Plote do histograma da Imagem Equalizada
plt.hist(img_equal.ravel(),256,[0,256])
plt.show()