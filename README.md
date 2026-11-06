# Rocket Trajectory Prediction Software

A modular Python toolkit for conceptual multistage ascent simulation, trajectory analysis, and numerical-methods experimentation. The implementation includes a two-dimensional point-mass model with a layered lower-atmosphere approximation, altitude-dependent gravity, aerodynamic drag, prescribed pitch schedules, sequential stage burns, and JSON/CSV output.

## Capabilities

- Lower-atmosphere pressure, temperature, density, viscosity, and speed of sound.
- Inverse-square Earth gravity and ideal rocket-equation calculations.
- Generic Mach-dependent drag rise, dynamic pressure, and Reynolds-number estimates.
- Multistage propellant depletion, dry-mass separation, and pressure-adjusted thrust.
- Piecewise-linear pitch programs and Euler, Heun, RK4, and embedded RK45 stepping.
- Trajectory metrics, event records, diagnostics, data export, and optional plots.

## Installation

Python 3.10 or newer is required.

```bash
git clone https://github.com/NihalShore/Rocket-Trajectory-Prediction-Software.git
cd Rocket-Trajectory-Prediction-Software
python -m pip install -e '.[test,plot]'
pytest
```

## Run an example

```bash
rocket-sim --output output/trajectory.json --csv output/trajectory.csv
rocket-sim --plot
```

Or use the API:

```python
from rocket_sim.cli import example_config
from rocket_sim.guidance import gravity_turn_program
from rocket_sim.simulation import simulate

result = simulate(example_config(), gravity_turn_program(12, 145, 8))
print(result.metrics)
```

## Model scope and limitations

This is a transparent educational and preliminary-analysis model, not a flight dynamics or launch-operations system. It uses a planar point-mass state and prescribed pitch angle. The generic drag curve is not vehicle-specific aerodynamic data. The atmosphere is intended for lower-atmosphere studies and uses an isothermal pressure extrapolation above its tabulated layers. Engine thrust is represented by a constant nominal value with a simple ambient-pressure correction. The model does not resolve attitude, steering constraints, winds, staging transients, structural loads, thermal response, plume interactions, orbital perturbations, or range safety.

Treat results as exploratory estimates. Validate assumptions against authoritative engineering data before using outputs in consequential design decisions.

## Repository layout

- `src/rocket_sim/`: physics, configuration, numerical integration, simulation, metrics, and I/O.
- `tests/`: unit and integration tests.
- `examples/`: short API examples.

## License

See [LICENSE](LICENSE).
