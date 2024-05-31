#!/usr/bin/python3
"""API routes for reviews"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def place_reviews(place_id):
    """Returns a list of reviews of a specific place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    return jsonify([review.to_dict() for review in place.reviews]), 200


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id):
    """Return a review by its id"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    return jsonify(review.to_dict()), 200


@app_views.route(
    "/reviews/<review_id>", methods=["DELETE"], strict_slashes=False
)
def delete_review(review_id):
    """Deletes a review using its id"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False
)
def create_review(place_id):
    """Creates a new review that is a related to a specific place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    try:
        review_data = request.get_json()
        if review_data is None:
            abort(400, description="Not a JSON")
    except Exception as e:
        abort(400, description="Not a JSON")

    if 'user_id' not in review_data:
        abort(400, "Missing user_id")

    user = storage.get(User, review_data['user_id'])

    if not user:
        abort(404)

    if 'text' not in review_data:
        abort(400, "Missing text")

    new_review = Review(**review_data)
    new_review.place_id = place_id

    storage.new(new_review)
    storage.save()

    return new_review.to_dict(), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a review"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    try:
        new_data = request.get_json()
        if new_data is None:
            abort(400, description="Not a JSON")
    except Exception as e:
        abort(400, description="Not a JSON")

    for key, value in new_data.items():
        if key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            continue
        setattr(review, key, value)

    review.save()

    return review.to_dict(), 200
