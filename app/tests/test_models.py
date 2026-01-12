from app.ksc.models import HostInfo, TaskInfo


def test_host_info_creation():
    host = HostInfo(
        id="123",
        name="server-01",
        display_name="Main Server",
        group_id=5,
        group_name="Managed Devices",
        status="1",
    )
    assert host.id == "123"
    assert host.name == "server-01"
    assert host.group_id == 5


def test_task_info_creation():
    task = TaskInfo(id="task-001", name="Virus Scan", type="Scan", state="Running")
    assert task.id == "task-001"
    assert task.state == "Running"
