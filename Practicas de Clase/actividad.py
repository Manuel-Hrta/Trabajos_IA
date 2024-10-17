import numpy as np
import cv2 as cv
import math

# Cargar el clasificador de rostros
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)
i = 0

# Inicializar variable para comparar la cantidad de píxeles blancos
blancos_anterior = 0

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in rostros:
        # Recortar el rostro detectado
        frame2 = frame[y:y+h, x:x+w]
        frame2 = cv.resize(frame2, (100, 100), interpolation=cv.INTER_AREA)
        
        # Convertir a escala de grises (por si no es ya en escala de grises)
        frame_gray = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        
        # Aplicar un umbral (threshold) para binarizar la imagen (blanco y negro)
        _, binario = cv.threshold(frame_gray, 127, 255, cv.THRESH_BINARY)

        # Contar la cantidad de píxeles blancos (valor 255)
        blancos_actual = cv.countNonZero(binario)

        # Comparar con la cantidad anterior de píxeles blancos
        if i > 0:
            diferencia_blancos = blancos_actual - blancos_anterior
            print(f'Blancos actuales: {blancos_actual}, Diferencia: {diferencia_blancos}')
        else:
            print(f'Blancos actuales: {blancos_actual}')

        # Actualizar el valor anterior
        blancos_anterior = blancos_actual

        # Guardar la imagen binaria (si deseas)
        cv.imwrite('capturas/ManuelFaceBinario' + str(i) + '.jpg', binario)

        # Mostrar la imagen binaria (para verificar visualmente)
        cv.imshow('Rostro Binario', binario)

    # Mostrar la imagen original con rostros detectados
    cv.imshow('Rostros', frame)

    i += 1
    k = cv.waitKey(1)
    if k == 27:  # Presiona 'Esc' para salir
        break

cap.release()
cv.destroyAllWindows()
