"""Quick-and-dirty aeroheating estimates.

Sutton-Graves stagnation point heat flux, nothing more. Useful to see if
you're cooking the nose or not. Units: W/m^2.
"""
import math

_K_SG = 1.7415e-4
_RN_DEFAULT = 0.3


def sutton_graves(density, speed, nose_radius=_RN_DEFAULT):
    """Stagnation heat flux ~ K * sqrt(rho/Rn) * V^3."""
    if speed < 1.0 or density <= 0 or nose_radius <= 0:
        return 0.0
    return _K_SG * math.sqrt(density / nose_radius) * (speed ** 3)


def total_heat_load(samples, nose_radius=_RN_DEFAULT):
    """Integrate heat flux over the trajectory. J/m^2."""
    total = 0.0
    for a, b in zip(samples, samples[1:]):
        dt = b.time - a.time
        if dt <= 0:
            continue

        def flux(s):
            v = s.state.speed
            if v < 1.0:
                return 0.0
            rho = 2.0 * s.dynamic_pressure / (v * v) if v > 0 else 0.0
            return sutton_graves(rho, v, nose_radius)

        total += 0.5 * (flux(a) + flux(b)) * dt
    return total


def peak_heat_flux(samples, nose_radius=_RN_DEFAULT):
    peak = 0.0
    t_peak = 0.0
    for s in samples:
        v = s.state.speed
        if v < 1.0:
            continue
        rho = 2.0 * s.dynamic_pressure / (v * v)
        qdot = sutton_graves(rho, v, nose_radius)
        if qdot > peak:
            peak = qdot
            t_peak = s.time
    return peak, t_peak
