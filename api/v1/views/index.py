#!/usr/bin/python3
"""This module contanis routes for /status and /stats"""
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """Returns the status of an API"""

    return {"status": "OK"}, 200


@app_views.route('/stats')
def stats():
    """Return the number of each objects by type"""

    classes = {
        "users": "User",
        "places": "Place",
        "cities": "City",
        "states": "State",
        "amenities": "Amenity",
        "reviews": "Review",
    }
    return {key: storage.count(value) for key, value in classes.items()}
