from typing import List, Callable

from plottoterminal.lib.plots import BasePlot, Scatter

SYMBOLS = "x*+>"


class Point(object):
    pass


class Graph(object):
    def __init__(self, width: int, height: int, plots: List[BasePlot],
                 x2bin: Callable[[float], int], y2bin: Callable[[float], int]):
        self.width = width
        self.height = height
        self.plots = plots
        self.x2bin = x2bin
        self.y2bin = y2bin
        self.pixels = List[List[Point]]
        self.canvas = [
            [' ' for _ in range(self.width)] for _ in range(self.height)]

    def collect(self):
        raise NotImplementedError

    def render(self):
        for ip, p in enumerate(self.plots):
            # handle different plot types differently
            # here it will be decided which symbol to place

            # normal scatter plot:
            # just put in what comes naturally first and then allow overriding
            if isinstance(p, Scatter):
                for px, py in zip(p.x, p.y):
                    bx = self.x2bin(px)
                    by = self.y2bin(py)
                    self.canvas[by][bx] = SYMBOLS[ip % len(SYMBOLS)]

        return self.canvas
