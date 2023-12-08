'''
Pré processamento de imagem - Escala de Cinza
Débora Fernandes Gonçalves
'''
import cv2 
import numpy as np 
import matplotlib.pyplot as plt
import math

class ImageProcessing:

    def __init__(self):
        print('Image Processing')
    
    #Escala de Cinza
    def to_gray(img_path):
        # Carregar Imagem Original
        img_rgb = cv2.imread(img_path) 
        cv2.imshow('Original', img_rgb)
        cv2.waitKey(0)

        # Converter para escala de cinzas
        gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) 
        cv2.imshow('Escala de Cinza', gray) 
        cv2.waitKey(0)

        return gray

    #Análise do Histograma
    def instantiate_histogram(image):   
        channels   = [0]
        histSize = [256]
        ranges   = [0, 256]
            
        hist = cv2.calcHist([image],channels,None,histSize,ranges) 
        
        # img_gray.ravel() transforma a imagem em um vetor (unidimensional)
        plt.hist(image.ravel(),256,[0,256])
        plt.bar(hist.keys(), hist.values())
        plt.xlabel("Níveis intensidade")
        ax = plt.gca()
        ax.axes.xaxis.set_ticks([])
        plt.grid(True)
        plt.show()
        
imagemGray = ImageProcessing.to_gray(r'C:\Users\debor\OneDrive\Documentos\VSPython\Area\piso_area.jpg')

ImageProcessing.instantiate_histogram(imagemGray)