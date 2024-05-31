#!/usr/bin/python3
"""Test module for api.v1.views.amenities.py"""
import json
import unittest
from api.v1.app import app
from models.amenity import Amenity
from models import storage, storage_type


class TestAmenitiesView(unittest.TestCase):
    """Test class for amenities view module"""

    def create_amenity(self):
        """Create a new amenity for testing"""
        new_amenity = Amenity(name="Test")
        storage.new(new_amenity)
        storage.save()
        return new_amenity.id

    @classmethod
    def setUpClass(cls):
        """Set up for the test"""
        cls.prefix = "/api/v1"
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Delete all created amenities"""
        for amenity in storage.all(Amenity).values():
            storage.delete(amenity)
        storage.close()

    def test_get_all(self):
        """Test the GET method for amenities"""
        self.create_amenity()
        response = self.client.get("{}/amenities".format(self.prefix))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        if storage_type == "db":
            data = json.loads(response.data.decode("utf-8"))
            self.assertGreaterEqual(len(data), 1)
            self.assertIn("Test", str(response.data))

    def test_get_one(self):
        """Test the GET method for amenities with id"""
        a_id = self.create_amenity()
        response = self.client.get("{}/amenities/{}".format(self.prefix, a_id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(data["name"], "Test")

    def test_create_one(self):
        """Test the POST method for amenities"""
        response = self.client.post(
            "{}/amenities".format(self.prefix),
            data=json.dumps({"name": "Test2"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.content_type, "application/json")
        self.assertIn("name", data)
        self.assertEqual(data["name"], "Test2")

    def test_create_with_no_json(self):
        """Test the POST method for amenities with no JSON"""
        response = self.client.post(
            "{}/amenities".format(self.prefix),
            data="Not a JSON",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_with_no_name(self):
        """Test the POST method for amenities with no name"""
        data = {}
        response = self.client.post(
            "{}/amenities".format(self.prefix),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing name", response.data.decode('utf-8'))

    def test_update_one(self):
        """Test the PUT method for amenities"""
        a_id = self.create_amenity()
        data = {"name": "Test123"}
        response = self.client.put(
            "{}/amenities/{}".format(self.prefix, a_id),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertIn("Test123", str(response.data))

    def test_update_with_no_name(self):
        """Test the PUT method for amenities with no name"""
        a_id = self.create_amenity()
        response = self.client.put(
            "{}/amenities/{}".format(self.prefix, a_id),
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertIn("Test", str(response.data))

    def test_update_with_no_json(self):
        """Test the PUT method for amenities with no JSON"""
        a_id = self.create_amenity()
        response = self.client.put(
            "{}/amenities/{}".format(self.prefix, a_id),
            data="Not a JSON",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_one(self):
        """Test the DELETE method for amenities"""
        a_id = self.create_amenity()
        response = self.client.delete(
            "{}/amenities/{}".format(self.prefix, a_id)
        )
        self.assertEqual(response.data, b'{}\n')
        self.assertEqual(response.status_code, 200)
        response = self.client.get("{}/amenities/{}".format(self.prefix, a_id))
        self.assertIn("Not found", response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 404)

    def test_delete_one_404(self):
        """Test the DELETE method for amenities with id not found"""
        response = self.client.delete("{}/amenities/12".format(self.prefix))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertIn("Not found", response.data.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
