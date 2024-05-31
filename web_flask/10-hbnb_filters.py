#!/usr/bin/python3
"""
Script that starts a Flask web application with a route:
>>  '/hbnb_filters' that displays a list of all States, Cities and Amenities
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy Session"""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Displays a list of all States, Cities and Amenities"""
    states = storage.all("State").values()
    amenities = storage.all("Amenity").values()
    return render_template(
        '10-hbnb_filters.html',
        stylesheets=True,
        states=states,
        amenities=amenities,
        css_file_prefix='10-',
    )


if __name__ == '__main__':
    app.run()
