"""Aerodynamic loads using velocity relative to an interpolated wind field."""
from dataclasses import dataclass
import math
from .aerodynamics import aerodynamic_loads
from .winds import WindProfile
@dataclass(frozen=True)
class RelativeFlow:
    horizontal: float
    vertical: float
    speed: float
    flight_path_angle: float
def relative_flow(vehicle_horizontal,vehicle_vertical,wind_horizontal,wind_vertical):
    horizontal=vehicle_horizontal-wind_horizontal
    vertical=vehicle_vertical-wind_vertical
    return RelativeFlow(horizontal,vertical,math.hypot(horizontal,vertical),math.atan2(vertical,horizontal))
def loads_with_wind(altitude,vehicle_horizontal,vehicle_vertical,area,base_cd,wind_profile: WindProfile,model="ussa1976"):
    wind=wind_profile.at(altitude)
    flow=relative_flow(vehicle_horizontal,vehicle_vertical,wind.east,wind.vertical)
    loads=aerodynamic_loads(altitude,flow.speed,area,base_cd,model)
    return flow,loads
