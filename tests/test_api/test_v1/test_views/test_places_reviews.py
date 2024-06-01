#!/usr/bin/python3
"""Test module for api/v1/views/places_reviews.py"""
import unittest
from api.v1.app import app
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models import storage


class TestPlacesReviews(unittest.TestCase):
    """Test class for Place reviews views"""

    def create_state(self):
        """Create a new state for testing"""
        state = State(name="Cairo")
        state.save()
        return state.id

    def create_city(self, state_id):
        """Create a new city for testing"""
        city = City(name="Giza", state_id=state_id)
        city.save()
        return city.id

    def create_place(self, user_id, city_id):
        """Create a new place for testing"""
        place = Place(
            name="Pyramids Heights",
            user_id=user_id,
            city_id=city_id,
            max_guest=6,
            number_rooms=3,
            number_bathrooms=2,
            price_by_night=100,
        )
        place.save()
        return place

    def create_user(self):
        """Create a new user for testing"""
        user = User(email="abc@13", password="123")
        user.save()
        return user.id

    def create_review(self, user_id, place_id):
        """Create a new review for testing"""
        review = Review(
            user_id=user_id,
            place_id=place_id,
            text="Great place to stay",
        )
        review.save()
        return review

    @classmethod
    def setUpClass(cls):
        """Setup for the test"""
        cls.prefix = '/api/v1'
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Teardown for the test"""
        storage.close()

    def test_get_place_reviews(self):
        """Test GET /places/<place_id>/reviews"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        review = self.create_review(u_id, place.id)
        url = "{}/places/{}/reviews".format(self.prefix, place.id)
        response = self.client.get(url)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]['id'], review.id)
        self.assertEqual(data[0]['user_id'], u_id)
        self.assertEqual(data[0]['place_id'], place.id)
        self.assertEqual(data[0]['text'], review.text)

    def test_with_invalid_place_id(self):
        """Test GET /places/<place_id>/reviews with invalid place id"""
        url = "{}/places/{}/reviews".format(self.prefix, "invalid_id")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_get_review(self):
        """Test GET /reviews/<review_id>"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        review = self.create_review(u_id, place.id)
        url = "{}/reviews/{}".format(self.prefix, review.id)
        response = self.client.get(url)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], review.id)
        self.assertEqual(data['user_id'], u_id)
        self.assertEqual(data['place_id'], place.id)
        self.assertEqual(data['text'], review.text)

    def test_with_invalid_review_id(self):
        """Test GET /reviews/<review_id> with invalid review id"""
        url = "{}/reviews/{}".format(self.prefix, "invalid_id")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_create_review(self):
        """Test POST /places/<place_id>/reviews"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        data = {
            "user_id": u_id,
            "place_id": place.id,
            "text": "Awesome place!",
        }
        url = "{}/places/{}/reviews".format(self.prefix, place.id)
        response = self.client.post(url, json=data)
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['user_id'], u_id)
        self.assertEqual(data['place_id'], place.id)
        self.assertEqual(data['text'], "Awesome place!")

    def test_create_with_invalid_json(self):
        """Test POST /places/<place_id>/reviews with invalid JSON"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        url = "{}/places/{}/reviews".format(self.prefix, place.id)
        response = self.client.post(url, data='')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "Not a JSON")

    def test_create_with_invalid_place_id(self):
        """Test POST /places/<place_id>/reviews with invalid place id"""
        u_id = self.create_user()
        data = {
            "user_id": u_id,
            "place_id": "invalid_id",
            "text": "Awesome place!",
        }
        url = "{}/places/{}/reviews".format(self.prefix, "invalid_id")
        response = self.client.post(url, json=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_create_with_invalid_user_id(self):
        """Test POST /places/<place_id>/reviews with invalid user id"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        data = {
            "user_id": "invalid_id",
            "place_id": place.id,
            "text": "Awesome place!",
        }
        url = "{}/places/{}/reviews".format(self.prefix, place.id)
        response = self.client.post(url, json=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_create_with_missing_user_id(self):
        """Test POST /places/<place_id>/reviews with missing user id"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        data = {
            "place_id": place.id,
            "text": "Awesome place!",
        }
        url = "{}/places/{}/reviews".format(self.prefix, place.id)
        response = self.client.post(url, json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "Missing user_id")

    def test_create_with_missing_text(self):
        """Test POST /places/<place_id>/reviews with missing text"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        data = {"user_id": u_id, "place_id": place.id}
        url = "{}/places/{}/reviews".format(self.prefix, place.id)
        response = self.client.post(url, json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "Missing text")

    def test_update_review(self):
        """Test PUT /reviews/<review_id>"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        review = self.create_review(u_id, place.id)
        url = "{}/reviews/{}".format(self.prefix, review.id)
        response = self.client.put(url, json={"text": "Not a great place"})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], review.id)
        self.assertEqual(data['user_id'], u_id)
        self.assertEqual(data['place_id'], place.id)
        self.assertEqual(data['text'], "Not a great place")

    def test_update_with_invalid_json(self):
        """Test PUT /reviews/<review_id> with invalid JSON"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        review = self.create_review(u_id, place.id)
        url = "{}/reviews/{}".format(self.prefix, review.id)
        response = self.client.put(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "Not a JSON")

    def test_update_with_invalid_review_id(self):
        """Test PUT /reviews/<review_id> with invalid review id"""
        url = "{}/reviews/{}".format(self.prefix, "invalid_id")
        response = self.client.put(url, json={"text": "Not a great place"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_delete_review(self):
        """Test DELETE /reviews/<review_id>"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        review = self.create_review(u_id, place.id)
        url = "{}/reviews/{}".format(self.prefix, review.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {})

    def test_delete_with_invalid_review_id(self):
        """Test DELETE /reviews/<review_id> with invalid review id"""
        url = "{}/reviews/{}".format(self.prefix, "invalid_id")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})


if __name__ == "__main__":
    unittest.main()
