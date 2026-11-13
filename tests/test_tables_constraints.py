import pytest
from rocket_sim.coefficient_table import CoefficientTable
from rocket_sim.constraints import upper_bound, lower_bound, all_satisfied


def test_linear_interpolation():
    assert CoefficientTable([(0, 1), (10, 3)])(5) == pytest.approx(2)


def test_clamped_extrapolation():
    table = CoefficientTable([(0, 1), (10, 3)])
    assert table(-5) == 1
    assert table(15) == 3


def test_linear_extrapolation():
    table = CoefficientTable([(0, 1), (10, 3)], "linear")
    assert table(15) == pytest.approx(4)


def test_table_derivative():
    assert CoefficientTable([(0, 1), (10, 3)]).derivative(3) == pytest.approx(.2)


def test_clamped_derivative_is_zero_outside_domain():
    table = CoefficientTable([(0, 1), (10, 3)])
    assert table.derivative(-5) == 0
    assert table.derivative(15) == 0


def test_linear_derivative_uses_end_segment_outside_domain():
    table = CoefficientTable([(0, 1), (10, 3)], "linear")
    assert table.derivative(-5) == pytest.approx(.2)
    assert table.derivative(15) == pytest.approx(.2)


def test_error_extrapolation_applies_to_derivative():
    table = CoefficientTable([(0, 1), (10, 3)], "error")
    with pytest.raises(ValueError, match="outside table"):
        table.derivative(15)


@pytest.mark.parametrize("points", [
    [(0, 1), (float("nan"), 2)],
    [(0, 1), (10, float("inf"))],
])
def test_non_finite_table_values_rejected(points):
    with pytest.raises(ValueError, match="finite"):
        CoefficientTable(points)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_non_finite_queries_rejected(value):
    table = CoefficientTable([(0, 1), (10, 3)])
    with pytest.raises(ValueError, match="finite"):
        table(value)
    with pytest.raises(ValueError, match="finite"):
        table.derivative(value)


def test_duplicate_abscissa_rejected():
    with pytest.raises(ValueError):
        CoefficientTable([(0, 1), (0, 2)])


def test_upper_constraint():
    assert upper_bound("q", 90, 100).margin == 10


def test_lower_constraint():
    assert lower_bound("altitude", 110, 100).satisfied


def test_aggregate_constraints():
    assert all_satisfied([upper_bound("a", 1, 2), lower_bound("b", 3, 2)])
