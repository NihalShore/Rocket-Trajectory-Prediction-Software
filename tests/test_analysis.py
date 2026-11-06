import numpy as np
import pytest
from rocket_sim.optimization import golden_section_minimize,grid_search
from rocket_sim.sensitivity import finite_difference_sensitivity
from rocket_sim.uncertainty import sample_normal,summarize
from rocket_sim.telemetry import finite_difference,moving_average
def test_golden_section_finds_quadratic_minimum():
    result=golden_section_minimize(lambda x:(x-2.5)**2,-5.,8.)
    assert result.x==pytest.approx(2.5,abs=1e-4)
def test_grid_search():
    result=grid_search(lambda x:(x+1)**2,[-2,-1,0])
    assert result.x==-1
def test_sensitivity():
    s=finite_difference_sensitivity(lambda x:x*x,3.,1e-4)
    assert s.derivative==pytest.approx(6.,rel=1e-5)
def test_seeded_samples_repeat():
    assert np.array_equal(sample_normal(0,1,20,seed=4),sample_normal(0,1,20,seed=4))
def test_summary_percentiles():
    s=summarize("x",[1,2,3,4,5])
    assert s.percentile_50==3 and s.count==5
def test_finite_difference():
    assert np.allclose(finite_difference([0,1,2],[0,1,4]),[1,2,3])
def test_moving_average():
    assert np.allclose(moving_average([1,2,3,4],2),[1.5,2.5,3.5])
