# Rocket Trajectory Prediction Software

Simulate multistage rocket ascent through the atmosphere with drag and thrust modelling.  
Python is the primary implementation; a lightweight C++ core and MATLAB scripts are also included for cross-checks and performance-critical loops.

## What it does

- 3-DOF point-mass equations of motion (down-range, cross-range, altitude)
- 1976 International Standard Atmosphere up to ~85 km
- Thrust curves (tabulated or generated) with multi-stage separation
- Aerodynamic drag (constant Cd or Mach table)
- Gravity turn after rail departure, optional custom pitch program
- Monte-Carlo dispersion and simple design optimisation helpers
- CSV / JSON / plot export

## Quick start

```bash
git clone https://github.com/NihalShore/Rocket-Trajectory-Prediction-Software.git
cd Rocket-Trajectory-Prediction-Software
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run the built-in model-rocket demo:

```bash
python main.py
```

Or a two-stage sounding-rocket config:

```bash
python main.py --config config/sounding_rocket.yaml --plot
```

Examples live under `examples/`:

```bash
python examples/simple_ascent.py
python examples/multistage.py
python examples/dispersion_study.py
```

## Project layout

```
src/rocket_traj/          Python package
  atmosphere/             ISA 1976
  aerodynamics/           drag models
  propulsion/             thrust curves, motors, stages
  dynamics/               state, EOM, integrators
  simulation/             high-level driver
  visualization/          matplotlib helpers
  monte_carlo/            dispersion analysis
  optimization/           grid search / simple GA
config/                   YAML vehicle definitions
examples/                 runnable scripts
tests/                    unit + integration tests
cpp/                      shared-library C++ core + CLI
matlab/                   atmosphere + single-stage solver
```

## Using the library

```python
from rocket_traj import make_solid_stage, SimulationEngine

stage = make_solid_stage(
    name="stage1",
    total_impulse=50000,   # N·s
    burn_time=6.0,
    propellant_mass=20.0,
    dry_mass=12.0,
    diameter=0.18,
)

eng = SimulationEngine([stage], launch_angle_deg=82, rail_length=6)
traj = eng.run()
print(traj.summary())
```

Config files are also supported – see `config/model_rocket.yaml` and `config/sounding_rocket.yaml`.

## C++ core

```bash
cd cpp
mkdir build && cd build
cmake ..
cmake --build .
./rocket_traj_cli 500 6 85    # thrust [N], burn [s], angle [deg]
```

## MATLAB

```matlab
addpath('matlab');
stage.dry_mass = 12;
stage.propellant_mass = 20;
stage.diameter = 0.18;
stage.thrust = 800;          % constant
stage.burn_time = 6;
traj = simulate_rocket(stage, struct('angle_deg', 85));
plot_trajectory(traj);
```

## Tests

```bash
pip install pytest
pytest tests/ -q
```

## Notes

- The gravity model is constant-g by default; inverse-square is available via a flag.
- Drag is axial only – no lift or moments.  Good enough for first-cut performance, not for stability work.
- Numbers in the example configs are illustrative, not flight-proven motors.

License: Apache 2.0 (see LICENSE).
