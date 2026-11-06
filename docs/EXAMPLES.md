# Example workflows

## Run the compact demonstrator

```python
from rocket_sim.profiles import compact_demonstrator
from rocket_sim.simulation import simulate
result = simulate(compact_demonstrator())
print(result.metrics.maximum_altitude)
```

## Run a staged ascent with a pitch schedule

```python
from rocket_sim.profiles import two_stage_reference
from rocket_sim.guidance import gravity_turn_program
from rocket_sim.simulation import simulate
config = two_stage_reference()
result = simulate(config, gravity_turn_program(12.0, 145.0, 8.0))
```

## Export results

```python
from rocket_sim.serialization import write_json, write_csv
from rocket_sim.reporting import write_summary
write_json(result, "output/run.json")
write_csv(result, "output/run.csv")
write_summary(result, "output/summary.txt")
```

## Compare time steps

Run the same configuration with progressively smaller time steps. Keep the
vehicle and all other settings unchanged. Compare peak altitude, peak speed,
peak dynamic pressure, apogee time, and final downrange. Do not infer
convergence from one metric alone.

## Estimate orbital quantities

After a suitable insertion state is available, compute the radial and
tangential components in a consistent central-body frame and pass them to
the orbital analysis helpers. The current ascent simulator does not itself
produce a complete inertial orbital state, so frame conversion must be
performed by the caller.
