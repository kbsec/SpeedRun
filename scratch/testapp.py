from flask import Flask 
from flask import request, abort

def ch0nky_ua(func):
    """
    Wraps a flask route to return a 403 if the user-agent isn't 'ch0nky'
    """
    def wrapped_func(*args, **kwargs):
        if request.headers.get('User-Agent') != "ch0nky":
            abort(403, description="You aren't ch0nky")
        return func(*args, **kwargs)
    return wrapped_func




app = Flask(__name__)




@app.route("/admin")
@ch0nky_ua
def admin():
    return "welcome admin!"


if __name__ == "__main__":
    app.run()
