import random
import heapq
import math

class Celda:
    def __init__(self, x, y, g=0, h=0, cerrada=False, peso=0):
        self.x = x  # Columna (empieza en 1)
        self.y = y  # Fila (empieza en 1)
        self.g = g  # Costo desde el inicio
        self.h = h  # Heurística (distancia al objetivo)
        self.f = g + h  # Función F = G + H
        self.cerrada = cerrada  # Si la celda está cerrada
        self.peso = peso  # Peso asignado a la celda
        self.padre = None  # Para almacenar el camino
        self.visitada = False  # Para marcar si la celda ha sido visitada

    def __lt__(self, other):
        return self.f < other.f

# Función para calcular  (heurística)
def heuristica(celda, meta):
    return math.sqrt((celda.x - meta[0]) ** 2 + (celda.y - meta[1]) ** 2)

# Función para obtener vecinos válidos 
def obtener_vecinos(tablero, actual, filas, columnas):
    vecinos = []
    direcciones = [
        (-1, 0), (1, 0), (0, -1), (0, 1),   # Arriba, abajo, izquierda, derecha
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonales: arriba-izquierda, arriba-derecha, abajo-izquierda, abajo-derecha
    ]
    for d in direcciones:
        nx, ny = actual.x + d[0], actual.y + d[1]
        if 1 <= nx <= columnas and 1 <= ny <= filas and not tablero[ny-1][nx-1].cerrada:
            vecinos.append(tablero[ny-1][nx-1])
    return vecinos

# Función para generar un tablero
def generar_tablero(filas, columnas, celdas_cerradas, meta):
    tablero = [[Celda(x+1, y+1) for x in range(columnas)] for y in range(filas)]
    
    # Asignar celdas cerradas
    for x, y in celdas_cerradas:
        tablero[y-1][x-1].cerrada = True

    # Asignar pesos aleatorios a las celdas abiertas
    num_celdas = filas * columnas
    for fila in tablero:
        for celda in fila:
            if not celda.cerrada:
                celda.peso = random.randint(1, num_celdas)

    return tablero

# Función para imprimir el tablero
def imprimir_tablero(tablero, meta, camino=None):
    for fila in tablero:
        for celda in fila:
            if celda.cerrada:
                print("X", end=" ")  # Celda cerrada
            elif camino and (celda.x, celda.y) == camino[-1]:
                print("*", end=" ")  # Última celda del camino (meta)
            elif (celda.x, celda.y) == meta:
                print("M", end=" ")  # Meta
            elif celda.visitada:
                print(".", end=" ")  # Celda visitada
            else:
                print(celda.peso, end=" ")  # Peso de la celda
        print()
    print()

# Algoritmo A*
def a_estrella(tablero, inicio, meta, filas, columnas):
    abiertos = []
    heapq.heappush(abiertos, inicio)  # Mantener siempre la celda con el menor valor de función f
    cerrados = set()

    while abiertos:
        actual = heapq.heappop(abiertos)

        # Marcar la celda actual como visitada
        actual.visitada = True

        if (actual.x, actual.y) == meta:
            # Llegamos al objetivo, y se guarda en la lista
            camino = []
            while actual:
                camino.append((actual.x, actual.y))
                actual = actual.padre
            return camino[::-1]

        cerrados.add((actual.x, actual.y))  # Se añade la celda actual al conjunto cerrados para marcarla como visitada
        vecinos = obtener_vecinos(tablero, actual, filas, columnas)

        for vecino in vecinos:
            if (vecino.x, vecino.y) in cerrados:
                continue

            # Se calcula el nuevo costo g para llegar a la celda vecina
            g_nuevo = actual.g + vecino.peso
            
            if g_nuevo < vecino.g or vecino not in abiertos:
                vecino.g = g_nuevo
                vecino.h = heuristica(vecino, meta)
                vecino.f = vecino.g + vecino.h
                vecino.padre = actual

                heapq.heappush(abiertos, vecino)

        # Mostrar el avance en consola
        print("Avance actual:")
        imprimir_tablero(tablero, meta)
        print(f"Posibles valores de la función heurística h(n) = √((x1 - x2)^2 + (y1 - y2)^2)) desde ({actual.x}, {actual.y}):")
        for vecino in vecinos:
            print(f"Vecino ({vecino.x}, {vecino.y}) - f: {vecino.f}, g: {vecino.g}, h: {vecino.h}")
        print()

    return None  # No hay camino

def main():
    filas = int(input("Introduce el número de filas del tablero: "))
    columnas = int(input("Introduce el número de columnas del tablero: "))

    # Obtener celdas cerradas
    celdas_cerradas = []
    num_celdas_cerradas = int(input("Introduce el número de celdas cerradas: "))
    for _ in range(num_celdas_cerradas):
        x, y = map(int, input("Introduce la coordenada de la celda cerrada (x y): ").split())
        celdas_cerradas.append((x, y))

    # Obtener estado meta
    meta_x, meta_y = map(int, input("Introduce la coordenada del estado meta (x y): ").split())
    meta = (meta_x, meta_y)

    tablero = generar_tablero(filas, columnas, celdas_cerradas, meta)

    # Seleccionar aleatoriamente el estado inicial (una celda abierta)
    inicio = None
    while not inicio:
        x, y = random.randint(1, columnas), random.randint(1, filas)
        if not tablero[y-1][x-1].cerrada:
            inicio = tablero[y-1][x-1]

    # Imprimir el tablero inicial
    print("Tablero inicial con pesos:")
    imprimir_tablero(tablero, meta)

    # Ejecutar A*
    camino = a_estrella(tablero, inicio, meta, filas, columnas)

    if camino:
        print("Camino más corto encontrado:", camino)
        # Imprimir el estado final del tablero
        print("Estado final del tablero:")
        imprimir_tablero(tablero, meta, camino)
    else:
        print("No se encontró un camino al objetivo.")

if __name__ == "__main__":
    main()
