import pytest
import logging
from server.ksc.service import ksc_service

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

    async def test_real_list_hosts_and_details(self):
        """
        Verifies we can fetch hosts and then get details for the first one.
        """
        try:
            # 1. List Hosts
            hosts = await ksc_service.list_hosts()
            assert isinstance(hosts, list)
            print(f"\nSuccessfully fetched {len(hosts)} hosts from KSC.")
            
            if len(hosts) > 0:
                first_host_id = hosts[0].id
                print(f"Testing details for host ID: {first_host_id} ({hosts[0].name})")
                
                # 2. Get Host Details
                details = await ksc_service.get_host_details(first_host_id)
                assert details is not None
                assert details.id == first_host_id
                print(f"Successfully fetched details for host {hosts[0].name}")
                
        except Exception as e:
            pytest.fail(f"Real host operations failed: {e}")

    async def test_real_list_tasks_and_state(self):
        """
        Verifies we can fetch tasks and get state for the first one.
        """
        try:
            # 1. List Tasks
            tasks = await ksc_service.list_tasks()
            assert isinstance(tasks, list)
            print(f"\nSuccessfully fetched {len(tasks)} tasks via MCP.")
            
            if len(tasks) > 0:
                first_task_id = tasks[0].id
                print(f"Testing state for task ID: {first_task_id} ({tasks[0].name})")
                
                # 2. Get Task State
                state = await ksc_service.get_task_state(first_task_id)
                assert state is not None
                assert hasattr(state, "state_desc")
                print(f"Successfully fetched state for task: {state.state_desc}")
                
        except Exception as e:
            pytest.fail(f"Real task operations failed: {e}")
