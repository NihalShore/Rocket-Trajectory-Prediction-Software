import csv

from rocket_sim.serialization import read_json, write_csv, write_json
from rocket_sim.simulation import simulate
from rocket_sim.config import StageConfig, VehicleConfig, SimulationConfig
from rocket_sim.winds import WindProfile


def test_exports_keep_unique_times_and_wind_telemetry(tmp_path):
    stage = StageConfig("stage", 100.0, 400.0, 12000.0, 20.0)
    vehicle = VehicleConfig([stage], 30.0, 0.8, 0.4)
    wind = WindProfile([(0.0, 4.0, 2.0, 1.0), (1000.0, 8.0, 3.0, 2.0)])
    config = SimulationConfig(
        vehicle,
        max_time=0.3,
        time_step=0.1,
        launch_azimuth_deg=90.0,
        wind_profile=wind,
    )
    result = simulate(config)

    json_path = write_json(result, tmp_path / "run.json")
    csv_path = write_csv(result, tmp_path / "run.csv")
    json_data = read_json(json_path)

    with csv_path.open(newline="", encoding="utf-8") as stream:
        csv_rows = list(csv.DictReader(stream))

    json_times = [sample["time"] for sample in json_data["samples"]]
    csv_times = [float(row["time"]) for row in csv_rows]
    assert len(json_times) == len(set(json_times))
    assert len(csv_times) == len(set(csv_times))
    assert json_data["samples"][0]["wind_downrange"] == 4.0
    assert json_data["samples"][0]["wind_vertical"] == 1.0
    assert float(csv_rows[0]["wind_downrange"]) == 4.0
    assert float(csv_rows[0]["wind_vertical"]) == 1.0
    assert "wind_profile" in json_data
    assert "air_relative_speed" in csv_rows[0]
