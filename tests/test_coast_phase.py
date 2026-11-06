from rocket_sim.config import StageConfig,VehicleConfig,SimulationConfig
from rocket_sim.simulation import simulate
def test_coast_phase_runs_after_burnout():
    stage=StageConfig("Short impulse",100.,100.,5000.,1.)
    vehicle=VehicleConfig([stage],10.,.5,.2)
    result=simulate(SimulationConfig(vehicle,max_time=10.,time_step=.02))
    burnout=next(e.time for e in result.events if e.name=="burnout")
    assert result.samples[-1].time>burnout
    assert result.samples[-1].state.mass==10.
def test_apogee_is_detected_during_coast():
    stage=StageConfig("Short impulse",100.,100.,5000.,1.)
    vehicle=VehicleConfig([stage],10.,.5,.2)
    result=simulate(SimulationConfig(vehicle,max_time=10.,time_step=.02,stop_at_apogee=True))
    assert any(e.name=="apogee" for e in result.events)
    assert result.samples[-1].event=="apogee"
    assert result.metrics.maximum_altitude>0
