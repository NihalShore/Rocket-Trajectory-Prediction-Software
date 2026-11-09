from rocket_sim.config import StageConfig, VehicleConfig, SimulationConfig
from rocket_sim.simulation import simulate
from rocket_sim.diagnostics import validate_samples
from rocket_sim.winds import WindProfile


def config(**kwargs):
    stage = StageConfig("Short stage", 100., 400., 12000., 20.)
    vehicle = VehicleConfig([stage], 30., .8, .4)
    options = {"max_time": 40., "time_step": .1}
    options.update(kwargs)
    return SimulationConfig(vehicle, **options)


def test_simulation_produces_ordered_samples():
    result = simulate(config())
    assert len(result.samples) > 10
    assert all(b.time > a.time for a, b in zip(result.samples, result.samples[1:]))


def test_simulation_mass_is_nonincreasing():
    result = simulate(config())
    masses = result.masses
    assert all(b <= a + 1e-8 for a, b in zip(masses, masses[1:]))


def test_simulation_records_burnout():
    result = simulate(config())
    assert any(e.name == "burnout" for e in result.events)


def test_simulation_diagnostics():
    result = simulate(config())
    assert not [
        d for d in validate_samples(list(result.samples)) if d.severity == "error"
    ]


def test_peak_altitude_positive():
    assert simulate(config()).metrics.maximum_altitude > 0


def test_wind_changes_airloads_and_pushes_rocket_downwind():
    wind = WindProfile([(0., 20., 0., 0.), (1000., 20., 0., 0.)])
    calm = simulate(config(max_time=1., wind_profile=None))
    windy = simulate(config(max_time=1., launch_azimuth_deg=90., wind_profile=wind))

    assert calm.samples[0].dynamic_pressure == 0.
    assert windy.samples[0].dynamic_pressure > 0.
    assert windy.samples[0].wind_downrange == 20.
    assert windy.samples[0].air_relative_speed == 20.
    assert windy.samples[-1].state.horizontal_velocity > calm.samples[-1].state.horizontal_velocity


def test_wind_profile_is_included_in_result_data():
    wind = WindProfile([(0., 4., 2., 0.), (1000., 8., 3., 0.)])
    result = simulate(config(max_time=.2, wind_profile=wind))
    data = result.to_dict()

    assert data["wind_profile"][0] == {
        "altitude": 0.,
        "east": 4.,
        "north": 2.,
        "vertical": 0.,
    }
    assert "air_relative_speed" in data["samples"][0]
