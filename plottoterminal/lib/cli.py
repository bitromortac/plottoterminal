from typing import TextIO
from plottoterminal.lib import figure


def plot_file(file: TextIO):
    """
    Plots a file of xy format.
    :param file: file name
    """
    x_data = []
    y_data = []
    for l in file.readlines():
        data = list(map(float, l.split()))
        if len(data) != 2:
            raise ValueError("File must contain only two columns.")

        x_data.append(data[0])
        y_data.append(data[1])

    # create figure
    f = figure.Figure()

    # plot data
    f.scatter(x_data, y_data)
    f.show()
