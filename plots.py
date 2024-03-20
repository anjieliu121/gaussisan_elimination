from math import ceil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json


from utils.plot_utils import plot_true_approx_solutions_oneK, plot_error
from utils.helpers import plot_trim_empty_subplot, plot_mode, plot_split_subplots, plot_layout, plot_calculate_slopes
from utils.get_params import get_x, get_w, get_y, get_H
from utils.constants import k_start, k_end

########################################################################################################################
#                                           plot true vs approximate solutions                                         #
########################################################################################################################
def plot_true_approx_solutions_allK(ks, mode="show"):
    """
    Plot a (n x 2) figure where each subplot represents one k
    :param ks: a list of k's
    :param mode:
     - "show" (default) display the plot
     - "save" save the plot to "images" folder
    :return: None
    """
    # creates the figure
    num_subplots = len(ks)
    rows = ceil(num_subplots / 2)
    fig, axes = plt.subplots(rows, 2, figsize=(20, 8*rows))
    plot_trim_empty_subplot(num_subplots, fig, axes)
    # plot each subplot for the corresponding k
    for ax, k in zip(axes.flat, ks):
        x = get_x(k)
        w = get_w(k)
        y = get_y(k)
        plot_true_approx_solutions_oneK(k, x, w, y, mode="pass", ax_given=ax)
    # show/save the figure
    title = f'True vs. Approximate Solutions for k={ks}.png'
    plot_mode(fig, mode, title)


########################################################################################################################
#                                           plot errors                                                                #
########################################################################################################################
def plot_errors_separate(mode="show", max_subplots_per_figure = 6, max_columns = 2):
    """
    Plot several figures with max size of (3x2) subplots
    :param mode:
    - "show" (default) display all figures
    - "save" save all figures to "images" folder
    :return: None
    """
    # read errors data
    with open("simulated_data/errors.json", "r+") as f:
        data = json.load(f)
    total_subplots = len(data.keys())
    figures = plot_split_subplots(total_subplots, max_subplots_per_figure)
    colors = cm.copper(np.linspace(0, 1, total_subplots))
    # plot each figure
    for ks in figures:
        num_subplots = len(ks)
        num_rows = ceil(num_subplots / max_columns)
        fig, axes = plt.subplots(num_rows, max_columns, figsize=(10*max_columns, 8*num_rows))
        plot_trim_empty_subplot(num_subplots, fig, axes)
        # plot each subplot
        for ax, k in zip(axes.flat, ks):
            d = data[str(k)]
            c = colors[k-1]
            plot_error(k, d, c=c, mode="pass", ax_given=ax)
        # show/save the figure
        title = f'Errors in Solutions for k={ks}.png'
        plot_mode(fig, mode, title)


def plot_errors_overlay(mode="show"):
    # load data
    with open("simulated_data/errors.json", "r+") as f:
        data = json.load(f)
    total_subplots = len(data.keys())
    colors = cm.copper(np.linspace(0, 1, total_subplots))
    # create figure
    fig, ax = plt.subplots()
    for k, c in zip(data.keys(), colors):
        d = data[k]
        # plot each k in the same subplot
        ax.scatter(x=d["x"], y=d["error"], label=f"k={k}", s=15, color=c)
    ax.set_yscale('log')
    ax.legend(loc='upper right')
    title = f"Errors in Solutions for k={k_start},...,{k_end}"
    plot_layout(ax, title, 'x', 'absolute error')
    # show/save the figure
    plot_mode(fig, mode, title)


########################################################################################################################
#                                           plot errors at the middle of the beam                                      #
########################################################################################################################
def plot_E(mode="show"):
    # load data
    with open("simulated_data/numbers.json", "r+") as f:
        data = json.load(f)
    errors_middle = data["errors_middle"]
    errors_middle_log10 = np.log10(errors_middle)
    H_log10 = np.log10(get_H())
    slopes = plot_calculate_slopes(H_log10, errors_middle_log10)
    # create figure
    fig, ax = plt.subplots()
    ax.plot(H_log10, errors_middle_log10, marker='o', color='indianred')
    title = f"E = O(h^2)"
    plot_layout(ax, title, 'log(h=length of the segment)', 'log(E=error at the middle of the beam)')
    # show/save the figure
    plot_mode(fig, mode, title)
    return slopes
