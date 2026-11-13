"""Validated immutable configuration records."""

import math
from dataclasses import dataclass, field
from typing import Sequence

from .winds import WindProfile


def _require_finite(values, label):
    try:
        valid = all(math.isfinite(value) for value in values)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{label} must contain numeric values") from exc
    if not valid:
        raise ValueError(f"{label} must be finite")


@dataclass(frozen=True)
class StageConfig:
    name: str
    dry_mass: float
    propellant_mass: float
    thrust_vacuum: float
    burn_time: float
    thrust_sea_level: float | None = None
    specific_impulse_vacuum: float | None = None
    specific_impulse_sea_level: float | None = None
    fairing_mass: float = 0.0
    separation_time: float = 0.0
    thrust_curve: tuple[tuple[float, float], ...] | None = None

    def __post_init__(self):
        required = (
            self.dry_mass, self.propellant_mass, self.thrust_vacuum,
            self.burn_time, self.fairing_mass, self.separation_time,
        )
        optional = (
            self.thrust_sea_level, self.specific_impulse_vacuum,
            self.specific_impulse_sea_level,
        )
        _require_finite(required, "stage values")
        _require_finite((value for value in optional if value is not None), "optional stage values")

        for key in ("dry_mass", "propellant_mass", "thrust_vacuum", "burn_time"):
            if getattr(self, key) <= 0:
                raise ValueError(f"{key} must be positive")
        if self.fairing_mass < 0 or self.separation_time < 0:
            raise ValueError("optional masses and times cannot be negative")
        if self.thrust_sea_level is not None and not 0 < self.thrust_sea_level <= self.thrust_vacuum:
            raise ValueError("invalid sea-level thrust")
        for key in ("specific_impulse_vacuum", "specific_impulse_sea_level"):
            value = getattr(self, key)
            if value is not None and value <= 0:
                raise ValueError(f"{key} must be positive")

        if self.thrust_curve is not None:
            try:
                curve = tuple(tuple(point) for point in self.thrust_curve)
            except (TypeError, ValueError) as exc:
                raise ValueError("thrust_curve must contain time/thrust pairs") from exc
            if len(curve) < 2 or any(len(point) != 2 for point in curve):
                raise ValueError("thrust_curve requires at least two time/thrust pairs")
            _require_finite((value for point in curve for value in point), "thrust curve")
            if curve[0][0] != 0.0 or not math.isclose(curve[-1][0], self.burn_time, rel_tol=0.0, abs_tol=1e-9):
                raise ValueError("thrust_curve must start at zero and end at burn_time")
            if any(time < 0 or thrust < 0 for time, thrust in curve):
                raise ValueError("thrust curve times and values cannot be negative")
            if any(b[0] <= a[0] for a, b in zip(curve, curve[1:])):
                raise ValueError("thrust curve times must be strictly increasing")
            if max(thrust for _, thrust in curve) > self.thrust_vacuum:
                raise ValueError("thrust curve cannot exceed thrust_vacuum")
            if not any(thrust > 0 for _, thrust in curve):
                raise ValueError("thrust curve must contain positive thrust")
            object.__setattr__(self, "thrust_curve", curve)

    def vacuum_thrust_at(self, elapsed):
        """Return linearly interpolated vacuum thrust at stage burn time."""
        if self.thrust_curve is None:
            return self.thrust_vacuum
        if elapsed <= 0:
            return self.thrust_curve[0][1]
        for (t0, f0), (t1, f1) in zip(self.thrust_curve, self.thrust_curve[1:]):
            if elapsed <= t1:
                fraction = (elapsed - t0) / (t1 - t0)
                return f0 + fraction * (f1 - f0)
        return self.thrust_curve[-1][1]

    @property
    def mass_flow_rate(self):
        if self.specific_impulse_vacuum:
            from .constants import G0
            return self.thrust_vacuum / (self.specific_impulse_vacuum * G0)
        return self.propellant_mass / self.burn_time


@dataclass(frozen=True)
class VehicleConfig:
    stages: Sequence[StageConfig]
    payload_mass: float
    reference_area: float
    drag_coefficient: float = 0.35
    nose_drag_coefficient: float | None = None
    name: str = "Configured launch vehicle"

    def __post_init__(self):
        _require_finite(
            (self.payload_mass, self.reference_area, self.drag_coefficient),
            "vehicle values",
        )
        if self.nose_drag_coefficient is not None:
            _require_finite((self.nose_drag_coefficient,), "nose drag coefficient")
            if self.nose_drag_coefficient < 0:
                raise ValueError("nose drag coefficient cannot be negative")
        if not self.stages:
            raise ValueError("at least one stage is required")
        if self.payload_mass <= 0 or self.reference_area <= 0:
            raise ValueError("payload mass and reference area must be positive")
        if self.drag_coefficient < 0:
            raise ValueError("drag coefficient cannot be negative")
        if any(not isinstance(s, StageConfig) for s in self.stages):
            raise TypeError("stages must be StageConfig objects")

    @property
    def initial_mass(self):
        return self.payload_mass + sum(
            s.dry_mass + s.propellant_mass + s.fairing_mass for s in self.stages
        )


@dataclass(frozen=True)
class SimulationConfig:
    vehicle: VehicleConfig
    max_time: float = 1200.0
    time_step: float = 0.25
    initial_altitude: float = 0.0
    initial_downrange: float = 0.0
    launch_elevation_deg: float = 90.0
    launch_azimuth_deg: float = 90.0
    latitude_deg: float = 0.0
    include_earth_rotation: bool = False
    include_gravity_loss: bool = True
    atmosphere_model: str = "ussa1976"
    integrator: str = "rk4"
    max_dynamic_pressure: float | None = None
    stop_at_apogee: bool = False
    metadata: dict = field(default_factory=dict)
    wind_profile: WindProfile | None = None
    absolute_tolerance: float = 1e-8
    relative_tolerance: float = 1e-6
    min_time_step: float = 1e-8
    max_internal_steps: int = 100000

    def __post_init__(self):
        values = (
            self.max_time, self.time_step, self.initial_altitude,
            self.initial_downrange, self.launch_elevation_deg,
            self.launch_azimuth_deg, self.latitude_deg,
            self.absolute_tolerance, self.relative_tolerance, self.min_time_step,
        )
        _require_finite(values, "simulation values")
        if self.max_dynamic_pressure is not None:
            _require_finite((self.max_dynamic_pressure,), "maximum dynamic pressure")
        if self.max_time <= 0 or self.time_step <= 0:
            raise ValueError("time controls must be positive")
        if self.absolute_tolerance <= 0 or self.relative_tolerance <= 0 or self.min_time_step <= 0:
            raise ValueError("adaptive solver tolerances and minimum step must be positive")
        if (
            not isinstance(self.max_internal_steps, int)
            or isinstance(self.max_internal_steps, bool)
            or self.max_internal_steps < 1
        ):
            raise ValueError("max_internal_steps must be a positive integer")
        if self.initial_altitude < 0:
            raise ValueError("initial altitude cannot be negative")
        if not -90 <= self.latitude_deg <= 90:
            raise ValueError("latitude must be within [-90,90]")
        if not 0 <= self.launch_elevation_deg <= 180:
            raise ValueError("launch elevation must be within [0,180]")
        if self.atmosphere_model not in {"ussa1976", "exponential"}:
            raise ValueError("unknown atmosphere model")
        if self.integrator not in {"rk4", "rk45", "euler", "heun"}:
            raise ValueError("unsupported integrator")
        if self.max_dynamic_pressure is not None and self.max_dynamic_pressure <= 0:
            raise ValueError("max dynamic pressure must be positive")
        if self.wind_profile is not None and not isinstance(self.wind_profile, WindProfile):
            raise TypeError("wind_profile must be a WindProfile or None")
        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")
