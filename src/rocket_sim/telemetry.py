"""Telemetry dump helpers.

Print or stream a crude flight console. Not real-time, just post-run
playback that looks like a strip chart operator is watching.
"""
import sys
import time


def print_console(result, every=10, stream=None):
    stream = stream or sys.stdout
    stream.write(f"{'t':>8} {'alt_km':>8} {'vel':>8} {'mach':>6} {'q_kPa':>8} {'mass':>8}  event\n")
    for i, s in enumerate(result.samples):
        if i % every != 0 and not s.event:
            continue
        stream.write(
            f"{s.time:8.2f} {s.state.altitude/1000:8.2f} {s.state.speed:8.1f} "
            f"{s.mach:6.2f} {s.dynamic_pressure/1000:8.2f} {s.state.mass:8.1f}  {s.event}\n"
        )
    stream.flush()


def playback(result, speed=10.0, every=5):
    """Replay samples at `speed` x realtime. Ctrl-C to stop."""
    t0 = result.samples[0].time if result.samples else 0.0
    wall0 = time.time()
    for i, s in enumerate(result.samples):
        if i % every != 0 and not s.event:
            continue
        target = (s.time - t0) / max(speed, 0.01)
        while time.time() - wall0 < target:
            time.sleep(0.01)
        print(
            f"T+{s.time:7.1f}s  alt={s.state.altitude/1000:6.2f}km  "
            f"V={s.state.speed:7.1f}  q={s.dynamic_pressure/1000:6.1f}kPa  {s.event}"
        )


def summary_block(result):
    m = result.metrics
    lines = [
        "---- flight summary ----",
        f"  apogee     {m.maximum_altitude/1000:.2f} km @ t={m.apogee_time}",
        f"  max speed  {m.maximum_speed:.1f} m/s  (M={m.maximum_mach:.2f})",
        f"  max q      {m.maximum_dynamic_pressure/1000:.1f} kPa",
        f"  final mass {m.final_mass:.1f} kg",
        f"  ideal dV   {m.ideal_delta_v:.0f} m/s",
        f"  grav loss  ~{m.estimated_gravity_loss:.0f} m/s",
        f"  drag loss  ~{m.estimated_drag_loss:.0f} m/s",
        "  events:",
    ]
    for e in result.events:
        lines.append(f"    t={e.time:8.2f}  {e.name}")
    return "\n".join(lines)


def finite_difference(x, y):
    """Simple central/edge differences. x,y sequences same length."""
    import numpy as np
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("need matching x,y with len>=2")
    dy = np.empty_like(y)
    dy[0] = (y[1] - y[0]) / (x[1] - x[0])
    dy[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2])
    for i in range(1, len(y) - 1):
        dy[i] = (y[i + 1] - y[i - 1]) / (x[i + 1] - x[i - 1])
    return dy


def moving_average(y, window):
    import numpy as np
    y = np.asarray(y, dtype=float)
    if window < 1 or window > len(y):
        raise ValueError("bad window")
    out = []
    for i in range(len(y) - window + 1):
        out.append(float(np.mean(y[i : i + window])))
    return np.asarray(out)
