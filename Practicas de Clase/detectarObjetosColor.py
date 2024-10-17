import cv2
import numpy as np

def is_valid_color(hsv_pixel, lower_red, upper_red):
    """ Verifica si el color HSV está dentro del rango del rojo. """
    return all(lower_red <= hsv_pixel) and all(hsv_pixel <= upper_red)

def flood_fill(hsv, seed_point, lower_red, upper_red, visited, min_size):
    rows, cols = hsv.shape[:2]
    object_pixels = []
    queue = [seed_point]

    while queue:
        x, y = queue.pop(0)
        if visited[y, x]:
            continue

        current_color = hsv[y, x]
        if is_valid_color(current_color, lower_red, upper_red):
            visited[y, x] = True
            object_pixels.append((x, y))

            # Agregar vecinos a la cola
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and not visited[ny, nx]:
                    queue.append((nx, ny))

    if len(object_pixels) >= min_size:
        return object_pixels
    return []

def find_objects(image, lower_red, upper_red, min_size):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    visited = np.zeros(hsv.shape[:2], dtype=bool)
    object_centers = []

    for y in range(hsv.shape[0]):
        for x in range(hsv.shape[1]):
            if is_valid_color(hsv[y, x], lower_red, upper_red) and not visited[y, x]:
                object_pixels = flood_fill(hsv, (x, y), lower_red, upper_red, visited, min_size)
                if object_pixels:
                    object_center = np.mean(object_pixels, axis=0)
                    object_centers.append((int(object_center[0]), int(object_center[1])))

    return object_centers

# Definir el tamaño mínimo para los objetos detectados (por ejemplo, 30 píxeles)
min_size = 50

# Definir los rangos de rojo en HSV
lower_red1 = np.array([0, 150, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 150, 50])
upper_red2 = np.array([180, 255, 255])


# Cargar la imagen
image_path = 'salida.jpg'
image = cv2.imread(image_path)

# Encontrar los objetos rojos utilizando flood fill
object_centers = find_objects(image, lower_red1, upper_red1, min_size)
object_centers.extend(find_objects(image, lower_red2, upper_red2, min_size))

# Mostrar las coordenadas de los centros de los objetos rojos detectados
for idx, center in enumerate(object_centers):
    print(f"Centro del objeto rojo {idx+1}: {center}")

# Dibujar círculos amarillos en los centros de los objetos rojos
for center in object_centers:
    cv2.circle(image, center=center, radius=5, color=(0, 255, 255), thickness=2)

# Guardar y mostrar la imagen resultante
output_image_path = 'objetosrojos.jpg'
cv2.imwrite(output_image_path, image)
cv2.imshow('Detected Red Objects', image)
cv2.waitKey(0)
cv2.destroyAllWindows()