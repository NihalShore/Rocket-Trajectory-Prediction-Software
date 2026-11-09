"""Rocket trajectory sim toolkit."""
__version__ = "0.2.0"

from .config import SimulationConfig, StageConfig, VehicleConfig
from .simulation import SimulationResult, simulate
from .guidance import PitchProgram, PitchKnot, gravity_turn_program, vertical_program
from .uncertainty import run_monte_carlo, print_summary
from .winds import WindProfile, WindVector, calm_wind, jet_streamish, random_wind, power_law

__all__ = [
    "SimulationConfig",
    "StageConfig",
    "VehicleConfig",
    "SimulationResult",
    "simulate",
    "PitchProgram",
    "PitchKnot",
    "gravity_turn_program",
    "vertical_program",
    "run_monte_carlo",
    "print_summary",
    "WindProfile",
    "WindVector",
    "calm_wind",
    "jet_streamish",
    "random_wind",
    "power_law",
    "__version__",
]
