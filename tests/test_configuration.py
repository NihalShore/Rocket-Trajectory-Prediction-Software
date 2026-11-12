import numpy as np
import pytest

from rocket_sim.config import StageConfig, VehicleConfig, SimulationConfig
from rocket_sim.winds import WindProfile


def stage():
    return StageConfig("Test", 100.0, 500.0, 10000.0, 50.0)


def test_vehicle_initial_mass():
    vehicle = VehicleConfig([stage()], 50.0, 1.0)
    assert vehicle.initial_mass == 650.0


def test_stage_rejects_zero_propellant():
    with pytest.raises(ValueError):
        StageConfig("Bad", 100.0, 0.0, 10000.0, 50.0)


def test_config_rejects_bad_timestep():
    with pytest.raises(ValueError):
        SimulationConfig(VehicleConfig([stage()], 50.0, 1.0), time_step=0.0)


def test_vehicle_requires_stage():
    with pytest.raises(ValueError):
        VehicleConfig([], 50.0, 1.0)


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
def test_stage_rejects_non_finite_values(value):
    with pytest.raises(ValueError):
        StageConfig("Bad", 100.0, 500.0, value, 50.0)


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
def test_vehicle_rejects_non_finite_values(value):
    with pytest.raises(ValueError):
        VehicleConfig([stage()], 50.0, value)


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
def test_simulation_rejects_non_finite_time_and_position(value):
    with pytest.raises(ValueError):
        SimulationConfig(VehicleConfig([stage()], 50.0, 1.0), max_time=value)
    with pytest.raises(ValueError):
        SimulationConfig(VehicleConfig([stage()], 50.0, 1.0), initial_downrange=value)


def test_simulation_requires_metadata_mapping():
    with pytest.raises(TypeError):
        SimulationConfig(VehicleConfig([stage()], 50.0, 1.0), metadata=[])


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
def test_wind_profile_rejects_non_finite_values(value):
    with pytest.raises(ValueError):
        WindProfile([(0.0, value, 0.0, 0.0)])
