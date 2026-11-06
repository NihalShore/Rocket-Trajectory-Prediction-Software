"""Validated immutable configuration records."""
from dataclasses import dataclass, field
from typing import Sequence
@dataclass(frozen=True)
class StageConfig:
    name: str
    dry_mass: float
    propellant_mass: float
    thrust_vacuum: float
    burn_time: float
    thrust_sea_level: float|None=None
    specific_impulse_vacuum: float|None=None
    specific_impulse_sea_level: float|None=None
    fairing_mass: float=0.0
    separation_time: float=0.0
    def __post_init__(self):
        for key in ("dry_mass","propellant_mass","thrust_vacuum","burn_time"):
            if getattr(self,key)<=0: raise ValueError(f"{key} must be positive")
        if self.fairing_mass<0 or self.separation_time<0: raise ValueError("optional masses and times cannot be negative")
        if self.thrust_sea_level is not None and not 0<self.thrust_sea_level<=self.thrust_vacuum: raise ValueError("invalid sea-level thrust")
        for key in ("specific_impulse_vacuum","specific_impulse_sea_level"):
            value=getattr(self,key)
            if value is not None and value<=0: raise ValueError(f"{key} must be positive")
    @property
    def mass_flow_rate(self):
        if self.specific_impulse_vacuum:
            from .constants import G0
            return self.thrust_vacuum/(self.specific_impulse_vacuum*G0)
        return self.propellant_mass/self.burn_time
@dataclass(frozen=True)
class VehicleConfig:
    stages: Sequence[StageConfig]
    payload_mass: float
    reference_area: float
    drag_coefficient: float=0.35
    nose_drag_coefficient: float|None=None
    name: str="Configured launch vehicle"
    def __post_init__(self):
        if not self.stages: raise ValueError("at least one stage is required")
        if self.payload_mass<=0 or self.reference_area<=0: raise ValueError("payload mass and reference area must be positive")
        if self.drag_coefficient<0: raise ValueError("drag coefficient cannot be negative")
        if any(not isinstance(s,StageConfig) for s in self.stages): raise TypeError("stages must be StageConfig objects")
    @property
    def initial_mass(self):
        return self.payload_mass+sum(s.dry_mass+s.propellant_mass+s.fairing_mass for s in self.stages)
@dataclass(frozen=True)
class SimulationConfig:
    vehicle: VehicleConfig
    max_time: float=1200.0
    time_step: float=0.25
    initial_altitude: float=0.0
    initial_downrange: float=0.0
    launch_elevation_deg: float=90.0
    launch_azimuth_deg: float=90.0
    latitude_deg: float=0.0
    include_earth_rotation: bool=False
    include_gravity_loss: bool=True
    atmosphere_model: str="ussa1976"
    integrator: str="rk4"
    max_dynamic_pressure: float|None=None
    stop_at_apogee: bool=False
    metadata: dict=field(default_factory=dict)
    def __post_init__(self):
        if self.max_time<=0 or self.time_step<=0: raise ValueError("time controls must be positive")
        if self.initial_altitude<0: raise ValueError("initial altitude cannot be negative")
        if not -90<=self.latitude_deg<=90: raise ValueError("latitude must be within [-90,90]")
        if self.atmosphere_model not in {"ussa1976","exponential"}: raise ValueError("unknown atmosphere model")
        if self.integrator not in {"rk4","rk45","euler","heun"}: raise ValueError("unsupported integrator")
        if self.max_dynamic_pressure is not None and self.max_dynamic_pressure<=0: raise ValueError("max dynamic pressure must be positive")
