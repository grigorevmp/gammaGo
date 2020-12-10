from __future__ import print_function
import numpy as np


def sigmoid_double(x):
    return 1.0 / (1.0 + np.exp(-x))


def sigmoid(z):
    return np.vectorize(sigmoid_double)(z)


def sigmoid_prime_double(x):
    return sigmoid_double(x) * (1 - sigmoid_double(x))


def sigmoid_prime(z):
    return np.vectorize(sigmoid_prime_double)(z)


class Layer:
    def __init__(self):
        self.params = []

        self.previous = None
        self.next = None

        self.input_data = None
        self.output_data = None

        self.input_delta = None
        self.output_delta = None

    def connect(self, layer):
        self.previous = layer
        layer.next = self

    def forward(self):
        raise NotImplementedError

    def get_forward_input(self):
        if self.previous is not None:
            return self.previous.output_data
        else:
            return self.input_data

    def backward(self):  # <3>
        raise NotImplementedError

    def get_backward_input(self):  # <4>
        if self.next is not None:
            return self.next.output_delta
        else:
            return self.input_delta

    def clear_deltas(self):  # <5>
        pass

    def update_params(self, learning_rate):  # <6>
        pass

    def describe(self):
        raise NotImplementedError


class ActivationLayer(Layer):
    def __init__(self, input_dim):
        super(ActivationLayer, self).__init__()

        self.input_dim = input_dim
        self.output_dim = input_dim

    def forward(self):
        data = self.get_forward_input()
        self.output_data = sigmoid(data)

    def backward(self):
        delta = self.get_backward_input()
        data = self.get_forward_input()
        self.output_delta = delta * sigmoid_prime(data)

    def describe(self):
        print("|-- " + self.__class__.__name__)
        print("  |-- dimensions: ({},{})"
              .format(self.input_dim, self.output_dim))


class DenseLayer(Layer):

    def __init__(self, input_dim, output_dim):
        super(DenseLayer, self).__init__()

        self.input_dim = input_dim
        self.output_dim = output_dim

        self.weight = np.random.randn(output_dim, input_dim)  # <2>
        self.bias = np.random.randn(output_dim, 1)

        self.params = [self.weight, self.bias]  # <3>

        self.delta_w = np.zeros(self.weight.shape)  # <4>
        self.delta_b = np.zeros(self.bias.shape)

    def forward(self):
        data = self.get_forward_input()
        self.output_data = np.dot(self.weight, data) + self.bias  # <1>

    def backward(self):
        data = self.get_forward_input()
        delta = self.get_backward_input()  # <1>

        self.delta_b += delta  # <2>

        self.delta_w += np.dot(delta, data.transpose())  # <3>

        self.output_delta = np.dot(self.weight.transpose(), delta)  # <4>

    def update_params(self, rate):  # <1>
        self.weight -= rate * self.delta_w
        self.bias -= rate * self.delta_b

    def clear_deltas(self):  # <2>
        self.delta_w = np.zeros(self.weight.shape)
        self.delta_b = np.zeros(self.bias.shape)

    def describe(self):  # <3>
        print("|--- " + self.__class__.__name__)
        print("  |-- dimensions: ({},{})"
              .format(self.input_dim, self.output_dim))
