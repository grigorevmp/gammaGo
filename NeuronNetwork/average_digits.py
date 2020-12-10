import numpy as np
from NeuronNetwork.load_mnist import load_data
from NeuronNetwork.layers import sigmoid_double
from matplotlib import pyplot as plt


def average_digit(data, digit):
    """
    filter data
    :param data:
    :param digit:
    :return:
    """
    filtered_data = [x[0] for x in data if np.argmax(x[1]) == digit]
    filtered_array = np.asarray(filtered_data)
    return np.average(filtered_array, axis=0)


def predict(x, W, b):
    """
    Predict function
    :param x:
    :param W:
    :param b:
    :return:
    """
    return sigmoid_double(np.dot(W, x) + b)


def evaluate(data, digit, threshold, W, b):
    """
    Evaluate quality of prediction
    :param data:
    :param digit:
    :param threshold:
    :param W:
    :param b:
    :return:
    """
    total_samples = 1.0 * len(data)
    correct_predictions = 0
    for x in data:
        if predict(x[0], W, b) > threshold and np.argmax(x[1]) == digit:  # <2>
            correct_predictions += 1
        if predict(x[0], W, b) <= threshold and np.argmax(x[1]) != digit:  # <3>
            correct_predictions += 1
    return correct_predictions / total_samples


train, test = load_data()
avg_eight = average_digit(train, 8)


img = (np.reshape(avg_eight, (28, 28)))
plt.imshow(img)
plt.show()


x_3 = train[2][0]
x_18 = train[17][0]

W = np.transpose(avg_eight)
np.dot(W, x_3)

b = -45

print(predict(x_3, W, b))
print(predict(x_18, W, b))


evaluate(data=train, digit=8, threshold=0.5, W=W, b=b)

evaluate(data=test, digit=8, threshold=0.5, W=W, b=b)

eight_test = [x for x in test if np.argmax(x[1]) == 8]
evaluate(data=eight_test, digit=8, threshold=0.5, W=W, b=b)