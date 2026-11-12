import numpy as np
import pytest

from rocket_sim.integrators import (
    euler_step,
    heun_step,
    integrate_fixed,
    rk4_step,
    rk45_step,
)


def decay(t, y):
    return -y


def test_rk4_exponential_accuracy():
    y = rk4_step(decay, 0.0, np.array([1.0]), 0.1)
    assert y[0] == pytest.approx(np.exp(-0.1), rel=1e-6)


def test_heun_is_better_than_euler_for_decay():
    exact = np.exp(-0.1)
    heun_error = abs(heun_step(decay, 0.0, np.array([1.0]), 0.1)[0] - exact)
    euler_error = abs(euler_step(decay, 0.0, np.array([1.0]), 0.1)[0] - exact)
    assert heun_error < euler_error


def test_rk45_embedded_error_shape():
    value, error = rk45_step(decay, 0.0, np.array([1.0]), 0.1)
    assert value.shape == error.shape == (1,)
    assert abs(error[0]) < 1e-5


def test_fixed_integrator_grid():
    times, states = integrate_fixed(decay, np.array([1.0]), 0.0, 1.0, 0.1)
    assert len(times) == 11
    assert states.shape == (11, 1)


def test_invalid_interval():
    with pytest.raises(ValueError):
        integrate_fixed(decay, np.array([1.0]), 1.0, 0.0, 0.1)


@pytest.mark.parametrize(
    "t0,t1,step",
    [
        (np.nan, 1.0, 0.1),
        (0.0, np.inf, 0.1),
        (0.0, 1.0, np.nan),
        (0.0, 1.0, np.inf),
        (0.0, 1.0, 0.0),
        (0.0, 1.0, -0.1),
    ],
)
def test_rejects_invalid_time_controls(t0, t1, step):
    with pytest.raises(ValueError):
        integrate_fixed(decay, [1.0], t0, t1, step)


@pytest.mark.parametrize("initial_state", [[], [[1.0]], [1.0, np.nan], [1.0, np.inf], ["bad"]])
def test_rejects_invalid_initial_state(initial_state):
    with pytest.raises(ValueError):
        integrate_fixed(decay, initial_state, 0.0, 1.0, 0.1)


def test_zero_duration_returns_initial_state():
    times, states = integrate_fixed(decay, [2.0], 3.0, 3.0, 0.1)

    np.testing.assert_array_equal(times, [3.0])
    np.testing.assert_array_equal(states, [[2.0]])


def test_accepts_list_initial_state():
    _, states = integrate_fixed(decay, [1.0], 0.0, 0.1, 0.1)

    assert states.shape == (2, 1)
