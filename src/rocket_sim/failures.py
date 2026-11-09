"""Failure and contingency scenarios built from stage variants."""

from dataclasses import replace
import math

from .config import StageConfig, VehicleConfig, SimulationConfig
from .simulation import simulate
from .guidance import PitchProgram, gravity_turn_program


def _stage_at(config, stage_index):
    if not isinstance(stage_index, int) or isinstance(stage_index, bool):
        raise TypeError("stage_index must be an integer")
    if not 0 <= stage_index < len(config.vehicle.stages):
        raise IndexError("stage_index out of range")
    return config.vehicle.stages[stage_index]


def engine_out(
    config: SimulationConfig,
    stage_index=0,
    engines_nominal=9,
    engines_out=1,
    at_time=30.0,
    pitch_program=None,
):
    """Model a fixed engine-count loss by splitting the affected stage."""
    if not isinstance(engines_nominal, int) or isinstance(engines_nominal, bool):
        raise TypeError("engines_nominal must be an integer")
    if not isinstance(engines_out, int) or isinstance(engines_out, bool):
        raise TypeError("engines_out must be an integer")
    if engines_nominal < 2 or not 1 <= engines_out < engines_nominal:
        raise ValueError("engine counts must satisfy 1 <= engines_out < engines_nominal")

    stages = list(config.vehicle.stages)
    stage = _stage_at(config, stage_index)
    if not math.isfinite(at_time) or not 0.0 < at_time < stage.burn_time:
        raise ValueError("at_time must be inside the stage burn")

    remaining_thrust = (engines_nominal - engines_out) / engines_nominal
    mass_flow = stage.propellant_mass / stage.burn_time
    propellant_before = mass_flow * at_time
    propellant_after = stage.propellant_mass - propellant_before

    # Keep the original dry mass on the post-failure segment.
    dry_mass_sliver = min(stage.dry_mass / 2.0, 1e-9)
    pre_failure = StageConfig(
        name=stage.name + "_pre",
        dry_mass=dry_mass_sliver,
        propellant_mass=propellant_before,
        thrust_vacuum=stage.thrust_vacuum,
        burn_time=at_time,
        thrust_sea_level=stage.thrust_sea_level,
        specific_impulse_vacuum=stage.specific_impulse_vacuum,
        specific_impulse_sea_level=stage.specific_impulse_sea_level,
    )
    post_failure = StageConfig(
        name=stage.name + "_post",
        dry_mass=stage.dry_mass - dry_mass_sliver,
        propellant_mass=propellant_after,
        thrust_vacuum=stage.thrust_vacuum * remaining_thrust,
        burn_time=stage.burn_time - at_time,
        thrust_sea_level=(
            stage.thrust_sea_level * remaining_thrust
            if stage.thrust_sea_level is not None
            else None
        ),
        specific_impulse_vacuum=stage.specific_impulse_vacuum,
        specific_impulse_sea_level=stage.specific_impulse_sea_level,
        fairing_mass=stage.fairing_mass,
        separation_time=stage.separation_time,
    )

    new_stages = stages[:stage_index] + [pre_failure, post_failure] + stages[stage_index + 1 :]
    vehicle = VehicleConfig(
        new_stages,
        payload_mass=config.vehicle.payload_mass,
        reference_area=config.vehicle.reference_area,
        drag_coefficient=config.vehicle.drag_coefficient,
        nose_drag_coefficient=config.vehicle.nose_drag_coefficient,
        name=config.vehicle.name + f" (engine out x{engines_out})",
    )
    return simulate(
        replace(config, vehicle=vehicle),
        pitch_program or gravity_turn_program(),
    )


def early_staging(
    config: SimulationConfig,
    stage_index=0,
    early_by=5.0,
    pitch_program=None,
):
    """End one stage early, carrying only the propellant burned before cutoff."""
    stages = list(config.vehicle.stages)
    stage = _stage_at(config, stage_index)
    if not math.isfinite(early_by) or not 0.0 < early_by < stage.burn_time:
        raise ValueError("early_by must be positive and shorter than the stage burn")

    new_burn_time = stage.burn_time - early_by
    propellant_fraction = new_burn_time / stage.burn_time
    shortened = StageConfig(
        name=stage.name + "_early",
        dry_mass=stage.dry_mass,
        propellant_mass=stage.propellant_mass * propellant_fraction,
        thrust_vacuum=stage.thrust_vacuum,
        burn_time=new_burn_time,
        thrust_sea_level=stage.thrust_sea_level,
        specific_impulse_vacuum=stage.specific_impulse_vacuum,
        specific_impulse_sea_level=stage.specific_impulse_sea_level,
        fairing_mass=stage.fairing_mass,
        separation_time=stage.separation_time,
    )
    new_stages = stages[:stage_index] + [shortened] + stages[stage_index + 1 :]
    vehicle = VehicleConfig(
        new_stages,
        payload_mass=config.vehicle.payload_mass,
        reference_area=config.vehicle.reference_area,
        drag_coefficient=config.vehicle.drag_coefficient,
        nose_drag_coefficient=config.vehicle.nose_drag_coefficient,
        name=config.vehicle.name + " (early stage)",
    )
    return simulate(
        replace(config, vehicle=vehicle),
        pitch_program or gravity_turn_program(),
    )


def stuck_throttle(
    config: SimulationConfig,
    stage_index=0,
    throttle=0.7,
    pitch_program=None,
):
    """Apply a constant thrust derate to one stage."""
    stages = list(config.vehicle.stages)
    stage = _stage_at(config, stage_index)
    if not math.isfinite(throttle) or not 0.0 < throttle <= 1.0:
        raise ValueError("throttle must be in (0, 1]")

    derated = StageConfig(
        name=stage.name + f"_thr{throttle}",
        dry_mass=stage.dry_mass,
        propellant_mass=stage.propellant_mass,
        thrust_vacuum=stage.thrust_vacuum * throttle,
        burn_time=stage.burn_time,
        thrust_sea_level=(
            stage.thrust_sea_level * throttle
            if stage.thrust_sea_level is not None
            else None
        ),
        specific_impulse_vacuum=stage.specific_impulse_vacuum,
        specific_impulse_sea_level=stage.specific_impulse_sea_level,
        fairing_mass=stage.fairing_mass,
        separation_time=stage.separation_time,
    )
    new_stages = stages[:stage_index] + [derated] + stages[stage_index + 1 :]
    vehicle = VehicleConfig(
        new_stages,
        payload_mass=config.vehicle.payload_mass,
        reference_area=config.vehicle.reference_area,
        drag_coefficient=config.vehicle.drag_coefficient,
        nose_drag_coefficient=config.vehicle.nose_drag_coefficient,
        name=config.vehicle.name + f" (throttle {throttle})",
    )
    return simulate(
        replace(config, vehicle=vehicle),
        pitch_program or gravity_turn_program(),
    )
