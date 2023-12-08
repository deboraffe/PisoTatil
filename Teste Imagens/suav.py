import cv2 
import numpy as np 
import matplotlib.pyplot as plt
import timeit
import time

#Imagem Original (Colorida)
img_rgb = cv2.imread(r'C:\Users\debor\OneDrive\Documentos\VSPython\Area\piso_area.jpg') 

#Imagem Escala de Cinza
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) 

#Equalização da Imagem
img_equal = cv2.equalizeHist(img_gray)

#Suavização da Imagem
ksize = (15, 15)

#Filtro de média
i_Media = timeit.default_timer()
ImgBlur_Media = cv2.blur(img_equal, ksize)
f_Media = timeit.default_timer()
processing_time_Media = f_Media - i_Media
#cv2.imshow('Filtro de media', ImgBlur_Media)

#Filtro Gaussiano sigma=0
i_Gaussiano = timeit.default_timer()
ImgBlur_Gaussiano = cv2.GaussianBlur(img_equal, ksize, 0)
f_Gaussiano = timeit.default_timer()
processing_time_Gaussiano = f_Gaussiano - i_Gaussiano
#cv2.imshow('Filtro Gaussiano com sigma=0', ImgBlur_Gaussiano)

#Filtro Gaussiano sigma=2
i_Gaussiano_2 = timeit.default_timer()
ImgBlur_Gaussiano_2 = cv2.GaussianBlur(img_equal, ksize, 2)
f_Gaussiano_2 = timeit.default_timer()
processing_time_Gaussiano_2 = f_Gaussiano_2 - i_Gaussiano_2
#cv2.imshow('Filtro Gaussiano com sigma=2', ImgBlur_Gaussiano_2)

#Filtro Gaussiano sigma=5
i_Gaussiano_5 = timeit.default_timer()
ImgBlur_Gaussiano_5 = cv2.GaussianBlur(img_equal, ksize, 5)
f_Gaussiano_5 = timeit.default_timer()
processing_time_Gaussiano_5 = f_Gaussiano_5 - i_Gaussiano_5
#cv2.imshow('Filtro Gaussiano com sigma=5', ImgBlur_Gaussiano_5)

#Filtro de mediana
i_Mediana = timeit.default_timer()
ImgBlur_Mediana= cv2.medianBlur(img_equal, 15)
f_Mediana = timeit.default_timer()
processing_time_Mediana = f_Mediana - i_Mediana

#cv2.imshow('Filtro de mediana', ImgBlur_Mediana)

cv2.waitKey(0)
cv2.destroyAllWindows()

#print(f" Tempo de processamento com o Filtro Média: {processing_time_Media * 1e6} microsegundos \n Tempo de processamento com o Filtro Gaussiano: {processing_time_Gaussiano * 1e6} microsegundos \n Tempo de processamento com o Filtro Mediana: {processing_time_Mediana * 1e6} microsegundos")
print(f"Filtro Gaussiano sigma=0: {processing_time_Gaussiano * 1e6} microsegundos \n Filtro Gaussiano sigma=2: {processing_time_Gaussiano_2 * 1e6} microsegundos \n Filtro Gaussiano sigma=5: {processing_time_Gaussiano_5 * 1e6} microsegundos")