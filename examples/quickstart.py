"""Minimal API example."""
from rocket_sim.config import StageConfig,VehicleConfig,SimulationConfig
from rocket_sim.guidance import gravity_turn_program
from rocket_sim.simulation import simulate
from rocket_sim.serialization import write_json
stage=StageConfig("Demonstrator",12000.,65000.,1.5e6,100.,1.3e6)
vehicle=VehicleConfig([stage],900.,5.2,.4,name="Demonstrator")
config=SimulationConfig(vehicle,max_time=300.,time_step=.25)
result=simulate(config,gravity_turn_program(8.,100.,12.))
print(result.metrics)
write_json(result,"output/demonstrator.json")
