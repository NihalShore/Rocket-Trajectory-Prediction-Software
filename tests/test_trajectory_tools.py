import pytest
from rocket_sim.state import State,TrajectorySample
from rocket_sim.trajectory import interpolate_sample,slice_time,maximum_sample
def samples():
    return [TrajectorySample(t,State(t,2*t,3*t,4*t,100-t),0,0,2*t,0,0) for t in (0.,1.,2.)]
def test_interpolation_between_samples():
    result=interpolate_sample(samples(),.5)
    assert result.state.altitude==pytest.approx(1)
    assert result.state.mass==pytest.approx(99.5)
def test_slice_inclusive_bounds():
    assert len(slice_time(samples(),1,2))==2
def test_maximum_sample():
    assert maximum_sample(samples(),"altitude").time==2
def test_interpolation_outside_range():
    with pytest.raises(ValueError): interpolate_sample(samples(),3)
