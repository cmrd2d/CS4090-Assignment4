import pytest
from tasks import filter_tasks_by_priority

@pytest.mark.parametrize("priority,expected_count", [
    ("High", 1),
    ("Medium", 2),
    ("Low", 0),
])
def test_filter_tasks_by_priority(priority, expected_count):
    tasks = [
        {"id": 1, "priority": "High"},
        {"id": 2, "priority": "Medium"},
        {"id": 3, "priority": "Medium"},
    ]
    result = filter_tasks_by_priority(tasks, priority)
    assert len(result) == expected_count
