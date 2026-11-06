# Cross-language reference implementations

The Python package is the primary end-to-end simulator. The C++ and MATLAB
folders contain small reference implementations of selected equations and
numerical routines. They are intended to make independent verification and
classroom comparison easier; they are not feature-identical ports.

## C++

The C++17 library includes the layered atmosphere approximation, inverse-square
gravity, vehicle mass validation, the ideal rocket equation, and a reusable
RK4 stepper.

Build and run the native checks:

```sh
cmake -S cpp -B cpp/build
cmake --build cpp/build --parallel
ctest --test-dir cpp/build --output-on-failure
./cpp/build/rocket_demo
```

The library uses SI units and standard-library facilities only. Public headers
are under `cpp/include/rocket`.

## MATLAB

The MATLAB scripts provide the atmosphere, ideal rocket equation, RK4 step,
aerodynamic load approximation, and a small vertical ascent demonstration.
Add the `matlab` folder to the MATLAB path and run `example_ascent`.

The demonstration is intentionally compact. It is useful for inspecting
individual terms and comparing numerical results, not for validating a real
vehicle. The Python package remains the reference for staged simulation and
result export.
