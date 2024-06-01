#!/usr/bin/python3
"""Unittest for DBStorage class"""
import pep8
import inspect
import unittest
from models import storage, storage_type
from models.engine import db_storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

DBStorage = db_storage.DBStorage
classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_models/test_engine/test_db_storage.py']
        )
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(
            db_storage.__doc__, None, "db_storage.py needs a docstring"
        )
        self.assertTrue(
            len(db_storage.__doc__) >= 1, "db_storage.py needs a docstring"
        )

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(
            DBStorage.__doc__, None, "DBStorage class needs a docstring"
        )
        self.assertTrue(
            len(DBStorage.__doc__) >= 1 if DBStorage.__doc__ else False,
            "DBStorage class needs a docstring",
        )

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(
                func[1].__doc__,
                None,
                "{} method needs a docstring".format(func[0]),
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1 if func[1].__doc__ else False,
                "{} method needs a docstring".format(func[0]),
            )


@unittest.skipIf(storage_type != 'db', "Skip for testing file storage")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        initial_count = len(storage.all())
        state = State(name='California')
        storage.new(state)
        storage.save()
        self.assertEqual(len(storage.all()), initial_count + 1)

    def test_save(self):
        """Test that save properly saves objects to DB"""
        init_count = len(storage.all(State))
        state = State(name='California')
        state.save()
        key = state.__class__.__name__ + '.' + state.id
        self.assertIn(key, storage.all(State))
        self.assertEqual(len(storage.all(State)), init_count + 1)

    def test_get(self):
        """Test retrieving an existing object from the database"""
        user = User(email='test@123.com', password='pswrd')
        storage.new(user)
        storage.save()
        retrieved_user = storage.get(User, user.id)
        self.assertEqual(retrieved_user, user)

    def test_get_with_invalid_id(self):
        """Test retrieving an object with an invalid id"""
        user = User(email='test@123', password='pswrd')
        storage.new(user)
        obj_id = 123
        retrieved_user = storage.get(User, obj_id)
        self.assertIsNone(retrieved_user)

    def test_get_nonexistent_obj(self):
        """Test retrieving a nonexistent object from the database"""
        obj_id = 'nonexistent_id'
        retrieved_user = storage.get(User, obj_id)
        self.assertIsNone(retrieved_user)

    def test_count(self):
        """Test the count method"""
        initial_count = storage.count()
        user = User(email="Cairoxx", password="1234")
        storage.new(user)
        storage.save()
        new_count = storage.count()
        self.assertEqual(new_count, initial_count + 1)
        user_count = storage.count(User)
        self.assertGreaterEqual(user_count, 1)

    def test_count2(self):
        """Test counting the number of objects in the database"""
        count = storage.count()
        count_all = len(storage.all().keys())
        self.assertEqual(count, count_all)

    def test_count_with_class(self):
        """Test counting the number of objects of a specific class"""
        state = State(name='California')
        storage.new(state)
        storage.save()
        self.assertEqual(storage.count(State), len(storage.all(State)))
