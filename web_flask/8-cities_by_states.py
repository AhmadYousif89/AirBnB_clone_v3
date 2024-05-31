#!/usr/bin/python3
"""
Script that starts a Flask web application with a route:
>>  '/cities_by_states' that displays a list of all City objects by State
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy Session"""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Displays a list of all City objects by State"""
    states = storage.all("State").values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run()
