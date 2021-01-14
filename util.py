import numpy as np


def random_zero_to_max(max_value):
    return max_value*np.random.rand()


def average(list):
    avg = 0
    for item in list:
        avg += item
    return avg/len(list)
