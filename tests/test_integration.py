import pytest
from src.server.ksc.service import ksc_service

# Marked as integration test - skipped by default unless --run-integration is passed
@pytest.mark.integration
@pytest.mark.asyncio
class TestRealConnection:
    
    async def test_real_ping(self):
        """
        Verifies real connectivity to the KSC server defined in .env.
        """
        print(f"\nAttempting to connect to {ksc_service.server}...")
        try:
            result = await ksc_service.ping()
            assert result == "pong"
        except Exception as e:
            pytest.fail(f"Real connection failed: {e}")

    async def test_real_list_hosts(self):
        """
        Verifies we can actually fetch hosts from the real server.
        """
        try:
            hosts = await ksc_service.list_hosts()
            assert isinstance(hosts, list)
            print(f"\nSuccessfully fetched {len(hosts)} hosts from KSC.")
        except Exception as e:
            pytest.fail(f"Real list_hosts failed: {e}")
