"""Failure / contingency cases.

Engine-out, stuck throttle, early staging — the kind of stuff you run
when someone asks "what if one engine dies at T+30".
"""
from dataclasses import replace
from .config import StageConfig, VehicleConfig, SimulationConfig
from .simulation import simulate
from .guidance import PitchProgram, gravity_turn_program


def engine_out(config: SimulationConfig, stage_index=0, engines_nominal=9, engines_out=1,
               at_time=30.0, pitch_program=None):
    """
    Scale stage thrust + mass flow as if some engines shut down at at_time.

    Hack: we don't have time-varying thrust in StageConfig, so we split the
    stage into two pseudo-stages — pre-failure and post-failure.
    """
    if engines_out >= engines_nominal:
        raise ValueError("that'd be all engines out, vehicle falls")
    if stage_index >= len(config.vehicle.stages):
        raise IndexError("stage_index out of range")

    stages = list(config.vehicle.stages)
    s = stages[stage_index]
    frac_remaining = (engines_nominal - engines_out) / engines_nominal

    t_fail = min(at_time, s.burn_time)
    mdot = s.propellant_mass / s.burn_time
    prop_before = mdot * t_fail
    prop_after = s.propellant_mass - prop_before
    if prop_after < 0:
        prop_after = 0.0
        prop_before = s.propellant_mass

    pre = StageConfig(
        name=s.name + "_pre",
        dry_mass=0.01,
        propellant_mass=max(prop_before, 0.01),
        thrust_vacuum=s.thrust_vacuum,
        burn_time=max(t_fail, 0.01),
        thrust_sea_level=s.thrust_sea_level,
        fairing_mass=0.0,
    )
    post = StageConfig(
        name=s.name + "_post",
        dry_mass=s.dry_mass,
        propellant_mass=max(prop_after, 0.01),
        thrust_vacuum=s.thrust_vacuum * frac_remaining,
        burn_time=max(s.burn_time - t_fail, 0.01),
        thrust_sea_level=(s.thrust_sea_level * frac_remaining) if s.thrust_sea_level else None,
        fairing_mass=s.fairing_mass,
    )
    new_stages = stages[:stage_index] + [pre, post] + stages[stage_index + 1 :]
    vehicle = VehicleConfig(
        new_stages,
        payload_mass=config.vehicle.payload_mass,
        reference_area=config.vehicle.reference_area,
        drag_coefficient=config.vehicle.drag_coefficient,
        name=config.vehicle.name + f" (engine out x{engines_out})",
    )
    cfg = replace(config, vehicle=vehicle)
    pitch = pitch_program or gravity_turn_program()
    return simulate(cfg, pitch)


def early_staging(config: SimulationConfig, stage_index=0, early_by=5.0, pitch_program=None):
    """Cut the stage burn short by early_by seconds."""
    stages = list(config.vehicle.stages)
    s = stages[stage_index]
    new_burn = max(0.5, s.burn_time - early_by)
    scale = new_burn / s.burn_time
    s2 = StageConfig(
        name=s.name + "_early",
        dry_mass=s.dry_mass,
        propellant_mass=s.propellant_mass * scale,
        thrust_vacuum=s.thrust_vacuum,
        burn_time=new_burn,
        thrust_sea_level=s.thrust_sea_level,
        fairing_mass=s.fairing_mass,
    )
    new_stages = stages[:stage_index] + [s2] + stages[stage_index + 1 :]
    vehicle = VehicleConfig(
        new_stages,
        payload_mass=config.vehicle.payload_mass,
        reference_area=config.vehicle.reference_area,
        drag_coefficient=config.vehicle.drag_coefficient,
        name=config.vehicle.name + " (early stage)",
    )
    cfg = replace(config, vehicle=vehicle)
    return simulate(cfg, pitch_program or gravity_turn_program())


def stuck_throttle(config: SimulationConfig, stage_index=0, throttle=0.7, pitch_program=None):
    """Constant derate on one stage."""
    stages = list(config.vehicle.stages)
    s = stages[stage_index]
    s2 = StageConfig(
        name=s.name + f"_thr{throttle}",
        dry_mass=s.dry_mass,
        propellant_mass=s.propellant_mass,
        thrust_vacuum=s.thrust_vacuum * throttle,
        burn_time=s.burn_time,
        thrust_sea_level=(s.thrust_sea_level * throttle) if s.thrust_sea_level else None,
        fairing_mass=s.fairing_mass,
    )
    new_stages = stages[:stage_index] + [s2] + stages[stage_index + 1 :]
    vehicle = VehicleConfig(
        new_stages,
        payload_mass=config.vehicle.payload_mass,
        reference_area=config.vehicle.reference_area,
        drag_coefficient=config.vehicle.drag_coefficient,
        name=config.vehicle.name + f" (throttle {throttle})",
    )
    return simulate(replace(config, vehicle=vehicle), pitch_program or gravity_turn_program())
