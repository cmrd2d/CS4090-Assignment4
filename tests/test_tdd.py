import pytest
from datetime import datetime, timedelta
from tasks import mark_all_completed
from tasks import filter_tasks_by_due_range
from tasks import get_task_summary

def test_mark_all_completed_marks_incomplete_tasks():
    tasks = [
        {"id": 1, "completed": False},
        {"id": 2, "completed": True},
        {"id": 3, "completed": False}
    ]
    mark_all_completed(tasks)
    assert all(task["completed"] for task in tasks)


def test_get_task_summary_counts_correctly():
    tasks = [
        {"id": 1, "completed": True},
        {"id": 2, "completed": False},
        {"id": 3, "completed": True}
    ]
    total, completed, incomplete = get_task_summary(tasks)
    assert total == 3
    assert completed == 2
    assert incomplete == 1


def test_filter_tasks_by_due_range_filters_correctly():
    tasks = [
        {"id": 1, "due_date": "2025-04-01"},
        {"id": 2, "due_date": "2025-04-15"},
        {"id": 3, "due_date": "2025-04-20"},
        {"id": 4, "due_date": "2025-04-25"}
    ]
    filtered = filter_tasks_by_due_range(tasks, "2025-04-10", "2025-04-20")
    assert [task["id"] for task in filtered] == [2, 3]

sample_tasks = [
    {"id": 1, "title": "Task 1", "completed": False, "due_date": "2025-04-25"},
    {"id": 2, "title": "Task 2", "completed": True, "due_date": "2025-04-26"},
    {"id": 3, "title": "Task 3", "completed": False, "due_date": "2025-04-28"},
]

def test_mark_all_completed_marks_all_tasks():
    tasks = [dict(t) for t in sample_tasks]
    mark_all_completed(tasks)
    assert all(task["completed"] for task in tasks)

def test_mark_all_completed_empty_list():
    tasks = []
    mark_all_completed(tasks)
    assert tasks == []

def test_get_task_summary_counts():
    summary = get_task_summary(sample_tasks)
    assert summary == (3, 1, 2)

def test_get_task_summary_empty():
    summary = get_task_summary([])
    assert summary == (0, 0, 0)

def test_filter_tasks_by_due_range_inclusive():
    start = "2025-04-25"
    end = "2025-04-26"
    filtered = filter_tasks_by_due_range(sample_tasks, start, end)
    assert len(filtered) == 2
    assert all(start <= task["due_date"] <= end for task in filtered)

def test_filter_tasks_by_due_range_excludes_outside():
    start = "2025-04-27"
    end = "2025-04-27"
    filtered = filter_tasks_by_due_range(sample_tasks, start, end)
    assert filtered == []

def test_filter_tasks_by_due_range_handles_invalid_date():
    tasks = [
        {"id": 1, "title": "Bad Date", "due_date": "invalid-date", "completed": False},
        {"id": 2, "title": "Valid Task", "due_date": "2025-04-28", "completed": False},
    ]
    filtered = filter_tasks_by_due_range(tasks, "2025-04-28", "2025-04-28")
    assert len(filtered) == 1
    assert filtered[0]["title"] == "Valid Task"
