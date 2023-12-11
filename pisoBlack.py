import cv2
import numpy as np
import RPi.GPIO as GPIO
import timeit
import time

# Abre a câmera
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # 0 indica o índice da câmera
# Abre o vídeo
#cap = cv2.VideoCapture("/home/deboradfg/Desktop/videoindoor_v2.h264")
# Verifica se a câmera foi aberta com sucesso
if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()
    
# Define o número do pino GPIO conectado ao LED
GPIO.setmode(GPIO.BOARD) # Define o modo de numeração (Board)
GPIO.setwarnings(False) # Desativa as mensagens de alerta
LED_DIRECIONAL = 11
LED_ALERTA = 7

# Inicializa o GPIO
GPIO.setup(LED_DIRECIONAL, GPIO.OUT)
GPIO.setup(LED_ALERTA, GPIO.OUT)

# Criação da janela para barras deslizantes
cv2.namedWindow('Video')

# Valores iniciais para as trackbars
ksize = (6, 6)  # Inicializado como uma tupla
thresh = 68

# Função de callback para a barra deslizante
def ksize_limit(value):
    global ksize
    ksize_value = 2 * value + 1  # Garante que o valor seja ímpar
    ksize = (ksize_value, ksize_value)  # Atualiza a variável ksize como uma tupla (value, value)

def thresh_limit(value):
    global thresh
    thresh = value

# Cria as barras deslizantes
cv2.createTrackbar('ksize', 'Video', ksize[0], 30, ksize_limit) 
cv2.createTrackbar('thresh', 'Video', thresh, 255, thresh_limit)

# Parâmetros para a média móvel
contagem_acima_limite = 0

try:
    while True:
        # Lê um frame do vídeo
        ret, frame = cap.read()

        # Se não foi possível obter um frame, nada mais deve ser feito
        if not ret:
            break
        
        # Pré-processamento
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frameEqual = cv2.equalizeHist(frameGray)
        frameBlur = cv2.blur(frameGray, ksize)    
            
        # Binarização
        _, frameThresh = cv2.threshold(frameBlur, thresh, 255, cv2.THRESH_BINARY)

        # Conta os pixels brancos
        white_pixels = cv2.countNonZero(frameThresh)
        black_pixels = frameThresh.size - white_pixels
                
        # Atualiza a contagem se a quantidade de pixels brancos estiver acima do limiar observado
        if black_pixels > 95000:
            contagem_acima_limite += 1
        else:
            contagem_acima_limite = 0

        # Verifica se a contagem atingiu o número de frames desejado
        if contagem_acima_limite >= 10:
            print(f"Número de pixels pretos: {black_pixels} Piso de alerta")
            GPIO.output(LED_DIRECIONAL, GPIO.LOW)  # Desliga o LED direcional
            GPIO.output(LED_ALERTA, GPIO.HIGH)     # Acende o LED de alerta
            
        else:
            print(f"Número de pixels pretos: {black_pixels} Piso direcional")
            GPIO.output(LED_ALERTA, GPIO.LOW)       # Desliga o LED de alerta
            GPIO.output(LED_DIRECIONAL, GPIO.HIGH)  # Acende o LED direcional
            
            
        # Exibe as imagens
        cv2.imshow('Video', frameThresh)
        cv2.imshow('Video Original', frame)

        # Verifica se o usuário pressionou a tecla 'q' para sair
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
         
 finally:
    # Limpa a configuração da GPIO quando o programa está prestes a encerrar
    GPIO.cleanup()
    # Fecha a janela do OpenCV
    cv2.destroyAllWindows()
