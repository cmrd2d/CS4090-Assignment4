import os
import json
import pytest
import datetime
from tasks import (
    load_tasks,
    save_tasks,
    generate_unique_id,
    filter_tasks_by_priority,
    filter_tasks_by_category,
    filter_tasks_by_completion,
    search_tasks,
    get_overdue_tasks,
)
from tasks import get_overdue_tasks
import tasks

TEST_FILE = "test_tasks.json"

@pytest.fixture(autouse=True)
def clean_test_file():
    """Setup and teardown for each test."""
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def test_load_tasks_file_not_exist():
    tasks = load_tasks(file_path="nonexistent.json")
    assert tasks == []

def test_load_tasks_invalid_json(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{bad json}")
    tasks = load_tasks(file_path=str(bad_file))
    assert tasks == []

def test_save_and_load_tasks():
    tasks_data = [{"id": 1, "title": "Test Task", "completed": False}]
    save_tasks(tasks_data, file_path=TEST_FILE)
    loaded = load_tasks(file_path=TEST_FILE)
    assert loaded == tasks_data

def test_generate_unique_id_empty():
    assert generate_unique_id([]) == 1

def test_generate_unique_id_nonempty():
    tasks = [{"id": 1}, {"id": 2}, {"id": 10}]
    assert generate_unique_id(tasks) == 11

def test_filter_tasks_by_priority():
    tasks = [
        {"id": 1, "priority": "High"},
        {"id": 2, "priority": "Low"},
    ]
    high_tasks = filter_tasks_by_priority(tasks, "High")
    assert len(high_tasks) == 1
    assert high_tasks[0]["id"] == 1

def test_filter_tasks_by_category():
    tasks = [
        {"id": 1, "category": "Work"},
        {"id": 2, "category": "Personal"},
    ]
    personal = filter_tasks_by_category(tasks, "Personal")
    assert len(personal) == 1
    assert personal[0]["id"] == 2

def test_filter_tasks_by_completion_true():
    tasks = [
        {"id": 1, "completed": True},
        {"id": 2, "completed": False},
    ]
    completed = filter_tasks_by_completion(tasks, completed=True)
    assert len(completed) == 1
    assert completed[0]["id"] == 1

def test_filter_tasks_by_completion_false():
    tasks = [
        {"id": 1, "completed": True},
        {"id": 2, "completed": False},
    ]
    incomplete = filter_tasks_by_completion(tasks, completed=False)
    assert len(incomplete) == 1
    assert incomplete[0]["id"] == 2

def test_search_tasks_title_and_description():
    tasks = [
        {"id": 1, "title": "Buy milk", "description": "Grocery shopping"},
        {"id": 2, "title": "Homework", "description": "Math exercises"},
    ]
    results = search_tasks(tasks, "milk")
    assert len(results) == 1
    assert results[0]["id"] == 1

    results = search_tasks(tasks, "math")
    assert len(results) == 1
    assert results[0]["id"] == 2

def test_get_overdue_tasks(monkeypatch):
    class MockDateTime(datetime.datetime):
        @classmethod
        def now(cls):
            return cls.strptime("2024-01-01", "%Y-%m-%d")
    
    monkeypatch.setattr(tasks, "datetime", MockDateTime)

    tasks_list = [
        {"id": 1, "due_date": "2023-12-31", "completed": False},
        {"id": 2, "due_date": "2024-01-02", "completed": False},
        {"id": 3, "due_date": "2023-12-31", "completed": True},
    ]

    overdue = tasks.get_overdue_tasks(tasks_list)
    assert len(overdue) == 1
    assert overdue[0]["id"] == 1
