"""A few standard ODE steps.

euler / heun / rk4 for fixed step, and a dormand-prince pair (rk45) when
you want an error estimate. Nothing fancy.
"""
import numpy as np


def euler_step(fun, t, y, h):
    return y + h * fun(t, y)


def heun_step(fun, t, y, h):
    k1 = fun(t, y)
    k2 = fun(t + h, y + h * k1)
    return y + 0.5 * h * (k1 + k2)


def rk4_step(fun, t, y, h):
    k1 = fun(t, y)
    k2 = fun(t + h / 2, y + h * k1 / 2)
    k3 = fun(t + h / 2, y + h * k2 / 2)
    k4 = fun(t + h, y + h * k3)
    return y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6


def rk45_step(fun, t, y, h):
    """Dormand-Prince 5(4). Returns (y5, y5-y4)."""
    k1 = fun(t, y)
    k2 = fun(t + h / 5, y + h * k1 / 5)
    k3 = fun(t + 3 * h / 10, y + h * (3 * k1 / 40 + 9 * k2 / 40))
    k4 = fun(t + 4 * h / 5, y + h * (44 * k1 / 45 - 56 * k2 / 15 + 32 * k3 / 9))
    k5 = fun(
        t + 8 * h / 9,
        y + h * (19372 * k1 / 6561 - 25360 * k2 / 2187 + 64448 * k3 / 6561 - 212 * k4 / 729),
    )
    k6 = fun(
        t + h,
        y
        + h
        * (
            9017 * k1 / 3168
            - 355 * k2 / 33
            + 46732 * k3 / 5247
            + 49 * k4 / 176
            - 5103 * k5 / 18656
        ),
    )
    y5 = y + h * (
        35 * k1 / 384 + 500 * k3 / 1113 + 125 * k4 / 192 - 2187 * k5 / 6784 + 11 * k6 / 84
    )
    k7 = fun(t + h, y5)
    y4 = y + h * (
        5179 * k1 / 57600
        + 7571 * k3 / 16695
        + 393 * k4 / 640
        - 92097 * k5 / 339200
        + 187 * k6 / 2100
        + k7 / 40
    )
    return y5, y5 - y4


def integrate_fixed(fun, y0, t0, t1, step, method="rk4"):
    try:
        t0, t1, step = float(t0), float(t1), float(step)
        y0 = np.asarray(y0, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("time values, step, and initial state must be numeric") from exc

    if not np.all(np.isfinite([t0, t1, step])):
        raise ValueError("time values and step must be finite")
    if step <= 0 or t1 < t0:
        raise ValueError("step must be positive and end time must not precede start time")
    if y0.ndim != 1 or y0.size == 0 or not np.all(np.isfinite(y0)):
        raise ValueError("initial state must be a non-empty, finite 1D array")

    methods = {"euler": euler_step, "heun": heun_step, "rk4": rk4_step}
    if method not in methods:
        raise ValueError(f"unsupported fixed method: {method}")

    count = int(np.ceil((t1 - t0) / step))
    times = np.linspace(t0, t1, count + 1) if count else np.array([t0])
    states = np.empty((len(times), y0.size))
    states[0] = y0
    for i in range(1, len(times)):
        states[i] = methods[method](fun, times[i - 1], states[i - 1], times[i] - times[i - 1])
    return times, states
