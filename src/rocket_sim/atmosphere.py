"""Layered lower-atmosphere model and transport properties."""
from dataclasses import dataclass
import math
from .constants import AIR_GAS_CONSTANT,G0,SEA_LEVEL_PRESSURE,SEA_LEVEL_TEMPERATURE,SUTHERLAND_CONSTANT,SUTHERLAND_REFERENCE_TEMPERATURE,SUTHERLAND_REFERENCE_VISCOSITY
@dataclass(frozen=True)
class AtmosphericState:
    altitude: float
    temperature: float
    pressure: float
    density: float
    speed_of_sound: float
    dynamic_viscosity: float
    @property
    def kinematic_viscosity(self): return self.dynamic_viscosity/self.density if self.density>0 else math.inf
    @property
    def scale_height(self): return AIR_GAS_CONSTANT*self.temperature/G0
_LAYERS=((0.,11000.,-.0065),(11000.,20000.,0.),(20000.,32000.,.001),(32000.,47000.,.0028),(47000.,51000.,0.),(51000.,71000.,-.0028),(71000.,86000.,-.002))
def _layer_state(h):
    temperature=SEA_LEVEL_TEMPERATURE; pressure=SEA_LEVEL_PRESSURE; base=0.
    for lower,upper,lapse in _LAYERS:
        if h<=lower: break
        span=min(h,upper)-lower
        if span<=0: continue
        t0=temperature
        if abs(lapse)<1e-12: pressure*=math.exp(-G0*span/(AIR_GAS_CONSTANT*t0))
        else:
            temperature=t0+lapse*span
            pressure*=(temperature/t0)**(-G0/(AIR_GAS_CONSTANT*lapse))
        base=upper
        if h<=upper: break
    if h>base: pressure*=math.exp(-G0*(h-base)/(AIR_GAS_CONSTANT*temperature))
    return temperature,pressure
def atmosphere(altitude,model="ussa1976"):
    if altitude<0: raise ValueError("altitude cannot be negative")
    if model=="exponential":
        density=1.225*math.exp(-altitude/8500.)
        temperature=max(180.,288.15-.0065*min(altitude,11000.))
        pressure=density*AIR_GAS_CONSTANT*temperature
    elif model=="ussa1976":
        temperature,pressure=_layer_state(altitude); density=pressure/(AIR_GAS_CONSTANT*temperature)
    else: raise ValueError(f"unknown atmosphere model: {model}")
    sound=math.sqrt(1.4*AIR_GAS_CONSTANT*temperature)
    viscosity=SUTHERLAND_REFERENCE_VISCOSITY*(temperature/SUTHERLAND_REFERENCE_TEMPERATURE)**1.5*(SUTHERLAND_REFERENCE_TEMPERATURE+SUTHERLAND_CONSTANT)/(temperature+SUTHERLAND_CONSTANT)
    return AtmosphericState(altitude,temperature,pressure,density,sound,viscosity)
def pressure_at_altitude(altitude,model="ussa1976"): return atmosphere(altitude,model).pressure
def density_at_altitude(altitude,model="ussa1976"): return atmosphere(altitude,model).density
def speed_of_sound(altitude,model="ussa1976"): return atmosphere(altitude,model).speed_of_sound
