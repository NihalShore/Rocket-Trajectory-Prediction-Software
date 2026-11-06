"""Compare still-air and crosswind relative-flow loads."""
from rocket_sim.winds import WindProfile
from rocket_sim.wind_aero import loads_with_wind
profile=WindProfile([(0.,0.,0.,0.),(10000.,25.,0.,0.),(20000.,40.,0.,0.)])
flow,loads=loads_with_wind(5000.,250.,0.,8.,.35,profile)
print("Relative speed:",flow.speed,"m/s")
print("Dynamic pressure:",loads.dynamic_pressure,"Pa")
print("Drag:",loads.drag,"N")
