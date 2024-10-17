import cv2
import numpy as np

def encontrarColores(image):
    # Convertir la imagen a espacio de color HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Ajustar los rangos de color amarillo para capturar solo los tonos amarillos
    lower_yellow1 = np.array([20, 150, 50])  # Ajustar la saturación y el valor para el amarillo más claro
    upper_yellow1 = np.array([30, 255, 255])

    # Crear la máscara usando los rangos
    colorToDetect = cv2.inRange(hsv_image, lower_yellow1, upper_yellow1)

    # Usar dilatación para conectar componentes
    kernel = np.ones((3, 3), np.uint8)
    colorToDetect_dilated = cv2.dilate(colorToDetect, kernel, iterations=2)

    # Encontrar contornos en la máscara dilatada
    contours, _ = cv2.findContours(colorToDetect_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Crear una copia de la imagen original para dibujar los resultados
    result_image = image.copy()

    red_objects_centers = []
    # Calcular el centroide de cada contorno detectado y dibujar un círculo amarillo
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] > 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            red_objects_centers.append((cX, cY))
            cv2.circle(result_image, (cX, cY), 7, (0, 255, 255), -1)  # Dibujar círculo amarillo

    return red_objects_centers, result_image

# Cargar la imagen
image_path = 'objetosrojos.jpg'
image = cv2.imread(image_path)

# Encontrar los objetos amarillos y mostrarlos en la imagen original
red_objects_centers, result_image = encontrarColores(image)

# Imprimir las coordenadas de los centros de los objetos detectados
for idx, center in enumerate(red_objects_centers):
    print(f"Centro del objeto amarillo {idx+1}: {center}")

# Guardar la imagen resultante
output_image_path = 'objetosDetectados.jpg'
cv2.imwrite(output_image_path, result_image)

# Mostrar la imagen resultante con los objetos detectados marcados
cv2.imshow('Detected Objects', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
