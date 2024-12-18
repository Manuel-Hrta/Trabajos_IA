import tensorflow as tf
import pickle
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from collections import Counter
from tensorflow.keras.layers import Conv2D, LeakyReLU, MaxPooling2D, Dropout, Flatten, Dense, Input
from tensorflow.keras.models import Model

def load_data_from_pickle():
    # Cargar datos del archivo pickle
    with open('data.pickle', 'rb') as pick:
        data = pickle.load(pick)

    features, labels = [], []
    for img, label in data:
        features.append(img)
        labels.append(label)

    features = np.array(features, dtype=np.float32) / 255.0  # Normalizar
    labels = np.array(labels, dtype=np.int32)

    return features, labels

# Cargar datos
features, labels = load_data_from_pickle()
print(f"Total imágenes cargadas: {len(features)}")
print(f"Distribución total de las clases: {Counter(labels)}")

# División de datos usando StratifiedShuffleSplit
sss = StratifiedShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
for train_index, test_index in sss.split(features, labels):
    x_train, x_test = features[train_index], features[test_index]
    y_train, y_test = labels[train_index], labels[test_index]

print(f"Distribución en entrenamiento: {Counter(y_train)}")
print(f"Distribución en prueba: {Counter(y_test)}")

# Crear un conjunto de datos tf.data
train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(1000).batch(32).prefetch(tf.data.AUTOTUNE)
test_dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32).prefetch(tf.data.AUTOTUNE)

# Número de clases
nClasses = len(np.unique(labels))

# Definir la arquitectura del modelo
input_layer = Input(shape=(80, 80, 3))

conv1 = Conv2D(32, kernel_size=(3, 3), activation='linear', padding='same')(input_layer)
act1 = LeakyReLU(alpha=0.1)(conv1)
pool1 = MaxPooling2D((2, 2), padding='same')(act1)
drop1 = Dropout(0.5)(pool1)

flt1 = Flatten()(drop1)
dense1 = Dense(32, activation='linear')(flt1)
act2 = LeakyReLU(alpha=0.1)(dense1)
drop2 = Dropout(0.5)(act2)

out = Dense(nClasses, activation='softmax')(drop2)

# Crear y compilar el modelo
model = Model(inputs=input_layer, outputs=out)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Resumen del modelo
model.summary()

# Entrenar el modelo
history = model.fit(
    train_dataset,
    validation_data=test_dataset,
    epochs=10
)

# Guardar el modelo y el historial
model.save('mymodel.h5')
with open('history.pkl', 'wb') as f:
    pickle.dump(history.history, f)

print("Modelo y historial guardados con éxito.")
