"""Command-line entry point for the example vehicle."""
import argparse
from .config import StageConfig,VehicleConfig,SimulationConfig
from .guidance import gravity_turn_program
from .serialization import write_csv,write_json
from .simulation import simulate
def example_config():
    first=StageConfig("First stage",25000.,180000.,4.2e6,125.,3.5e6)
    second=StageConfig("Second stage",6500.,42000.,9.0e5,110.,specific_impulse_vacuum=340.)
    vehicle=VehicleConfig([first,second],1800.,10.5,.32,name="Reference two-stage vehicle")
    return SimulationConfig(vehicle,max_time=700.,time_step=.2,integrator="rk4")
def main(argv=None):
    parser=argparse.ArgumentParser(description="Run a conceptual point-mass ascent simulation.")
    parser.add_argument("--output",default="trajectory.json")
    parser.add_argument("--csv",default="trajectory.csv")
    parser.add_argument("--plot",action="store_true")
    parser.add_argument("--step",type=float,default=.2)
    args=parser.parse_args(argv)
    config=example_config()
    from dataclasses import replace
    config=replace(config,time_step=args.step)
    result=simulate(config,gravity_turn_program(12.,145.,8.))
    write_json(result,args.output); write_csv(result,args.csv)
    print(f"Peak altitude: {result.metrics.maximum_altitude/1000:.2f} km")
    print(f"Peak speed: {result.metrics.maximum_speed:.1f} m/s")
    print(f"Peak dynamic pressure: {result.metrics.maximum_dynamic_pressure/1000:.1f} kPa")
    print(f"Samples: {len(result.samples)}")
    if args.plot:
        from .plotting import plot_trajectory
        plot_trajectory(result)
    return 0
if __name__=="__main__": raise SystemExit(main())
