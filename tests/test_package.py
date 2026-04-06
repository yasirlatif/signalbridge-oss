import signalbridge


def test_package_exposes_version() -> None:
    assert signalbridge.__version__ == "0.1.0"
