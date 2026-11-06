# Contribution guide

## Before changing a model

Identify the physical equation, units, expected domain, and limiting cases.
State whether a parameter is measured, derived, fitted, or merely illustrative.
If an approximation is introduced, document its consequences and expected
validity range.

## Code quality

Prefer small functions with explicit inputs and outputs. Avoid hidden global
state and nondeterministic behavior. Keep numerical routines independent from
plotting and file-system side effects. Use descriptive variable names and
document public APIs.

## Tests

Add tests for ordinary values, boundaries, invalid inputs, and limiting
behavior. When possible, compare a numerical routine with an analytical
solution or an independently calculated reference value. For an integration
change, include a step-size or convergence test.

## Documentation

Update the model reference and assumptions register when equations or
approximations change. Keep examples runnable and avoid presenting illustrative
parameters as operational data.

## Review checklist

- Are units explicit?
- Are input domains validated?
- Are numerical edge cases covered?
- Are events and stage transitions deterministic?
- Are output units documented?
- Are model limitations stated accurately?
- Do the Python and C++ reference implementations still agree on shared
  equations where both provide the same function?
