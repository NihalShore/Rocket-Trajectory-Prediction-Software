# Analysis workflows

## Parameter sensitivity

Use a deterministic baseline and change one parameter at a time. The
sensitivity helpers estimate local derivatives with central or forward
finite differences. Choose a perturbation large enough to exceed numerical
noise but small enough to remain in a locally smooth region. Repeat with
half and double the perturbation to inspect derivative stability.

## Monte Carlo exploration

The uncertainty module accepts a base SimulationConfig and perturbs stage
thrust, stage dry and propellant mass, and vehicle drag coefficient. Runs
accept an explicit random seed and return each SimulationResult plus summary
statistics for apogee, maximum dynamic pressure, maximum speed, and downrange.
Simulation errors are not suppressed. Record the seed, perturbation scales,
and metric definitions with each study.

## Constraint margins

The constraints module reports signed margin for upper- and lower-bound
checks. Positive margin indicates a satisfied constraint; negative margin
indicates a violation. Constraint limits should come from a separately
approved requirements source, not from tuning the model until it passes.

## Coefficient data

CoefficientTable interpolates a monotonic independent variable and supports
clamp, linear, and error extrapolation. Use it to hold externally sourced
coefficient data. Include provenance, reference area, Reynolds range, Mach
range, angle-of-attack range, and uncertainty alongside the table in the
calling application.

## Trajectory resampling

Trajectory utilities interpolate state variables between recorded output
samples and slice by time. Interpolation is linear and does not reconstruct
the continuous integrator solution. Use a sufficiently fine output step when
the local trajectory curvature or load gradient is important.
