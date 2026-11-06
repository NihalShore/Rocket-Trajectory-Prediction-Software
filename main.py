#!/usr/bin/env python3
"""
Command-line entry point for the rocket trajectory simulator.

Examples
--------
    python main.py                          # default model rocket
    python main.py --config config/sounding_rocket.yaml
    python main.py --config config/model_rocket.yaml --plot
    python main.py --angle 80 --impulse 50000 --burn 6 --mass 20
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# allow running without installation
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from rocket_traj import (
    make_solid_stage,
    make_model_rocket_stage,
    SimulationEngine,
    run_simple,
)
from rocket_traj.utils.io import load_config, stages_from_config, export_csv, export_json


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Multistage rocket trajectory prediction",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to YAML/JSON vehicle config",
    )
    p.add_argument("--angle", type=float, default=85.0, help="Launch angle [deg]")
    p.add_argument("--rail", type=float, default=5.0, help="Rail length [m]")
    p.add_argument("--impulse", type=float, default=None, help="Total impulse [N·s] (single stage)")
    p.add_argument("--burn", type=float, default=5.0, help="Burn time [s]")
    p.add_argument("--prop", type=float, default=10.0, help="Propellant mass [kg]")
    p.add_argument("--dry", type=float, default=8.0, help="Dry mass [kg]")
    p.add_argument("--diameter", type=float, default=0.15, help="Body diameter [m]")
    p.add_argument("--plot", action="store_true", help="Show overview plot")
    p.add_argument("--csv", type=str, default=None, help="Write trajectory CSV")
    p.add_argument("--json", type=str, default=None, help="Write trajectory JSON")
    p.add_argument("--max-time", type=float, default=600.0, help="Simulation time limit [s]")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)

    if args.config:
        cfg = load_config(args.config)
        stages = stages_from_config(cfg)
        launch_cfg = cfg.get("launch", {})
        angle = launch_cfg.get("angle_deg", args.angle)
        rail = launch_cfg.get("rail_length", args.rail)
    elif args.impulse is not None:
        stages = [
            make_solid_stage(
                name="stage1",
                total_impulse=args.impulse,
                burn_time=args.burn,
                propellant_mass=args.prop,
                dry_mass=args.dry,
                diameter=args.diameter,
            )
        ]
        angle = args.angle
        rail = args.rail
    else:
        # default demo
        stages = [make_model_rocket_stage("C6")]
        angle = args.angle
        rail = 1.0

    eng = SimulationEngine(
        stages=stages,
        launch_angle_deg=angle,
        rail_length=rail,
        max_time=args.max_time,
    )
    traj = eng.run()

    print("=" * 50)
    print("Trajectory summary")
    print("=" * 50)
    for k, v in traj.summary().items():
        if isinstance(v, float):
            print(f"  {k:25s} {v:12.3f}")
        else:
            print(f"  {k:25s} {v}")

    print("\nEvents:")
    for ev in traj.events:
        print(f"  t = {ev['t']:8.2f} s   {ev['name']}")

    if args.csv:
        export_csv(traj, args.csv)
        print(f"\nCSV written to {args.csv}")
    if args.json:
        export_json(traj, args.json)
        print(f"JSON written to {args.json}")

    if args.plot:
        from rocket_traj.visualization import plot_overview
        import matplotlib.pyplot as plt

        fig = plot_overview(traj)
        plt.show()


if __name__ == "__main__":
    main()
