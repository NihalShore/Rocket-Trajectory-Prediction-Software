"""Max-q throttle-back helper.

When dynamic pressure climbs past a limit, scale thrust down. Comes back
up after q drops.
"""


def throttle_for_q(q, q_limit, min_throttle=0.6, gain=1.5):
    if q_limit <= 0:
        return 1.0
    if q <= q_limit:
        return 1.0
    over = (q - q_limit) / q_limit
    thr = 1.0 - gain * over
    if thr < min_throttle:
        thr = min_throttle
    if thr > 1.0:
        thr = 1.0
    return thr


def schedule_from_trajectory(result, q_limit, min_throttle=0.6):
    out = []
    for s in result.samples:
        out.append((s.time, throttle_for_q(s.dynamic_pressure, q_limit, min_throttle)))
    return out
