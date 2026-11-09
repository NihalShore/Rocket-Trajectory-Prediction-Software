"""Validated one-dimensional coefficient tables with linear interpolation."""
from dataclasses import dataclass
import bisect
import math


@dataclass(frozen=True)
class CoefficientPoint:
    independent: float
    coefficient: float


class CoefficientTable:
    def __init__(self, points, extrapolation="clamp"):
        self.points = tuple(CoefficientPoint(float(x), float(y)) for x, y in points)
        if len(self.points) < 2:
            raise ValueError("at least two points required")
        if any(
            not math.isfinite(point.independent) or not math.isfinite(point.coefficient)
            for point in self.points
        ):
            raise ValueError("table values must be finite")
        if any(
            b.independent <= a.independent
            for a, b in zip(self.points, self.points[1:])
        ):
            raise ValueError("abscissas must increase")
        if extrapolation not in {"clamp", "linear", "error"}:
            raise ValueError("invalid extrapolation mode")

        self.extrapolation = extrapolation
        self._x = tuple(point.independent for point in self.points)

    def __call__(self, value):
        x = float(value)
        if not math.isfinite(x):
            raise ValueError("query must be finite")

        if x < self._x[0] or x > self._x[-1]:
            if self.extrapolation == "error":
                raise ValueError("query outside table")
            if self.extrapolation == "clamp":
                return self.points[0 if x < self._x[0] else -1].coefficient
            i = 0 if x < self._x[0] else len(self.points) - 2
        else:
            i = min(len(self.points) - 2, max(0, bisect.bisect_right(self._x, x) - 1))

        a, b = self.points[i], self.points[i + 1]
        fraction = (x - a.independent) / (b.independent - a.independent)
        return a.coefficient + fraction * (b.coefficient - a.coefficient)

    def derivative(self, value):
        x = float(value)
        if not math.isfinite(x):
            raise ValueError("query must be finite")

        outside = x < self._x[0] or x > self._x[-1]
        if outside and self.extrapolation == "error":
            raise ValueError("query outside table")
        if outside and self.extrapolation == "clamp":
            return 0.0

        if x <= self._x[0]:
            i = 0
        elif x >= self._x[-1]:
            i = len(self.points) - 2
        else:
            i = bisect.bisect_right(self._x, x) - 1

        a, b = self.points[i], self.points[i + 1]
        return (b.coefficient - a.coefficient) / (b.independent - a.independent)

    @property
    def domain(self):
        return self._x[0], self._x[-1]
