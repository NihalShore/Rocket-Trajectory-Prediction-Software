#!/usr/bin/env python3
"""
Kitchen-sink demo:
  - monte carlo
  - engine-out
  - aeroheating
  - range safety footprint
  - thrust table
  - telemetry dump
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rocket_sim.config import StageConfig, VehicleConfig, SimulationConfig
from rocket_sim.guidance import gravity_turn_program
from rocket_sim.simulation import simulate
from rocket_sim.uncertainty import run_monte_carlo, print_summary
from rocket_sim.failures import engine_out, early_staging
from rocket_sim.aeroheating import peak_heat_flux, total_heat_load
from rocket_sim.range_safety import impact_point, footprint_ellipse, max_q_location
from rocket_sim.thrust_tables import fake_o_motor
from rocket_sim.telemetry import summary_block, print_console
from rocket_sim.winds import jet_streamish


def nominal():
    s1 = StageConfig("S1", 8000, 45000, 1.1e6, 80, 0.95e6)
    s2 = StageConfig("S2", 2000, 12000, 2.5e5, 90, specific_impulse_vacuum=320)
    veh = VehicleConfig([s1, s2], payload_mass=500, reference_area=3.5, drag_coefficient=0.35, name="demo")
    return SimulationConfig(veh, max_time=400, time_step=0.25)


def main():
    cfg = nominal()
    pitch = gravity_turn_program(10, 120, 10)
    print("=== nominal ===")
    r = simulate(cfg, pitch)
    print(summary_block(r))

    print("\n=== aeroheating (Sutton-Graves, Rn=0.25m) ===")
    peak, tpeak = peak_heat_flux(r.samples, nose_radius=0.25)
    load = total_heat_load(r.samples, nose_radius=0.25)
    print(f"  peak flux {peak/1e6:.2f} MW/m^2 @ t={tpeak:.1f}s")
    print(f"  integrated load {load/1e6:.1f} MJ/m^2")

    print("\n=== max-q location ===")
    print(" ", max_q_location(r))

    print("\n=== impact ===")
    print(" ", impact_point(r))

    print("\n=== engine out (1 of 9 @ T+25 on S1) ===")
    r_eo = engine_out(cfg, stage_index=0, engines_nominal=9, engines_out=1, at_time=25.0, pitch_program=pitch)
    print(f"  apogee {r_eo.metrics.maximum_altitude/1000:.1f} km  (was {r.metrics.maximum_altitude/1000:.1f})")

    print("\n=== early staging (-4s on S1) ===")
    r_es = early_staging(cfg, stage_index=0, early_by=4.0, pitch_program=pitch)
    print(f"  apogee {r_es.metrics.maximum_altitude/1000:.1f} km")

    print("\n=== monte carlo (n=25) ===")
    def prog(i, n):
        print(f"  ... {i}/{n}")
    _, summary = run_monte_carlo(cfg, n=25, seed=7, pitch_program=pitch, progress=prog)
    print_summary(summary)

    results, _ = run_monte_carlo(cfg, n=20, seed=7, pitch_program=pitch)
    drs = [rr.metrics.downrange_at_apogee or 0.0 for rr in results]
    mx, my, a, b, ang = footprint_ellipse(drs)
    print(f"\n=== 3-sigma footprint ===")
    print(f"  center downrange={mx:.0f}m  semi-axes={a:.0f}/{b:.0f}m  angle={ang:.2f}rad")

    print("\n=== thrust table peek ===")
    tab = fake_o_motor()
    print(f"  O-ish motor: Itot={tab.total_impulse:.0f} N·s  burn={tab.burn_time}s  F(1s)={tab.thrust_at(1):.0f}N")

    print("\n=== wind profile sample ===")
    w = jet_streamish()
    for h in (0, 5000, 12000, 30000):
        v = w.at(h)
        print(f"  h={h:5d}m  east={v.east:5.1f}  north={v.north:5.1f}  |V|={v.speed:.1f}")

    print("\n=== telemetry strip ===")
    print_console(r, every=40)


if __name__ == "__main__":
    main()
