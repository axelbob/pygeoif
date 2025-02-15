"""Test MultiPoint."""
import pytest

from pygeoif import geometry


def test_geoms():
    multipoint = geometry.MultiPoint([(0, 0), (1, 1), (1, 2), (2, 2)])

    for point in multipoint.geoms:
        assert type(point) is geometry.Point


def test_len():
    multipoint = geometry.MultiPoint(
        [(0, 0), (1, 1), (1, 2), (2, 2), (0, 0), (1, 1), (1, 2), (2, 2)],
    )

    assert len(multipoint) == 8


def test_bounds():
    multipoint = geometry.MultiPoint(
        [(0, 1), (1, 1), (3, 2)],
    )

    assert multipoint.bounds == (0, 1, 3, 2)


def test_has_z_empty():
    multipoint = geometry.MultiPoint(())

    assert multipoint.has_z is None


def test_geo_interface():
    multipoint = geometry.MultiPoint([(0, 0), (1, 1), (1, 2), (2, 2)])

    assert multipoint.__geo_interface__ == {
        "type": "MultiPoint",
        "bbox": (0, 0, 2, 2),
        "coordinates": ((0, 0), (1, 1), (1, 2), (2, 2)),
    }


def test_from_dict():
    multipoint = geometry.MultiPoint._from_dict(
        {
            "type": "MultiPoint",
            "bbox": (0.0, 0.0, 1.0, 1.0),  # pragma: no mutate
            "coordinates": ((0.0, 0.0), (1.0, 1.0)),
        },
    )

    assert multipoint.__geo_interface__ == {
        "type": "MultiPoint",
        "bbox": (0.0, 0.0, 1.0, 1.0),  # pragma: no mutate
        "coordinates": ((0.0, 0.0), (1.0, 1.0)),
    }


def test_coords():
    multipoint = geometry.MultiPoint([(0, 0), (1, 1), (1, 2), (2, 2)])

    with pytest.raises(
        NotImplementedError,
        match="^Multi-part geometries do not provide a coordinate sequence$",
    ):
        assert multipoint.coords


def test_unique():
    multipoint = geometry.MultiPoint(
        [(0, 0), (1, 1), (1, 2), (2.0, 2.0), (0, 0), (1.0, 1.0), (1, 2), (2, 2)],
        unique=True,
    )

    assert len(multipoint) == 4


def test_wkt():
    multipoint = geometry.MultiPoint([(0, 0), (1, 1), (1, 2), (2, 2)])

    assert multipoint.wkt == "MULTIPOINT(0 0, 1 1, 1 2, 2 2)"


def test_repr():
    multipoint = geometry.MultiPoint([(0, 0), (1, 1), (1, 2), (2, 2)])

    assert repr(multipoint) == "MultiPoint(((0, 0), (1, 1), (1, 2), (2, 2)))"


def test_repr_eval():
    multipoint = geometry.MultiPoint([(0, 0), (1, 1), (1, 2), (2, 2)])

    assert (
        eval(
            repr(multipoint),
            {},
            {"MultiPoint": geometry.MultiPoint},
        ).__geo_interface__
        == multipoint.__geo_interface__
    )


def test_convex_hull():
    multipoint = geometry.MultiPoint([(0, 0), (1, 1), (2, 2)])

    assert multipoint.convex_hull == geometry.LineString([(0, 0), (2, 2)])


def test_convex_hull_3d():
    multipoint = geometry.MultiPoint([(0, 0, 0), (1, 1, 1), (2, 2, 2)])

    assert multipoint.convex_hull == geometry.LineString([(0, 0), (2, 2)])


def test_convex_hull_3d_collapsed_to_point():
    multipoint = geometry.MultiPoint([(0, 0, 0), (0, 0, 1), (0, 0, 2)])

    assert multipoint.convex_hull == geometry.Point(0, 0)


def test_convex_hull_linear_ring():
    multipoint = geometry.MultiPoint([(0, 0), (1, 0), (2, 2)])

    assert multipoint.convex_hull == geometry.Polygon([(0, 0), (1, 0), (2, 2), (0, 0)])


def test_from_points():
    multipoint = geometry.MultiPoint([(0, 0), (1, 0), (2, 2)])
    p1 = geometry.Point(0, 0)
    p2 = geometry.Point(1, 0)
    p3 = geometry.Point(2.0, 2.0)

    assert geometry.MultiPoint.from_points(p1, p2, p3) == multipoint


def test_from_points_unique():
    multipoint = geometry.MultiPoint([(0, 0), (1, 0), (2, 2)], unique=True)
    p1 = geometry.Point(0, 0)
    p2 = geometry.Point(1, 0)
    p3 = geometry.Point(2.0, 2.0)

    assert (
        geometry.MultiPoint.from_points(p1, p2, p3, p1, p2, p3, p1, unique=True)
        == multipoint
    )


def test_empty():
    multipoint = geometry.MultiPoint([(1, None)])

    assert multipoint.is_empty


def test_repr_empty():
    multipoint = geometry.MultiPoint([(None, None)])

    assert repr(multipoint) == "MultiPoint(((),))"


def test_empty_bounds():
    multipoint = geometry.MultiPoint([(None, None)])

    assert multipoint.bounds == ()
