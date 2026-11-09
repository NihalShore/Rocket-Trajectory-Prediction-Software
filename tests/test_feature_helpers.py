from types import SimpleNamespace

import pytest

from rocket_sim.aeroheating import peak_heat_flux, sutton_graves
from rocket_sim.config import SimulationConfig, StageConfig, VehicleConfig
from rocket_sim.failures import early_staging, engine_out
from rocket_sim.maxq_throttle import throttle_for_q
from rocket_sim.range_safety import footprint_ellipse, impact_point
from rocket_sim.state import State, TrajectorySample
from rocket_sim.uncertainty import run_monte_carlo


def short_config():
    stage = StageConfig("booster", 10.0, 40.0, 1000.0, 4.0)
    vehicle = VehicleConfig([stage], 2.0, 0.2)
    return SimulationConfig(vehicle, max_time=5.0, time_step=0.2)


def test_engine_out_keeps_vehicle_initial_mass():
    config = short_config()
    result = engine_out(
        config,
        stage_index=0,
        engines_nominal=9,
        engines_out=1,
        at_time=1.0,
    )

    assert result.config.vehicle.initial_mass == pytest.approx(config.vehicle.initial_mass)
    assert any(event.name == "stage_separation" for event in result.events)


def test_failure_helpers_validate_inputs():
    config = short_config()
    with pytest.raises(ValueError):
        engine_out(config, at_time=0.0)
    with pytest.raises(ValueError):
        early_staging(config, early_by=4.0)
    with pytest.raises(IndexError):
        early_staging(config, stage_index=-1)
    with pytest.raises(ValueError):
        engine_out(config, engines_nominal=4, engines_out=4)


def test_early_staging_uses_the_shortened_burn():
    result = early_staging(short_config(), early_by=1.0)

    assert result.config.vehicle.stages[0].burn_time == pytest.approx(3.0)
    assert any(event.name == "burnout" for event in result.events)


def test_monte_carlo_completes_requested_runs():
    results, summary = run_monte_carlo(short_config(), n=3, seed=4)

    assert len(results) == 3
    assert summary["n_ok"] == 3
    assert summary["n_requested"] == 3


def test_monte_carlo_does_not_hide_simulation_errors(monkeypatch):
    import rocket_sim.uncertainty as uncertainty

    def fail(*args, **kwargs):
        raise RuntimeError("simulation failed")

    monkeypatch.setattr(uncertainty, "simulate", fail)
    with pytest.raises(RuntimeError, match="simulation failed"):
        run_monte_carlo(short_config(), n=1, seed=1)


def test_downrange_footprint_does_not_invent_crossrange():
    center_x, center_y, major, minor, angle = footprint_ellipse([10.0, 20.0, 30.0])

    assert center_x == pytest.approx(20.0)
    assert center_y == 0.0
    assert major > 0.0
    assert minor == 0.0
    assert angle == pytest.approx(0.0)


def test_impact_point_interpolates_ground_crossing():
    samples = [
        TrajectorySample(0.0, State(0.0, 100.0, 0.0, 5.0, 10.0), 0, 0, 0, 0, 0),
        TrajectorySample(2.0, State(200.0, -100.0, 0.0, -5.0, 10.0), 0, 0, 0, 0, 0),
    ]
    result = SimpleNamespace(samples=samples)

    downrange, altitude, time = impact_point(result)

    assert downrange == pytest.approx(100.0)
    assert altitude == 0.0
    assert time == pytest.approx(1.0)


def test_heat_flux_uses_air_relative_speed():
    dynamic_pressure = 0.5 * 1.2 * 20.0**2
    sample = TrajectorySample(
        0.0,
        State(0.0, 100.0, 0.0, 0.0, 10.0),
        0.0,
        0.0,
        dynamic_pressure,
        0.0,
        0,
        air_relative_speed=20.0,
    )

    heat_flux, time = peak_heat_flux([sample], nose_radius=0.25)

    assert heat_flux == pytest.approx(sutton_graves(1.2, 20.0, 0.25))
    assert time == 0.0


def test_max_q_throttle_schedule_helper():
    assert throttle_for_q(50000.0, 40000.0) < 1.0
    assert throttle_for_q(30000.0, 40000.0) == 1.0
    with pytest.raises(ValueError):
        throttle_for_q(100.0, 0.0)
