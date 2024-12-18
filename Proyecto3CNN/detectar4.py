import pickle
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def load_data():
    # Cargar datos desde el archivo pickle
    with open('data.pickle', 'rb') as pick:
        data = pickle.load(pick)

    np.random.shuffle(data)

    feature = []
    labels = []

    for img, label in data:
        feature.append(img)
        labels.append(label)

    feature = np.array(feature, dtype=np.float32)
    labels = np.array(labels)

    feature = feature / 255.0  # Normalización

    return [feature, labels]

(feature, labels) = load_data()

# Dividir los datos en entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(feature, labels, test_size=0.1)

categories = ['Autobus', 'Ford F-150', 'Honda Accord', 'Tesla Cybertruck', 'Volkswagen Beetle']

# Cargar el modelo entrenado
model = tf.keras.models.load_model('mymodel.h5')

# Realizar predicciones en el conjunto de prueba
predictions = model.predict(x_test)
predicted_classes = np.argmax(predictions, axis=1)

# Generar el informe de clasificación
nClasses = len(categories)
target_names = ["Class {}".format(i) for i in range(nClasses)]

print(classification_report(y_test, predicted_classes, target_names=target_names))

# Intentar cargar y graficar el historial
try:
    with open('history.pkl', 'rb') as f:
        history = pickle.load(f)

    print("Contenido del historial:", history.keys())  # Verificar claves disponibles

    # Extraer métricas
    accuracy = history['accuracy']
    val_accuracy = history['val_accuracy']
    loss = history['loss']
    val_loss = history['val_loss']
    epochs = range(len(accuracy))

    # Graficar precisión
    plt.figure()
    plt.plot(epochs, accuracy, 'bo', label='Training accuracy')
    plt.plot(epochs, val_accuracy, 'b-', label='Validation accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()

    # Graficar pérdida
    plt.figure()
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b-', label='Validation loss')
    plt.title('Training and Validation Loss')
    plt.legend()

    plt.show()

except (FileNotFoundError, KeyError):
    print("El historial no está disponible o no contiene datos suficientes para graficar.")

# Mostrar algunas predicciones con etiquetas reales y predichas
plt.figure(figsize=(9, 9))
for i in range(9):
    plt.subplot(3, 3, i + 1)
    plt.imshow(x_test[i])
    plt.xlabel('Actual:' + categories[y_test[i]] + '\n' + 'Predicted:' + categories[predicted_classes[i]])
    plt.xticks([])
plt.show()
