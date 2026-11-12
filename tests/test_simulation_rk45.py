from rocket_sim.config import StageConfig, VehicleConfig, SimulationConfig
from rocket_sim.simulation import simulate


def test_rk45_simulation_uses_adaptive_solver_and_completes():
    stage = StageConfig("Short stage", 100.0, 400.0, 12000.0, 20.0)
    vehicle = VehicleConfig([stage], 30.0, 0.8, 0.4)
    config = SimulationConfig(
        vehicle,
        max_time=25.0,
        time_step=0.5,
        integrator="rk45",
        absolute_tolerance=1e-8,
        relative_tolerance=1e-6,
    )

    result = simulate(config)

    assert result.samples[-1].time == 25.0
    assert all(
        later.time > earlier.time
        for earlier, later in zip(result.samples, result.samples[1:])
    )
    assert all(sample.state.mass > 0 for sample in result.samples)
