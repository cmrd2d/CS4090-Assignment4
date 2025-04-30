import streamlit as st
import pandas as pd
from datetime import datetime
from tasks import (
    load_tasks, save_tasks,
    filter_tasks_by_priority, filter_tasks_by_category,
    mark_all_completed, get_task_summary, filter_tasks_by_due_range
)
import os


def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")
        
        if submit_button and task_title:
            new_task = {
                "id": len(tasks) + 1,
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
    
    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    
    show_completed = st.checkbox("Show Completed Tasks")
    
    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    
    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()
    
    st.sidebar.header("PyTest!")

    if st.sidebar.button("Run Unit Tests"):
        st.write("Running tests...")
        import os
        exit_code = os.system("PYTHONPATH=src pytest --cov=tasks tests/ --maxfail=5 --disable-warnings -q")
        if exit_code == 0:
            st.success("All tests passed!")
        else:
            st.error("Some tests failed. Check the terminal output.")

    if st.sidebar.button("Generate HTML Report"):
        st.write("Generating HTML test report...")
        import os
        report_path = "tests/report.html"
        exit_code = os.system(f"PYTHONPATH=src pytest tests/ --html={report_path} --self-contained-html --disable-warnings")
        
        if exit_code == 0:
            st.success("HTML report generated successfully!")
            st.markdown(f"[View HTML Report]({report_path})", unsafe_allow_html=True)
        else:
            st.error("Some tests failed. HTML report still generated.")
            st.markdown(f"[View HTML Report]({report_path})", unsafe_allow_html=True)

    if st.sidebar.button("Check Coverage"):
        st.write("Running coverage report...")
        import os
        exit_code = os.system("PYTHONPATH=src pytest --cov=tasks --cov-report=term --disable-warnings tests/")

        if exit_code == 0:
            with open("coverage_output.txt", "r") as f:
                coverage_report = f.read()
            st.code(coverage_report, language="bash")
            st.success("Coverage check complete!")
        else:
            st.error("Tests failed during coverage check.")

    if st.sidebar.button("Run Parameterized Tests"):
        st.write("Running parameterized tests...")
        import os
        exit_code = os.system("PYTHONPATH=src pytest tests/test_param.py -k test_filter_tasks_by_priority -v")

        if exit_code == 0:
            with open("param_output.txt", "r") as f:
                output = f.read()
            st.code(output, language="bash")
            st.success("Parameterized tests passed!")
        else:
            st.error("Some parameterized tests failed. Check the output below.")
            with open("param_output.txt", "r") as f:
                output = f.read()
            st.code(output, language="bash")

    if st.sidebar.button("Run Mocking Test"):
        st.write("Running mocking test...")
        import os
        exit_code = os.system("PYTHONPATH=src pytest tests/test_mock.py -k test_load_tasks_with_mock -v")

        if exit_code == 0:
            with open("mock_output.txt", "r") as f:
                output = f.read()
            st.code(output, language="bash")
            st.success("Mocking test passed!")
        else:
            st.error("Mocking test failed. Check output below.")
            with open("mock_output.txt", "r") as f:
                output = f.read()
            st.code(output, language="bash")

    if st.sidebar.button("Run BDD Tests"):
        st.write("Running BDD tests...")
        import os
        exit_code = os.system("PYTHONPATH=src pytest tests/test_bdd.py --disable-warnings")

        if exit_code == 0:
            with open("bdd_output.txt", "r") as f:
                st.code(f.read(), language="bash")
            st.success("All BDD tests passed!")
        else:
            with open("bdd_output.txt", "r") as f:
                st.code(f.read(), language="bash")
            st.error("Some BDD tests failed.")

    if st.sidebar.button("Run Property-Based Tests"):
        st.write("Running property-based tests...")

        import subprocess
        import os
        result = subprocess.run(
            ["pytest", "tests/test_property.py", "-v", "--disable-warnings"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"}
        )

        st.code(result.stdout, language="bash")

        if result.returncode == 0:
            st.success("Property-based tests passed!")
        else:
            st.error("Some property-based tests failed. See output above.")



    # TDD Features Section
    st.subheader("Additional Tools")

    # Mark all completed
    if st.button("Mark All as Completed"):
        mark_all_completed(tasks)
        save_tasks(tasks)
        st.success("All tasks marked as completed.")
        st.rerun()

    # Task Summary
    total, completed, incomplete = get_task_summary(tasks)
    st.info(f"📋 Total: {total} | ✅ Completed: {completed} | ❌ Incomplete: {incomplete}")

    # Date Range Filtering
    st.markdown("### 📅 Filter Tasks by Due Date Range")
    start_date = st.date_input("Start Date", value=datetime.today())
    end_date = st.date_input("End Date", value=datetime.today())

    if st.button("Apply Date Filter"):
        filtered_tasks = filter_tasks_by_due_range(tasks, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        st.success(f"Showing tasks due between {start_date} and {end_date}")


if __name__ == "__main__":
    main()
