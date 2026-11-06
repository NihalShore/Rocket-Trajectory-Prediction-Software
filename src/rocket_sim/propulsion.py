"""Ideal rocket equation and simple engine performance relationships."""
import math
from dataclasses import dataclass
from .constants import G0
@dataclass(frozen=True)
class EnginePerformance:
    thrust: float
    mass_flow: float
    effective_exhaust_velocity: float
    specific_impulse: float
def performance_from_isp(thrust,specific_impulse):
    if thrust<0 or specific_impulse<=0: raise ValueError("invalid thrust or Isp")
    flow=thrust/(specific_impulse*G0)
    return EnginePerformance(thrust,flow,specific_impulse*G0,specific_impulse)
def ideal_rocket_delta_v(initial_mass,final_mass,exhaust_velocity):
    if initial_mass<=final_mass or final_mass<=0 or exhaust_velocity<=0: raise ValueError("require initial > final > 0 and positive exhaust velocity")
    return exhaust_velocity*math.log(initial_mass/final_mass)
def stage_delta_v(dry_mass,propellant_mass,carried_mass,isp):
    if min(dry_mass,propellant_mass,carried_mass,isp)<=0: raise ValueError("all inputs must be positive")
    return ideal_rocket_delta_v(dry_mass+propellant_mass+carried_mass,dry_mass+carried_mass,isp*G0)
def thrust_at_pressure(vacuum_thrust,exit_area,ambient_pressure,reference_pressure=0.):
    if min(vacuum_thrust,exit_area,ambient_pressure)<0: raise ValueError("inputs cannot be negative")
    return max(0.,vacuum_thrust-(ambient_pressure-reference_pressure)*exit_area)
def engine_performance(thrust,mass_flow):
    if thrust<0 or mass_flow<=0: raise ValueError("invalid thrust or flow")
    ve=thrust/mass_flow
    return EnginePerformance(thrust,mass_flow,ve,ve/G0)
