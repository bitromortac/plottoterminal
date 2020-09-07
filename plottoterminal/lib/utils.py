PI = 3.14159265359


def linspace(start: float, end: float, steps: int = 100):
    assert start < end
    return [start + (end - start) * i / steps for i in range(steps + 1)]


def rint(f: float) -> int:
    """
    Rounds to an int.
    rint(-0.5) = 0
    rint(0.5) = 0
    rint(0.6) = 1
    :param f: number
    :return: int
    """

    return int(round(f, 0))
