import cv2
import numpy as np

# Abre o vídeo
cap = cv2.VideoCapture("/home/deboradfg/Desktop/videov2.h264")

# Verifica se o vídeo foi aberto com sucesso
if not cap.isOpened():
    print("Erro ao abrir o vídeo. Verifique o caminho do arquivo.")
    exit()

# Função de callback para barras deslizantes
def on_trackbar(value):
    pass  # Função de espaço reservado, não faz nada

# Criação da janela para barras deslizantes
cv2.namedWindow('Trackbars')

# Define os valores iniciais e máximos para os intervalos de cor
hsv_lower = np.array([0, 110, 160])
hsv_upper = np.array([30, 255, 255])
contagem_acima_limite = 0

# Criação das barras deslizantes
cv2.createTrackbar('Hue Min', 'Trackbars', hsv_lower[0], 179, on_trackbar)
cv2.createTrackbar('Saturation Min', 'Trackbars', hsv_lower[1], 255, on_trackbar)
cv2.createTrackbar('Value Min', 'Trackbars', hsv_lower[2], 255, on_trackbar)
cv2.createTrackbar('Hue Max', 'Trackbars', hsv_upper[0], 179, on_trackbar)
cv2.createTrackbar('Saturation Max', 'Trackbars', hsv_upper[1], 255, on_trackbar)
cv2.createTrackbar('Value Max', 'Trackbars', hsv_upper[2], 255, on_trackbar)

while True:
    # Lê um frame do vídeo
    ret, frame = cap.read()

    # Se não foi possível obter um frame, nada mais deve ser feito
    if not ret:
        break

    # Conversão RGB -> HSV
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Obter os valores atuais das barras deslizantes
    hsv_lower = np.array([
        cv2.getTrackbarPos('Hue Min', 'Trackbars'),
        cv2.getTrackbarPos('Saturation Min', 'Trackbars'),
        cv2.getTrackbarPos('Value Min', 'Trackbars')
    ])
    hsv_upper = np.array([
        cv2.getTrackbarPos('Hue Max', 'Trackbars'),
        cv2.getTrackbarPos('Saturation Max', 'Trackbars'),
        cv2.getTrackbarPos('Value Max', 'Trackbars')
    ])

    # Cria uma máscara usando o intervalo de cores
    mask = cv2.inRange(frameHSV, hsv_lower, hsv_upper)

    # Aplica operação de abertura para remover ruídos
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Conta pixels brancos
    white_pixels = cv2.countNonZero(mask)
    #print(f"Número de pixels brancos: {white_pixels}")
    
    # Atualiza a contagem se a quantidade de pixels brancos estiver acima do limiar
    if white_pixels > 400000:
        contagem_acima_limite += 1
    else:
        contagem_acima_limite = 0

    # Verifica se a contagem atingiu o número de frames desejado
    if contagem_acima_limite >= 10:
        print(f"Número de pixels brancos: {white_pixels} Piso de alerta")
    else:
        print(f"Número de pixels brancos: {white_pixels} Piso direcional")


    # Exibe os vídeos
    cv2.imshow('Video Binarizado', mask)
    cv2.imshow('Video Original', frame)

    # Verifica se o usuário pressionou a tecla 'q' para sair
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
