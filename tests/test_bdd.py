from pytest_bdd import scenarios, given, when, then
from datetime import datetime, timedelta
from tasks import filter_tasks_by_category, filter_tasks_by_priority, search_tasks, get_overdue_tasks

scenarios('feature/feature.feature')

# Shared task list
tasks = []

@given("an empty task list")
def given_empty_task_list():
    tasks.clear()

@when('I add a task with title "Test Task"')
def when_add_task():
    tasks.append({
        "id": 1,
        "title": "Test Task",
        "description": "A test task",
        "priority": "Medium",
        "category": "Personal",
        "due_date": "2030-01-01",
        "completed": False,
        "created_at": datetime.now().isoformat()
    })

@then("the task list should contain 1 task")
def then_task_list_has_one():
    assert len(tasks) == 1

@given('a task list with a task in category "Work"')
def given_task_in_category():
    tasks.clear()
    tasks.append({
        "id": 1,
        "title": "Work Task",
        "description": "Something for work",
        "priority": "Low",
        "category": "Work",
        "due_date": "2030-01-01",
        "completed": False,
        "created_at": datetime.now().isoformat()
    })

@when('I filter tasks by category "Work"')
def when_filter_category():
    global filtered
    filtered = filter_tasks_by_category(tasks, "Work")

@then("I should get 1 task back")
def then_one_task_back():
    assert len(filtered) == 1

@given('a task list with a "High" priority task')
def given_high_priority():
    tasks.clear()
    tasks.append({
        "id": 1,
        "title": "Urgent Task",
        "description": "Handle immediately",
        "priority": "High",
        "category": "Work",
        "due_date": "2030-01-01",
        "completed": False,
        "created_at": datetime.now().isoformat()
    })

@when('I filter tasks by priority "High"')
def when_filter_priority():
    global filtered
    filtered = filter_tasks_by_priority(tasks, "High")

@given('a task with title "Read Book" and description "Read about Python"')
def given_read_book():
    tasks.clear()
    tasks.append({
        "id": 1,
        "title": "Read Book",
        "description": "Read about Python",
        "priority": "Low",
        "category": "School",
        "due_date": "2030-01-01",
        "completed": False,
        "created_at": datetime.now().isoformat()
    })

@when('I search tasks with keyword "Python"')
def when_search_python():
    global filtered
    filtered = search_tasks(tasks, "Python")

@given("a task due yesterday and not completed")
def given_overdue_task():
    tasks.clear()
    tasks.append({
        "id": 1,
        "title": "Old Task",
        "description": "Overdue",
        "priority": "Low",
        "category": "Work",
        "due_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "completed": False,
        "created_at": datetime.now().isoformat()
    })

@when("I check for overdue tasks")
def when_check_overdue():
    global filtered
    filtered = get_overdue_tasks(tasks)
