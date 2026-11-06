from rocket_sim.config import StageConfig,VehicleConfig,SimulationConfig
from rocket_sim.simulation import simulate
from rocket_sim.diagnostics import validate_samples
def config():
    stage=StageConfig("Short stage",100.,400.,12000.,20.)
    vehicle=VehicleConfig([stage],30.,.8,.4)
    return SimulationConfig(vehicle,max_time=40.,time_step=.1)
def test_simulation_produces_ordered_samples():
    result=simulate(config())
    assert len(result.samples)>10
    assert all(b.time>a.time for a,b in zip(result.samples,result.samples[1:]))
def test_simulation_mass_is_nonincreasing():
    result=simulate(config())
    masses=result.masses
    assert all(b<=a+1e-8 for a,b in zip(masses,masses[1:]))
def test_simulation_records_burnout():
    result=simulate(config())
    assert any(e.name=="burnout" for e in result.events)
def test_simulation_diagnostics():
    result=simulate(config())
    assert not [d for d in validate_samples(list(result.samples)) if d.severity=="error"]
def test_peak_altitude_positive():
    assert simulate(config()).metrics.maximum_altitude>0
