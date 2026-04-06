from signalbridge.config import load_config

def test_load_config():
    config = load_config("examples/config.sample.yaml")
    assert "base_url" in config.api
