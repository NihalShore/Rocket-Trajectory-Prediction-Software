"""Adaptive Dormand-Prince integration with bounded step-size control."""

from dataclasses import dataclass

import numpy as np

from .integrators import rk45_step


@dataclass(frozen=True)
class AdaptiveResult:
    times: np.ndarray
    states: np.ndarray
    accepted_steps: int
    rejected_steps: int
    function_evaluations: int


def integrate_adaptive(
    fun,
    y0,
    t0,
    t1,
    initial_step,
    absolute_tolerance=1e-8,
    relative_tolerance=1e-6,
    min_step=1e-8,
    max_step=float("inf"),
    safety_factor=0.9,
    max_steps=100000,
):
    try:
        t0 = float(t0)
        t1 = float(t1)
        initial_step = float(initial_step)
        absolute_tolerance = float(absolute_tolerance)
        relative_tolerance = float(relative_tolerance)
        min_step = float(min_step)
        max_step = float(max_step)
        safety_factor = float(safety_factor)
        y = np.asarray(y0, dtype=float).copy()
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("integration controls and initial state must be numeric") from exc

    if not np.all(np.isfinite([t0, t1, initial_step, absolute_tolerance,
                               relative_tolerance, min_step, safety_factor])):
        raise ValueError("integration controls must be finite")
    if not (np.isfinite(max_step) or max_step == float("inf")):
        raise ValueError("max_step must be finite or positive infinity")
    if t1 < t0 or initial_step <= 0 or min_step <= 0 or max_step < min_step:
        raise ValueError("invalid integration interval or step bounds")
    if absolute_tolerance <= 0 or relative_tolerance <= 0:
        raise ValueError("tolerances must be positive")
    if not 0 < safety_factor < 1:
        raise ValueError("safety_factor must be between zero and one")
    if y.ndim != 1 or y.size == 0 or not np.all(np.isfinite(y)):
        raise ValueError("initial state must be a non-empty, finite 1D array")
    if not isinstance(max_steps, int) or isinstance(max_steps, bool) or max_steps < 1:
        raise ValueError("max_steps must be a positive integer")

    times = [t0]
    states = [y.copy()]
    accepted = 0
    rejected = 0
    evaluations = 0
    if t0 == t1:
        return AdaptiveResult(
            np.asarray(times), np.asarray(states), accepted, rejected, evaluations
        )

    h = min(max(initial_step, min_step), max_step, t1 - t0)
    for _ in range(max_steps):
        h = min(h, max_step, t1 - t0)
        candidate, error = rk45_step(fun, t0, y, h)
        evaluations += 7
        candidate = np.asarray(candidate, dtype=float)
        error = np.asarray(error, dtype=float)
        if candidate.shape != y.shape or error.shape != y.shape:
            raise ValueError("derivative function returned an incompatible state shape")
        if not np.all(np.isfinite(candidate)) or not np.all(np.isfinite(error)):
            raise FloatingPointError("RK45 produced a non-finite state or error estimate")

        scale = absolute_tolerance + relative_tolerance * np.maximum(
            np.abs(y), np.abs(candidate)
        )
        norm = float(np.sqrt(np.mean((error / scale) ** 2)))
        if not np.isfinite(norm):
            raise FloatingPointError("RK45 error norm is not finite")

        if norm <= 1.0:
            t0 += h
            y = candidate
            times.append(t0)
            states.append(y.copy())
            accepted += 1
        else:
            rejected += 1

        factor = 5.0 if norm == 0 else safety_factor * norm ** -0.2
        factor = min(5.0, max(0.2, factor))
        next_step = min(max_step, max(min_step, h * factor))
        if norm > 1.0 and h <= min_step * (1.0 + 1e-12):
            raise RuntimeError("adaptive solver cannot satisfy tolerance at min_step")
        h = next_step

        if t0 >= t1:
            break
    else:
        raise RuntimeError("maximum adaptive step count exceeded")

    if t0 < t1:
        raise RuntimeError("integration ended before final time")

    return AdaptiveResult(
        np.asarray(times), np.asarray(states), accepted, rejected, evaluations
    )
