#!/usr/bin/python3
"""
Script that starts a Flask web application with a route:
>>  '/states' that displays a list of all States
>>  '/states/<state_id>' that displays a list of all Cities in a State
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy Session"""
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def states(state_id=None):
    """Displays a list of all States or Cities in a State"""
    states = storage.all("State")
    if state_id:
        state_id = "State.{}".format(state_id)
    return render_template('9-states.html', states=states, state_id=state_id)


if __name__ == '__main__':
    app.run()
