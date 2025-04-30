from hypothesis import given
from hypothesis.strategies import text, lists, sampled_from, booleans, dates
from tasks import filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion, search_tasks, get_overdue_tasks
from datetime import datetime, timedelta

@given(lists(sampled_from(["High", "Medium", "Low"])))
def test_filter_by_priority_returns_correct_priority(priorities):
    tasks = [{"priority": p} for p in priorities]
    for level in ["High", "Medium", "Low"]:
        filtered = filter_tasks_by_priority(tasks, level)
        assert all(task["priority"] == level for task in filtered)

@given(lists(sampled_from(["Work", "Personal", "School", "Other"])))
def test_filter_by_category_returns_correct_category(categories):
    tasks = [{"category": c} for c in categories]
    for cat in set(categories):
        filtered = filter_tasks_by_category(tasks, cat)
        assert all(task["category"] == cat for task in filtered)

@given(lists(booleans()))
def test_filter_by_completion_only_returns_matching_status(completed_flags):
    tasks = [{"completed": flag} for flag in completed_flags]
    for status in [True, False]:
        filtered = filter_tasks_by_completion(tasks, status)
        assert all(task["completed"] == status for task in filtered)

@given(text(), text())
def test_search_tasks_finds_keywords(title, description):
    task = {"title": title, "description": description}
    query = title[:2] if title else "a"
    result = search_tasks([task], query)
    assert all(query.lower() in t["title"].lower() or query.lower() in t["description"].lower() for t in result)

@given(dates())
def test_get_overdue_tasks_only_returns_past_due_dates(due_date):
    task = {
        "due_date": (due_date - timedelta(days=1)).strftime("%Y-%m-%d"),
        "completed": False
    }
    today = datetime.now().date()
    if due_date < today:
        overdue = get_overdue_tasks([task])
        assert len(overdue) == 1
    else:
        overdue = get_overdue_tasks([task])
        assert len(overdue) == 0

