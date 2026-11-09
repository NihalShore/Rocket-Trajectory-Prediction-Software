# Model reference

## State and reference frame

The integrator advances a planar state vector: downrange position, altitude,
horizontal velocity, vertical velocity, and total vehicle mass. The reference
frame is local and non-rotating unless the initial eastward surface velocity
option is enabled. The current propagation equations do not include curvature
of the trajectory or a rotating Earth frame.

## Translational equations

For vehicle mass m, thrust magnitude T, prescribed unit direction u, drag
magnitude D, speed relative to the air v_a, and gravitational acceleration
g(h), the implemented acceleration is the sum of thrust, drag opposite the
air-relative velocity vector, and vertical gravity. Propellant flow is
represented by a constant rate during each stage burn. Stage dry mass is
removed at the end of its burn interval.

The air-relative velocity is formed by subtracting the wind projected onto the
launch plane from the vehicle velocity. East/north wind is projected onto the
launch azimuth; the vertical wind component is used directly.

## Atmosphere

The tabulated lapse-rate layers are integrated hydrostatically using the
ideal-gas relation. Density follows p/(R T), sound speed follows sqrt(gamma R
T), and viscosity follows Sutherland's law. The model is not a complete
thermosphere model; high-altitude extrapolation is deliberately simple.

## Aerodynamics

Dynamic pressure is q = rho |v_a|^2 / 2. Drag is D = q A Cd and acts opposite
the air-relative velocity. The supplied coefficient curve adds a smooth
transonic rise to a baseline coefficient. Replace it with validated
vehicle-specific data for meaningful aerodynamic loads. Reynolds number uses
the equivalent circular reference length.

## Propulsion

The ideal rocket equation is used only for a theoretical velocity increment.
The time-domain model uses nominal thrust and propellant flow inferred from
stage propellant mass and nominal burn duration. The pressure correction is a
simple linear interpolation when sea-level thrust is provided.

## Numerical methods

Euler and Heun methods are first- and second-order explicit schemes. RK4 is
the default fixed-step method. The embedded Dormand-Prince routine returns a
fifth-order estimate and a fourth-order error estimate; the current simulator
uses the fifth-order state on the configured output step rather than a fully
adaptive error controller.

## Interpretation

This code is intended for education and preliminary sensitivity studies. It
does not provide a validated launch vehicle performance prediction, flight
control design, structural sizing, thermal analysis, or range-safety
assessment.
