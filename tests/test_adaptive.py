import numpy as np
import pytest

from rocket_sim.adaptive import integrate_adaptive


def decay(t, y):
    return -y


def test_adaptive_solver_matches_exponential():
    result = integrate_adaptive(decay, [1.0], 0.0, 2.0, 0.2)

    assert result.states[-1, 0] == pytest.approx(np.exp(-2.0), rel=1e-6)
    assert result.accepted_steps > 0
    assert result.function_evaluations == 7 * (
        result.accepted_steps + result.rejected_steps
    )


def test_adaptive_solver_records_rejections_when_tolerance_is_tight():
    result = integrate_adaptive(
        decay, [1.0], 0.0, 1.0, 0.8,
        absolute_tolerance=1e-12, relative_tolerance=1e-12,
    )

    assert result.rejected_steps > 0


def test_adaptive_solver_invalid_bounds():
    with pytest.raises(ValueError):
        integrate_adaptive(decay, [1.0], 0.0, 1.0, 0.1, min_step=0.2, max_step=0.1)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"t0": np.nan},
        {"t1": np.inf},
        {"initial_step": np.nan},
        {"absolute_tolerance": np.inf},
        {"relative_tolerance": 0.0},
        {"min_step": np.nan},
        {"max_step": -np.inf},
        {"safety_factor": np.nan},
        {"max_steps": 0},
    ],
)
def test_adaptive_solver_rejects_invalid_controls(kwargs):
    controls = {
        "t0": 0.0, "t1": 1.0, "initial_step": 0.1,
        "absolute_tolerance": 1e-8, "relative_tolerance": 1e-6,
        "min_step": 1e-8, "max_step": np.inf,
        "safety_factor": 0.9, "max_steps": 100,
    }
    controls.update(kwargs)
    with pytest.raises(ValueError):
        integrate_adaptive(decay, [1.0], **controls)


@pytest.mark.parametrize("initial_state", [[], [[1.0]], [np.nan], [np.inf], ["bad"]])
def test_adaptive_solver_rejects_invalid_initial_state(initial_state):
    with pytest.raises(ValueError):
        integrate_adaptive(decay, initial_state, 0.0, 1.0, 0.1)


def test_adaptive_solver_rejects_non_finite_derivatives():
    def invalid_derivative(t, y):
        return np.full_like(y, np.nan)

    with pytest.raises(FloatingPointError):
        integrate_adaptive(invalid_derivative, [1.0], 0.0, 1.0, 0.1)


def test_adaptive_solver_handles_zero_interval():
    result = integrate_adaptive(decay, [1.0], 2.0, 2.0, 0.1)

    assert result.accepted_steps == 0
    assert result.times.tolist() == [2.0]
    np.testing.assert_array_equal(result.states, [[1.0]])


def test_adaptive_solver_converges_as_tolerance_tightens():
    loose = integrate_adaptive(
        decay, [1.0], 0.0, 2.0, 0.5,
        absolute_tolerance=1e-5, relative_tolerance=1e-5,
    )
    tight = integrate_adaptive(
        decay, [1.0], 0.0, 2.0, 0.5,
        absolute_tolerance=1e-9, relative_tolerance=1e-9,
    )
    exact = np.exp(-2.0)

    assert abs(tight.states[-1, 0] - exact) < abs(loose.states[-1, 0] - exact)
