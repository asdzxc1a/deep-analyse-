from src.example import ExampleRunner, load_config


def test_example_runner_defaults_to_dev(tmp_path):
    runner = ExampleRunner(tmp_path)
    assert runner.run() == "dev"


def test_load_config_tracks_path(tmp_path):
    config = load_config(tmp_path / "settings.toml")
    assert config["path"].endswith("settings.toml")
