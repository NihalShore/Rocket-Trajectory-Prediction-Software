"""Monte Carlo dispersion.

Perturb a few knobs, rerun, collect stats. Not a full UQ pipeline.
"""
from dataclasses import dataclass, replace
import math
import random
import numpy as np

from .config import StageConfig, VehicleConfig, SimulationConfig
from .simulation import simulate
from .guidance import gravity_turn_program, PitchProgram


@dataclass(frozen=True)
class MonteCarloSummary:
    parameter: str
    count: int
    mean: float
    standard_deviation: float
    minimum: float
    maximum: float
    p05: float
    p50: float
    p95: float


def _stats(name, values):
    a = np.asarray(values, dtype=float)
    if len(a) == 0:
        return MonteCarloSummary(name, 0, 0, 0, 0, 0, 0, 0, 0)
    return MonteCarloSummary(
        name, len(a),
        float(np.mean(a)), float(np.std(a)),
        float(np.min(a)), float(np.max(a)),
        float(np.percentile(a, 5)), float(np.percentile(a, 50)), float(np.percentile(a, 95)),
    )


def _jitter_stage(stage, rng, thrust_sigma=0.03, mass_sigma=0.02):
    tf = max(0.5, rng.gauss(1.0, thrust_sigma))
    mf = max(0.5, rng.gauss(1.0, mass_sigma))
    curve = (
        tuple((time, thrust * tf) for time, thrust in stage.thrust_curve)
        if stage.thrust_curve is not None else None
    )
    return StageConfig(
        name=stage.name,
        dry_mass=max(1.0, stage.dry_mass * rng.gauss(1.0, mass_sigma)),
        propellant_mass=max(1.0, stage.propellant_mass * mf),
        thrust_vacuum=stage.thrust_vacuum * tf,
        burn_time=stage.burn_time,
        thrust_sea_level=(stage.thrust_sea_level * tf) if stage.thrust_sea_level else None,
        specific_impulse_vacuum=stage.specific_impulse_vacuum,
        specific_impulse_sea_level=stage.specific_impulse_sea_level,
        fairing_mass=stage.fairing_mass,
        separation_time=stage.separation_time,
        thrust_curve=curve,
    )


def run_monte_carlo(
    base_config,
    n=50,
    thrust_sigma=0.03,
    mass_sigma=0.02,
    cd_sigma=0.05,
    pitch_program=None,
    seed=None,
    progress=None,
):
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")
    for name, sigma in (
        ("thrust_sigma", thrust_sigma),
        ("mass_sigma", mass_sigma),
        ("cd_sigma", cd_sigma),
    ):
        if not math.isfinite(sigma) or sigma < 0:
            raise ValueError(f"{name} must be finite and nonnegative")

    rng = random.Random(seed)
    pitch = pitch_program or gravity_turn_program()
    results = []
    apogees, max_qs, max_speeds, downranges = [], [], [], []

    for i in range(n):
        stages = [_jitter_stage(s, rng, thrust_sigma, mass_sigma) for s in base_config.vehicle.stages]
        cd = max(0.05, base_config.vehicle.drag_coefficient * rng.gauss(1.0, cd_sigma))
        vehicle = VehicleConfig(
            stages,
            payload_mass=base_config.vehicle.payload_mass,
            reference_area=base_config.vehicle.reference_area,
            drag_coefficient=cd,
            nose_drag_coefficient=base_config.vehicle.nose_drag_coefficient,
            name=base_config.vehicle.name,
        )
        cfg = replace(base_config, vehicle=vehicle)
        r = simulate(cfg, pitch)
        results.append(r)
        apogees.append(r.metrics.maximum_altitude)
        max_qs.append(r.metrics.maximum_dynamic_pressure)
        max_speeds.append(r.metrics.maximum_speed)
        if r.metrics.downrange_at_apogee is not None:
            downranges.append(r.metrics.downrange_at_apogee)
        else:
            downranges.append(r.samples[-1].state.downrange if r.samples else 0.0)
        if progress and (i + 1) % max(1, n // 10) == 0:
            progress(i + 1, n)

    summary = {
        "apogee_m": _stats("apogee_m", apogees),
        "max_q_pa": _stats("max_q_pa", max_qs),
        "max_speed_ms": _stats("max_speed_ms", max_speeds),
        "downrange_m": _stats("downrange_m", downranges),
        "n_ok": len(results),
        "n_requested": n,
    }
    return results, summary


def print_summary(summary):
    for key in ("apogee_m", "max_q_pa", "max_speed_ms", "downrange_m"):
        s = summary[key]
        print(f"{key:16s}  mean={s.mean:10.1f}  std={s.standard_deviation:10.1f}  "
              f"p05={s.p05:10.1f}  p95={s.p95:10.1f}")
    print(f"completed {summary['n_ok']}/{summary['n_requested']}")


@dataclass(frozen=True)
class SampleSummary:
    name: str
    count: int
    mean: float
    standard_deviation: float
    minimum: float
    maximum: float
    percentile_5: float
    percentile_50: float
    percentile_95: float


def sample_normal(mean, std, n, seed=None):
    rng = np.random.default_rng(seed)
    return rng.normal(mean, std, size=int(n))


def summarize(name, values):
    a = np.asarray(list(values), dtype=float)
    if len(a) == 0:
        return SampleSummary(name, 0, 0, 0, 0, 0, 0, 0, 0)
    return SampleSummary(
        name, len(a),
        float(np.mean(a)), float(np.std(a)),
        float(np.min(a)), float(np.max(a)),
        float(np.percentile(a, 5)), float(np.percentile(a, 50)), float(np.percentile(a, 95)),
    )
