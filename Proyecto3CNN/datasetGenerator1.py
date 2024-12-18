from bing_image_downloader import downloader
import cv2
import os
import numpy as np

def make_background_transparent(image, threshold=0):
    tmp = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    black_pixels = np.all(tmp[:, :, :3] <= threshold, axis=2)
    tmp[black_pixels, 3] = 0
    return tmp

def descargar_y_transformar_opencv(query, total_images, download_path):
    try:
        downloader.download(query, limit=total_images, output_dir=download_path, adult_filter_off=True)
    except Exception as e:
        print(f"Error al descargar imágenes: {e}")
        return
    
    variantes_folder = os.path.join(download_path, query, 'dataTransformed')
    
    os.makedirs(variantes_folder, exist_ok=True)

    folder_path = os.path.join(download_path, query)
    if not os.path.exists(folder_path):
        print("No se encontró la carpeta de descarga. Es posible que no se hayan descargado imágenes.")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            try:
                img = cv2.imread(image_path)
                if img is None:
                    print(f"No se pudo cargar la imagen: {filename}")
                    continue


                # Redimensionar imagen original a 300x300 y guardar
                resized_original = cv2.resize(img, (300, 300))
                original_variant_filename = f"{os.path.splitext(filename)[0]}{query}_original.png"
                resized_original_path = os.path.join(variantes_folder, original_variant_filename)
                cv2.imwrite(resized_original_path, resized_original)

                # Crear 10 variantes de la imagen
                for i in range(10):
                    variant = resized_original.copy()
                    angle = np.random.randint(0, 360)
                    M = cv2.getRotationMatrix2D((150, 150), angle, 1)
                    variant = cv2.warpAffine(variant, M, (300, 300), borderMode=cv2.BORDER_CONSTANT)
                    variant = make_background_transparent(variant)

                    # Guardar la variante de la imagen
                    variant_filename = f"{os.path.splitext(filename)[0]}{query}_variant_{i}.png"
                    variant_path = os.path.join(variantes_folder, variant_filename)
                    cv2.imwrite(variant_path, variant)
            except Exception as e:
                print(f"Error al procesar la imagen {filename}: {e}")
    print("Descarga y variaciones realizadas.")

# Uso de la función
descargar_y_transformar_opencv('2007 Silver Nissan Sentra', 50, 'datasetTadeo/')