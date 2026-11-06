import pytest
from rocket_sim.config import StageConfig,VehicleConfig,SimulationConfig
def stage(): return StageConfig("Test",100.,500.,10000.,50.)
def test_vehicle_initial_mass():
    v=VehicleConfig([stage()],50.,1.)
    assert v.initial_mass==650.
def test_stage_rejects_zero_propellant():
    with pytest.raises(ValueError): StageConfig("Bad",100.,0.,10000.,50.)
def test_config_rejects_bad_timestep():
    with pytest.raises(ValueError): SimulationConfig(VehicleConfig([stage()],50.,1.),time_step=0.)
def test_vehicle_requires_stage():
    with pytest.raises(ValueError): VehicleConfig([],50.,1.)
