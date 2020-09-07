from typing import List, Optional


class BasePlot(object):
    """
    Represents a certain type of plot.
    """
    def __init__(self, x: List[float], y: List[float],
                 z: Optional[List[float]] = None):
        self.x = x
        self.y = y
        self.z = z
        pass

    def min_x(self) -> float:
        return min(self.x)

    def max_x(self) -> float:
        return max(self.x)

    def min_y(self) -> float:
        return min(self.y)

    def max_y(self) -> float:
        return max(self.y)


class Scatter(BasePlot):
    """
    Represents a scatter plot.
    """

    def __init__(self, x: List[float], y: List[float],
                 z: Optional[List[float]] = None):
        super().__init__(x, y, z)
