"""Stable JSON and CSV export functions."""
import csv
import json
from pathlib import Path
from .simulation import SimulationResult


def write_json(result: SimulationResult, path):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return target


def write_csv(result: SimulationResult, path):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "time", "downrange", "altitude", "horizontal_velocity", "vertical_velocity",
        "speed", "mass", "thrust", "drag", "dynamic_pressure", "mach", "stage_index",
        "event", "wind_downrange", "wind_vertical", "air_relative_speed",
    ]
    with target.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for s in result.samples:
            writer.writerow({
                "time": s.time,
                "downrange": s.state.downrange,
                "altitude": s.state.altitude,
                "horizontal_velocity": s.state.horizontal_velocity,
                "vertical_velocity": s.state.vertical_velocity,
                "speed": s.state.speed,
                "mass": s.state.mass,
                "thrust": s.thrust,
                "drag": s.drag,
                "dynamic_pressure": s.dynamic_pressure,
                "mach": s.mach,
                "stage_index": s.stage_index,
                "event": s.event,
                "wind_downrange": s.wind_downrange,
                "wind_vertical": s.wind_vertical,
                "air_relative_speed": s.air_relative_speed,
            })
    return target


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
