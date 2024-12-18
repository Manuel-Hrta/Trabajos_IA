import cv2
import numpy as np
from tensorflow import keras

def preprocesar(cuadro):
    # Convertir la imagen de BGR (OpenCV por defecto) a RGB
    cuadro_rgb = cv2.cvtColor(cuadro, cv2.COLOR_BGR2RGB)
    # Redimensionar la imagen a 224x224 (tamaño estándar para muchos modelos)
    cuadro_redimensionado = cv2.resize(cuadro_rgb, (80, 80))
    # Normalizar la imagen dividiendo entre 255.0
    cuadro_normalizado = cuadro_redimensionado / 255.0
    # Expande las dimensiones de la imagen para que el modelo la reciba como un lote de tamaño 1
    cuadro_expandido = np.expand_dims(cuadro_normalizado, axis=0)
    return cuadro_expandido

# Cargar el modelo previamente entrenado
modelo = keras.models.load_model('mymodel.h5')

# Definir las categorías (marcas de los carros)
categories = ['Autobus', 'Ford F-150', "Honda Accord", "Tesla Cybertruck", "Volkswagen Golf"]

# Cargar la imagen desde el archivo (reemplaza 'path_to_image.jpg' con el camino real de la imagen)
imagen = cv2.imread('D:/Proyectos/IA_trabajos/ProyectoCarrosCNN/honda.jpg')  # Reemplaza con la ruta de tu imagen

# Verificar si la imagen fue cargada correctamente
if imagen is not None:
    # Preprocesar la imagen
    imagen_procesada = preprocesar(imagen)

    # Hacer la predicción con el modelo
    prediccion = modelo.predict(imagen_procesada)

    # Obtener el índice de la clase con mayor probabilidad
    marca_predicha = categories[np.argmax(prediccion)]

    # Mostrar el nombre de la marca predicha
    print(f'La marca predicha es: {marca_predicha}')

    # Mostrar la imagen con la marca predicha
    cv2.putText(imagen, f'{marca_predicha}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Imagen predicha', imagen)

    # Espera a que el usuario cierre la ventana
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No se pudo cargar la imagen. Verifica la ruta del archivo.")