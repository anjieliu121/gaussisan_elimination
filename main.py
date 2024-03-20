from utils.constants import *
from utils.plot_utils import *
from utils.get_params import *
from utils.helpers import *
from utils.simulation import *
from plots import *

import pprint
from scipy.linalg import lu, solve
from numpy.linalg import cond


########################################################################################################################
#                                           set up A and b                                                             #
########################################################################################################################
def setup(k):
    n = get_n(k)
    h = L / n
    Q = S / (E * I)
    d = 2 + h ** 2 * Q
    n = n - 1
    A = tridiagonal_matrix(n, -1, d, -1)

    R = q / (2 * E * I)
    r = lambda x: R * x * (x - L)
    x = np.linspace(h, L-h, n)
    b = -h * h * r(x)
    return A, b


########################################################################################################################
#                                           calculate true solution                                                    #
########################################################################################################################
def true_solution(k):
    x = get_x(k)
    w = c1 * e**(a*x) + c2 * e**(-a*x) + b * x * (x-L) + c
    return w


########################################################################################################################
#                                           calculate estimate solution                                                #
########################################################################################################################

def forward_substitution(A, b):
    n = len(b)
    x = np.zeros(n)

    for i in range(n):
        x[i] = (b[i] - np.dot(A[i, :i], x[:i])) / A[i, i]

    return x


def backward_substitution(A, b):
    n = len(b)
    x = np.zeros(n)

    for i in range(n - 1, -1, -1):
        x[i] = b[i] / A[i, i]
        for j in range(i - 1, -1, -1):
            b[j] -= A[j, i] * x[i]
    return x


def guassian_elimination(k):
    # goal: solve Ay = b for y
    A, b = setup(k)
    # factorization: PA = LU
    P, _L, U = lu(A)  # _L: to avoid confusion with the global variable
    # forward substitution: solve Lc = Pb for c
    Pb = P @ b
    c = forward_substitution(_L, Pb)
    # backward substitution: solve Uy = c for y
    y = backward_substitution(U, c)
    return y


########################################################################################################################
#                                           errors                                                                     #
########################################################################################################################
def get_error(k):
    w = true_solution(k)
    y = guassian_elimination(k)
    y = pad(y)
    error = abs(w - y)
    return error


########################################################################################################################
#                                           errors at the middle of the beam                                           #
########################################################################################################################
def get_error_middle(k):
    with open("simulated_data/errors.json", "r+") as f2:
        data = json.load(f2)
    error = data[str(k)]["error"]
    middle = error[len(error) // 2]  # all len(error) are odd numbers
    return middle


########################################################################################################################
#                                           condition number of matrix A                                               #
########################################################################################################################
def get_condition_number(k):
    A = get_A(k)
    c = cond(A, np.inf)
    return c


def plot_KN(mode="show"):
    with open("simulated_data/numbers.json", "r+") as f:
        data = json.load(f)
    KN = data["condition_numbers"]
    KN_log10 = np.log10(KN)
    H_log10 = np.log10(get_H())
    slopes = plot_calculate_slopes(H_log10, KN_log10)
    # create figure
    fig, ax = plt.subplots()
    ax.plot(H_log10, KN_log10, marker='o', color='indianred')
    title = f"KN = O(h^-2)"
    plot_layout(ax, title, 'log(h=length of the segment)', 'log(KN=condition number of matrix A)')
    # show/save the figure
    plot_mode(fig, mode, title)
    return slopes


def main():
    # plot True vs. Approx Solutions for k = 1 and 2
    plot_true_approx_solutions_allK([1, 2], mode="pass")
    # simulate errors
    save_errors()
    # plot Errors for each k
    plot_errors_separate(mode="pass", max_subplots_per_figure=6, max_columns=2)
    # plot Errors in one plot
    plot_errors_overlay(mode="pass")
    # simulate errors at the middle of the beams
    errors_middle = save_E()
    pp = pprint.PrettyPrinter(width=38, compact=True)
    print("Error at the middle of the beam for each k:")
    pp.pprint(errors_middle)
    # plot Errors at the middle of the beams
    slopes_errors_middle = plot_E(mode="pass")
    print("Slope at each point:")
    pp.pprint(slopes_errors_middle)
    # simulate condition number of matrix A
    KN = save_KN()
    print("Condition number of matrix A for each k:")
    pp.pprint(KN)
    # plot Condition Numbers
    slopes_KN = plot_KN(mode="pass")
    print("Slope at each point:")
    pp.pprint(slopes_KN)

if __name__ == '__main__':
    main()
