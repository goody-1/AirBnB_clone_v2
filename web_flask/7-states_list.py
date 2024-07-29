#!/usr/bin/python3
"""simple flask script

Returns:
    dict: all states in the db
"""
from flask import Flask, render_template

from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def show_states():
    """display a HTML page with the states listed in alphabetical order"""
    all_states = storage.all(State)
    states = {}
    for key, value in all_states.items():
        states[key.split(".")[1]] = value.name
    # sorted_states = dict(sorted(states.items(), key=lambda item: item[1]))
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def close_db(error):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    # Start the Flask development server on 0.0.0.0:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
