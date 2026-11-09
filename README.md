# Rocket Trajectory Prediction Software

Point-mass multistage ascent sim. Python first, with a small C++ core and a
couple of MATLAB helpers for cross-checks.

Does the usual stuff: atmosphere, drag, thrust vs ambient pressure, sequential
staging, a pitch program, and a few integrators. Not a 6-DOF vehicle dynamics
code — no aero moments or structural modes. Wind profiles can be applied in the
planar flight model.

Extra toys: monte carlo, engine-out / early staging, aeroheating, recovery chutes,
range-safety footprint, thrust tables, max-q throttle helper.

## Setup

```bash
git clone https://github.com/NihalShore/Rocket-Trajectory-Prediction-Software.git
cd Rocket-Trajectory-Prediction-Software
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[test,plot]"
```

## Run something

```bash
python main.py
python main.py --vehicle small --step 0.05 --stop-apogee
python -m rocket_sim.cli --plot
python examples/crazy_features_demo.py
```

## Library usage

```python
from rocket_sim import (
    StageConfig, VehicleConfig, SimulationConfig, WindProfile, simulate,
)
from rocket_sim.guidance import gravity_turn_program

stage = StageConfig(
    name="S1",
    dry_mass=12000,
    propellant_mass=65000,
    thrust_vacuum=1.5e6,
    burn_time=100,
    thrust_sea_level=1.3e6,
)
vehicle = VehicleConfig([stage], payload_mass=900, reference_area=5.2, drag_coefficient=0.4)
wind = WindProfile([
    (0, 3, 0, 0),       # altitude, east, north, vertical (m/s)
    (1000, 8, 2, 0),
    (10000, 25, 5, 0),
])
config = SimulationConfig(
    vehicle, max_time=300, time_step=0.25, wind_profile=wind,
)

result = simulate(config, gravity_turn_program(8, 100, 12))
print(result.metrics)
```

Wind is interpolated by altitude and included in air-relative velocity, drag,
Mach number, and dynamic pressure. The current 2D solver projects the east/north
wind onto the launch azimuth; crosswind perpendicular to the launch plane is
not modeled. Wind values are retained in JSON and CSV telemetry.

## Layout

```
src/rocket_sim/     simulator
config/             yaml examples
examples/           scripts
tests/              pytest
cpp/                C++ mirror
matlab/             atmosphere + simple ascent
docs/               model notes
```

## Tests

```bash
pytest tests/ -q
```

Apache 2.0 — see LICENSE.
