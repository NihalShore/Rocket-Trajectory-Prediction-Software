"""Tabulated thrust curves.

time [s] vs thrust [N]. Optional mass-flow column. Linear interp, clamps
outside the table. Burnout = last point above ~1% of peak.
"""
from dataclasses import dataclass


@dataclass
class ThrustTable:
    times: list
    thrusts: list
    mass_flows: list | None = None

    def __post_init__(self):
        if len(self.times) != len(self.thrusts):
            raise ValueError("time/thrust length mismatch")
        if len(self.times) < 2:
            raise ValueError("need >= 2 points")
        self.times = [float(t) for t in self.times]
        self.thrusts = [float(f) for f in self.thrusts]
        if self.mass_flows is not None:
            self.mass_flows = [float(m) for m in self.mass_flows]
            if len(self.mass_flows) != len(self.times):
                raise ValueError("mdot length mismatch")

        self._Itot = 0.0
        for i in range(1, len(self.times)):
            self._Itot += 0.5 * (self.thrusts[i] + self.thrusts[i - 1]) * (
                self.times[i] - self.times[i - 1]
            )
        peak = max(self.thrusts) if self.thrusts else 0.0
        thresh = 0.01 * peak
        self._tburn = 0.0
        for i in range(len(self.thrusts) - 1, -1, -1):
            if self.thrusts[i] > thresh:
                self._tburn = self.times[i]
                break

    def thrust_at(self, t):
        if t < self.times[0] or t > self.times[-1]:
            if t > self.times[-1]:
                return 0.0
            return self.thrusts[0]
        for i in range(1, len(self.times)):
            if t <= self.times[i]:
                u = (t - self.times[i - 1]) / (self.times[i] - self.times[i - 1])
                return self.thrusts[i - 1] + u * (self.thrusts[i] - self.thrusts[i - 1])
        return 0.0

    def mdot_at(self, t):
        if self.mass_flows is None:
            return 0.0
        if t < self.times[0] or t > self.times[-1]:
            return 0.0
        for i in range(1, len(self.times)):
            if t <= self.times[i]:
                u = (t - self.times[i - 1]) / (self.times[i] - self.times[i - 1])
                return self.mass_flows[i - 1] + u * (self.mass_flows[i] - self.mass_flows[i - 1])
        return 0.0

    @property
    def total_impulse(self):
        return self._Itot

    @property
    def burn_time(self):
        return self._tburn

    @classmethod
    def from_csv(cls, path, time_col=0, thrust_col=1, mdot_col=None):
        times, thrusts, mdots = [], [], []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.replace(",", " ").split()
                try:
                    times.append(float(parts[time_col]))
                    thrusts.append(float(parts[thrust_col]))
                    if mdot_col is not None:
                        mdots.append(float(parts[mdot_col]))
                except (ValueError, IndexError):
                    continue
        return cls(times, thrusts, mdots if mdot_col is not None else None)

    @classmethod
    def boxcar(cls, thrust, burn_time, n=40):
        ts = [burn_time * i / (n - 1) for i in range(n)]
        fs = [thrust] * (n - 1) + [0.0]
        return cls(ts, fs)


def fake_c_motor():
    t = [0, 0.05, 0.1, 0.3, 0.6, 1.0, 1.4, 1.6]
    f = [0, 12, 14, 11, 9, 7, 2, 0]
    return ThrustTable(t, f)


def fake_o_motor():
    t = [0, 0.2, 1.0, 3.0, 5.0, 6.5, 7.0]
    f = [0, 8000, 12000, 11000, 9000, 2000, 0]
    return ThrustTable(t, f)
