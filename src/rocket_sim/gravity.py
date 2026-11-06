"""Central-body gravity helpers."""
import math
from .constants import EARTH_MU,EARTH_RADIUS,G0
def gravity(altitude,model="inverse_square"):
    if altitude<=-EARTH_RADIUS: raise ValueError("altitude outside gravity model")
    if model=="constant": return G0
    if model=="inverse_square": return EARTH_MU/(EARTH_RADIUS+altitude)**2
    raise ValueError(f"unknown gravity model: {model}")
def gravitational_potential(altitude): return EARTH_MU*(1/EARTH_RADIUS-1/(EARTH_RADIUS+altitude))
def escape_speed(altitude=0.): return math.sqrt(2*EARTH_MU/(EARTH_RADIUS+altitude))
