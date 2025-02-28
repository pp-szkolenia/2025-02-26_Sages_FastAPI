import streamlit as st
import pandas as pd


def tasks_page(tasks):
    st.header("Manage Tasks")

    # Display tasks
    df_tasks = pd.DataFrame(tasks)
    st.write("### Existing Tasks")
    st.dataframe(df_tasks)

    # Layout with two columns for Add and Update
    col1, col2 = st.columns(2)

    with col1:
        with st.form("new_task_form"):
            st.subheader("Add New Task")
            description = st.text_input("Description")
            priority = st.selectbox("Priority", [1, 2, 3])
            is_completed = st.checkbox("Completed")
            submit_task = st.form_submit_button("Add Task")

            if submit_task:
                new_task = {"id": len(tasks) + 1, "description": description, "priority": priority,
                            "is_completed": is_completed}
                tasks.append(new_task)
                st.success("Task added successfully!")
                # API CALL: POST /tasks (send new_task)

    with col2:
        with st.form("update_task_form"):
            st.subheader("Update Task")
            task_id = st.number_input("Enter Task ID to update", min_value=1, step=1)
            description = st.text_input("New Description")
            priority = st.selectbox("New Priority", [1, 2, 3])
            is_completed = st.checkbox("Completed")
            submit_update = st.form_submit_button("Update Task")

            if submit_update:
                for task in tasks:
                    if task["id"] == task_id:
                        task["description"] = description
                        task["priority"] = priority
                        task["is_completed"] = is_completed
                        st.success(f"Task {task_id} updated successfully!")
                        # API CALL: PUT /tasks/{task_id} (update task data)

    # Delete task
    delete_task_id = st.number_input("Enter Task ID to delete", min_value=1, step=1)
    if st.button("Delete Task"):
        tasks = [task for task in tasks if task["id"] != delete_task_id]
        st.success(f"Task {delete_task_id} deleted successfully!")
        # API CALL: DELETE /tasks/{delete_task_id}
