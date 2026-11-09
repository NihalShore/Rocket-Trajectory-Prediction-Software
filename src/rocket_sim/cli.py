"""Command-line interface for the ascent simulator."""

from __future__ import annotations

import argparse

from .config import SimulationConfig, StageConfig, VehicleConfig
from .guidance import gravity_turn_program
from .serialization import write_csv, write_json
from .simulation import simulate


def build_vehicle(kind: str = "demo") -> VehicleConfig:
    if kind == "small":
        stage = StageConfig(
            "stage1",
            dry_mass=100.0,
            propellant_mass=400.0,
            thrust_vacuum=12000.0,
            burn_time=20.0,
        )
        return VehicleConfig(
            [stage],
            payload_mass=30.0,
            reference_area=0.8,
            drag_coefficient=0.4,
            name="small solid",
        )

    first = StageConfig(
        "first",
        dry_mass=25000.0,
        propellant_mass=180000.0,
        thrust_vacuum=4.2e6,
        burn_time=125.0,
        thrust_sea_level=3.5e6,
    )
    second = StageConfig(
        "second",
        dry_mass=6500.0,
        propellant_mass=42000.0,
        thrust_vacuum=9.0e5,
        burn_time=110.0,
        specific_impulse_vacuum=340.0,
    )
    return VehicleConfig(
        [first, second],
        payload_mass=1800.0,
        reference_area=10.5,
        drag_coefficient=0.32,
        name="two-stage reference",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a point-mass rocket ascent.")
    parser.add_argument("--vehicle", choices=("demo", "small"), default="demo")
    parser.add_argument("--step", type=float, default=0.2, help="integrator step [s]")
    parser.add_argument("--max-time", type=float, default=700.0, help="simulation limit [s]")
    parser.add_argument("--output", help="write JSON results to this path")
    parser.add_argument("--csv", help="write CSV telemetry to this path")
    parser.add_argument("--plot", action="store_true", help="show the trajectory plot")
    parser.add_argument(
        "--stop-apogee",
        action="store_true",
        help="stop when vertical velocity crosses zero",
    )
    args = parser.parse_args(argv)

    vehicle = build_vehicle(args.vehicle)
    config = SimulationConfig(
        vehicle,
        max_time=args.max_time,
        time_step=args.step,
        stop_at_apogee=args.stop_apogee,
    )
    pitch = gravity_turn_program(
        start_time=12.0,
        end_time=145.0,
        terminal_angle_deg=8.0,
    )
    result = simulate(config, pitch)

    metrics = result.metrics
    print(f"vehicle : {vehicle.name}")
    print(f"samples : {len(result.samples)}")
    print(f"apogee  : {metrics.maximum_altitude / 1000:.2f} km  @ t={metrics.apogee_time} s")
    print(f"max V   : {metrics.maximum_speed:.1f} m/s")
    print(f"max q   : {metrics.maximum_dynamic_pressure / 1000:.1f} kPa")
    print(f"max mach: {metrics.maximum_mach:.2f}")
    print(f"final m : {metrics.final_mass:.1f} kg")
    print("events:")
    for event in result.events:
        print(f"  t={event.time:8.2f}s  {event.name}")

    if args.output:
        write_json(result, args.output)
        print(f"wrote {args.output}")
    if args.csv:
        write_csv(result, args.csv)
        print(f"wrote {args.csv}")
    if args.plot:
        from .plotting import plot_trajectory

        plot_trajectory(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
