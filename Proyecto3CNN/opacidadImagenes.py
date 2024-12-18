import cv2 as cv
import os
import numpy as np

def apply_opacity(image, alpha):
    """
    Aplica un nivel de opacidad a una imagen. 
    La opacidad se define mediante el factor alpha (0.0 - totalmente transparente, 1.0 - opacidad completa).
    """
    overlay = np.zeros_like(image, dtype=np.uint8)  # Crear una capa negra del mismo tamaño que la imagen
    return cv.addWeighted(image, alpha, overlay, 1 - alpha, 0)  # Combinar la imagen original con la capa negra

def generate_opacity_variants(input_folder, alphas):
    """
    Genera variantes de opacidad para todas las imágenes de una carpeta y las guarda en la misma carpeta.
    
    Args:
        input_folder (str): Ruta de la carpeta con imágenes.
        alphas (list): Lista de niveles de opacidad (valores entre 0.0 y 1.0).
    """
    # Recorrer todas las imágenes en la carpeta de entrada
    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)
        if not os.path.isfile(input_path):
            continue  # Saltar si no es un archivo
        
        # Leer la imagen
        image = cv.imread(input_path, cv.IMREAD_UNCHANGED)
        if image is None:
            print(f"Error al leer la imagen: {file_name}")
            continue
        
        # Generar variantes con diferentes opacidades
        base_name, ext = os.path.splitext(file_name)
        for alpha in alphas:
            # Aplicar opacidad
            variant = apply_opacity(image, alpha)
            
            # Guardar la imagen resultante en la misma carpeta de entrada
            output_name = f"{base_name}_opacity_{int(alpha * 100)}{ext}"
            output_path = os.path.join(input_folder, output_name)
            cv.imwrite(output_path, variant)
            print(f"Guardada: {output_path}")

# Parámetros
input_folder = r'D:\Proyectos\IA_trabajos\ProyectoCarrosCNN\datasetRecized\Volkswagen Beetle'  # Ruta de la carpeta con las imágenes Honda CRV
opacity_levels = [0.7, 0.5]  # Niveles de opacidad (30%, 50%, 70%, 100%)

# Generar variantes
generate_opacity_variants(input_folder, opacity_levels)
