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
