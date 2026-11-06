# Orbital analysis utilities

The orbital module contains two-body relations for interpreting a state after
powered ascent. It provides circular and escape speed, vis-viva speed, orbital
period, osculating two-body elements for a planar radial/tangential velocity
pair, and a Hohmann transfer estimate between circular radii.

The calculations assume a point-mass central body with the package Earth
gravitational parameter. They omit oblateness, third-body perturbations,
atmospheric drag after insertion, thrust during transfer, finite-burn effects,
and all orbit-determination uncertainty. The functions are analytical checks,
not a full numerical orbit propagator.

For an elliptical orbit, the semi-major axis follows from specific orbital
energy. The specific angular momentum and energy determine eccentricity.
Periapsis and apoapsis radii are converted to altitudes using the supplied
body radius. Parabolic states have no finite semi-major axis or period;
hyperbolic states have no apoapsis or closed-orbit period.
