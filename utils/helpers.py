import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags


def tridiagonal_matrix(n, lower, main, upper):
    A = diags([lower, main, upper], [-1, 0, 1], shape=(n, n)).toarray()
    return A


def pad(y):
    y = np.pad(y, (1, 1), mode='constant', constant_values=0)
    return y


def plot_initiate(ax=None):
    if ax is None:
        fig, ax = plt.subplots()
        return fig, ax
    else:
        return None, ax


def plot_mode(fig, mode, title="", ax=None):
    if ax is not None:
        return ax
    if mode == "show":
        fig.show()
    elif mode == "save":
        fig.savefig(f'images/{title}.png', bbox_inches='tight')
    elif mode == "pass":
        pass
    elif mode == "both":
        temp = fig
        temp.show()
        fig.savefig(f'images/{title}.png', bbox_inches='tight')


def plot_split_subplots(n, max_per_figure):
    result = []
    sublist = []

    for i in range(1, n + 1):
        sublist.append(i)
        if len(sublist) == max_per_figure:
            result.append(sublist)
            sublist = []

    # Append the remaining elements if any
    if sublist:
        result.append(sublist)

    return result


def plot_trim_empty_subplot(num_subplots, fig, axes):
    if num_subplots % 2 == 1:
        fig.delaxes(axes[-1, -1])
    return fig, axes


def plot_layout(ax, title, x, y):
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(x, fontweight='bold')
    ax.set_ylabel(y, fontweight='bold')
    ax.grid(which='major', axis='both', linestyle='--')
    ax.tick_params(which='both', direction="in")
    return ax


def plot_calculate_slopes(x, y):
    i = np.argsort(x)
    x = x[i]
    y = y[i]
    dy = y[2:] - y[1:-1]
    dx = x[2:] - x[1:-1]
    slopes = dy / dx
    return slopes