# Frequently asked questions

## Why is the trajectory planar?

The current core is a compact two-dimensional point-mass model. It is easier
to inspect and validate than a full six-degree-of-freedom model. The C++
and MATLAB directories are selected-equation references, not full ports.

## Why does the atmosphere continue above its tabulated layers?

The implementation remains numerically defined for high-altitude trajectory
exploration. Above the last lower-atmosphere layer it uses an isothermal
pressure extrapolation. This is not a physical thermosphere representation.

## Why are the drag coefficients generic?

A vehicle-specific coefficient table requires geometry, Reynolds number,
Mach number, angle of attack, and test or validated computational data. The
built-in curve is a generic demonstration. The coefficient-table utility
allows callers to provide their own tabulated data.

## Why does RK45 not choose its own time step?

The embedded routine currently exposes a fifth-order state and error estimate
on the configured output grid. A future adaptive driver should add tolerance
controls, rejection logic, event localization, and tests for step-size
independence before being described as adaptive.

## Can this software certify a launch vehicle?

No. It is intended for learning, numerical-methods experimentation, and
preliminary trade studies. It is not a certified design, flight control,
launch operations, or range-safety tool.
