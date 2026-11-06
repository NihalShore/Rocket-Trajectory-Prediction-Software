"""
Rocket Trajectory Prediction Software
=====================================

3-DOF multistage ascent simulator with atmosphere, drag and thrust modelling.

Quick start
-----------
>>> from rocket_traj import make_model_rocket_stage, run_simple
>>> stage = make_model_rocket_stage("C6")
>>> traj = run_simple([stage], launch_angle_deg=85)
>>> print(traj.summary())
"""

from .propulsion import (
    ThrustCurve,
    Motor,
    Stage,
    make_solid_stage,
    make_model_rocket_stage,
    estes_c6,
    estes_d12,
)
from .simulation import SimulationEngine, run_simple
from .dynamics import FlightState, Trajectory
from .atmosphere import AtmosphereModel
from .aerodynamics import DragModel
from .monte_carlo import run_dispersion
from .optimization import grid_search_1d, apogee_vs_burn_time

__version__ = "0.2.0"

__all__ = [
    "ThrustCurve",
    "Motor",
    "Stage",
    "make_solid_stage",
    "make_model_rocket_stage",
    "estes_c6",
    "estes_d12",
    "SimulationEngine",
    "run_simple",
    "FlightState",
    "Trajectory",
    "AtmosphereModel",
    "DragModel",
    "run_dispersion",
    "grid_search_1d",
    "apogee_vs_burn_time",
    "__version__",
]
