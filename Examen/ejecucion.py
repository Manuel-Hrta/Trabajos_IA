import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

# Generar datos artificales
np.random.seed(0)
n_samples_per_class = 333 
n_samples = n_samples_per_class * 3

# Inicializar datos
X = np.zeros((n_samples, 3))
y = np.zeros((n_samples, 3))

# Riesgo Bajo (1, 0, 0): historial >= 0.7, ingresos >= 0.7, relación <= 0.4
for i in range(n_samples_per_class):
    X[i] = [np.random.uniform(0.7, 1.0), np.random.uniform(0.7, 1.0), np.random.uniform(0.0, 0.4)]
    y[i] = [1, 0, 0]

# Riesgo Medio (0, 1, 0): historial entre 0.5 y 0.7, ingresos entre 0.5 y 0.7, relación entre 0.4 y 0.6
for i in range(n_samples_per_class, 2 * n_samples_per_class):
    X[i] = [np.random.uniform(0.5, 0.7), np.random.uniform(0.5, 0.7), np.random.uniform(0.4, 0.6)]
    y[i] = [0, 1, 0]

# Riesgo Alto (0, 0, 1): historial <= 0.5, ingresos <= 0.5, relación >= 0.6
for i in range(2 * n_samples_per_class, 3 * n_samples_per_class):
    X[i] = [np.random.uniform(0.0, 0.5), np.random.uniform(0.0, 0.5), np.random.uniform(0.6, 1.0)]
    y[i] = [0, 0, 1]

#dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#crear el modelo de red neuronal multicapa
model = Sequential([
    Dense(12, input_dim=3, activation='relu'), 
    Dense(6, activation='relu'),           
    Dense(3, activation='softmax')            
])


#compilar el modelo
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

#entrenar el modelo
model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)

#evaluar el modelo en el conjuntode prueba
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nPrecisión en el conjunto de prueba: {accuracy:.2f}")

# datos tabla del ejercicio
nuevos_datos = np.array([
    [0.9, 0.8, 0.2],  # Bajo
    [0.7, 0.6, 0.5],  # Medio
    [0.4, 0.4, 0.8],  # Alto
    [0.8, 0.9, 0.3],  # Bajo
    [0.5, 0.7, 0.6],  # Medio
    [0.3, 0.5, 0.9]   # Alto
])

# imprimir a que corresponde de acuerdo al numero de clases que genera la red
clases = {0: "Riesgo Bajo", 1: "Riesgo Medio", 2: "Riesgo Alto"}

# Predicciones
predicciones = model.predict(nuevos_datos)
for i, prediccion in enumerate(predicciones):
    clase = np.argmax(prediccion)  
    nombre_clase = clases[clase]  
    print(f"Dato {i + 1}: {nuevos_datos[i]} => Predicción: {prediccion} => Clase: {nombre_clase}")

