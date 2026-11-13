# Configuration reference

All distances are metres, masses kilograms, forces newtons, time seconds,
angles degrees in configuration records, and pressures pascals. The numerical
state is always stored in SI units.

## StageConfig

A stage record includes a unique descriptive name, dry mass, usable propellant
mass, vacuum thrust, nominal burn duration, optional sea-level thrust, optional
specific impulse annotations, fairing mass, and separation timing metadata.
Dry mass, propellant mass, vacuum thrust, and burn duration must be positive.
Fairing mass and separation metadata cannot be negative.

An optional `thrust_curve` is a sequence of `(elapsed_time, vacuum_thrust)`
pairs in seconds and newtons. It must start at zero, end at the configured burn
time, use strictly increasing times, and stay at or below `thrust_vacuum`.
Thrust is linearly interpolated between points. When sea-level thrust is
configured, the pressure correction is applied as a time-varying scale using
the sea-level-to-vacuum thrust ratio.

Propellant is still consumed uniformly over the nominal burn interval. The
curve changes acceleration, not burn duration or mass flow. For a physically
consistent engine model, supply a curve and propellant/burn-time values that
represent the same engine operating point. The ideal velocity estimate uses
the stage's nominal vacuum thrust and nominal mass flow.

## VehicleConfig

Stages are ordered from the lowest stage to the uppermost stage. The vehicle
also defines payload mass, aerodynamic reference area, baseline drag
coefficient, and a display name. Initial mass is the payload plus the dry,
propellant, and fairing masses of every stage.

## SimulationConfig

The simulation record controls maximum propagation time, maximum integration
step, initial position, launch elevation and azimuth, latitude, Earth-rotation
initial velocity, gravity inclusion, atmosphere choice, integrator selection,
optional dynamic-pressure stopping threshold, and apogee stopping behavior.

The atmosphere selector accepts `ussa1976` and `exponential`. Integrator
choices are `euler`, `heun`, `rk4`, and `rk45`. RK45 adapts its internal
steps within each configured output interval; output samples remain on the
configured time grid.

## Pitch schedules

A PitchProgram is a piecewise-linear schedule. Each PitchKnot specifies time
and angle measured from the local horizontal. Ninety degrees is vertical
upward; zero degrees is horizontal. If no pitch program is supplied, the
launch elevation in SimulationConfig is held constant.

## Mapping-based construction

The profiles module contains helpers to construct VehicleConfig and
SimulationConfig records from ordinary mappings. This is useful when loading
a parameter file in a caller application. Validate untrusted external data
before passing it into a simulation.
