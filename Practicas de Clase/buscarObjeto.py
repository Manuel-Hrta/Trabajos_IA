import numpy as np
import cv2 as cv

# Inicializa la captura de video
cap = cv.VideoCapture(0)

# Leer el primer cuadro para usarlo como referencia
ret, frame_anterior = cap.read()
frame_anterior_gray = cv.cvtColor(frame_anterior, cv.COLOR_BGR2GRAY)
frame_anterior_gray = cv.GaussianBlur(frame_anterior_gray, (21, 21), 0)

i = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el cuadro actual a escala de grises y desenfocarlo (para eliminar el ruido)
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.GaussianBlur(frame_gray, (21, 21), 0)

    # Calcular la diferencia absoluta entre el cuadro anterior y el cuadro actual
    diferencia = cv.absdiff(frame_anterior_gray, frame_gray)

    # Aplicar un umbral (threshold) para obtener la imagen binaria (blanco y negro)
    _, umbral = cv.threshold(diferencia, 25, 255, cv.THRESH_BINARY)

    # Dilatar la imagen binaria para unir áreas cercanas
    umbral = cv.dilate(umbral, None, iterations=2)

    # Encontrar los contornos de las áreas en movimiento
    contornos, _ = cv.findContours(umbral, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Procesar cada contorno detectado
    for contorno in contornos:
        if cv.contourArea(contorno) < 500:  # Ignorar pequeños movimientos
            continue

        # Obtener las coordenadas del rectángulo delimitador del objeto en movimiento
        (x, y, w, h) = cv.boundingRect(contorno)

        # Dibujar un rectángulo alrededor del objeto en movimiento (opcional)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Recortar el área del objeto en movimiento
        objeto_recortado = frame[y:y+h, x:x+w]

        # Guardar el recorte del objeto
        cv.imwrite('capturas2/ObjetoMovimiento' + str(i) + '.jpg', objeto_recortado)
        cv.imshow('Objeto Recortado', objeto_recortado)

    # Mostrar la imagen con los objetos detectados
    cv.imshow('Detección de Movimiento', frame)

    # Actualizar el cuadro anterior con el cuadro actual
    frame_anterior_gray = frame_gray.copy()

    # Incrementar el contador para guardar las imágenes
    i += 1

    # Presionar 'Esc' para salir
    k = cv.waitKey(1)
    if k == 27:
        break

# Liberar el video y cerrar las ventanas
cap.release()
cv.destroyAllWindows()
