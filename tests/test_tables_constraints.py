import pytest
from rocket_sim.coefficient_table import CoefficientTable
from rocket_sim.constraints import upper_bound,lower_bound,all_satisfied
def test_linear_interpolation(): assert CoefficientTable([(0,1),(10,3)])(5)==pytest.approx(2)
def test_clamped_extrapolation():
 t=CoefficientTable([(0,1),(10,3)]); assert t(-5)==1 and t(15)==3
def test_linear_extrapolation(): assert CoefficientTable([(0,1),(10,3)],"linear")(15)==pytest.approx(4)
def test_table_derivative(): assert CoefficientTable([(0,1),(10,3)]).derivative(3)==pytest.approx(.2)
def test_duplicate_abscissa_rejected():
 with pytest.raises(ValueError): CoefficientTable([(0,1),(0,2)])
def test_upper_constraint(): assert upper_bound("q",90,100).margin==10
def test_lower_constraint(): assert lower_bound("altitude",110,100).satisfied
def test_aggregate_constraints(): assert all_satisfied([upper_bound("a",1,2),lower_bound("b",3,2)])
