import streamlit as st
from streamlit import session_state as ss
from my_task import MyTask
import db_utils

class PageTasks:
    def __init__(self):
        self.name = "Tarefas"

    def create_task(self, crew=None):
        task = MyTask()   
        if 'tasks' not in ss:
            ss.tasks = []
        ss.tasks.append(task)
        task.edit = True                
        db_utils.save_task(task)

        if crew:
            crew.tasks.append(task)
            db_utils.save_crew(crew)

        return task

    def draw(self):
        with st.container():
            st.subheader(self.name)
            editing = False
            if 'tasks' not in ss:
                ss.tasks = db_utils.load_tasks()
            if 'crews' not in ss:
                ss.crews = db_utils.load_crews()

            task_assignment = {task.id: [] for task in ss.tasks}

            for crew in ss.crews:
                for task in crew.tasks:
                    task_assignment[task.id].append(crew.name)

            tabs = ["Todas as Tarefas", "Tarefas não Atribuídas"] + [crew.name for crew in ss.crews]
            tab_objects = st.tabs(tabs)

            with tab_objects[0]:
                st.markdown("#### Todas as Tarefas")
                for task in ss.tasks:
                    task.draw()
                    if task.edit:
                        editing = True
                if st.button('Nova Tarefa', on_click=self.create_task, disabled=editing, key="create_task_all"):
                    st.success("Nova tarefa criada com sucesso!")

            with tab_objects[1]:
                st.markdown("#### Tarefas não Atribuídas")
                unassigned_tasks = [task for task in ss.tasks if not task_assignment[task.id]]
                for task in unassigned_tasks:
                    unique_key = f"{task.id}_unasigned"
                    task.draw(key=unique_key)
                    if task.edit:
                        editing = True
                if st.button('Nova Tarefa', on_click=self.create_task, disabled=editing, key="create_task_unassigned"):
                    st.success("Nova tarefa criada com sucesso!")

            for i, crew in enumerate(ss.crews, 2):
                with tab_objects[i]:
                    st.markdown(f"#### Tarefas da Equipe: {crew.name}")
                    assigned_tasks = [task for task in crew.tasks]
                    for task in assigned_tasks:
                        unique_key = f"{task.id}_{crew.name}"
                        task.draw(key=unique_key)
                        if task.edit:
                            editing = True
                    if st.button('Nova Tarefa', on_click=self.create_task, disabled=editing, kwargs={'crew': crew}, key=f"create_task_{crew.name}"):
                        st.success("Nova tarefa criada e atribuída à equipe com sucesso!")

            if len(ss.tasks) == 0:
                st.write("Nenhuma tarefa definida ainda.")
                if st.button('Nova Tarefa', on_click=self.create_task, disabled=editing):
                    st.success("Nova tarefa criada com sucesso!")
