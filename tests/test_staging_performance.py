import pytest
from rocket_sim.config import StageConfig,VehicleConfig
from rocket_sim.staging import stage_schedule,propellant_fraction,dry_mass_fraction
from rocket_sim.performance import stage_performance
def vehicle():
    a=StageConfig("Lower",100.,500.,10000.,50.)
    b=StageConfig("Upper",30.,100.,2000.,40.)
    return VehicleConfig([a,b],20.,1.)
def test_stage_schedule_is_sequential():
    schedule=stage_schedule(vehicle())
    assert schedule[0].ignition_time==0
    assert schedule[1].ignition_time==50
    assert schedule[1].burnout_time==90
def test_stage_mass_fractions():
    v=vehicle()
    assert 0<propellant_fraction(v)<1
    assert 0<dry_mass_fraction(v)<1
def test_stage_performance_is_positive():
    p=stage_performance(vehicle().stages[0],150.)
    assert p.mass_flow>0 and p.ideal_delta_v>0
    assert p.initial_thrust_to_weight<p.final_thrust_to_weight
