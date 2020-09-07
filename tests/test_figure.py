from math import sin
from unittest import TestCase

from plottoterminal.lib import figure
from plottoterminal.lib.utils import linspace, PI


class TestFigure(TestCase):
    def test_decorate_axes(self):
        f = figure.Figure()
        f.set_x_label("price")
        f.set_y_label("demand")
        print(f.export_str())

    def test_width(self):
        f = figure.Figure()
        self.assertEqual(73, f.graph_width)
        self.assertEqual(19, f.graph_height)

    def test_lim_scale(self):
        f = figure.Figure()
        xs = [0, 1, 2, 3, 4]
        ys = [0, 1, 2, 3, 4]
        f.scatter(xs, ys)

        f.set_x_lim()
        self.assertEqual((0, 4.0), f.x_lim)
        f.set_y_lim()
        self.assertEqual((0, 4.0), f.y_lim)

        f.init_x_scale()
        f.init_y_scale()

        print([f.x2bin(x) for x in xs])
        print([f.y2bin(y) for y in ys])

        print(f.get_x_tick_positions())
        print(f.get_x_tick_labels())

    def test_scale_exponent(self):
        f = figure.Figure()
        xs = linspace(-10, 10, 100)
        ys = linspace(-10, 10, 100)
        f.scatter(xs, ys)
        f.set_x_lim()
        f.init_x_scale()
        f.set_x_label("fruit 1")
        f.set_y_label("fruit 2")
        f.set_x_unit("apple")
        f.set_y_unit("banana")
        f.show()

    def test_draw_graph_components(self):
        f = figure.Figure(figsize=(50, 15))
        xs = [0, 1, 2, 3, 4, 5]
        ys = [0, 1, 2, 3, 4, 5]
        f.set_x_label("price")
        f.set_y_label("demand")
        f.scatter(xs, ys)

        f.draw_x_axis()
        f.draw_y_axis()
        f.draw_plots()
        f.decorate_axes()
        print(f.draw_canvas())

    def test_sin(self):
        f = figure.Figure(figsize=(100, 30))
        xs = linspace(-PI, PI, 200)
        ys = [sin(x) for x in xs]
        f.set_x_label("x")
        f.set_y_label("sin(x)")
        f.scatter(xs, ys)
        f.show()

    def test_parabola(self):
        f = figure.Figure(figsize=(60, 15))
        xs = linspace(-2, 2, 200)
        ys = [x*x for x in xs]
        f.set_x_label("x")
        f.set_y_label("x*x")
        f.scatter(xs, ys)
        f.show()

    def test_small(self):
        f = figure.Figure(figsize=(30, 8))
        xs = linspace(-2, 2, 200)
        ys = [x*x for x in xs]
        f.set_x_label("x")
        f.set_y_label("x*x")
        f.scatter(xs, ys)
        f.show()

    def test_multi(self):
        """
        Tests putting multiple graphs into one plot.
        """
        f = figure.Figure(figsize=(57, 20))
        xs = linspace(-10, 10, 200)

        ys = [x*x for x in xs]
        f.scatter(xs, ys)

        ys2 = [-x*x for x in xs]
        f.scatter(xs, ys2)

        f.set_x_label("x")
        f.set_y_label("x*x")
        f.set_x_unit("m")
        f.set_y_unit("m^2")
        f.show()

    def test_cube(self):
        """
        Tests x^3.
        """
        f = figure.Figure(figsize=(30, 10))
        xs = linspace(-1, 1, 200)
        ys = [x*x*x for x in xs]
        f.set_x_label("x")
        f.set_y_label("x*x*x")
        f.scatter(xs, ys)

        string_tested = f.export_str()
        string_expected = \
            "   1.0ᐃ                  x    \n" \
            "x     │                xx     \n" \
            "*     │              xxx      \n" \
            "x  0.0├    xxxxxxxxxxx        \n" \
            "*     │  xxx                  \n" \
            "x     │ xx                    \n" \
            "  -1.0├x                      \n" \
            "      └┴─────┴─────┴─────┴───ᐅ\n" \
            "       -1.0  -0.3  0.3   1.0  \n" \
            "                  x           \n"

        self.assertEqual(string_expected, string_tested)

    def test_lin(self):
        """
        Test a linear function.
        """
        f = figure.Figure(figsize=(50, 15))
        xs = linspace(-1, 1, 50)
        ys = xs
        f.set_x_label("x")
        f.set_y_label("x")
        f.scatter(xs, ys)
        f.show()
        string_expected = \
            "      ᐃ                                           \n" \
            "   1.0├                                   xx      \n" \
            "      │                               xxxx        \n" \
            "   0.6├                           xxxx            \n" \
            "      │                        xxxx               \n" \
            "x  0.2├                    xxxx                   \n" \
            "      │                 xxx                       \n" \
            "  -0.2├             xxxx                          \n" \
            "      │         xxxx                              \n" \
            "  -0.6├      xxxx                                 \n" \
            "      │  xxxx                                     \n" \
            "  -1.0├xx                                         \n" \
            "      └┴────────┴────────┴────────┴────────┴─────ᐅ\n" \
            "       -1.0     -0.5     0.0      0.5      1.0    \n" \
            "                            x                     \n"

        string_tested = f.export_str()
        self.assertEqual(string_expected, string_tested)
