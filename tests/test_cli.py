from rocket_sim.cli import build_vehicle, main


def test_build_vehicle_variants():
    assert build_vehicle("small").name == "small solid"
    assert build_vehicle("demo").name == "two-stage reference"


def test_cli_accepts_shared_entry_point_options(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    status = main([
        "--vehicle", "small",
        "--step", "0.05",
        "--max-time", "0.2",
        "--stop-apogee",
    ])

    assert status == 0
    output = capsys.readouterr().out
    assert "vehicle : small solid" in output
    assert not (tmp_path / "trajectory.json").exists()
    assert not (tmp_path / "trajectory.csv").exists()
