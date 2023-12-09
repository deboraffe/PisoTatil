import cv2
import numpy as np
import timeit

# Inicializa variáveis
frame_count = 0
total_processing_time = 0

# Abre a câmera
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# Verifica se a câmera foi aberta corretamente
if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

# Loop principal
while frame_count < 10:  # Processar 10 frames
	
    i_time = timeit.default_timer()

    # Lê um frame do vídeo
    ret, frame = cap.read()

    # Pré-processamento
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameEqual = cv2.equalizeHist(frameGray)
    frameBlur = cv2.blur(frameGray, (6, 6))

    # Binarização
    _, frameThresh = cv2.threshold(frameBlur, 68, 255, cv2.THRESH_BINARY)

    # Contar pixels brancos
    white_pixels = cv2.countNonZero(frameThresh)
    black_pixels = frameThresh.size - white_pixels

    f_time = timeit.default_timer()

    # Atualiza o tempo total de processamento
    total_processing_time += f_time - i_time

    # Incrementa o contador de frames
    frame_count += 1

# Libera os recursos da câmera
cap.release()

# Calcula a média do tempo de processamento
average_processing_time = total_processing_time / frame_count
print(f"Média do tempo de processamento para 10 frames: {average_processing_time} segundos")

