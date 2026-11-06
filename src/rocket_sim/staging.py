"""Stage sequence inspection and deterministic burnout schedule helpers."""
from dataclasses import dataclass
from .config import VehicleConfig
@dataclass(frozen=True)
class StageScheduleEntry:
    index: int
    name: str
    ignition_time: float
    burnout_time: float
    separation_mass: float
def stage_schedule(vehicle: VehicleConfig,first_ignition=0.):
    if first_ignition<0: raise ValueError("first ignition time cannot be negative")
    result=[]; clock=float(first_ignition)
    for index,stage in enumerate(vehicle.stages):
        burnout=clock+stage.burn_time
        result.append(StageScheduleEntry(index,stage.name,clock,burnout,stage.dry_mass+stage.fairing_mass))
        clock=burnout
    return tuple(result)
def cumulative_burn_time(vehicle): return sum(stage.burn_time for stage in vehicle.stages)
def propellant_fraction(vehicle):
    total=vehicle.initial_mass
    return sum(s.propellant_mass for s in vehicle.stages)/total
def dry_mass_fraction(vehicle):
    return (vehicle.payload_mass+sum(s.dry_mass+s.fairing_mass for s in vehicle.stages))/vehicle.initial_mass
