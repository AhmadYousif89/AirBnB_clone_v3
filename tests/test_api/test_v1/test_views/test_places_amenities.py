#!/usr/bin/python3
"""Test module for api/v1/views/places_amenities.py"""
import unittest
from api.v1.app import app
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models import storage, storage_type


@unittest.skipIf(storage_type != "db", "Testing DB storage only")
class TestPlacesAmenities(unittest.TestCase):
    """Test class for Place amenities views"""

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

    def create_amenity(self):
        """Create a new amenity for testing"""
        amenity = Amenity(name="Wifi")
        amenity.save()
        return amenity

    @classmethod
    def setUpClass(cls):
        """Setup for the test"""
        cls.prefix = '/api/v1'
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Teardown for the test"""
        storage.close()

    def test_place_amenities(self):
        """Test the get place_amenities route"""
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        u_id = self.create_user()
        place = self.create_place(u_id, c_id)
        amenity = self.create_amenity()
        place.amenities.append(amenity)
        url = "{}/places/{}/amenities".format(self.prefix, place.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], amenity.id)
        self.assertEqual(data[0]['name'], amenity.name)

    def test_place_amenities_404(self):
        """Test the get place_amenities route with 404 error"""
        url = "{}/places/{}/amenities".format(self.prefix, "12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_create_place_amenity(self):
        """Test the post place_amenity route"""
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        u_id = self.create_user()
        place = self.create_place(u_id, c_id)
        amenity = self.create_amenity()
        url = "{}/places/{}/amenities/{}"
        response = self.client.post(
            url.format(self.prefix, place.id, amenity.id)
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['id'], amenity.id)
        self.assertEqual(data['name'], amenity.name)

    def test_create_with_invalid_place_id(self):
        """Test the create_place_amenity route with invalid place id"""
        amenity = self.create_amenity()
        url = "{}/places/{}/amenities/{}".format(self.prefix, "1", amenity.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_create_with_invalid_amenity_id(self):
        """Test the create_place_amenity route with invalid amenity id"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        url = "{}/places/{}/amenities/{}".format(self.prefix, place.id, "1")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_create_with_existing_amenity(self):
        """Test the create_place_amenity route with existing amenity"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        amenity = self.create_amenity()
        place.amenities.append(amenity)
        url = "{}/places/{}/amenities/{}".format(
            self.prefix, place.id, amenity.id
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], amenity.id)
        self.assertEqual(data['name'], amenity.name)

    def test_delete_place_amenity(self):
        """Test the delete place_amenity route"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        amenity = self.create_amenity()
        place.amenities.append(amenity)
        url = "{}/places/{}/amenities/{}".format(
            self.prefix, place.id, amenity.id
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {})

    def test_delete_with_invalid_place_id(self):
        """Test the delete_place_amenity route with invalid place id"""
        amenity = self.create_amenity()
        url = "{}/places/{}/amenities/{}".format(self.prefix, "1", amenity.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_delete_with_invalid_amenity_id(self):
        """Test the delete_place_amenity route with invalid amenity id"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        url = "{}/places/{}/amenities/{}".format(self.prefix, place.id, "1")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_delete_with_non_linked_amenity(self):
        """Test the delete_place_amenity route with non associated amenity"""
        u_id = self.create_user()
        s_id = self.create_state()
        c_id = self.create_city(s_id)
        place = self.create_place(u_id, c_id)
        amenity = self.create_amenity()
        url = "{}/places/{}/amenities/{}".format(
            self.prefix, place.id, amenity.id
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})


if __name__ == "__main__":
    unittest.main()
