import math
import pytest
from rocket_sim.orbital import circular_speed,escape_speed_at_radius,orbital_period,orbital_state,hohmann_transfer
from rocket_sim.constants import EARTH_RADIUS,EARTH_MU
def test_circular_speed_at_earth_surface():
    assert circular_speed(EARTH_RADIUS)==pytest.approx(math.sqrt(EARTH_MU/EARTH_RADIUS))
def test_escape_speed_exceeds_circular_speed():
    assert escape_speed_at_radius(EARTH_RADIUS)==pytest.approx(math.sqrt(2)*circular_speed(EARTH_RADIUS))
def test_circular_orbit_period():
    r=EARTH_RADIUS+400000
    state=orbital_state(r,0,circular_speed(r))
    assert state.eccentricity==pytest.approx(0,abs=1e-7)
    assert state.apoapsis_altitude==pytest.approx(400000)
    assert state.period==pytest.approx(orbital_period(r))
def test_hohmann_transfer_is_symmetric_for_same_radius():
    result=hohmann_transfer(7000000,7000000)
    assert result["departure_delta_v"]==pytest.approx(0)
    assert result["arrival_delta_v"]==pytest.approx(0)
def test_invalid_orbit_radius():
    with pytest.raises(ValueError): circular_speed(0)
