"""Rocket trajectory simulation toolkit."""
__version__ = "0.1.0"
from .config import SimulationConfig, StageConfig, VehicleConfig
from .simulation import SimulationResult, simulate
__all__ = ["SimulationConfig", "StageConfig", "VehicleConfig", "SimulationResult", "simulate", "__version__"]
