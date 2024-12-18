import os
import cv2
import numpy as np
import pickle

data_dir = "D:\\Proyectos\\IA_trabajos\\ProyectoCarrosCNN\\dataset"


categories = ['Autobus', 'Ford F-150', 'Honda Accord', 'Tesla Cybertruck', 'Volkswagen Beetle']

data = []

def make_data():
    corrupt_count = 0  # Contador de imágenes no legibles
    error_count = 0  # Contador de errores de procesamiento
    valid_extensions = ('.jpg', '.jpeg', '.png')  # Extensiones válidas

    for category in categories:
        path = os.path.join(data_dir, category)
        label = categories.index(category)

        if not os.path.exists(path):
            print(f"Directory {path} does not exist.")
            continue

        for img_name in os.listdir(path):
            # Filtrar archivos no válidos
            if not img_name.lower().endswith(valid_extensions):
                print(f"Archivo ignorado (no es imagen): {img_name}")
                continue

            image_path = os.path.join(path, img_name)
            if not os.path.isfile(image_path):
                continue

            image = cv2.imread(image_path)
            if image is None:
                corrupt_count += 1
                print(f"Imagen no legible: {image_path}")
                continue

            try:
                # Procesar imagen
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, (80, 80))  # Tamaño reducido
                data.append([image, label])
            except Exception as e:
                error_count += 1
                print(f"Error procesando {image_path}: {e}")

    print(f"Total imágenes procesadas: {len(data)}")
    print(f"Imágenes corruptas/no legibles: {corrupt_count}")
    print(f"Errores de procesamiento: {error_count}")

    # Guardar datos procesados
    with open('data.pickle', 'wb') as pik:
        pickle.dump(data, pik)
        print("Data saved to data.pickle")

make_data()
