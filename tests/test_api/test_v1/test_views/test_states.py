#!/usr/bin/python3
"""Test module for api.v1.views.states.py"""
import unittest
from api.v1.app import app
from models.state import State
from models import storage, storage_type


class TestStates(unittest.TestCase):
    """Test cases for the states view module"""

    def create_state(self):
        """Create a new state for testing"""
        new_state = State(name="Cairo")
        storage.new(new_state)
        storage.save()
        return new_state.id

    @classmethod
    def setUpClass(cls):
        """Set up for the test cases"""
        cls.prefix = '/api/v1'
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Delete all created states"""
        storage.close()

    def test_get_all(self):
        """Test state GET route"""
        self.create_state()
        response = self.client.get('{}/states'.format(self.prefix))
        self.assertEqual(response.status_code, 200)
        if storage_type == "db":
            data = response.get_json()
            self.assertGreaterEqual(len(data), 1)

    def test_get_one(self):
        """Test state GET by id route"""
        s_id = self.create_state()
        response = self.client.get('{}/states/{}'.format(self.prefix, s_id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(s_id, response.data.decode('utf-8'))

    def test_get_one_404(self):
        """Test state GET by id route with 404"""
        response = self.client.get('{}/states/invalid_id'.format(self.prefix))
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"error": "Not found"})

    def test_create_one(self):
        """Test state POST route"""
        response = self.client.post(
            '{}/states/'.format(self.prefix), json={"name": "Giza"}
        )
        data = response.get_json()
        self.assertIn('name', data)
        self.assertEqual(data['name'], "Giza")
        self.assertEqual(response.status_code, 201)

    def test_create_with_no_json(self):
        """Test state POST route with no JSON data"""
        response = self.client.post('{}/states/'.format(self.prefix), data='')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "Not a JSON")

    def test_create_with_no_name(self):
        """Test state POST route with no name"""
        response = self.client.post(
            '{}/states/'.format(self.prefix), json={"not_name": "Giza"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "Missing name")

    def test_update_one(self):
        """Test state PUT route"""
        s_id = self.create_state()
        response = self.client.get('{}/states/{}'.format(self.prefix, s_id))
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], "Cairo")
        response = self.client.put(
            '{}/states/{}'.format(self.prefix, s_id),
            json={"name": "Alexandria"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], "Alexandria")

    def test_update_with_no_json(self):
        """Test state PUT route with no JSON data"""
        s_id = self.create_state()
        response = self.client.put(
            '{}/states/{}'.format(self.prefix, s_id), data=''
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "Not a JSON")

    def test_update_with_404(self):
        """Test state PUT route with 404"""
        response = self.client.put(
            '{}/states/invalid_id'.format(self.prefix),
            json={"name": "Alexandria"},
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"error": "Not found"})

    def test_delete_one(self):
        """Test state DELETE route"""
        s_id = self.create_state()
        response = self.client.get('{}/states/{}'.format(self.prefix, s_id))
        self.assertEqual(response.status_code, 200)
        response = self.client.delete('{}/states/{}'.format(self.prefix, s_id))
        self.assertEqual(response.data, b'{}\n')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('{}/states/{}'.format(self.prefix, s_id))
        self.assertEqual(response.status_code, 404)

    def test_delete_one_404(self):
        """Test state DELETE route with 404"""
        response = self.client.delete(
            '{}/states/invalid_id'.format(self.prefix)
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"error": "Not found"})


if __name__ == '__main__':
    unittest.main()
