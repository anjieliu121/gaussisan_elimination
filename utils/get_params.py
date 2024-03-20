import json
import numpy as np
from scipy.linalg import solve
from numpy.linalg import cond

from utils.constants import *
from utils.helpers import *


def get_n(k):
    assert 1 <= k <= 20
    n = 2**(k+1)
    return n


def get_x(k):
    n = get_n(k)
    x = np.linspace(0, L, n+1)
    return x


def get_w(k):
    x = get_x(k)
    w = c1 * e ** (a * x) + c2 * e ** (-a * x) + b * x * (x - L) + c
    return w


def get_A(k):
    n = get_n(k)
    h = L / n
    d = 2 + h ** 2 * Q
    n = n - 1
    A = tridiagonal_matrix(n, -1, d, -1)
    return A


def get_b(k):
    n = get_n(k)
    h = L / n
    n = n - 1
    x = np.linspace(h, L - h, n)
    b = -h * h * r(x)
    return b


def get_y(k):
    A = get_A(k)
    b = get_b(k)
    y = solve(A, b)
    return y





def get_h(k):
    n = get_n(k)
    h = L / n
    return h


def get_H():  # vector of h's
    H = []
    for k in range(1, 13):
        h = get_h(k)
        H.append(h)
    return H


# same functions in main.py to avoid circular import
def get_error(k):
    w = get_w(k)
    y = get_y(k)
    y = pad(y)
    error = abs(w - y)
    return error


def get_error_middle(k):
    with open("simulated_data/errors.json", "r+") as f2:
        data = json.load(f2)
    error = data[str(k)]["error"]
    middle = error[len(error) // 2]  # all len(error) are odd numbers
    return middle


def get_condition_number(k):
    A = get_A(k)
    c = cond(A, np.inf)
    return c

