import os
import cv2

# Directorio de datos de entrada
data_dir = "D:\Proyectos\IA_trabajos\ProyectoCarrosCNN\dataset"

# Categorías de imágenes
categories = ['Volkswagen Beetle']

# Directorio de salida
output_dir = "D:\Proyectos\IA_trabajos\ProyectoCarrosCNN\datasetRecized"

# Función para redimensionar y guardar imágenes
def resize_and_convert_images():
    corrupt_count = 0  # Contador de imágenes no legibles
    error_count = 0  # Contador de errores de procesamiento
    valid_extensions = ('.png',)  # Extensión válida para las imágenes PNG

    # Crear directorio de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for category in categories:
        input_path = os.path.join(data_dir, category)
        category_output_path = os.path.join(output_dir, category)

        # Crear directorio para cada categoría en la salida
        if not os.path.exists(category_output_path):
            os.makedirs(category_output_path)

        if not os.path.exists(input_path):
            print(f"Directory {input_path} does not exist.")
            continue

        for img_name in os.listdir(input_path):
            # Filtrar archivos no válidos (solo PNG)
            if not img_name.lower().endswith(valid_extensions):
                print(f"Archivo ignorado (no es imagen PNG): {img_name}")
                continue

            image_path = os.path.join(input_path, img_name)
            if not os.path.isfile(image_path):
                continue

            try:
                image = cv2.imread(image_path)
                if image is None:
                    corrupt_count += 1
                    print(f"Imagen no legible: {image_path}")
                    continue

                # Redimensionar la imagen
                resized_image = cv2.resize(image, (80, 80))
                
                # Generar la ruta de salida y mantener el formato PNG
                output_image_path = os.path.join(category_output_path, img_name)
                
                # Guardar la imagen redimensionada como PNG
                cv2.imwrite(output_image_path, resized_image)
                print(f"Imagen redimensionada y guardada: {output_image_path}")

            except Exception as e:
                error_count += 1
                print(f"Error procesando {image_path}: {e}")

    print(f"Imágenes corruptas/no legibles: {corrupt_count}")
    print(f"Errores de procesamiento: {error_count}")
    print("Proceso completado. Imágenes redimensionadas y guardadas.")

resize_and_convert_images()
