import numpy as np
from math import ceil
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from utils.helpers import *
from utils.get_params import get_x

########################################################################################################################
#                                           plot true vs approximate solutions                                         #
########################################################################################################################
# plot for 1 k
def plot_true_approx_solutions_oneK(k, x, w, y, mode="show", ax_given=None):
    y = pad(y)
    # w: true solution; y: approximated solution
    fig, ax = plot_initiate(ax_given)
    p1 = ax.scatter(x=x, y=w, color="indianred", label='true')
    p2 = ax.scatter(x=x, y=y, color="steelblue", label='approximate')
    ax.legend(handles=[p1, p2], loc='upper right')
    title = f"True vs. Approximate Solutions for k={k}"
    plot_layout(ax, title, 'x', 'deflection')
    plot_mode(fig, mode, title, ax_given)


########################################################################################################################
#                                           plot errors                                                                #
########################################################################################################################
def plot_error(k, d, c="indianred", mode="show", ax_given=None):
    fig, ax = plot_initiate(ax_given)
    ax.scatter(d["x"], d["error"], label=f"k={k}", color=c, s=60, alpha=1)
    ax.set_yscale('log')
    ax.legend(loc='upper right')
    title = f"Errors in Solutions for k={k}"
    plot_layout(ax, title, 'x', 'absolute error')
    plot_mode(fig, mode, title, ax_given)






