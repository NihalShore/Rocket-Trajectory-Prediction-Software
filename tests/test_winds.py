import numpy as np
import pytest

from rocket_sim.winds import WindProfile, random_wind, power_law


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
def test_wind_profile_rejects_non_finite_levels(value):
    with pytest.raises(ValueError):
        WindProfile([(0.0, value, 0.0, 0.0)])


def test_wind_profile_rejects_non_finite_query_altitude():
    profile = WindProfile([(0.0, 0.0, 0.0, 0.0)])

    with pytest.raises(ValueError):
        profile.at(np.nan)


def test_random_wind_rejects_invalid_speed_limit():
    with pytest.raises(ValueError):
        random_wind(max_speed=np.inf)


def test_power_law_rejects_invalid_reference_height():
    with pytest.raises(ValueError):
        power_law(z_ref=0.0)
