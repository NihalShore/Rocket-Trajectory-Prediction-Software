# Rocket Trajectory Prediction Software

A Python-first, planar point-mass simulator for multistage rocket ascent. It
models a prescribed pitch program, stage burns and separation, atmospheric
drag, gravity, and altitude-dependent wind. It is intended for education and
preliminary studies, not flight design or certification.

The solver has two translational dimensions: downrange and altitude. It does
not model attitude, aerodynamic moments, structural response, or cross-range
motion.

## Setup

    git clone https://github.com/NihalShore/Rocket-Trajectory-Prediction-Software.git
    cd Rocket-Trajectory-Prediction-Software
    python -m venv .venv
    source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
    pip install -e ".[test,plot]"

## Run

    python main.py
    python main.py --vehicle small --step 0.05 --stop-apogee
    python -m rocket_sim.cli --plot
    python examples/feature_analysis.py

Both main.py and python -m rocket_sim.cli use the same parser and simulation
implementation. Use --output run.json or --csv run.csv to write telemetry;
neither file is written unless requested.

## Library use

    from rocket_sim import (
        StageConfig,
        VehicleConfig,
        SimulationConfig,
        WindProfile,
        simulate,
    )
    from rocket_sim.guidance import gravity_turn_program

    stage = StageConfig(
        name="S1",
        dry_mass=12000,
        propellant_mass=65000,
        thrust_vacuum=1.5e6,
        burn_time=100,
        thrust_sea_level=1.3e6,
        thrust_curve=[
            (0, 0), (2, 1.2e6), (90, 1.5e6), (100, 0),
        ],
    )
    vehicle = VehicleConfig(
        [stage],
        payload_mass=900,
        reference_area=5.2,
        drag_coefficient=0.4,
    )
    wind = WindProfile([
        (0, 3, 0, 0),       # altitude, east, north, vertical (m/s)
        (1000, 8, 2, 0),
        (10000, 25, 5, 0),
    ])
    config = SimulationConfig(
        vehicle,
        max_time=300,
        time_step=0.25,
        integrator="rk45",
        wind_profile=wind,
    )
    pitch = gravity_turn_program(
        start_time=8,
        end_time=100,
        terminal_angle_deg=12,
    )

    result = simulate(config, pitch)
    print(result.metrics)

A stage thrust curve is optional and represents vacuum thrust against elapsed
stage burn time. Values between points are linearly interpolated. Propellant
consumption remains uniform over the configured burn duration, so the curve
should be consistent with the selected propellant load and burn time.

The wind table is stored in east/north/vertical components. The planar solver
projects east/north wind onto the launch azimuth and applies the vertical
component directly. Wind perpendicular to the launch plane is not modeled.
JSON stores the input wind profile; JSON and CSV samples store the projected
downrange and vertical wind components and air-relative speed.

## Analysis helpers

The package also includes Monte Carlo parameter perturbations, engine-out and
early-staging scenario helpers, Sutton-Graves heat-flux estimates, impact and
downrange-dispersion calculations, and a max-q throttle schedule helper.
These are analysis utilities: heat flux and dispersion are not certified
engineering assessments, and the throttle schedule is not fed back into the
flight integrator.

Parachute recovery dynamics are not part of the simulator.

## Other language directories

- cpp/ contains a small C++17 library for selected atmosphere, gravity, RK4,
  vehicle-mass, and ideal rocket-equation calculations. It is not a port of
  the Python flight solver.
- matlab/ contains selected equation helpers and an illustrative vertical
  ascent script. It is not feature-equivalent to the Python package.

## Tests

    pytest tests/ -q

Apache 2.0 — see LICENSE.
