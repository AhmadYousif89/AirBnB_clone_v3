#!/usr/bin/python3
"""Test module for api.v1.app.py"""
import flask
import unittest
from api.v1.app import app


class AppTestCase(unittest.TestCase):
    """Test cases for the main app module"""

    def setUp(self):
        self.client = app.test_client()

    def test_app_init(self):
        """Test that the app is a Flask app"""
        self.assertIsInstance(self.client, flask.testing.FlaskClient)


if __name__ == '__main__':
    unittest.main()
