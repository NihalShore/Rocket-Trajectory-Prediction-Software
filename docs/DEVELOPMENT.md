# Development guide

## Environment

Use Python 3.10 or newer. Install the package with the same extras used by CI:

    python -m pip install -e ".[test,plot]"
    pytest tests/ -q

## Design conventions

- All internal physical quantities use SI units.
- Public configuration records are immutable dataclasses.
- Numerical helpers should validate domains before computing.
- Keep optional dependencies out of package import paths.
- Add a focused test whenever a physical relation or numerical behavior changes.
- Document approximations and validity ranges rather than implying higher fidelity.

## Adding a model

A new model should have a narrow interface, explicit units, deterministic
behavior, and tests at limiting cases. Prefer small pure functions for
physical relationships. Keep simulation orchestration separate from plotting,
serialization, and command-line concerns.

## Reproducibility

Monte Carlo utilities accept explicit seeds. Record configuration metadata,
the parameter distributions, and software version alongside analysis results.
