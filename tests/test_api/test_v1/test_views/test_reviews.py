#!/usr/bin/python3
"""Test module for api/v1/views/reviews.py"""
import unittest
from api.v1.app import app
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models import storage


class TestReviews(unittest.TestCase):
    """Test class for Review views"""

    def create_state(self):
        """Create a new state for testing"""
        new_state = State(name="Cairo")
        storage.new(new_state)
        storage.save()
        return new_state.id

    def create_city(self, state_id):
        """Create a new city for testing"""
        new_city = City(name="Giza", state_id=state_id)
        storage.new(new_city)
        storage.save()
        return new_city.id

    def create_place(self, user_id, city_id):
        """Create a new place for testing"""
        new_place = Place(
            name="Pyramids Heights",
            user_id=user_id,
            city_id=city_id,
            max_guest=6,
            number_rooms=3,
            number_bathrooms=2,
            price_by_night=100,
        )
        storage.new(new_place)
        storage.save()
        return new_place.id

    def create_user(self):
        """Create a new user for testing"""
        new_user = User(email="abc@13", password="123")
        storage.new(new_user)
        storage.save()
        return new_user.id

    def create_review(self, user_id, place_id):
        """Create a new review for testing"""
        new_review = Review(
            user_id=user_id,
            place_id=place_id,
            text="Great place to stay",
        )
        storage.new(new_review)
        storage.save()
        return new_review.id

    @classmethod
    def setUpClass(cls):
        """Setup for the test"""
        cls.prefix = '/api/v1'
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Teardown for the test"""
        storage.close()

    def test_get_reviews(self):
        """Test get reviews"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        p_id = self.create_place(u_id, c_id)
        r_id = self.create_review(u_id, p_id)
        url = "{}/places/{}/reviews".format(self.prefix, p_id)
        response = self.client.get(url)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]['id'], r_id)
        self.assertEqual(data[0]['user_id'], u_id)
        self.assertEqual(data[0]["place_id"], p_id)

    def test_get_review(self):
        """Test get review"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        p_id = self.create_place(u_id, c_id)
        r_id = self.create_review(u_id, p_id)
        url = "{}/reviews/{}".format(self.prefix, r_id)
        response = self.client.get(url)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], r_id)
        self.assertEqual(data['user_id'], u_id)
        self.assertEqual(data["place_id"], p_id)

    def test_get_404(self):
        """Test get review with 404"""
        response = self.client.get('{}/reviews/invalid_id'.format(self.prefix))
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data, {"error": "Not found"})

    def test_create_review(self):
        """Test create review"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        p_id = self.create_place(u_id, c_id)
        url = "{}/places/{}/reviews".format(self.prefix, p_id)
        data = {"user_id": u_id, "text": "Great place to stay"}
        response = self.client.post(url, json=data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['user_id'], u_id)
        self.assertEqual(data["place_id"], p_id)
        self.assertEqual(data['text'], "Great place to stay")

    def test_create_with_no_json(self):
        """Test create review with no JSON"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        p_id = self.create_place(u_id, c_id)
        url = "{}/places/{}/reviews".format(self.prefix, p_id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "Not a JSON")

    def test_create_with_no_user_id(self):
        """Test create review with no user_id"""
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        p_id = self.create_place(self.create_user(), c_id)
        url = "{}/places/{}/reviews".format(self.prefix, p_id)
        response = self.client.post(url, json={"text": "Great place to stay"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing user_id", response.data.decode('utf-8'))

    def test_create_with_no_text(self):
        """Test create review with no text"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        p_id = self.create_place(u_id, c_id)
        url = "{}/places/{}/reviews".format(self.prefix, p_id)
        response = self.client.post(url, json={"user_id": u_id})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing text", response.data.decode('utf-8'))

    def test_update(self):
        """Test update review"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        p_id = self.create_place(u_id, c_id)
        r_id = self.create_review(u_id, p_id)
        url = "{}/reviews/{}".format(self.prefix, r_id)
        response = self.client.put(
            url, json={"text": "Awesome place to stay!"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertNotEqual(data['text'], "Great place to stay")
        self.assertEqual(data['text'], "Awesome place to stay!")

    def test_update_with_no_json(self):
        """Test update review with no JSON"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        p_id = self.create_place(u_id, c_id)
        r_id = self.create_review(u_id, p_id)
        url = "{}/reviews/{}".format(self.prefix, r_id)
        response = self.client.put(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "Not a JSON")

    def test_update_404(self):
        """Test update review with 404"""
        response = self.client.put(
            '{}/reviews/invalid_id'.format(self.prefix),
            json={"text": "Awesome place to stay!"},
        )
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data, {"error": "Not found"})

    def test_delete_review(self):
        """Test delete review"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        p_id = self.create_place(u_id, c_id)
        r_id = self.create_review(u_id, p_id)
        url = "{}/reviews/{}".format(self.prefix, r_id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{}\n')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_404(self):
        """Test delete review with 404"""
        response = self.client.delete(
            '{}/reviews/invalid_id'.format(self.prefix)
        )
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data, {"error": "Not found"})


if __name__ == "__main__":
    unittest.main()
