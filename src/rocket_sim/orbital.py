"""Two-body orbital mechanics helpers for post-ascent analysis."""
from dataclasses import dataclass
import math
from .constants import EARTH_MU,EARTH_RADIUS
@dataclass(frozen=True)
class OrbitalState:
    radius: float
    speed: float
    specific_energy: float
    specific_angular_momentum: float
    semi_major_axis: float|None
    eccentricity: float|None
    periapsis_altitude: float|None
    apoapsis_altitude: float|None
    period: float|None
def circular_speed(radius):
    if radius<=0: raise ValueError("radius must be positive")
    return math.sqrt(EARTH_MU/radius)
def escape_speed_at_radius(radius):
    if radius<=0: raise ValueError("radius must be positive")
    return math.sqrt(2*EARTH_MU/radius)
def vis_viva_speed(radius,semi_major_axis):
    if radius<=0 or semi_major_axis<=0: raise ValueError("radii must be positive")
    term=EARTH_MU*(2/radius-1/semi_major_axis)
    if term<0: raise ValueError("no real speed at this radius and semi-major axis")
    return math.sqrt(term)
def orbital_period(semi_major_axis):
    if semi_major_axis<=0: raise ValueError("semi-major axis must be positive")
    return 2*math.pi*math.sqrt(semi_major_axis**3/EARTH_MU)
def orbital_state(radius,radial_velocity,tangential_velocity,body_radius=EARTH_RADIUS):
    if radius<=0 or body_radius<=0: raise ValueError("radii must be positive")
    speed=math.hypot(radial_velocity,tangential_velocity)
    energy=.5*speed**2-EARTH_MU/radius
    h=radius*tangential_velocity
    if abs(energy)<1e-12:
        return OrbitalState(radius,speed,energy,h,None,None,None,None,None)
    a=-EARTH_MU/(2*energy)
    eccentricity=math.sqrt(max(0.,1+2*energy*h*h/EARTH_MU**2))
    if a>0:
        peri=a*(1-eccentricity); apo=a*(1+eccentricity)
        period=orbital_period(a)
        return OrbitalState(radius,speed,energy,h,a,eccentricity,peri-body_radius,apo-body_radius,period)
    peri=a*(1-eccentricity)
    return OrbitalState(radius,speed,energy,h,a,eccentricity,peri-body_radius,None,None)
def hohmann_transfer(r1,r2):
    if r1<=0 or r2<=0: raise ValueError("orbital radii must be positive")
    a=.5*(r1+r2)
    v1=math.sqrt(EARTH_MU/r1); v2=math.sqrt(EARTH_MU/r2)
    transfer_peri=math.sqrt(EARTH_MU*(2/r1-1/a))
    transfer_apo=math.sqrt(EARTH_MU*(2/r2-1/a))
    return {"departure_delta_v":transfer_peri-v1,"arrival_delta_v":v2-transfer_apo,
            "transfer_time":math.pi*math.sqrt(a**3/EARTH_MU)}
