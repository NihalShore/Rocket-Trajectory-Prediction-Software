"""Post-processing helper for a max-q throttle schedule.

The returned schedule is not applied by the flight integrator.
"""

import math


def throttle_for_q(q, q_limit, min_throttle=0.6, gain=1.5):
    if not math.isfinite(q) or q < 0.0:
        raise ValueError("q must be finite and nonnegative")
    if not math.isfinite(q_limit) or q_limit <= 0.0:
        raise ValueError("q_limit must be finite and positive")
    if not math.isfinite(min_throttle) or not 0.0 <= min_throttle <= 1.0:
        raise ValueError("min_throttle must be in [0, 1]")
    if not math.isfinite(gain) or gain < 0.0:
        raise ValueError("gain must be finite and nonnegative")

    if q <= q_limit:
        return 1.0
    excess = (q - q_limit) / q_limit
    return max(min_throttle, 1.0 - gain * excess)


def schedule_from_trajectory(result, q_limit, min_throttle=0.6):
    return [
        (sample.time, throttle_for_q(sample.dynamic_pressure, q_limit, min_throttle))
        for sample in result.samples
    ]
