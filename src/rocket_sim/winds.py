"""Wind profiles.

Nothing fancy — just altitude tables. Not real weather data.
East/north/up, m/s.
"""
from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class WindVector:
    east: float
    north: float
    vertical: float = 0.0

    @property
    def speed(self):
        return math.sqrt(self.east ** 2 + self.north ** 2 + self.vertical ** 2)


class WindProfile:
    def __init__(self, levels):
        self.levels = tuple(sorted((float(h), float(e), float(n), float(u)) for h, e, n, u in levels))
        if not self.levels:
            raise ValueError("need at least one level")
        hs = [L[0] for L in self.levels]
        if len(hs) != len(set(hs)):
            raise ValueError("duplicate altitudes in wind table")

    def at(self, altitude):
        if altitude <= self.levels[0][0]:
            _, e, n, u = self.levels[0]
            return WindVector(e, n, u)
        if altitude >= self.levels[-1][0]:
            _, e, n, u = self.levels[-1]
            return WindVector(e, n, u)
        for a, b in zip(self.levels, self.levels[1:]):
            if a[0] <= altitude <= b[0]:
                f = (altitude - a[0]) / (b[0] - a[0])
                return WindVector(
                    a[1] + f * (b[1] - a[1]),
                    a[2] + f * (b[2] - a[2]),
                    a[3] + f * (b[3] - a[3]),
                )
        raise RuntimeError("wind interp fell through")


def calm_wind():
    return WindProfile([(0.0, 0.0, 0.0, 0.0), (100000.0, 0.0, 0.0, 0.0)])


def jet_streamish():
    return WindProfile(
        [
            (0.0, 2.0, 1.0, 0.0),
            (1000.0, 5.0, 2.0, 0.0),
            (5000.0, 15.0, 8.0, 0.0),
            (10000.0, 35.0, 12.0, 0.0),
            (12000.0, 40.0, 10.0, 0.0),
            (20000.0, 25.0, 5.0, 0.0),
            (40000.0, 10.0, 2.0, 0.0),
            (80000.0, 5.0, 0.0, 0.0),
        ]
    )


def random_wind(seed=None, max_speed=25.0):
    rng = random.Random(seed)
    levels = [(0.0, 0.0, 0.0, 0.0)]
    h = 0.0
    for _ in range(6):
        h += rng.uniform(2000, 12000)
        spd = rng.uniform(0, max_speed)
        az = rng.uniform(0, 2 * math.pi)
        levels.append((h, spd * math.cos(az), spd * math.sin(az), 0.0))
    return WindProfile(levels)


def power_law(v_ref=5.0, z_ref=10.0, alpha=0.15, direction_deg=90.0):
    toward = math.radians((direction_deg + 180.0) % 360.0)
    levels = []
    for h in [0.1, 10, 50, 100, 500, 1000, 3000, 10000, 30000]:
        spd = v_ref * (max(h, 0.1) / z_ref) ** alpha
        levels.append((h, spd * math.sin(toward), spd * math.cos(toward), 0.0))
    return WindProfile(levels)
