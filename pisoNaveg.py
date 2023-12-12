import cv2
import numpy as np
import RPi.GPIO as GPIO
import timeit
import time

# Abre a câmera
#cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # 0 indica o índice da câmera
# Abre o vídeo
cap = cv2.VideoCapture("/home/deboradfg/Desktop/videoNaveg.h264")
# Verifica se a câmera foi aberta com sucesso
if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()
    
# Define o número do pino GPIO conectado ao LED
GPIO.setmode(GPIO.BOARD) # Define o modo de numeração (Board)
GPIO.setwarnings(False) # Desativa as mensagens de alerta
LED_DIRECIONAL = 13
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
media_PisoAlerta = 0

try:
    estado_atual = "direcional"  # Inicializa o estado como direcional
    print("Saia do seu destino inicial e siga em frente")
    ponto = 1 #Inicializa no ponto 1
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Pré-processamento
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frameEqual = cv2.equalizeHist(frameGray)
        frameBlur = cv2.blur(frameGray, ksize)

        # Binarização
        _, frameThresh = cv2.threshold(frameBlur, thresh, 255, cv2.THRESH_BINARY)

        # Contar pixels brancos
        white_pixels = cv2.countNonZero(frameThresh)
        black_pixels = frameThresh.size - white_pixels

        # Atualizar contagem se o número de pixels pretos estiver acima do limite (Detecção piso de alerta)
        if black_pixels > 170000:
            media_PisoAlerta += 1
        else:
            media_PisoAlerta = 0

        # Verifica transições entre piso direcional e piso de alerta
        # Ponto 1
        if estado_atual == "direcional" and media_PisoAlerta >= 5 and ponto == 1:
            print("Siga em frente")
            # Exiba a mensagem para o usuário ou realize outras ações necessárias
            estado_atual = "alerta"
            ponto += 1
            
        # Ponto 2    
        elif estado_atual == "alerta" and media_PisoAlerta <= 5 and ponto == 2:
            print("Siga em frente")
            # Exiba a mensagem para o usuário ou realize outras ações necessárias
            estado_atual = "direcional"
            ponto += 1
            
        # Ponto 3    
        elif estado_atual == "direcional" and media_PisoAlerta >= 5 and ponto == 3:
            print("Vire à esquerda e siga em frente ")
            # Exiba a mensagem para o usuário ou realize outras ações necessárias
            estado_atual = "alerta"
            ponto += 1
            
        # Ponto 4   
        elif estado_atual == "alerta" and media_PisoAlerta <= 5 and ponto == 4:
            print("Siga em frente")
            estado_atual = "direcional"
            ponto += 1
            
        # Ponto 5    
        elif estado_atual == "direcional" and media_PisoAlerta >= 5 and ponto == 5:
            print("Vire à esquerda")
            print("Você chegou no seu destino final")
            # Exiba a mensagem para o usuário ou realize outras ações necessárias
            estado_atual = "alerta"
            ponto += 1
            
        # Controla o LED de acordo com o piso
        if estado_atual == "alerta":
            # Acende o LED de alerta
            GPIO.output(LED_DIRECIONAL, GPIO.LOW)
            GPIO.output(LED_ALERTA, GPIO.HIGH)
        else:
            # Acende o LED direcional
            GPIO.output(LED_ALERTA, GPIO.LOW)
            GPIO.output(LED_DIRECIONAL, GPIO.HIGH)

        # Exibir imagens
        cv2.imshow('Video', frameThresh)
        cv2.imshow('Video Original', frame)

        # Verificar se o usuário pressionou 'q' para sair
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

finally:
    GPIO.cleanup()
    cv2.destroyAllWindows()


