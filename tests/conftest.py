import sys
from os.path import dirname, abspath
import pytest


# Ensure src is in path
# sys.path.append(dirname(dirname(abspath(__file__))))

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("KSC_HOST", "https://mock:13299")
    monkeypatch.setenv("KSC_USERNAME", "user")
    monkeypatch.setenv("KSC_PASSWORD", "pass")


def pytest_addoption(parser):
    parser.addoption(
        "--run-integration", action="store_true", default=False, help="run integration tests"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-integration"):
        return
    skip_integration = pytest.mark.skip(reason="need --run-integration option to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)
