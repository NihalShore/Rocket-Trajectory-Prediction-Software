"""Evaluate an ideal two-impulse transfer between circular radii."""
from rocket_sim.constants import EARTH_RADIUS
from rocket_sim.orbital import hohmann_transfer
low=EARTH_RADIUS+300000.
high=EARTH_RADIUS+800000.
result=hohmann_transfer(low,high)
print(f"Departure impulse: {result['departure_delta_v']:.1f} m/s")
print(f"Arrival impulse: {result['arrival_delta_v']:.1f} m/s")
print(f"Transfer coast: {result['transfer_time']/3600:.2f} h")
