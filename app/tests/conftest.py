import sys
from unittest.mock import MagicMock

import pytest

# Mock KlAkOAPI modules before they are imported by app code
# This is critical because they might not exist in the test environment
# or we don't want to actually connect
module_mock = MagicMock()
sys.modules["KlAkOAPI"] = module_mock
sys.modules["KlAkOAPI.AdmServer"] = module_mock
sys.modules["KlAkOAPI.HostGroup"] = module_mock
sys.modules["KlAkOAPI.Tasks"] = module_mock
sys.modules["KlAkOAPI.ChunkAccessor"] = module_mock
sys.modules["KlAkOAPI.Params"] = module_mock
sys.modules["KlAkOAPI.Error"] = module_mock

from app.ksc.service import KscService  # noqa: E402


@pytest.fixture
def mock_ksc_server():
    """Mocks the KlAkAdmServer.Create return value."""
    mock_server = MagicMock()
    mock_server.connected = True
    return mock_server


@pytest.fixture
def ksc_service(mock_ksc_server):
    """Returns a KscService instance with a mocked server."""
    service = KscService()
    # Inject the mocked server directly to bypass connection logic
    service.server = mock_ksc_server
    service._connected = True
    return service
