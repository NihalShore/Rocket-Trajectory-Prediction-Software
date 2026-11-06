import math
import pytest
from rocket_sim.atmosphere import atmosphere
from rocket_sim.gravity import gravity,escape_speed
from rocket_sim.propulsion import ideal_rocket_delta_v,performance_from_isp
def test_sea_level_atmosphere():
    a=atmosphere(0.)
    assert a.pressure==pytest.approx(101325.,rel=1e-8)
    assert a.density==pytest.approx(1.225,rel=.01)
def test_density_decreases_with_altitude():
    assert atmosphere(10000).density<atmosphere(0).density
def test_exponential_density():
    assert atmosphere(8500,"exponential").density==pytest.approx(1.225/math.e)
def test_gravity_decreases():
    assert gravity(100000)<gravity(0)
def test_escape_speed():
    assert escape_speed()>10000
def test_rocket_equation():
    assert ideal_rocket_delta_v(1000,500,3000)==pytest.approx(3000*math.log(2))
def test_engine_isp_relation():
    p=performance_from_isp(100000,300)
    assert p.mass_flow==pytest.approx(100000/(300*9.80665))
def test_invalid_rocket_equation():
    with pytest.raises(ValueError): ideal_rocket_delta_v(10,10,300)
