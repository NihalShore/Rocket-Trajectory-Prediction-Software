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
        try:
            parsed = tuple(
                sorted((float(h), float(e), float(n), float(u)) for h, e, n, u in levels)
            )
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("wind levels must contain numeric altitude and velocity values") from exc
        if not parsed:
            raise ValueError("need at least one level")
        if not all(math.isfinite(value) for level in parsed for value in level):
            raise ValueError("wind levels must contain only finite values")

        self.levels = parsed
        altitudes = [level[0] for level in self.levels]
        if len(altitudes) != len(set(altitudes)):
            raise ValueError("duplicate altitudes in wind table")

    def at(self, altitude):
        if not math.isfinite(altitude):
            raise ValueError("altitude must be finite")
        if altitude <= self.levels[0][0]:
            _, east, north, vertical = self.levels[0]
            return WindVector(east, north, vertical)
        if altitude >= self.levels[-1][0]:
            _, east, north, vertical = self.levels[-1]
            return WindVector(east, north, vertical)
        for lower, upper in zip(self.levels, self.levels[1:]):
            if lower[0] <= altitude <= upper[0]:
                fraction = (altitude - lower[0]) / (upper[0] - lower[0])
                return WindVector(
                    lower[1] + fraction * (upper[1] - lower[1]),
                    lower[2] + fraction * (upper[2] - lower[2]),
                    lower[3] + fraction * (upper[3] - lower[3]),
                )
        raise RuntimeError("wind interpolation failed")


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
    if not math.isfinite(max_speed) or max_speed < 0:
        raise ValueError("max_speed must be finite and nonnegative")
    rng = random.Random(seed)
    levels = [(0.0, 0.0, 0.0, 0.0)]
    altitude = 0.0
    for _ in range(6):
        altitude += rng.uniform(2000, 12000)
        speed = rng.uniform(0, max_speed)
        direction = rng.uniform(0, 2 * math.pi)
        levels.append(
            (altitude, speed * math.cos(direction), speed * math.sin(direction), 0.0)
        )
    return WindProfile(levels)


def power_law(v_ref=5.0, z_ref=10.0, alpha=0.15, direction_deg=90.0):
    if not all(math.isfinite(value) for value in (v_ref, z_ref, alpha, direction_deg)):
        raise ValueError("wind power-law parameters must be finite")
    if v_ref < 0 or z_ref <= 0:
        raise ValueError("wind speed must be nonnegative and reference height positive")
    toward = math.radians((direction_deg + 180.0) % 360.0)
    levels = []
    for altitude in [0.1, 10, 50, 100, 500, 1000, 3000, 10000, 30000]:
        speed = v_ref * (max(altitude, 0.1) / z_ref) ** alpha
        levels.append(
            (altitude, speed * math.sin(toward), speed * math.cos(toward), 0.0)
        )
    return WindProfile(levels)
