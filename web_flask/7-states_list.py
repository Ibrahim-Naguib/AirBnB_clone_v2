#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /states_list: HTML page with a list of all State objects in DBStorage.
"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Displays an HTML page with a list of all State objects in DBStorage.

    States are sorted by name.
    """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template("7-states_list.html", sorted_states=sorted_states)


@app.teardown_appcontext
def teardown(exc):
    """removes the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
