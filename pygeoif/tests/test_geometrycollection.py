"""Test Baseclass."""
from pygeoif import geometry


def test_geo_interface():
    poly1 = geometry.Polygon([(0, 0), (1, 1), (1, 0), (0, 0)])
    e = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
    i = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)]
    poly2 = geometry.Polygon(e, [i])
    p0 = geometry.Point(0, 0)
    p1 = geometry.Point(-1, -1)
    ring = geometry.LinearRing(
        [
            (0, 0),
            (1, 1),
            (1, 0),
            (0, 0),
        ],
    )
    line = geometry.LineString(
        [
            (0, 0),
            (1, 1),
        ],
    )
    gc = geometry.GeometryCollection([poly1, poly2, p0, p1, ring, line])

    assert gc.__geo_interface__ == {
        "geometries": (
            {
                "bbox": (0, 0, 1, 1),
                "coordinates": (((0, 0), (1, 1), (1, 0), (0, 0)),),
                "type": "Polygon",
            },
            {
                "bbox": (0, 0, 2, 2),
                "coordinates": (
                    ((0, 0), (0, 2), (2, 2), (2, 0), (0, 0)),
                    ((1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)),
                ),
                "type": "Polygon",
            },
            {"bbox": (0, 0, 0, 0), "coordinates": (0, 0), "type": "Point"},
            {"bbox": (-1, -1, -1, -1), "coordinates": (-1, -1), "type": "Point"},
            {
                "bbox": (0, 0, 1, 1),
                "coordinates": ((0, 0), (1, 1), (1, 0), (0, 0)),
                "type": "LinearRing",
            },
            {
                "bbox": (0, 0, 1, 1),
                "coordinates": ((0, 0), (1, 1)),
                "type": "LineString",
            },
        ),
        "type": "GeometryCollection",
    }


def test_geo_wkt():
    poly1 = geometry.Polygon([(0, 0), (1, 1), (1, 0), (0, 0)])
    e = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
    i = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)]
    poly2 = geometry.Polygon(e, [i])
    p0 = geometry.Point(0, 0)
    p1 = geometry.Point(-1, -1)
    ring = geometry.LinearRing([(0, 0), (1, 1), (1, 0), (0, 0)])
    line = geometry.LineString([(0, 0), (1, 1)])
    gc = geometry.GeometryCollection([poly1, poly2, p0, p1, ring, line])

    assert gc.wkt == (
        "GEOMETRYCOLLECTION"
        "(POLYGON ((0 0, 1 1, 1 0, 0 0)), "
        "POLYGON ((0 0, 0 2, 2 2, 2 0, 0 0),(1 0, 0.5 0.5, 1 1, 1.5 0.5, 1 0)), "
        "POINT (0 0), POINT (-1 -1), "
        "LINEARRING (0 0, 1 1, 1 0, 0 0), "
        "LINESTRING (0 0, 1 1))"
    )


def test_len():
    poly1 = geometry.Polygon([(0, 0), (1, 1), (1, 0), (0, 0)])
    e = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
    i = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)]
    poly2 = geometry.Polygon(e, [i])
    p0 = geometry.Point(0, 0)
    p1 = geometry.Point(-1, -1)
    ring = geometry.LinearRing([(0, 0), (1, 1), (1, 0), (0, 0)])
    line = geometry.LineString([(0, 0), (1, 1)])
    gc = geometry.GeometryCollection([poly1, poly2, p0, p1, ring, line])

    assert len(gc) == 6


def test_geoms():
    poly1 = geometry.Polygon([(0, 0), (1, 1), (1, 0), (0, 0)])
    e = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
    i = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)]
    poly2 = geometry.Polygon(e, [i])
    p0 = geometry.Point(0, 0)
    p1 = geometry.Point(-1, -1)
    ring = geometry.LinearRing([(0, 0), (1, 1), (1, 0), (0, 0)])
    line = geometry.LineString([(0, 0), (1, 1)])
    gc = geometry.GeometryCollection([poly1, poly2, p0, p1, ring, line])

    for k, v in zip(gc.geoms, [poly1, poly2, p0, p1, ring, line]):
        assert k == v


def test_repr():
    poly1 = geometry.Polygon([(0, 0), (1, 1), (1, 0), (0, 0)])
    e = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
    i = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)]
    poly2 = geometry.Polygon(e, [i])
    p0 = geometry.Point(0, 0)
    p1 = geometry.Point(-1, -1)
    ring = geometry.LinearRing([(0, 0), (1, 1), (1, 0), (0, 0)])
    line = geometry.LineString([(0, 0), (1, 1)])
    gc = geometry.GeometryCollection([poly1, poly2, p0, p1, ring, line])

    assert repr(gc) == (
        "GeometryCollection("
        "(Polygon(((0, 0), (1, 1), (1, 0), (0, 0)),), "
        "Polygon(((0, 0), (0, 2), (2, 2), (2, 0), (0, 0)), "
        "(((1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)),)), "
        "Point(0, 0), Point(-1, -1), "
        "LinearRing(((0, 0), (1, 1), (1, 0), (0, 0))), "
        "LineString(((0, 0), (1, 1))))"
        ")"
    )


def test_repr_eval():
    poly1 = geometry.Polygon([(0, 0), (1, 1), (1, 0), (0, 0)])
    e = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
    i = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)]
    poly2 = geometry.Polygon(e, [i])
    p0 = geometry.Point(0, 0)
    p1 = geometry.Point(-1, -1)
    ring = geometry.LinearRing([(0, 0), (1, 1), (1, 0), (0, 0)])
    line = geometry.LineString([(0, 0), (1, 1)])
    gc = geometry.GeometryCollection([poly1, poly2, p0, p1, ring, line])

    assert (
        eval(
            repr(gc),
            {},
            {
                "LinearRing": geometry.LinearRing,
                "Polygon": geometry.Polygon,
                "Point": geometry.Point,
                "LineString": geometry.LineString,
                "GeometryCollection": geometry.GeometryCollection,
            },
        ).__geo_interface__
        == gc.__geo_interface__
    )


def test_eq():
    poly1 = geometry.Polygon([(0, 0), (1, 1), (1, 0), (0, 0)])
    e = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
    i = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)]
    poly2 = geometry.Polygon(e, [i])
    p0 = geometry.Point(0, 0)
    p1 = geometry.Point(-1, -1)
    ring = geometry.LinearRing([(0, 0), (1, 1), (1, 0), (0, 0)])
    line = geometry.LineString([(0, 0), (1, 1)])
    gc1 = geometry.GeometryCollection([poly1, poly2, p0, p1, ring, line])
    gc2 = geometry.GeometryCollection([poly1, poly2, p0, p1, ring, line])

    assert gc1 == gc2


def test_neq_len():
    poly1 = geometry.Polygon([(0, 0), (1, 1), (1, 0), (0, 0)])
    e = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
    i = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)]
    poly2 = geometry.Polygon(e, [i])
    p0 = geometry.Point(0, 0)
    p1 = geometry.Point(-1, -1)
    ring = geometry.LinearRing([(0, 0), (1, 1), (1, 0), (0, 0)])
    line = geometry.LineString([(0, 0), (1, 1)])
    gc1 = geometry.GeometryCollection([poly1, poly2, p0, p1, ring, line])
    gc2 = geometry.GeometryCollection([poly1, poly2, p0, p1, ring])

    assert gc1 != gc2


def test_neq_sort():
    poly1 = geometry.Polygon([(0, 0), (1, 1), (1, 0), (0, 0)])
    e = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
    i = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)]
    poly2 = geometry.Polygon(e, [i])
    p0 = geometry.Point(0, 0)
    p1 = geometry.Point(-1, -1)
    ring = geometry.LinearRing([(0, 0), (1, 1), (1, 0), (0, 0)])
    line = geometry.LineString([(0, 0), (1, 1)])
    gc1 = geometry.GeometryCollection([poly1, poly2, p0, p1, ring, line])
    gc2 = geometry.GeometryCollection([poly1, poly2, p0, p1, line, line])

    assert gc1 != gc2


def test_neq_type():
    line = geometry.LineString([(0, 0), (1, 1)])
    gc1 = geometry.GeometryCollection([line])

    assert gc1 != line


def test_neq_coords():
    p0 = geometry.Point(0, 0)
    p1 = geometry.Point(-1, -1)
    p2 = geometry.Point(-1, -2)
    gc1 = geometry.GeometryCollection([p0, p1])
    gc2 = geometry.GeometryCollection([p0, p2])

    assert gc1 != gc2


def test_neq_interface():
    line = geometry.LineString([(0, 0), (1, 1)])
    gc1 = geometry.GeometryCollection([line])

    assert gc1 != object()


def test_convex_hull():
    p0 = geometry.Point(0, 0)
    p1 = geometry.Point(-1, -1)
    p2 = geometry.Point(-1, -2)
    line = geometry.LineString([(0, 0), (3, 1)])
    poly1 = geometry.Polygon([(0, 0), (1, 1), (1, 0), (0, 0)])
    e = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
    i = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)]
    poly2 = geometry.Polygon(e, [i])
    gc = geometry.GeometryCollection([p0, p1, p2, line, poly1, poly2])

    assert gc.convex_hull == geometry.Polygon(
        ((-1, -2), (2, 0), (3, 1), (2, 2), (0, 2), (-1, -1), (-1, -2)),
    )


def test_is_empty():
    gc = geometry.GeometryCollection([])

    assert gc.is_empty


def test_empty_wkt():
    gc = geometry.GeometryCollection([])

    assert gc.wkt == "GEOMETRYCOLLECTION EMPTY"


def test_repr_empty():
    gc = geometry.GeometryCollection([])

    assert repr(gc) == "GeometryCollection(())"


def test_empty_bounds():
    gc = geometry.GeometryCollection([])

    assert gc.bounds == ()
