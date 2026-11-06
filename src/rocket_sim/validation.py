"""Input and result validation routines."""
import math
def validate_vehicle(vehicle):
    errors=[]
    if vehicle.payload_mass<=0: errors.append("payload mass must be positive")
    if vehicle.reference_area<=0: errors.append("reference area must be positive")
    if not vehicle.stages: errors.append("vehicle requires at least one stage")
    names=[s.name for s in vehicle.stages]
    if len(names)!=len(set(names)): errors.append("stage names should be unique")
    if vehicle.initial_mass<=vehicle.payload_mass: errors.append("initial mass must exceed payload mass")
    return errors
def validate_simulation_config(config):
    errors=validate_vehicle(config.vehicle)
    if config.time_step>config.max_time: errors.append("time step exceeds maximum simulation time")
    if not math.isfinite(config.max_time) or not math.isfinite(config.time_step): errors.append("time controls must be finite")
    if not 0<=config.launch_elevation_deg<=180: errors.append("launch elevation must be within [0,180]")
    if not math.isfinite(config.launch_azimuth_deg): errors.append("launch azimuth must be finite")
    return errors
def require_valid_config(config):
    errors=validate_simulation_config(config)
    if errors: raise ValueError("Invalid simulation configuration: "+"; ".join(errors))
    return config
