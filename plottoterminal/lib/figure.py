from typing import List, Tuple, Callable, Optional
from math import log10

from plottoterminal.lib.plots import BasePlot, Scatter
from plottoterminal.lib.graph import Graph

AXIS = [  # defines the axis characters
    '─',
    '┴',  # ┬
    '│',
    '├',  # ┤
    '└',
    'ᐃ',
    'ᐅ',
]
TIMES = '×'

CHARS_AXIS = 1  # width and height of the axes lines, usually one character

X_TICK_LABEL_HEIGHT = 1
X_TICK_LABEL_WIDTH = 4

Y_TICK_LABEL_HEIGHT = 1
Y_TICK_LABEL_WIDTH = 4

X_LABEL_HEIGHT = 1
Y_LABEL_WIDTH = 2

# LEFT_PAD is the width of the y axis plus labels
LEFT_PAD = Y_LABEL_WIDTH + Y_TICK_LABEL_WIDTH + CHARS_AXIS
# LOW_PAD is the height of the x axis plus labels
LOW_PAD = X_LABEL_HEIGHT + X_TICK_LABEL_HEIGHT + CHARS_AXIS

# precision of tick labels, numbers: +-PREF_DIGITS.POSTF_DIGITS, e.g., -1.00
X_TICK_LABEL_PREF_DIGITS = 1
X_TICK_LABEL_POST_DIGITS = X_TICK_LABEL_WIDTH - 2 - X_TICK_LABEL_PREF_DIGITS
Y_TICK_LABEL_PREF_DIGITS = 1
Y_TICK_LABEL_POST_DIGITS = Y_TICK_LABEL_WIDTH - 2 - Y_TICK_LABEL_PREF_DIGITS


class Figure(object):
    """
    Figure holds the main ingredients of a plot like the axis, axis labels,
    axis.
    """

    def __init__(self, figsize: Tuple[int, int] = (80, 22)):
        """
        :param figsize: in units of terminal characters, width, height
        """
        self.figsize = figsize
        # x_lim and y_lim give the minimal and maximal values to be plotted
        self.x_lim: Optional[Tuple[float, float]] = None
        self.y_lim: Optional[Tuple[float, float]] = None
        # graph width and height give the dimensions of the plotting area in
        # number of characters
        self._graph_width: Optional[int] = None
        self._graph_height: Optional[int] = None
        # x2bin and y2bin convert from the x/y values to column/row inside the
        # graph region
        self.x2bin: Optional[Callable[[float], int]] = None
        self.y2bin: Optional[Callable[[float], int]] = None
        # bin2x and bin2y convert from the column/row inside the graph region to
        # units to x/y values
        self.bin2x: Optional[Callable[[int], float]] = None
        self.bin2y: Optional[Callable[[int], float]] = None
        # scale exponents
        self.scale_exponent_x: Optional[int] = None
        self.scale_exponent_y: Optional[int] = None
        # axis units
        self.unit_x: Optional[str] = None
        self.unit_y: Optional[str] = None
        # axis labels
        self.x_label: str = ''
        self.y_label: str = ''
        # plots is where different plots are stored
        # TODO: make plot objects
        self.plots: List[BasePlot] = []
        # canvas holds all the characters for the figure
        # TODO: make canvas object
        self.canvas: List[List[str]] = self.init_canvas()

    def draw_horizontal(self, string: str, row: int, start: int, stop: int):
        """
        Draws a string from left to right.
        :param string: the string to be added
        :param row: the row of the string
        :param start: the starting point on the x axis
        :param stop: the stopping point on the x axis
        modifies:
        self.canvas
        """
        self.canvas[row][start:stop] = list(string)

    def draw_vertical(self, string: str, col: int, start: int, stop: int):
        """
        Draws from bottom to top.
        :param string: the string to be added
        :param col: the column of the string
        :param start: the starting point on the y axis
        :param stop: the stopping point on the y axis
        modifies:
        self.canvas
        """
        for ic, i in enumerate(range(start, stop)):
            self.canvas[i][col] = list(string)[::-1][ic]

    def set_x_label(self, label: str):
        """
        Puts the x label horizontally aligned below the x axis.
        :param label: the x label
        modifies:
        self.x_label
        """
        self.x_label = label

    def set_y_label(self, label):
        """
        Puts the y label horizontally aligned below the x axis.
        :param label: the y label
        modifies:
        self.y_label
        """
        self.y_label = label

    def init_canvas(self) -> List[List[str]]:
        """
        Initializes the canvas with white space.
        """
        return [
            [' ' for _ in range(self.figsize[0])]
            for _ in range(self.figsize[1])]

    def set_x_lim(self, buffer: float = 0.00):
        """
        Determines the x axis value delimiters by taking into account
        all the plots available.

        :param buffer: a buffer that is added to the min and max limits
        modifies: self.x_lim
        """

        x_min = float('inf')
        x_max = 0.0
        for p in self.plots:
            x_min_p = p.min_x()
            if x_min > x_min_p:
                x_min = x_min_p
            x_max_p = p.max_x()
            if x_max < x_max_p:
                x_max = x_max_p

        # add a buffer
        x_dist = x_max - x_min
        x_buffer = x_dist * buffer / 2
        self.x_lim = (x_min - x_buffer, x_max + x_buffer)

    def set_y_lim(self, buffer=0.00):
        """
        Determines the y axis value delimiters by taking into account
        all the plots available.

        :param buffer: a buffer that is added to the min and max limits
        modifies: self.y_lim
        """
        y_min = float('inf')
        y_max = 0
        for p in self.plots:
            y_min_p = p.min_y()
            if y_min > y_min_p:
                y_min = y_min_p
            y_max_p = p.max_y()
            if y_max < y_max_p:
                y_max = y_max_p

        # add a buffer
        y_dist = y_max - y_min
        y_buffer = y_dist * buffer / 2
        self.y_lim = (y_min - y_buffer, y_max + y_buffer)

    @property
    def graph_width(self) -> int:
        """
        Gives the width in characters of the graph area (without axis).
        :return: width in units of characters
        """
        if self._graph_width is not None:
            return self._graph_width
        else:
            graph_width: int = self.figsize[0]
            # account for y label
            graph_width -= Y_LABEL_WIDTH
            # account for y tick labels
            graph_width -= Y_TICK_LABEL_WIDTH
            # account for axis and ticks
            graph_width -= CHARS_AXIS
            self._graph_width = graph_width
            return self._graph_width

    @property
    def graph_height(self) -> int:
        """
        Gives the height in characters of the graph area (without axis).
        :return: height in units of characters
        """
        if self._graph_height is not None:
            return self._graph_height
        else:
            graph_height = self.figsize[1]
            # account for x label
            graph_height -= X_LABEL_HEIGHT
            # account for x tick labels
            graph_height -= X_TICK_LABEL_HEIGHT
            # account for axis and ticks
            graph_height -= CHARS_AXIS
            self._graph_height = graph_height
            return self._graph_height

    def get_x_tick_positions(self) -> List[int]:
        """
        Returns a list of x tick positions in character units of the graph.
        :return: list of tick positions
        """
        # solve diophantine equation
        # w = label_width * n + spacer * (n-1) + rest
        # there should be at least min_n ticks
        min_n = 4

        # there should be at least min_spacer spaces between each tick, but
        # only maximally max_spacer
        min_spacer = 1
        max_spacer = 8

        # number of rest spaces should be minimized, say it can be
        max_rest = int(0.10 * self.graph_width)

        # try all combinations and stop if conditions from above are met
        found = False
        n = 0
        spacer = min_spacer
        for n in range(min_n, 20):
            for spacer in range(min_spacer, max_spacer):
                rest = self.graph_width - (
                        X_TICK_LABEL_WIDTH * n + spacer * (n - 1))
                if (rest >= 0) and (rest <= max_rest):
                    found = True
                    break
            if found:
                break

        if not found:
            raise ValueError(
                "Could not determine good tick labels for x. "
                "Figsize too small in x direction?"
            )

        n_x_ticks = n
        labels = []
        for i in range(n_x_ticks):
            label_pos = i * (spacer + X_TICK_LABEL_WIDTH)
            labels.append(label_pos)

        return labels

    def get_y_tick_positions(self) -> List[int]:
        """
        Returns a list of x tick positions in character units of the graph.
        :return: list of tick positions
        """
        # solve diophantine equation
        # w = label_width * n + spacer * (n-1) + rest
        # there should be at least min_n ticks
        min_n = 3

        # there should be at least min_spacer spaces between each tick, but only
        # maximally max_spacer
        min_spacer = 1
        max_spacer = 4

        # number of rest spaces should be minimized
        max_rest = 1

        # try all combinations and stop if conditions from above are met
        found = False
        n = 0
        spacer = min_spacer
        for n in range(min_n, 20):
            for spacer in range(min_spacer, max_spacer):
                rest = self.graph_height - (
                        Y_TICK_LABEL_HEIGHT * n + spacer * (n - 1))
                if (rest >= 0) and (rest <= max_rest):
                    found = True
                    break
            if found:
                break

        if not found:
            raise ValueError(
                "Could not determine good tick labels for y. "
                "Figsize too small in y direction?"
            )

        n_y_ticks = n
        labels = []
        for i in range(n_y_ticks):
            label_pos = i * (spacer + Y_TICK_LABEL_HEIGHT)
            labels.append(label_pos)

        return labels

    def get_x_tick_labels(self) -> List[Tuple[int, float]]:
        """
        Gives a list of tick positions and the corresponding value it
        represents.
        :return: list of tick positions and labels
        """
        tick_positions = self.get_x_tick_positions()
        # bin2x must be initialized
        assert self.bin2x is not None
        return [(t, self.bin2x(t) / 10 ** self.scale_exponent_x) for t in
                tick_positions]

    def get_y_tick_labels(self) -> List[Tuple[int, float]]:
        """
        Gives a list of tick positions and the corresponding value it
        represents.
        :return: list of tick positions and labels
        """
        tick_positions = self.get_y_tick_positions()
        # bin2y must be initialized
        assert self.bin2y is not None
        return [(t, self.bin2y(t) / 10 ** self.scale_exponent_y) for t in
                tick_positions]

    def init_x_scale(self):
        """
        Initializes the scale for the x axis.
        modifies: self.bin2x and self.x2bin
        """
        label_positions = self.get_x_tick_positions()
        # min and max label positions should correspond to min and max x values:
        # need to solve for coefficients in linear equation x = m * x_b + t
        # first point is first label at position zero, x_b = 0
        t = self.x_lim[0]
        # second point is x_b_max = m * x_lim[1] + t
        # m = (x_b_max - t) / x_lim[1]
        m = (self.x_lim[1] - t) / label_positions[-1]

        self.bin2x = lambda x: m * x + t
        self.x2bin = lambda x_b: int(round((x_b - t) / m, 0))

        # determine scale factor
        interval_length = self.x_lim[1] - self.x_lim[0]
        interval_exponent = log10(interval_length)
        round_interval_exponent = int(interval_exponent)
        self.scale_exponent_x = round_interval_exponent

    def init_y_scale(self):
        """
        Initializes the scale for the x axis.
        modifies: self.bin2x and self.x2bin
        """
        label_positions = self.get_y_tick_positions()
        # min and max label positions should correspond to min and max x values
        # need to solve for coefficients in linear equation x = m * x_b + t
        # first point is first label at position zero, x_b = 0
        t = self.y_lim[0]
        # second point is x_b_max = m * x_lim[1] + t
        # m = (x_b_max - t) / x_lim[1]
        m = (self.y_lim[1] - t) / label_positions[-1]

        self.bin2y = lambda y: m * y + t
        self.y2bin = lambda y_b: int(round((y_b - t) / m, 0))

        # determine scale factor
        interval_length = self.y_lim[1] - self.y_lim[0]
        interval_exponent = log10(interval_length)
        round_interval_exponent = int(interval_exponent)
        self.scale_exponent_y = round_interval_exponent

    def draw_x_axis(self):
        """
        Draws the x axis including the solid line, tick positions, tick labels.
        modifies: self.canvas
        """
        # update the scale
        self.set_x_lim()
        self.init_x_scale()

        # draw labels
        x_tick_labels = self.get_x_tick_labels()
        x_b_start = Y_LABEL_WIDTH + Y_TICK_LABEL_WIDTH + CHARS_AXIS
        y_b = X_LABEL_HEIGHT
        for t in x_tick_labels:
            # format label with variable precision, left aligned
            label = '{:<{len}.{prec}f}'.format(
                t[1], len=X_TICK_LABEL_WIDTH, prec=X_TICK_LABEL_POST_DIGITS)
            self.canvas[y_b][
            x_b_start + t[0]:x_b_start + t[0] + X_TICK_LABEL_WIDTH] = label

        # draw x axis
        y_b = X_LABEL_HEIGHT + CHARS_AXIS
        for xb in range(self.graph_width):
            self.canvas[y_b][x_b_start + xb] = AXIS[0]

        # draw x ticks
        y_b = X_LABEL_HEIGHT + X_TICK_LABEL_HEIGHT
        for t in x_tick_labels:
            self.canvas[y_b][LEFT_PAD + t[0]] = AXIS[1]

    def draw_y_axis(self):
        """
        Draws the y axis including the solid line, tick positions, tick labels.
        modifies: self.canvas
        """
        # update the scale
        self.set_y_lim()
        self.init_y_scale()

        y_tick_labels = self.get_y_tick_labels()
        y_b_start = X_LABEL_HEIGHT + X_TICK_LABEL_HEIGHT + CHARS_AXIS
        x_b = Y_LABEL_WIDTH
        for t in y_tick_labels:
            # format label with variable precision, left aligned
            label = '{:>{disp}.{dosp}f}'.format(
                t[1], disp=Y_TICK_LABEL_WIDTH, dosp=Y_TICK_LABEL_POST_DIGITS)
            self.canvas[
                y_b_start + t[0]][x_b:x_b + Y_TICK_LABEL_WIDTH] = label

        # draw y axis
        x_b = Y_LABEL_WIDTH + Y_TICK_LABEL_WIDTH
        for yb in range(self.graph_height):
            self.canvas[y_b_start + yb][x_b] = AXIS[2]

        # draw y ticks
        x_b = Y_LABEL_WIDTH + Y_TICK_LABEL_WIDTH
        for t in y_tick_labels:
            self.canvas[LOW_PAD + t[0]][x_b] = AXIS[3]

    def decorate_axes(self):
        """
        Decorates the axes with the origin intersection and with arrows at the
        end of the axes.
        :modifies: self.canvas
        """
        # draw x axis arrow
        self.canvas[LOW_PAD + self.graph_height - 1][LEFT_PAD - 1] = AXIS[5]
        # draw y axis arrow
        self.canvas[LOW_PAD - 1][LEFT_PAD + self.graph_width - 1] = AXIS[6]
        # draw origin
        self.canvas[LOW_PAD - 1][LEFT_PAD - 1] = AXIS[4]

        # draw x scale exponent and unit
        scale_text_x = ''
        if self.scale_exponent_x != 0:
            scale_text_x += f"{TIMES}10^{self.scale_exponent_x}"
        if self.unit_x:
            scale_text_x += f" [{self.unit_x}]"
        if scale_text_x:
            self.canvas[0][-len(scale_text_x):] = scale_text_x

        # draw y scale exponent and unit
        y_tick_positions = self.get_y_tick_positions()
        y_position_scale = y_tick_positions[-1]
        if self.scale_exponent_y != 0:
            scale_exponent = f"{TIMES}10^{self.scale_exponent_y}"
            self.canvas[y_position_scale + LOW_PAD - 1][
                0:len(scale_exponent)] = scale_exponent
        if self.unit_y:
            unit = f"[{self.unit_y}]"
            self.canvas[y_position_scale + LOW_PAD - 2][
                0:len(unit)] = unit

        # draw x label
        len_label = len(self.x_label)
        center = LEFT_PAD + (self.figsize[0] - LEFT_PAD) // 2
        odd = len_label % 2
        self.draw_horizontal(
            self.x_label, 0, center - len_label // 2,
            center + len_label // 2 + odd
        )

        # draw y label
        len_label = len(self.y_label)
        center = LOW_PAD + (self.figsize[1] - LOW_PAD) // 2
        odd = len_label % 2
        # set label
        self.draw_vertical(
            self.y_label, 0, center - len_label // 2,
            center + len_label // 2 + odd
        )

    def draw_canvas(self) -> str:
        """
        Draws the canvas as a string with newlines, ready to be put out to
        the terminal.
        :return: the figure in form of a string
        """
        figure = ''
        for line in self.canvas[::-1]:
            figure += ''.join(line)
            figure += '\n'
        return figure

    def scatter(self, x: List[float], y: List[float]):
        """
        Scatters x-y data.

        :param x: x values
        :param y: y values
        """
        self.plots.append(Scatter(x, y))

    def set_x_unit(self, unit: str):
        """
        Sets the unit of the x axis, which appears in []-brackets at the
        bottom right of the figure.
        :param unit:
        """
        self.unit_x = unit

    def set_y_unit(self, unit: str):
        """
        Sets the unit of the y axis, which appears in []-brackets at the top
        left of the figrue.

        :param unit:
        """
        self.unit_y = unit

    def draw_plots(self):
        """
        Draws the list of plots in self.plots into the graph area.

        :modifies: self.canvas
        """
        graph = Graph(self.graph_width, self.graph_height, self.plots,
                      self.x2bin, self.y2bin)

        graph_canvas = graph.render()

        # row-wise replace
        for ir, r in enumerate(graph_canvas):
            self.canvas[LOW_PAD + ir][LEFT_PAD:] = r

    def export_str(self) -> str:
        """
        Plots the whole figure with the axes and plots and returns them as
        a string.
        :return: figure as a string
        """
        if self.plots:
            self.draw_x_axis()
            self.draw_y_axis()
            self.draw_plots()
        self.decorate_axes()
        figure = self.draw_canvas()

        return figure

    def show(self):
        """
        Shows the figure in stdout.
        """
        print(self.export_str())
