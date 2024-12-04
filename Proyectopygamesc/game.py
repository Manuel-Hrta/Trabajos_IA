import pygame
import random
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
import csv
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib 

# Inicializar Pygame
pygame.init()


# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None

# Variables de salto
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False

# Archivo de datos
archivo_datos = "datos_juego.csv"

# Variables del juego
datos_modelo = []

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo2.png')
nave_img = pygame.image.load('assets/game/ufo.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10
frame_count = 0

# Variables para la bala
velocidad_bala = -10
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w



# Inicializar el archivo CSV
def inicializar_csv():
    try:
        with open(archivo_datos, mode="w", newline="") as archivo_csv:
            escritor = csv.writer(archivo_csv)
            escritor.writerow(["Velocidad", "Distancia", "Salto"])
    except Exception as e:
        print(f"Error al inicializar el archivo CSV: {e}")

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -8)
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50
    bala_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo
    if salto:
        jugador.y -= salto_altura
        salto_altura -= gravedad
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15
            en_suelo = True
# Función para actualizar el juego
def update():
    global fondo_x1, fondo_x2, current_frame, frame_count, bala, velocidad_bala, salto, en_suelo, bala_disparada

    # Movimiento del fondo
    fondo_x1 -= 1
    fondo_x2 -= 1
    if fondo_x1 <= -w: fondo_x1 = w
    if fondo_x2 <= -w: fondo_x2 = w

    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Movimiento de la bala
    if bala_disparada:
        bala.x += velocidad_bala
    if bala.x < 0:
        reset_bala()
    pantalla.blit(bala_img, (bala.x, bala.y))

    if jugador.colliderect(bala):
        print("Colisión detectada!")
        guardar_datos()
        reiniciar_juego()

# Función para guardar datos en la lista y el archivo CSV
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0
    nuevo_dato = (velocidad_bala, distancia, salto_hecho)
    datos_modelo.append(nuevo_dato)
    try:
        with open(archivo_datos, mode="a", newline="") as archivo_csv:
            escritor = csv.writer(archivo_csv)
            escritor.writerow(nuevo_dato)
    except Exception as e:
        print(f"Error al guardar datos en CSV: {e}")

#cargar modelo arbol
def cargar_arbol():
    global modelo_arbol
    try:
        modelo_arbol = joblib.load("modelo_arbol.pkl")
        print("Modelo de árbol cargado desde 'modelo_arbol.pkl'.")
    except FileNotFoundError:
        print("El archivo 'modelo_arbol.pkl' no existe. Entrena el modelo primero.")

# Función para cargar el modelo de red neuronal
def cargar_modelo():
    global modelo_salto
    try:
        modelo_salto = load_model('modelo_salto.h5')
        print("Modelo cargado correctamente.")
    except FileNotFoundError:
        print("El modelo 'modelo_salto.h5' no existe. Entrena el modelo primero.")

# Función para reiniciar el juego
def reiniciar_juego():
    global menu_activo, bala, jugador, nave, bala_disparada, salto, en_suelo
    jugador.x, jugador.y = 50, h - 100
    bala.x = w - 50
    nave.x, nave.y = w - 100, h - 100
    bala_disparada = False
    salto = False
    en_suelo = True
    menu_activo = True
    mostrar_menu()

def decision_automatica():
    global modelo_salto, jugador, bala
    if modelo_salto is None:
        print("modelo_salto no cargado.")
        return False

     # Obtener los datos de entrada
    velocidad = velocidad_bala
    distancia = abs(jugador.x - bala.x)
    entrada = np.array([[velocidad, distancia]])  # Crear entrada para el modelo

    # # # Hacer la predicción
    prediccion = modelo_salto.predict(entrada)[0][0]
    print(f"Probabilidad de saltar: {prediccion:.2f}")

    # # # Decidir si saltar (umbral 0.5)
    return prediccion > 0.5

def decision_automatica_arbol():
    global modelo_arbol, jugador, bala
    if modelo_arbol is None:
        print("Modelo de árbol no cargado.")
        return False

    # # Preparar los datos de entrada para el árbol
    velocidad = velocidad_bala
    distancia = abs(jugador.x - bala.x)
    entrada = [[velocidad, distancia]]  # Crear la entrada como una lista de listas

    # # Hacer la predicción
    prediccion = modelo_arbol.predict(entrada)[0]  # Obtener la predicción (0 o 1)
    print(f"Decisión del árbol: {'Salto' if prediccion == 1 else 'No salto'}")
    return prediccion == 1  # True si debe saltar, False si no


# Función para generar el árbol de decisión
def entrenar_arbol():
    global modelo_arbol
    print("Entrenando el árbol de decisión...")
    try:
        # Cargar los datos del archivo CSV
        datos = pd.read_csv(archivo_datos)
        if datos.empty:
            print("El archivo CSV está vacío. No se puede entrenar el árbol.")
            return

        # Separar las características (X) y la etiqueta (y)
        X = datos[["Velocidad", "Distancia"]]
        y = datos["Salto"]

        # Verificar si hay suficientes datos para entrenar
        if len(datos) < 5:
            print("No hay suficientes datos para entrenar el árbol de decisión.")
            return

        # Entrenar el modelo de árbol de decisión
        modelo_arbol = DecisionTreeClassifier()
        modelo_arbol.fit(X, y)

        # Guardar el modelo entrenado en un archivo .pkl
        joblib.dump(modelo_arbol, "modelo_arbol.pkl")
        print("Modelo de árbol entrenado y guardado como 'modelo_arbol.pkl'.")

    except FileNotFoundError:
        print(f"El archivo '{archivo_datos}' no existe. Asegúrate de guardar datos antes de entrenar.")
    except Exception as e:
        print(f"Error al entrenar el árbol de decisión: {e}")



#entrenar modelo con boton 
def entrenar_modelo():
    global modelo_salto
    print("Entrenando el modelo...")

    try:
        # Cargar los datos
        datos = pd.read_csv(archivo_datos)
        if datos.empty:
            print("No hay datos suficientes para entrenar el modelo.")
            return

        # Dividir los datos
        X = datos[["Velocidad", "Distancia"]]
        y = datos["Salto"]

        # Dividir en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Definir el modelo
        modelo = Sequential([
            Dense(16, input_dim=2, activation="relu"),
            Dense(8, activation="relu"),
            Dense(1, activation="sigmoid")
        ])

        # Compilar el modelo
        modelo.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

        # Entrenar el modelo
        modelo.fit(X_train, y_train, epochs=20, batch_size=10, validation_data=(X_test, y_test))

        # Evaluar el modelo en el conjunto de prueba
        loss, accuracy = modelo.evaluate(X_test, y_test, verbose=0)
        print(f"Modelo actualizado con precisión en conjunto de prueba: {accuracy:.2f}")

        # Guardar el modelo actualizado
        modelo.save("modelo_salto.h5")
        print("Modelo actualizado y guardado correctamente.")

        # Cargar el nuevo modelo en memoria para el modo automático
        cargar_modelo()

    except Exception as e:
        print(f"Error al entrenar el modelo: {e}")


# Función para mostrar el menú
def mostrar_menu():
    global menu_activo, modo_auto, modo_auto_arbol
    pantalla.fill(NEGRO)

    # Títulos
    titulo = fuente.render("MENÚ PRINCIPAL", True, BLANCO)
    subtitulo = fuente.render("================", True, BLANCO)

    # Opciones
    opcion1 = fuente.render("[M] Modo Manual", True, BLANCO)
    opcion2 = fuente.render("[A] Modo Automático", True, BLANCO)
    opcion3 = fuente.render("[P] Modo Automático (Árbol)", True, BLANCO)  # Nueva opción
    opcion7 = fuente.render("[Q] Salir del Programa", True, BLANCO)

    # Definir las posiciones iniciales para las opciones
    espacio_entre_opciones = 40
    y_inicio = 50  # Lugar donde inicia el menú, más cerca del top

    # Renderizar en pantalla
    pantalla.blit(titulo, (w // 8, y_inicio))  # Título en la parte superior
    pantalla.blit(subtitulo, (w // 8, y_inicio + 40))  # Subtítulo debajo del título
    pantalla.blit(opcion1, (w // 8, y_inicio + 80))
    pantalla.blit(opcion2, (w // 8, y_inicio + 120))
    pantalla.blit(opcion3, (w // 8, y_inicio + 160))
    pantalla.blit(opcion7, (w // 8, y_inicio + 200))

    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    entrenar_modelo()
                    modo_auto = True
                    menu_activo = False
                    modo_auto_arbol = False  # Activar el modo automático con el árbol
                    print(modo_auto_arbol)
                elif evento.key == pygame.K_m:
                    inicializar_csv()
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_p:  # Modo Automático (Árbol)
                    entrenar_arbol()
                    cargar_arbol()
                    if modelo_arbol is None:  # Validar si se cargó correctamente
                        print("El modelo de árbol no está disponible. Genera el modelo primero.")
                        pausa = True  # Pausar el juego
                    else:
                        modo_auto = True
                        modo_auto_arbol = True  # Activar el modo automático con el árbol
                        menu_activo = False
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    exit()


# Función principal
# Modificar la función principal para reiniciar con la tecla ESC
def main():
    global pausa  # Asegurarse de que pausa sea global
    cargar_modelo()
    cargar_arbol()
    global salto, en_suelo, bala_disparada, modo_auto
    reloj = pygame.time.Clock()
    mostrar_menu()
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_ESCAPE:  # Detectar la tecla ESC
                    print("Tecla ESC presionada. Reiniciando juego.")
                    reiniciar_juego()  # Llamar a la función de reinicio del juego

        if not pausa:  # Validación de pausa
            if not bala_disparada:
                disparar_bala()

            if salto:
                manejar_salto()

            if not modo_auto:
                guardar_datos()
            elif modo_auto:
                if modo_auto_arbol:  # Usar el árbol de decisión
                    if decision_automatica_arbol():  # Basado en el árbol
                        salto = True
                        en_suelo = False
                elif not modo_auto_arbol:  # Usar la red neuronal
                    if decision_automatica():  # Basado en la red neuronal
                        salto = True
                        en_suelo = False

            update()

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()




if __name__ == "__main__":
    main()
