from rocket_sim import (
    SimulationConfig,
    StageConfig,
    VehicleConfig,
    WindProfile,
    simulate,
)
from rocket_sim.guidance import gravity_turn_program


def test_readme_library_example_runs():
    stage = StageConfig(
        name="S1",
        dry_mass=12000,
        propellant_mass=65000,
        thrust_vacuum=1.5e6,
        burn_time=100,
        thrust_sea_level=1.3e6,
    )
    vehicle = VehicleConfig(
        [stage],
        payload_mass=900,
        reference_area=5.2,
        drag_coefficient=0.4,
    )
    wind = WindProfile([
        (0, 3, 0, 0),
        (1000, 8, 2, 0),
        (10000, 25, 5, 0),
    ])
    config = SimulationConfig(
        vehicle,
        max_time=300,
        time_step=0.25,
        wind_profile=wind,
    )
    pitch = gravity_turn_program(
        start_time=8,
        end_time=100,
        terminal_angle_deg=12,
    )

    result = simulate(config, pitch)

    assert result.samples
    assert result.metrics.maximum_altitude > 0.0
