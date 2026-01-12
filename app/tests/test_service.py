from unittest.mock import MagicMock, patch

import pytest


# We need to patch the classes where they are imported in service.py
@pytest.mark.asyncio
async def test_ping(ksc_service):
    # Setup
    with patch("app.ksc.service.KlAkHostGroup") as MockHostGroup:
        mock_hg_instance = MockHostGroup.return_value
        mock_hg_instance.GetDomains.return_value = None  # Just needs to not raise

        # Act
        result = await ksc_service.ping()

        # Assert
        assert result == "pong"
        MockHostGroup.assert_called_once_with(ksc_service.server)


@pytest.mark.asyncio
async def test_list_hosts(ksc_service):
    # Setup
    with (
        patch("app.ksc.service.KlAkHostGroup") as MockHostGroup,
        patch("app.ksc.service.KlAkChunkAccessor") as MockChunkAccessor,
    ):
        # Mock HostGroup
        mock_hg = MockHostGroup.return_value
        mock_res = MagicMock()
        mock_res.OutPar.return_value = "fake_accessor"
        mock_hg.FindHosts.return_value = mock_res

        # Mock ChunkAccessor
        mock_ca = MockChunkAccessor.return_value
        mock_count_res = MagicMock()
        mock_count_res.RetVal.return_value = 1
        mock_ca.GetItemsCount.return_value = mock_count_res

        mock_chunk_res = MagicMock()
        mock_chunk_res.OutPar.return_value = {
            "KLCSP_ITERATOR_ARRAY": [
                {
                    "id": "h-1",
                    "name": "test-host",
                    "KLHST_WKS_DN": "Test Host",
                    "KLHST_WKS_GRP": 3,
                    "KLHST_WKS_STATUS": "1",
                }
            ]
        }
        mock_ca.GetItemsChunk.return_value = mock_chunk_res

        # Act
        hosts = await ksc_service.list_hosts()

        # Assert
        assert len(hosts) == 1
        assert hosts[0].id == "h-1"
        assert hosts[0].display_name == "Test Host"


@pytest.mark.asyncio
async def test_run_task(ksc_service):
    with patch("app.ksc.service.KlAkTasks") as MockTasks:
        mock_tasks = MockTasks.return_value

        result = await ksc_service.run_task("task-123")

        assert "started" in result
        mock_tasks.RunTask.assert_called_once_with(strTask="task-123")
