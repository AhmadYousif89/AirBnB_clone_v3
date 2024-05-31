#!/usr/bin/python3
"""
Script that starts a Flask web application with a route:
>>  '/states_list' that displays an HTML page with a list of all State objects
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy Session"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays an HTML page with a list of all State objects"""
    states = list(storage.all("State").values())
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
