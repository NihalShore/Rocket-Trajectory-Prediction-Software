"""2D point-mass ascent.

Downrange + altitude only. Drag, variable g, pitch program, sequential stages.
No attitude dynamics, no wind, no flexible body stuff. Good enough for
first-cut performance numbers.
"""
from dataclasses import dataclass
import math
import numpy as np

from .aerodynamics import aerodynamic_loads, drag_coefficient
from .atmosphere import atmosphere
from .config import SimulationConfig
from .constants import EARTH_ROTATION_RATE
from .gravity import gravity
from .integrators import euler_step, heun_step, rk4_step, rk45_step
from .metrics import TrajectoryMetrics, compute_metrics
from .state import Event, State, TrajectorySample
from .guidance import PitchKnot, PitchProgram


@dataclass(frozen=True)
class SimulationResult:
    config: SimulationConfig
    samples: tuple
    events: tuple
    metrics: TrajectoryMetrics

    @property
    def times(self):
        return np.asarray([s.time for s in self.samples])

    @property
    def altitudes(self):
        return np.asarray([s.state.altitude for s in self.samples])

    @property
    def downrange(self):
        return np.asarray([s.state.downrange for s in self.samples])

    @property
    def speeds(self):
        return np.asarray([s.state.speed for s in self.samples])

    @property
    def masses(self):
        return np.asarray([s.state.mass for s in self.samples])

    def to_dict(self):
        return {
            "metadata": dict(self.config.metadata),
            "metrics": self.metrics.__dict__,
            "events": [e.__dict__ for e in self.events],
            "samples": [
                {
                    "time": s.time,
                    "downrange": s.state.downrange,
                    "altitude": s.state.altitude,
                    "horizontal_velocity": s.state.horizontal_velocity,
                    "vertical_velocity": s.state.vertical_velocity,
                    "mass": s.state.mass,
                    "thrust": s.thrust,
                    "drag": s.drag,
                    "dynamic_pressure": s.dynamic_pressure,
                    "mach": s.mach,
                    "stage_index": s.stage_index,
                    "event": s.event,
                }
                for s in self.samples
            ],
        }


def _stage_thrust(stage, pressure):
    # if we only have vacuum thrust, just use that
    sea = stage.thrust_sea_level
    if sea is None:
        return stage.thrust_vacuum
    # crude linear blend between sea-level and vacuum
    frac = min(1.0, max(0.0, pressure / 101325.0))
    return stage.thrust_vacuum - (stage.thrust_vacuum - sea) * frac


def _sample(time, y, thrust, loads, stage_index, event=""):
    state = State(float(y[0]), float(y[1]), float(y[2]), float(y[3]), float(y[4]))
    return TrajectorySample(
        float(time),
        state,
        float(thrust),
        float(loads.drag),
        float(loads.dynamic_pressure),
        float(loads.mach),
        int(stage_index),
        event,
    )


def simulate(config: SimulationConfig, pitch_program: PitchProgram | None = None) -> SimulationResult:
    vehicle = config.vehicle
    pitch = pitch_program or PitchProgram([PitchKnot(0.0, config.launch_elevation_deg)])
    heading = math.radians(config.launch_azimuth_deg)

    # optional earth-rotation boost along the launch azimuth
    vx0 = 0.0
    vy0 = 0.0
    if config.include_earth_rotation:
        vx0 = (
            EARTH_ROTATION_RATE
            * 6371000.0
            * math.cos(math.radians(config.latitude_deg))
            * math.sin(heading)
        )

    y = np.array(
        [
            config.initial_downrange,
            config.initial_altitude,
            vx0,
            vy0,
            vehicle.initial_mass,
        ],
        dtype=float,
    )

    t = 0.0
    samples = []
    events = []
    stage_index = 0
    stage_elapsed = 0.0
    stages = list(vehicle.stages)

    fixed = {"euler": euler_step, "heun": heun_step, "rk4": rk4_step}
    if config.integrator not in fixed and config.integrator != "rk45":
        raise ValueError(f"unsupported integrator: {config.integrator}")

    empty = aerodynamic_loads(
        max(0.0, y[1]),
        0.0,
        vehicle.reference_area,
        vehicle.drag_coefficient,
        config.atmosphere_model,
    )
    samples.append(_sample(t, y, 0.0, empty, 0, "liftoff"))

    while t < config.max_time and y[1] >= 0.0:
        stage = stages[stage_index] if stage_index < len(stages) else None

        if stage is None:
            flow = 0.0
            h = min(config.time_step, config.max_time - t)
            remaining = 1e9
        else:
            flow = stage.propellant_mass / stage.burn_time
            remaining = stage.burn_time - stage_elapsed
            h = min(config.time_step, remaining, config.max_time - t)

        # stage is done — drop its dry/fairing mass and move on
        if stage is not None and remaining <= 1e-10:
            stage_index += 1
            stage_elapsed = 0.0
            y[4] = max(y[4] - stage.dry_mass - stage.fairing_mass, 0.0)
            # snap mass to avoid float noise like 10.000000000057
            y[4] = round(y[4], 9)

            name = "stage_separation" if stage_index < len(stages) else "burnout"
            events.append(
                Event(
                    t,
                    name,
                    float(y[1]),
                    float(math.hypot(y[2], y[3])),
                    float(y[4]),
                    {"stage": stage.name, "stage_index": stage_index - 1},
                )
            )
            # don't add another sample at the exact same timestamp —
            # just tag the last one so time stays strictly increasing
            if samples:
                last = samples[-1]
                samples[-1] = _sample(
                    last.time,
                    y,
                    0.0,
                    aerodynamic_loads(
                        max(0.0, y[1]),
                        math.hypot(y[2], y[3]),
                        vehicle.reference_area,
                        vehicle.drag_coefficient,
                        config.atmosphere_model,
                    ),
                    stage_index,
                    name,
                )
            continue

        if h <= 1e-12:
            break

        def derivative(time, state):
            x, alt, vx, vy, mass = state
            safe_alt = max(0.0, alt)
            atm = atmosphere(safe_alt, config.atmosphere_model)
            speed = math.hypot(vx, vy)
            q = 0.5 * atm.density * speed * speed
            cd = drag_coefficient(speed / atm.speed_of_sound, vehicle.drag_coefficient)
            drag = q * vehicle.reference_area * cd

            if speed > 1e-9:
                ax_drag = -drag * vx / (speed * max(mass, 1e-9))
                ay_drag = -drag * vy / (speed * max(mass, 1e-9))
            else:
                ax_drag = ay_drag = 0.0

            thrust = _stage_thrust(stage, atm.pressure) if stage is not None else 0.0
            ux, uy = pitch.direction(time)
            g = gravity(safe_alt) if config.include_gravity_loss else 0.0

            return np.array(
                [
                    vx,
                    vy,
                    thrust * ux / max(mass, 1e-9) + ax_drag,
                    thrust * uy / max(mass, 1e-9) + ay_drag - g,
                    -flow,
                ]
            )

        if config.integrator == "rk45":
            yn, _err = rk45_step(derivative, t, y, h)
        else:
            yn = fixed[config.integrator](derivative, t, y, h)

        # don't burn more propellant than the stage has
        if stage is not None:
            yn[4] = max(yn[4], y[4] - stage.propellant_mass)
        yn[1] = max(-1.0, yn[1])

        t += h
        if stage is not None:
            stage_elapsed += h
        y = yn

        atm = atmosphere(max(0.0, y[1]), config.atmosphere_model)
        speed = math.hypot(y[2], y[3])
        loads = aerodynamic_loads(
            max(0.0, y[1]),
            speed,
            vehicle.reference_area,
            vehicle.drag_coefficient,
            config.atmosphere_model,
        )
        thrust = _stage_thrust(stage, atm.pressure) if stage is not None else 0.0
        samples.append(_sample(t, y, thrust, loads, stage_index))

        if config.max_dynamic_pressure and loads.dynamic_pressure > config.max_dynamic_pressure:
            events.append(
                Event(
                    t,
                    "dynamic_pressure_limit",
                    float(y[1]),
                    speed,
                    float(y[4]),
                    {"limit": config.max_dynamic_pressure},
                )
            )
            break

        # apogee: vertical velocity crossed zero going down
        if len(samples) > 1 and samples[-2].state.vertical_velocity > 0 >= y[3]:
            events.append(Event(t, "apogee", float(y[1]), speed, float(y[4]), {}))
            samples[-1] = _sample(t, y, thrust, loads, stage_index, "apogee")
            if config.stop_at_apogee:
                break

    if stage_index >= len(stages) and not any(e.name == "burnout" for e in events):
        events.append(
            Event(
                t,
                "burnout",
                float(y[1]),
                float(math.hypot(y[2], y[3])),
                float(y[4]),
                {},
            )
        )

    from .vehicle import ideal_vehicle_delta_v

    ideal_dv = ideal_vehicle_delta_v(vehicle)
    metrics = compute_metrics(samples, ideal_dv)
    return SimulationResult(config, tuple(samples), tuple(events), metrics)
