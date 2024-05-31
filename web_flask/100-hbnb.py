#!/usr/bin/python3
"""
Script that starts a Flask web application with a route:
>>  '/hbnb' that displays a list of all States, Cities and Amenities
"""
import os
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


def get_image_names():
    """Returns a list of image names without extension"""
    image_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
    return [
        os.path.splitext(f)[0]
        for f in os.listdir(image_dir)
        if os.path.isfile(os.path.join(image_dir, f))
    ]


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy Session"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb_filters():
    """Displays a list of all States, Cities and Amenities"""
    states = list(storage.all("State").values())
    places = list(storage.all("Place").values())
    amenities = list(storage.all("Amenity").values())
    return render_template(
        '100-hbnb.html',
        stylesheets=True,
        states=states,
        places=places[:6],  # Display only first 6 places
        amenities=amenities,
        css_file_prefix='102-',
        image_names=get_image_names(),
    )


if __name__ == '__main__':
    app.run()
