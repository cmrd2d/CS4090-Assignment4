Feature: Task management behaviors

  Scenario: Adding a new task and saving it
    Given an empty task list
    When I add a task with title "Test Task"
    Then the task list should contain 1 task

  Scenario: Filtering tasks by category
    Given a task list with a task in category "Work"
    When I filter tasks by category "Work"
    Then I should get 1 task back

  Scenario: Filtering tasks by priority
    Given a task list with a "High" priority task
    When I filter tasks by priority "High"
    Then I should get 1 task back

  Scenario: Searching tasks by keyword
    Given a task with title "Read Book" and description "Read about Python"
    When I search tasks with keyword "Python"
    Then I should get 1 task back

  Scenario: Getting overdue tasks
    Given a task due yesterday and not completed
    When I check for overdue tasks
    Then I should get 1 task back
