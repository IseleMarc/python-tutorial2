"""This module helps with plotting."""

def lines(ax, x, y, color, label=None):
    ax.plot(x, y, color=color, label=label)

def points(ax, x, y, color, label=None, s=300, marker='x'):
    ax.scatter(x, y, c=color, label=label, s=s, marker=marker)

def vlines(ax, x, y, color, label=None, origin=0):
    ax.vlines(x, origin, y, colors=color)


exe_func = {
    'lines': lines,
    'points': points,
    'vlines': vlines
}

colorcycle = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']


def plot_any(vals, plotcase='lines', labels=None, title='', x_label='', y_label='',
             xlims=None, ylims=None, show=True, save=False, grid=False, savename='plot.png',
             linewidth=5, formatfuncx=None, formatfuncy=None, invert=[], **kwargs):
    """Plot a dataset as line(s), points or vertical lines.
    Args:
        vals (list of lists of lists): A list of lists of lists, where every 2nd
            order list contains two lists of x and y values each.
            E.g.: [[[1, 2, 3], [1, 2, 3]], [[1, 2, 3], [3, 2, 1]]]
        plotcase (str): Implementation of how to represent the data. Can be
            either 'lines', 'points' or 'vlines'.
        labels (list): A list of strings where every string corresponds to a
            2nd order list above.
        title (str): Title of plot.
        x_label (str): Label of the x-axis.
        y_label (str): Label of the y-axis.
        xlims (list of int or float): List with two values, the first being
            the lower and the second being the upper limit of the x-axis.
        ylims (list of int or float): List with two values, the first being
            the lower and the second being the upper limit of the y-axis.
        show (bool): Show the plot immediately.
        save (bool): Save the plot to savename.
        grid (bool): Show a grid.
        savename (str): The savename if save is True.
        linewidth (int): The width of the lines, points or vlines.
        formatfuncx (function): A function that formats the values of the x-axis.
        formatfuncy (function): A function that formats the values of the y-axis.
        invert (str, list of strings or tuple of strings): If any of the axes
            should be inverted. Possible: 'x' or 'y' (or both in list or tuple).
        kwargs: can be used for points(s:size, marker:markershape),
                for vlines(origin:list or integer -> origin of the lines)
    """
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from matplotlib.ticker import FuncFormatter

    fontsize = 30
    label_fontsize = 25
    label_linewidth = 2.5

    mpl.rcParams['lines.linewidth'] = linewidth
    mpl.rcParams['font.size'] = fontsize

    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(24, 18))

    # Plot all lines.
    if labels:
        for index, values in enumerate(vals):
            exe_func[plotcase](ax, values[0], values[1],
                               color=colorcycle[index % len(colorcycle)],
                               label=labels[index], **kwargs)
    else:
        for index, values in enumerate(vals):
            exe_func[plotcase](ax, values[0], values[1],
                               color=colorcycle[index % len(colorcycle)], **kwargs)

    # Set axis etc.
    if xlims:
        ax.set(xlim=xlims)
    if ylims:
        ax.set(ylim=ylims)
    ax.set(xlabel=x_label, ylabel=y_label, title=title)

    # Add distance between tick labels and graph.
    ax.tick_params(axis='x', which='major', pad=7)
    ax.grid(grid)

    # Set legend
    if labels:
        leg = ax.legend(fontsize=label_fontsize, loc='upper left', bbox_to_anchor=(1, 1),
                        borderaxespad=0.1, frameon=False)
        # Set linewidth in legend.
        for legobj in leg.legendHandles:
            legobj.set_linewidth(label_linewidth)

    # Invert the axes.
    for axis in invert:
        if axis == 'x':
            plt.gca().invert_xaxis()
        elif axis == 'y':
            plt.gca().invert_yaxis()

    # Format the Tics on the axis.
    if formatfuncx:
        formatterx = FuncFormatter(formatfuncx)
        ax.xaxis.set_major_formatter(formatterx)
    if formatfuncy:
        formattery = FuncFormatter(formatfuncy)
        ax.yaxis.set_major_formatter(formattery)

    # Save.
    if save:
        plt.savefig(savename, bbox_inches='tight')

    # Show graph or not.
    if not show:
        plt.close(fig)

    return


def ps_time(x_val, pos):
    """Format picoseconds to larger time units."""
    if x_val == 0:
        t_val = '{:1.0f}'.format(x_val)
    elif x_val >= 1e6:
        t_val = '{:1.0f} µs'.format(x_val * 1e-6)
    elif x_val >= 1e3:
        t_val = '{:1.0f} ns'.format(x_val * 1e-3)
    else:
        t_val = '{:1.0f} ps'.format(x_val)
    return t_val

