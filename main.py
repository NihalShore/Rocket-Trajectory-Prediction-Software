#!/usr/bin/env python3
"""
Quick CLI for the trajectory sim.

Examples:
  python main.py
  python main.py --step 0.1 --plot
  python main.py --output out.json --csv out.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from rocket_sim.config import StageConfig, VehicleConfig, SimulationConfig
from rocket_sim.guidance import gravity_turn_program
from rocket_sim.simulation import simulate
from rocket_sim.serialization import write_csv, write_json


def build_vehicle(kind: str = "demo"):
    if kind == "small":
        # short solid, useful for quick checks
        stage = StageConfig("stage1", dry_mass=100.0, propellant_mass=400.0,
                            thrust_vacuum=12000.0, burn_time=20.0)
        return VehicleConfig([stage], payload_mass=30.0, reference_area=0.8,
                             drag_coefficient=0.4, name="small solid")
    # default: two-stage conceptual vehicle
    first = StageConfig("first", dry_mass=25000.0, propellant_mass=180000.0,
                        thrust_vacuum=4.2e6, burn_time=125.0, thrust_sea_level=3.5e6)
    second = StageConfig("second", dry_mass=6500.0, propellant_mass=42000.0,
                         thrust_vacuum=9.0e5, burn_time=110.0,
                         specific_impulse_vacuum=340.0)
    return VehicleConfig([first, second], payload_mass=1800.0, reference_area=10.5,
                         drag_coefficient=0.32, name="two-stage reference")


def main(argv=None):
    p = argparse.ArgumentParser(description="point-mass rocket ascent")
    p.add_argument("--vehicle", choices=["demo", "small"], default="demo")
    p.add_argument("--step", type=float, default=0.2, help="integrator step [s]")
    p.add_argument("--max-time", type=float, default=700.0)
    p.add_argument("--output", default=None, help="json path")
    p.add_argument("--csv", default=None, help="csv path")
    p.add_argument("--plot", action="store_true")
    p.add_argument("--stop-apogee", action="store_true")
    args = p.parse_args(argv)

    vehicle = build_vehicle(args.vehicle)
    config = SimulationConfig(
        vehicle,
        max_time=args.max_time,
        time_step=args.step,
        stop_at_apogee=args.stop_apogee,
    )
    pitch = gravity_turn_program(12.0, 145.0, 8.0)
    result = simulate(config, pitch)

    m = result.metrics
    print(f"vehicle : {vehicle.name}")
    print(f"samples : {len(result.samples)}")
    print(f"apogee  : {m.maximum_altitude/1000:.2f} km  @ t={m.apogee_time} s")
    print(f"max V   : {m.maximum_speed:.1f} m/s")
    print(f"max q   : {m.maximum_dynamic_pressure/1000:.1f} kPa")
    print(f"max mach: {m.maximum_mach:.2f}")
    print(f"final m : {m.final_mass:.1f} kg")
    print("events:")
    for e in result.events:
        print(f"  t={e.time:8.2f}s  {e.name}")

    if args.output:
        write_json(result, args.output)
        print(f"wrote {args.output}")
    if args.csv:
        write_csv(result, args.csv)
        print(f"wrote {args.csv}")
    if args.plot:
        from rocket_sim.plotting import plot_trajectory
        plot_trajectory(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
