from speedrunC2.app import db
from speedrunC2.models import Task, Agent
import logging



def create_task():
    task = Task(
        job_id= make_job_id() ,
        command_type = task_type, 
        cmd = task_command, 
        Status=CREATED,
        agent_id= agent_id
    )
    db.session.add(task)
    db.session.commit()
    logging.info(f"Created new task {task.job_id} for agent {task.agent_id}")
    return task
    