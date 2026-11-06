# Numerical methods and verification notes

## Fixed-step integration

The simulator supports explicit Euler, Heun's method, and classical RK4.
Each method advances the coupled position, velocity, and mass state using
the same derivative function. The configured time step is an upper bound:
the last step of each burn is shortened to land on the nominal burnout time.

The embedded Dormand-Prince 5(4) method computes two approximations and an
error estimate. The present integration driver uses the fifth-order estimate
on the requested output grid. It does not yet adapt the step size using the
error estimate, so it should be treated as a fixed-step high-order method.

## Event resolution

Stage burnout is aligned to the nominal burn duration. Stage dry mass and
fairing mass are removed at the transition. After the last stage, the vehicle
continues on a ballistic coast until the requested end time, ground crossing,
or an enabled apogee stop. Apogee is detected from a change in the sign of
vertical velocity and interpolated only to the resolution of the output step.

Dynamic-pressure limit events are sampled at output times. This is not a
continuous root finder and can miss a very short excursion between samples.
Reduce the step size when examining sharp transients.

## Convergence checks

For a selected configuration, repeat the run with successively smaller time
steps. Compare peak altitude, peak speed, peak dynamic pressure, burnout time,
and downrange distance. A converged result should change by less than the
tolerance appropriate to the study. The tolerance must be chosen before
reviewing the results.

## Independent checks

Use the ideal rocket equation as a propulsion upper-bound check, not as a
prediction of achieved velocity. Compare the Python, C++, and MATLAB
implementations of shared atmosphere and integration equations. Agreement
between implementations is a useful software check but does not validate
the physical assumptions shared by all of them.
