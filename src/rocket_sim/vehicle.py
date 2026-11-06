"""Vehicle mass bookkeeping and ideal staging estimates."""
from dataclasses import dataclass
from .config import VehicleConfig
from .constants import G0
@dataclass(frozen=True)
class MassBreakdown:
    payload: float
    dry: float
    propellant: float
    fairings: float
    total: float
def mass_breakdown(vehicle: VehicleConfig):
    dry=sum(s.dry_mass for s in vehicle.stages)
    prop=sum(s.propellant_mass for s in vehicle.stages)
    fairings=sum(s.fairing_mass for s in vehicle.stages)
    return MassBreakdown(vehicle.payload_mass,dry,prop,fairings,vehicle.initial_mass)
def stage_mass_ratios(vehicle: VehicleConfig):
    carried=vehicle.payload_mass
    ratios=[]
    for stage in reversed(vehicle.stages):
        wet=stage.dry_mass+stage.propellant_mass+carried
        dry=stage.dry_mass+carried
        ratios.append(wet/dry)
        carried=wet
    return tuple(reversed(ratios))
def ideal_vehicle_delta_v(vehicle: VehicleConfig):
    carried=vehicle.payload_mass
    total=0.
    for stage in reversed(vehicle.stages):
        ve=stage.thrust_vacuum/(stage.propellant_mass/stage.burn_time)
        total+=ve*__import__("math").log((stage.dry_mass+stage.propellant_mass+carried)/(stage.dry_mass+carried))
        carried+=stage.dry_mass+stage.propellant_mass+stage.fairing_mass
    return total
def thrust_to_weight(thrust,mass,gravity=G0):
    if mass<=0 or gravity<=0: raise ValueError("mass and gravity must be positive")
    return thrust/(mass*gravity)
