"""Stage-stack mass properties and simple axial center-of-mass estimates."""
from dataclasses import dataclass
from .config import VehicleConfig
@dataclass(frozen=True)
class AxialComponent:
    name: str
    mass: float
    center_from_base: float
@dataclass(frozen=True)
class MassProperties:
    total_mass: float
    center_of_mass_from_base: float
    component_count: int
def center_of_mass(components):
    items=tuple(components)
    if not items: raise ValueError("at least one component is required")
    if any(c.mass<0 for c in items): raise ValueError("component masses cannot be negative")
    total=sum(c.mass for c in items)
    if total<=0: raise ValueError("total mass must be positive")
    center=sum(c.mass*c.center_from_base for c in items)/total
    return MassProperties(total,center,len(items))
def stack_mass_properties(vehicle: VehicleConfig,stage_lengths,payload_length):
    if len(stage_lengths)!=len(vehicle.stages): raise ValueError("one length is required per stage")
    if any(length<=0 for length in stage_lengths) or payload_length<=0: raise ValueError("component lengths must be positive")
    components=[]; base=0.
    for stage,length in zip(vehicle.stages,stage_lengths):
        components.append(AxialComponent(stage.name,stage.dry_mass+stage.propellant_mass,base+length/2))
        base+=length
    components.append(AxialComponent("Payload",vehicle.payload_mass,base+payload_length/2))
    return center_of_mass(components)
