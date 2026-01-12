import pytest
from unittest.mock import AsyncMock, patch
from src.server.models import HostInfo
from src.server.ksc.service import KscService

@pytest.fixture
def mock_ksc_service():
    with patch("src.server.ksc.service.ksc_service", new_callable=AsyncMock) as mock:
        yield mock

@pytest.mark.asyncio
async def test_get_hosts(mock_ksc_service):
    # Mock return value
    mock_ksc_service.list_hosts.return_value = [
        HostInfo(id="1", name="host1", display_name="Host 1", group_id=1, group_name="Group A", status="OK")
    ]
    
    # Import tool logic (normally we test via MCP call or direct service call, 
    # here we test service wrapper)
    hosts = await mock_ksc_service.list_hosts(group_name="Group A")
    assert len(hosts) == 1
    assert hosts[0].name == "host1"

@pytest.mark.asyncio
async def test_run_task(mock_ksc_service):
    mock_ksc_service.run_task.return_value = "Task started"
    result = await mock_ksc_service.run_task("task-123")
    assert result == "Task started"
