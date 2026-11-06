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

The time-domain model consumes the configured propellant mass uniformly over
the nominal burn interval. The effective exhaust velocity for the ideal
velocity estimate is derived from vacuum thrust divided by this flow rate.
If a specific impulse is supplied, treat it as descriptive metadata unless
you separately reconcile it with the configured thrust and flow.

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
choices are `euler`, `heun`, `rk4`, and `rk45`. The RK45 option currently
uses the embedded fifth-order estimate on the fixed output grid; it does not
adapt the time step automatically.

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
