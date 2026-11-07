"""Range safety doodles.

Impact point, simple 3-sigma ellipse from a monte carlo set, keep-out radius.
Not FAA certifiable. Don't use this to clear a real range.
"""
import math
import numpy as np


def impact_point(result):
    for s in reversed(result.samples):
        if s.state.altitude <= 0:
            return s.state.downrange, 0.0, s.time
    s = result.samples[-1]
    return s.state.downrange, s.state.altitude, s.time


def footprint_ellipse(downranges, crossranges=None):
    x = np.asarray(downranges, dtype=float)
    if crossranges is None:
        y = np.zeros_like(x)
        rng = np.random.default_rng(0)
        y = rng.normal(0, max(1.0, 0.15 * np.std(x)), size=len(x))
    else:
        y = np.asarray(crossranges, dtype=float)

    mx, my = float(np.mean(x)), float(np.mean(y))
    if len(x) < 2:
        return mx, my, 0.0, 0.0, 0.0
    cov = np.cov(x, y)
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]
    a = 3.0 * math.sqrt(max(eigvals[0], 0.0))
    b = 3.0 * math.sqrt(max(eigvals[1], 0.0))
    angle = math.atan2(eigvecs[1, 0], eigvecs[0, 0])
    return mx, my, a, b, angle


def keepout_radius(downranges, factor=3.0):
    x = np.asarray(downranges, dtype=float)
    mx = float(np.mean(x))
    r = np.abs(x - mx)
    return mx, float(np.mean(r) + factor * np.std(r))


def max_q_location(result):
    best = None
    for s in result.samples:
        if best is None or s.dynamic_pressure > best.dynamic_pressure:
            best = s
    if best is None:
        return None
    return {
        "time": best.time,
        "altitude": best.state.altitude,
        "speed": best.state.speed,
        "q": best.dynamic_pressure,
        "downrange": best.state.downrange,
    }
