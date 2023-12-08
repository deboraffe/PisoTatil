import cv2 
import numpy as np 
import matplotlib.pyplot as plt

#Imagem Original (Colorida)
img_rgb = cv2.imread(r'C:\Users\debor\OneDrive\Documentos\VSPython\Area\piso_area.jpg') 
cv2.imshow('Original', img_rgb)

#Imagem Escala de Cinza
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) 
cv2.imshow('Escala de Cinza', img_gray)

#Calculo do Histograma
#channels   = [0]
#histSize = [256]
#ranges   = [0, 256]   
#hist = cv2.calcHist([img_gray],channels,None,histSize,ranges)

#Calculo e Plote Direto do Histograma
#plt.hist(img_gray.ravel(),256,[0,256])
#plt.show()

#Equalização da Imagem
img_equal = cv2.equalizeHist(img_gray)
#cv2.imshow('Imagem Equalizada', img_equal)

#Plote do histograma da Imagem Equalizada
#plt.hist(img_equal.ravel(),256,[0,256])
#plt.show()

#Suavização(blur) da Imagem
ksize = (20, 20)
#img_blur = cv2.blur(img_equal, ksize, cv2.BORDER_DEFAULT) 
#img_blur = cv2.medianBlur(img_equal, 15)
img_blur = cv2.GaussianBlur (img_equal,(5,5),0)
#cv2.imshow('Imagem Suavizada', img_blur)

#Limiarização(thresholding) da Imagem
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

cv2.imshow('Imagem Limiarizada', th1)

#Contornos da Imagem
contours, hierarchies = cv2.findContours(th1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #Desenhar os cortornos
blank = np.zeros(th4.shape[:2],dtype='uint8')
cv2.drawContours(blank, contours, -1,(255, 0, 0), 1)
cv2.imshow('Imagem com Contornos', blank)

number_of_white_pix = np.sum (blank == 255) # extraindo apenas pixels brancos 
print('Number of white pixels:', number_of_white_pix)

cv2.waitKey()