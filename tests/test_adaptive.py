import numpy as np
import pytest
from rocket_sim.adaptive import integrate_adaptive
def decay(t,y): return -y
def test_adaptive_solver_matches_exponential():
    result=integrate_adaptive(decay,[1.],0.,2.,.2)
    assert result.states[-1,0]==pytest.approx(np.exp(-2),rel=1e-6)
    assert result.accepted_steps>0
def test_adaptive_solver_records_rejections_when_tolerance_is_tight():
    result=integrate_adaptive(decay,[1.],0.,1.,.8,absolute_tolerance=1e-12,relative_tolerance=1e-12)
    assert result.rejected_steps>0
def test_adaptive_solver_invalid_bounds():
    with pytest.raises(ValueError): integrate_adaptive(decay,[1.],0.,1.,.1,min_step=.2,max_step=.1)
def test_adaptive_solver_handles_zero_interval():
    result=integrate_adaptive(decay,[1.],2.,2.,.1)
    assert result.accepted_steps==0 and result.times.tolist()==[2.]
