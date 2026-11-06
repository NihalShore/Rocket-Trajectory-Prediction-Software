# Analysis workflows

## Parameter sensitivity

Use a deterministic baseline and change one parameter at a time. The
sensitivity helpers estimate local derivatives with central or forward
finite differences. Choose a perturbation large enough to exceed numerical
noise but small enough to remain in a locally smooth region. Repeat with
half and double the perturbation to inspect derivative stability.

## Monte Carlo exploration

The uncertainty module provides seeded scalar sampling and summary statistics.
A caller supplies the configuration factory that maps each sample to a full
simulation result. Record the random seed, distribution family, parameter
units, truncation rules, and metric name. A mean and percentile interval do
not replace inspection of multimodal or heavy-tailed distributions.

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
