"""Reusable illustrative vehicle configuration profiles."""
from .config import StageConfig,VehicleConfig,SimulationConfig
def compact_demonstrator():
    stage=StageConfig("Demonstrator booster",12000.,65000.,1.5e6,100.,1.3e6)
    vehicle=VehicleConfig([stage],900.,5.2,.4,name="Compact demonstrator")
    return SimulationConfig(vehicle,max_time=300.,time_step=.25)
def two_stage_reference():
    lower=StageConfig("Lower stage",25000.,180000.,4.2e6,125.,3.5e6)
    upper=StageConfig("Upper stage",6500.,42000.,9.0e5,110.,specific_impulse_vacuum=340.)
    vehicle=VehicleConfig([lower,upper],1800.,10.5,.32,name="Two-stage reference")
    return SimulationConfig(vehicle,max_time=700.,time_step=.2)
def create_vehicle_from_mapping(data):
    stages=[StageConfig(**item) for item in data["stages"]]
    fields={key:data[key] for key in ("payload_mass","reference_area") if key in data}
    for key in ("drag_coefficient","nose_drag_coefficient","name"):
        if key in data: fields[key]=data[key]
    return VehicleConfig(stages=stages,**fields)
def create_config_from_mapping(data,vehicle):
    return SimulationConfig(vehicle=vehicle,**{key:value for key,value in data.items() if key!="vehicle"})
