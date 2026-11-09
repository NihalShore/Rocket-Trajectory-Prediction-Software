#!/usr/bin/env python3
"""Run the supported post-processing and scenario helpers."""

from rocket_sim.aeroheating import peak_heat_flux, total_heat_load
from rocket_sim.config import SimulationConfig, StageConfig, VehicleConfig
from rocket_sim.failures import early_staging, engine_out
from rocket_sim.guidance import gravity_turn_program
from rocket_sim.maxq_throttle import schedule_from_trajectory
from rocket_sim.range_safety import footprint_ellipse, impact_point, max_q_location
from rocket_sim.simulation import simulate
from rocket_sim.telemetry import print_console, summary_block
from rocket_sim.uncertainty import print_summary, run_monte_carlo
from rocket_sim.winds import jet_streamish


def nominal_config():
    first = StageConfig("S1", 8000, 45000, 1.1e6, 80, 0.95e6)
    second = StageConfig(
        "S2",
        2000,
        12000,
        2.5e5,
        90,
        specific_impulse_vacuum=320,
    )
    vehicle = VehicleConfig(
        [first, second],
        payload_mass=500,
        reference_area=3.5,
        drag_coefficient=0.35,
        name="two-stage analysis vehicle",
    )
    return SimulationConfig(
        vehicle,
        max_time=350,
        time_step=0.5,
        wind_profile=jet_streamish(),
    )


def main():
    config = nominal_config()
    pitch = gravity_turn_program(
        start_time=10,
        end_time=120,
        terminal_angle_deg=10,
    )
    result = simulate(config, pitch)
    print(summary_block(result))

    peak_flux, peak_time = peak_heat_flux(result.samples, nose_radius=0.25)
    heat_load = total_heat_load(result.samples, nose_radius=0.25)
    print(f"peak heat flux: {peak_flux / 1e6:.2f} MW/m^2 at {peak_time:.1f} s")
    print(f"integrated heat load: {heat_load / 1e6:.1f} MJ/m^2")
    print("max-q location:", max_q_location(result))
    print("ground crossing:", impact_point(result))

    failed = engine_out(
        config,
        stage_index=0,
        engines_nominal=9,
        engines_out=1,
        at_time=25,
        pitch_program=pitch,
    )
    shortened = early_staging(
        config,
        stage_index=0,
        early_by=4,
        pitch_program=pitch,
    )
    print(f"engine-out apogee: {failed.metrics.maximum_altitude / 1000:.1f} km")
    print(f"early-stage apogee: {shortened.metrics.maximum_altitude / 1000:.1f} km")

    monte_carlo_runs, summary = run_monte_carlo(
        config,
        n=12,
        seed=7,
        pitch_program=pitch,
    )
    print_summary(summary)
    downranges = [
        run.metrics.downrange_at_apogee
        if run.metrics.downrange_at_apogee is not None
        else run.samples[-1].state.downrange
        for run in monte_carlo_runs
    ]
    center_x, center_y, major, minor, angle = footprint_ellipse(downranges)
    print(
        "downrange-only 3-sigma spread:",
        f"center={center_x:.0f} m, semi-axes={major:.0f}/{minor:.0f} m,",
        f"angle={angle:.2f} rad",
    )

    throttle_schedule = schedule_from_trajectory(result, q_limit=35_000)
    print(f"max-q schedule samples: {len(throttle_schedule)}")
    print_console(result, every=80)


if __name__ == "__main__":
    main()
