from speedrunC2.app import db

CREATED = "CREATED"
TASKED = "TASKED"
DONE = "DONE"


# Agent class 
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String)
    username = db.Column(db.String)





# ORM for a task 
class Task(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String)
    command_type = db.Column(db.String)
    cmd = db.Column(db.String)
    Status = db.Column(db.String)
    agent_id = db.Column(db.String
    )


class Operator(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True)
    salt = db.Column(db.String)
    salted_hash = db.Column(db.string)
    
