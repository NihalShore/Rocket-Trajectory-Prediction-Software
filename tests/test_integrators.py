import numpy as np
import pytest
from rocket_sim.integrators import euler_step,heun_step,rk4_step,rk45_step,integrate_fixed
def decay(t,y): return -y
def test_rk4_exponential_accuracy():
    y=rk4_step(decay,0.,np.array([1.]),.1)
    assert y[0]==pytest.approx(np.exp(-.1),rel=1e-6)
def test_heun_is_better_than_euler_for_decay():
    exact=np.exp(-.1)
    assert abs(heun_step(decay,0.,np.array([1.]),.1)[0]-exact)<abs(euler_step(decay,0.,np.array([1.]),.1)[0]-exact)
def test_rk45_embedded_error_shape():
    value,error=rk45_step(decay,0.,np.array([1.]),.1)
    assert value.shape==error.shape==(1,)
    assert abs(error[0])<1e-5
def test_fixed_integrator_grid():
    t,y=integrate_fixed(decay,np.array([1.]),0.,1.,.1)
    assert len(t)==11 and y.shape==(11,1)
def test_invalid_interval():
    with pytest.raises(ValueError): integrate_fixed(decay,np.array([1.]),1.,0.,.1)
