"""Stage-level performance and thrust-to-weight calculations."""
from dataclasses import dataclass
import math
from .constants import G0
@dataclass(frozen=True)
class StagePerformance:
    mass_flow: float
    effective_exhaust_velocity: float
    specific_impulse: float
    initial_thrust_to_weight: float
    final_thrust_to_weight: float
    ideal_delta_v: float
def stage_performance(stage,carried_mass,ambient_gravity=G0):
    if carried_mass<=0 or ambient_gravity<=0: raise ValueError("carried mass and gravity must be positive")
    flow=stage.propellant_mass/stage.burn_time
    ve=stage.thrust_vacuum/flow
    initial=stage.dry_mass+stage.propellant_mass+carried_mass
    final=stage.dry_mass+carried_mass
    return StagePerformance(flow,ve,ve/G0,stage.thrust_vacuum/(initial*ambient_gravity),
                            stage.thrust_vacuum/(final*ambient_gravity),ve*math.log(initial/final))
def vehicle_performance(vehicle,ambient_gravity=G0):
    carried=vehicle.payload_mass
    reports=[]
    for stage in reversed(vehicle.stages):
        reports.append(stage_performance(stage,carried,ambient_gravity))
        carried+=stage.dry_mass+stage.propellant_mass+stage.fairing_mass
    return tuple(reversed(reports))
