"""Simple impact and downrange dispersion helpers.

These estimates are for model inspection, not operational range safety.
"""

import math

import numpy as np


def impact_point(result):
    samples = result.samples
    if not samples:
        raise ValueError("result has no trajectory samples")

    for previous, current in reversed(list(zip(samples, samples[1:]))):
        h0 = previous.state.altitude
        h1 = current.state.altitude
        if h0 > 0.0 >= h1:
            fraction = h0 / (h0 - h1)
            downrange = previous.state.downrange + fraction * (
                current.state.downrange - previous.state.downrange
            )
            time = previous.time + fraction * (current.time - previous.time)
            return downrange, 0.0, time

    last = samples[-1]
    return last.state.downrange, last.state.altitude, last.time


def footprint_ellipse(downranges, crossranges=None):
    x = np.asarray(downranges, dtype=float)
    if x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x)):
        raise ValueError("downranges must be a nonempty finite 1D sequence")

    if crossranges is None:
        y = np.zeros_like(x)
    else:
        y = np.asarray(crossranges, dtype=float)
        if y.shape != x.shape or not np.all(np.isfinite(y)):
            raise ValueError("crossranges must match downranges and be finite")

    mean_x = float(np.mean(x))
    mean_y = float(np.mean(y))
    if x.size < 2:
        return mean_x, mean_y, 0.0, 0.0, 0.0

    covariance = np.cov(x, y)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    major = 3.0 * math.sqrt(max(float(eigenvalues[0]), 0.0))
    minor = 3.0 * math.sqrt(max(float(eigenvalues[1]), 0.0))
    angle = math.atan2(eigenvectors[1, 0], eigenvectors[0, 0])
    return mean_x, mean_y, major, minor, angle


def keepout_radius(downranges, factor=3.0):
    values = np.asarray(downranges, dtype=float)
    if values.ndim != 1 or values.size == 0 or not np.all(np.isfinite(values)):
        raise ValueError("downranges must be a nonempty finite 1D sequence")
    if not math.isfinite(factor) or factor < 0.0:
        raise ValueError("factor must be finite and nonnegative")

    center = float(np.mean(values))
    radius = float(np.mean(np.abs(values - center)) + factor * np.std(values))
    return center, radius


def max_q_location(result):
    if not result.samples:
        return None
    sample = max(result.samples, key=lambda item: item.dynamic_pressure)
    return {
        "time": sample.time,
        "altitude": sample.state.altitude,
        "speed": sample.state.speed,
        "q": sample.dynamic_pressure,
        "downrange": sample.state.downrange,
    }
