import six.moves.cPickle as pickle
import gzip
import numpy as np


def encode_label(j):
    """
    encode labels
    :param j:
    :return:
    """
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e


def shape_data(data):
    """
    return shaped data
    :param data:
    :return:
    """
    features = [np.reshape(x, (784, 1)) for x in data[0]]
    labels = [encode_label(y) for y in data[1]]
    return list(zip(features, labels))


def load_data():
    """
    load data
    :return:
    """
    with gzip.open('mnist.pkl.gz', 'rb') as f:
        train_data, validation_data, test_data = pickle.load(f, encoding='bytes')

    return shape_data(train_data), shape_data(test_data)
