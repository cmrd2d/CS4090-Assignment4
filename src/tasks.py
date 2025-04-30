import json
import os
from datetime import datetime

# File path for task storage
DEFAULT_TASKS_FILE = "tasks.json"

def load_tasks(file_path=DEFAULT_TASKS_FILE):
    """
    Load tasks from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing tasks
        
    Returns:
        list: List of task dictionaries, empty list if file doesn't exist
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Warning: {file_path} contains invalid JSON. Renaming and creating new list.")
        os.rename(file_path, file_path + ".corrupt")
        return []

def save_tasks(tasks, file_path=DEFAULT_TASKS_FILE):
    """
    Save tasks to a JSON file.
    
    Args:
        tasks (list): List of task dictionaries
        file_path (str): Path to save the JSON file
    """
    try:
        with open(file_path, "w") as f:
            json.dump(tasks, f, indent=2)
    except (IOError, TypeError) as e:
        print(f"Error saving tasks to {file_path}: {e}")


def generate_unique_id(tasks):
    """
    Generate a unique ID for a new task.
    
    Args:
        tasks (list): List of existing task dictionaries
        
    Returns:
        int: A unique ID for a new task
    """
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1


def filter_tasks_by_priority(tasks, priority):
    """
    Filter tasks by priority level.
    
    Args:
        tasks (list): List of task dictionaries
        priority (str): Priority level to filter by (High, Medium, Low)
        
    Returns:
        list: Filtered list of tasks matching the priority
    """
    return [task for task in tasks if task.get("priority") == priority]

def filter_tasks_by_category(tasks, category):
    """
    Filter tasks by category.
    
    Args:
        tasks (list): List of task dictionaries
        category (str): Category to filter by
        
    Returns:
        list: Filtered list of tasks matching the category
    """
    return [task for task in tasks if task.get("category") == category]

def filter_tasks_by_completion(tasks, completed=True):
    """
    Filter tasks by completion status.
    
    Args:
        tasks (list): List of task dictionaries
        completed (bool): Completion status to filter by
        
    Returns:
        list: Filtered list of tasks matching the completion status
    """
    return [task for task in tasks if task.get("completed") == completed]

def search_tasks(tasks, query):
    """
    Search tasks by a text query in title and description.
    
    Args:
        tasks (list): List of task dictionaries
        query (str): Search query
        
    Returns:
        list: Filtered list of tasks matching the search query
    """
    query = str(query or "").lower()
    return [
        task for task in tasks 
        if query in task.get("title", "").lower() or 
           query in task.get("description", "").lower()
    ]

def get_overdue_tasks(tasks):
    """
    Get tasks that are past their due date and not completed.

    Args:
        tasks (list): List of task dictionaries

    Returns:
        list: List of overdue tasks
    """
    today = datetime.now().date()
    overdue_tasks = []
    for task in tasks:
        if task.get("completed", False):
            continue
        due_date_str = task.get("due_date", "")
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            if due_date < today:
                overdue_tasks.append(task)
        except ValueError:
            continue
    return overdue_tasks

def mark_all_completed(tasks):
    """
    Mark all tasks as completed.

    Args:
        tasks (list): List of task dictionaries
    """
    for task in tasks:
        task["completed"] = True


def get_task_summary(tasks):
    """
    Return a summary of task counts.

    Args:
        tasks (list): List of task dictionaries

    Returns:
        tuple: (total, completed, incomplete)
    """
    total = len(tasks)
    completed = sum(task.get("completed", False) for task in tasks)
    incomplete = total - completed
    return total, completed, incomplete


def filter_tasks_by_due_range(tasks, start, end):
    """
    Filter tasks whose due date falls between a given range.

    Args:
        tasks (list): List of task dictionaries
        start (str): Start date in 'YYYY-MM-DD' format
        end (str): End date in 'YYYY-MM-DD' format

    Returns:
        list: Filtered tasks within the date range
    """
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
    except ValueError:
        return []

    filtered = []
    for task in tasks:
        try:
            due_date = datetime.strptime(task.get("due_date", ""), "%Y-%m-%d").date()
            if start_date <= due_date <= end_date:
                filtered.append(task)
        except ValueError:
            continue
    return filtered
