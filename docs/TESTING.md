# Testing strategy

The test suite is organized around independent responsibilities.

- Physics tests check limiting values and known analytical relationships.
- Configuration tests check invalid and boundary input handling.
- Integrator tests compare numerical updates against closed-form solutions.
- Simulation tests check monotonic time, mass depletion, staging, coast, and
  event recording.
- Analysis tests cover search methods, sensitivity estimates, uncertainty
  summaries, and telemetry transformations.
- Orbital tests check circular speed, escape speed, period, and transfer limits.
- Helper tests cover coordinate transforms, wind interpolation, and constraints.

Run the complete Python suite with the same commands used by CI:

    python -m pip install -e ".[test,plot]"
    pytest tests/ -q

The C++ reference library has a CMake/CTest suite. Its test executable checks
selected atmosphere, gravity, rocket-equation, and RK4 relationships.

A test passing establishes that the tested software behavior matches the
assertion. It does not establish that an empirical coefficient, vehicle
configuration, or model assumption is representative of a physical vehicle.
