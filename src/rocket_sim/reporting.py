"""Human-readable summary generation for simulation results."""
from pathlib import Path
def format_summary(result):
    m=result.metrics
    rows=[("Vehicle",result.config.vehicle.name),("Samples",str(len(result.samples))),
    ("Elapsed time",f"{result.samples[-1].time:.2f} s"),("Maximum altitude",f"{m.maximum_altitude/1000:.3f} km"),
    ("Maximum speed",f"{m.maximum_speed:.2f} m/s"),("Maximum Mach",f"{m.maximum_mach:.3f}"),
    ("Maximum dynamic pressure",f"{m.maximum_dynamic_pressure/1000:.3f} kPa"),
    ("Maximum acceleration estimate",f"{m.maximum_acceleration:.3f} m/s²"),("Final mass",f"{m.final_mass:.2f} kg"),
    ("Ideal delta-v estimate",f"{m.ideal_delta_v:.2f} m/s")]
    width=max(len(k) for k,_ in rows)
    return "\n".join(f"{key:<{width}} : {value}" for key,value in rows)
def write_summary(result,path):
    target=Path(path); target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(format_summary(result)+"\n",encoding="utf-8")
    return target
