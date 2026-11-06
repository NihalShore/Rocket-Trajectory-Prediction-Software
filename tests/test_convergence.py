import pytest
from rocket_sim.config import StageConfig,VehicleConfig,SimulationConfig
from rocket_sim.simulation import simulate
def run(step):
    stage=StageConfig("Convergence article",150.,250.,12000.,12.)
    vehicle=VehicleConfig([stage],35.,.7,.3)
    return simulate(SimulationConfig(vehicle,max_time=25.,time_step=step,stop_at_apogee=True))
def test_smaller_step_gives_similar_apogee():
    coarse=run(.05).metrics.maximum_altitude
    fine=run(.025).metrics.maximum_altitude
    assert fine==pytest.approx(coarse,rel=.02)
def test_burnout_time_matches_input():
    result=run(.05)
    assert result.metrics.burnout_time==pytest.approx(12.,abs=.05)
