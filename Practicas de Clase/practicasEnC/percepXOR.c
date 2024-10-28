#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define EPOCHS 3000
#define LEARNING_RATE 0.1f

float sigmoid(float x) {
    return 1 / (1 + exp(-x));
}

float sigmoid_derivative(float x) {
    return x * (1 - x);
}

// Definición de la estructura de una neurona
typedef struct {
    float weights[2];
    float bias;
} Neuron;

// Inicialización de pesos y bias aleatorios para una neurona
void initialize_neuron(Neuron *neuron) {
    neuron->weights[0] = (float)rand() / RAND_MAX;
    neuron->weights[1] = (float)rand() / RAND_MAX;
    neuron->bias = (float)rand() / RAND_MAX;
}

// Calcular la salida de una neurona
float neuron_output(Neuron *neuron, float x0, float x1) {
    float net_input = neuron->weights[0] * x0 + neuron->weights[1] * x1 + neuron->bias;
    return sigmoid(net_input);
}

// Ajustar los pesos y el bias de la neurona
void train_neuron(Neuron *neuron, float x0, float x1, float error, float learning_rate) {
    neuron->weights[0] += learning_rate * error * x0;
    neuron->weights[1] += learning_rate * error * x1;
    neuron->bias += learning_rate * error;
}

int main() {
    // Inicializar neuronas de la capa oculta y la capa de salida
    Neuron hidden_layer[2];
    Neuron output_neuron;
    initialize_neuron(&hidden_layer[0]);
    initialize_neuron(&hidden_layer[1]);
    initialize_neuron(&output_neuron);

    // Datos de entrenamiento para la función XOR
    float inputs[4][2] = {{1, 1}, {1, 0}, {0, 1}, {0, 0}};
    float targets[4] = {0, 1, 1, 0};

    for (int epoch = 0; epoch < EPOCHS; epoch++) {
        float total_error = 0;

        for (int i = 0; i < 4; i++) {
            // Paso de forward
            float h1_output = neuron_output(&hidden_layer[0], inputs[i][0], inputs[i][1]);
            float h2_output = neuron_output(&hidden_layer[1], inputs[i][0], inputs[i][1]);
            float output = neuron_output(&output_neuron, h1_output, h2_output);

            // Calcular el error de la salida
            float output_error = targets[i] - output;
            total_error += output_error * output_error;

            // Paso de backward - retropropagación
            float output_delta = output_error * sigmoid_derivative(output);

            float h1_error = output_delta * output_neuron.weights[0];
            float h2_error = output_delta * output_neuron.weights[1];

            float h1_delta = h1_error * sigmoid_derivative(h1_output);
            float h2_delta = h2_error * sigmoid_derivative(h2_output);

            // Actualizar pesos de la capa de salida
            train_neuron(&output_neuron, h1_output, h2_output, output_delta, LEARNING_RATE);

            // Actualizar pesos de la capa oculta
            train_neuron(&hidden_layer[0], inputs[i][0], inputs[i][1], h1_delta, LEARNING_RATE);
            train_neuron(&hidden_layer[1], inputs[i][0], inputs[i][1], h2_delta, LEARNING_RATE);
        }

        if (epoch % 10000 == 0) {
            printf("Epoca %d, Error Total: %f\n", epoch, total_error);
        }
    }

    // Pruebas de la red neuronal entrenada
    printf("Resultados despues del entrenamiento:\n");
    for (int i = 0; i < 4; i++) {
        float h1_output = neuron_output(&hidden_layer[0], inputs[i][0], inputs[i][1]);
        float h2_output = neuron_output(&hidden_layer[1], inputs[i][0], inputs[i][1]);
        float output = neuron_output(&output_neuron, h1_output, h2_output);
        printf("Input: (%.0f, %.0f) -> Prediccion: %f (Esperado: %.0f)\n", inputs[i][0], inputs[i][1], output, targets[i]);
    }

    return 0;
}
