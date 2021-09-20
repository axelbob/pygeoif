"""Test geometric functions."""
import math
import random

import pytest

from pygeoif.functions import centeroid
from pygeoif.functions import convex_hull
from pygeoif.functions import signed_area


def circle_ish(x, y, r, steps):
    pts = []
    steps = max(steps, 3)
    for step in range(steps):
        phi = 2 * math.pi * step / steps
        pts.append((r * math.cos(phi) + x, r * math.sin(phi) + y))
    pts.append((x + r, y))
    return pts


def star_ish(x, y, r, steps):
    pts = []
    steps = max(steps, 3)
    for step in range(steps):
        phi = 2 * math.pi * step / steps
        pts.append(
            (random.randrange(1, r + 1) * math.cos(phi) + x, r * math.sin(phi) + y),
        )
    pts.append((x + r, y))
    return pts


def spiral_ish(x, y, r, steps):
    pts = []
    for step in range(1, steps):
        phi = math.pi * step / steps
        pts.append((step * r * math.cos(phi) + x, step * r * math.sin(phi) + y))
    pts.append((x + r, y))
    return pts


def crescent_ish(x, y, r, steps):
    pts = []
    for step in range(1, steps):
        phi = math.pi * step / steps
        pts.append((step * r * 2 * math.cos(phi) + x, step * r * math.sin(phi) + y))
    for step in range(steps, 0, -1):
        phi = math.pi * step / steps
        pts.append((step * r * math.cos(phi) + x, step * r * math.sin(phi) + y))
    pts.append(pts[0])
    return pts


def test_signed_area():
    a0 = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
    a1 = [(0, 0, 1), (0, 2, 2), (2, 2, 3), (2, 0, 4), (0, 0, 1)]
    assert signed_area(a0) == signed_area(a1) == -4
    assert centeroid(a0)[1] == centeroid(a1)[1] == -4


def test_signed_area2():
    a0 = [(0, 0), (0, 1), (1, 1), (0, 0)]
    assert centeroid(a0)[1] == signed_area(a0)


def test_signed_area_0_3d():
    assert signed_area(((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))) == 0.0


def test_signed_area_0_2d():
    assert signed_area(((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))) == 0.0


def test_signed_area_circle_ish():
    for i in range(100):
        x = random.randrange(20)
        y = random.randrange(20)
        r = random.randrange(1, 20 + i)
        pts = []
        steps = random.randrange(20)
        pts = circle_ish(x, y, r, steps)
        center1, area = centeroid(pts)
        assert abs(area - signed_area(pts)) < 0.001
        center2, area = centeroid(list(reversed(pts)))
        assert abs(area - signed_area(list(reversed(pts)))) < 0.001
        assert center2 == center2
        assert -0.1 < center1[0] - x < 0.1


def test_signed_area_crescent_ish():
    for i in range(100):
        x = random.randrange(20) - i
        y = random.randrange(20 + i)
        r = random.randrange(1, 20)
        pts = []
        steps = random.randrange(4, 20)
        pts = crescent_ish(x, y, r, steps)
        center1, area = centeroid(pts)
        assert abs(area - signed_area(pts)) < 0.001
        center2, area = centeroid(list(reversed(pts)))
        assert abs(area - signed_area(list(reversed(pts)))) < 0.001
        assert 0.001 > abs(center2[0] - center1[0])
        assert 0.001 > abs(center2[1] - center1[1])


def test_empty_hull():
    assert not convex_hull([])


def test_point():
    pts = [(0, 0)]

    hull = convex_hull(pts)

    assert hull == [(0, 0)]


def test_line():
    pts = [(0, 0), (1, 1)]

    hull = convex_hull(pts)

    assert hull == [(0, 0), (1, 1)]


def test_line2():
    pts = ((x, x) for x in range(5))

    hull = convex_hull(pts)

    assert hull == [(0, 0), (4, 4)]


def test_line3():
    pts = ((x, x) for x in range(3))

    hull = convex_hull(pts)

    assert hull == [(0, 0), (2, 2)]


def test_square():
    pts = []
    for x in range(100):
        for y in range(100):
            pts.append((x, y))

    hull = convex_hull(pts)

    assert hull == [(0, 0), (99, 0), (99, 99), (0, 99), (0, 0)]


def test_triangle():
    pts = []
    for x in range(100):
        for y in range(x + 1):
            pts.append((x, y))

    hull = convex_hull(pts)

    assert hull == [(0, 0), (99, 0), (99, 99), (0, 0)]


def test_trapezoid():
    pts = []
    for x in range(100):
        for y in range(-x - 1, x + 1):
            pts.append((x, y))

    hull = convex_hull(pts)

    assert hull == [(0, -1), (99, -100), (99, 99), (0, 0), (0, -1)]


def test_circles():
    for _ in range(10):
        x = random.randrange(20)
        y = random.randrange(20)
        r = random.randrange(1, 20)
        steps = random.randrange(4, 20)
        pts = circle_ish(x, y, r, steps)

        hull = convex_hull(pts)

        assert set(hull) == set(pts)
        assert len(hull) == len(pts)


def test_spiral():
    for _ in range(10):
        x = random.randrange(20)
        y = random.randrange(20)
        pts = []
        steps = random.randrange(4, 20)
        spiral_ish(x, y, 1, steps)

        hull = convex_hull(pts)

        assert set(hull) == set(pts)
        assert len(hull) == len(pts)


def test_cresent():
    for _ in range(10):
        x = random.randrange(20)
        y = random.randrange(20)
        pts = []
        steps = random.randrange(4, 20)
        crescent_ish(x, y, 1, steps)

        hull = convex_hull(pts)
        assert len(hull) == len(pts) / 2


def test_star():
    for _ in range(10):
        x = random.randrange(20)
        y = random.randrange(20)
        pts = []
        steps = random.randrange(4, 20)
        star_ish(x, y, 1, steps)

        hull = convex_hull(pts)

        assert set(hull).issubset(set(pts))
        assert len(hull) <= len(pts)


def test_random():
    """The convex hull of an exiting hull must be the same as the hull itself."""
    for i in range(100):
        pts = (
            (random.randrange(-x, x + 1), random.randrange(-x, x + 1))
            for x in range(i + 1)
        )
        hull = convex_hull(pts)

        assert convex_hull(hull) == hull
        if len(hull) > 3:
            _, area = centeroid(tuple(hull))
            assert abs(area - signed_area(hull)) < 0.001
