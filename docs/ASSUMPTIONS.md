# Assumptions register

This register summarizes the main simplifications that affect interpretation.

| Area | Current assumption | Consequence |
|---|---|---|
| Geometry | Planar local frame | No full 3-D path or Earth curvature |
| Vehicle motion | Point mass | No attitude or flexible-body response |
| Guidance | Prescribed pitch schedule | No closed-loop steering |
| Gravity | Spherical inverse-square field | No oblateness or third bodies |
| Atmosphere | Layered lower-atmosphere approximation | High-altitude values are extrapolated |
| Wind | East/north wind projected onto launch azimuth; vertical wind applied directly | No wind component perpendicular to the launch plane |
| Drag | Generic Mach-dependent coefficient | Not vehicle-specific |
| Propulsion | Constant nominal stage thrust | No startup, shutdown, throttling, or transients |
| Propellant | Uniform mass flow during burn | No feed-system or mixture-ratio dynamics |
| Staging | Instantaneous dry-mass removal | No separation impulse or transient |
| Numerical events | Output-step detection | Short excursions can be missed |
| Orbital mechanics | Two-body analytical post-processing | No numerical perturbation propagation |

These assumptions are deliberate boundaries of the current implementation.
When a study depends on an excluded effect, extend the model and add tests
rather than silently interpreting the simplified result as high fidelity.
