import pytest
from rocket_sim.coordinates import heading_components,polar_velocity,rotate_2d
from rocket_sim.guidance import PitchKnot,PitchProgram
from rocket_sim.winds import WindProfile
from rocket_sim.vehicle import thrust_to_weight
from rocket_sim.validation import validate_vehicle
from rocket_sim.config import StageConfig,VehicleConfig
def test_heading_components():
    east,north=heading_components(10.,90.)
    assert east==pytest.approx(10.) and north==pytest.approx(0.,abs=1e-9)
def test_polar_velocity():
    speed,angle=polar_velocity(3.,4.)
    assert speed==5. and angle==pytest.approx(53.1301,rel=1e-4)
def test_rotation():
    x,y=rotate_2d(1.,0.,3.141592653589793/2)
    assert x==pytest.approx(0.,abs=1e-9) and y==pytest.approx(1.)
def test_pitch_interpolation():
    p=PitchProgram([PitchKnot(0,90),PitchKnot(10,0)])
    assert p.angle(5)==pytest.approx(3.141592653589793/4)
def test_wind_interpolation():
    p=WindProfile([(0,0,0,0),(100,10,20,0)])
    assert p.at(50).east==5 and p.at(50).north==10
def test_thrust_to_weight():
    assert thrust_to_weight(19613.3,1000.)==pytest.approx(2.)
def test_vehicle_validation():
    s=StageConfig("A",100,200,10000,20)
    v=VehicleConfig([s],50,1)
    assert validate_vehicle(v)==[]
