"""Aerodynamic loads with a generic transonic drag-rise approximation."""
from dataclasses import dataclass
import math
from .atmosphere import atmosphere
@dataclass(frozen=True)
class AeroLoads:
    mach: float
    reynolds: float
    dynamic_pressure: float
    drag: float
    drag_coefficient: float
def drag_coefficient(mach,base_cd=.35):
    if base_cd<0: raise ValueError("base_cd cannot be negative")
    m=abs(mach); rise=.28*math.exp(-((m-1.)/.22)**2)
    relief=.06*(1-math.exp(-max(0.,m-1.)/2.))
    return max(0.,base_cd+rise-relief)
def aerodynamic_loads(altitude,speed,area,base_cd=.35,model="ussa1976"):
    if area<=0: raise ValueError("area must be positive")
    atm=atmosphere(altitude,model); q=.5*atm.density*speed*speed
    mach=abs(speed)/atm.speed_of_sound; cd=drag_coefficient(mach,base_cd)
    reynolds=atm.density*abs(speed)*math.sqrt(area/math.pi)/atm.dynamic_viscosity
    return AeroLoads(mach,reynolds,q,q*area*cd,cd)
