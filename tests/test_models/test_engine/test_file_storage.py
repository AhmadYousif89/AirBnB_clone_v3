#!/usr/bin/python3
"""Unittest for FileStorage class"""
import json
import pep8
import inspect
import unittest
from models import storage, storage_type
from models.engine import file_storage
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.user import User

FileStorage = file_storage.FileStorage
classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_models/test_engine/test_file_storage.py']
        )
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(
            file_storage.__doc__, None, "file_storage.py needs a docstring"
        )
        self.assertTrue(
            len(file_storage.__doc__) >= 1, "file_storage.py needs a docstring"
        )

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(
            FileStorage.__doc__, None, "FileStorage class needs a docstring"
        )
        self.assertTrue(
            len(FileStorage.__doc__) >= 1 if FileStorage.__doc__ else False,
            "FileStorage class needs a docs",
        )

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(
                func[1].__doc__,
                None,
                "{} method needs a docstring".format(func[0]),
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1 if func[1].__doc__ else False,
                "{} method needs a docstring".format(func[0]),
            )


@unittest.skipIf(storage_type == 'db', "Skip for testing db storage")
class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)  # type: ignore

    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects  # type: ignore
        FileStorage._FileStorage__objects = {}  # type: ignore
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                objs = storage._FileStorage__objects  # type: ignore
                self.assertEqual(test_dict, objs)
        FileStorage._FileStorage__objects = save  # type: ignore

    def test_save(self):
        """Test that save properly saves objects to hbnb.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects  # type: ignore
        FileStorage._FileStorage__objects = new_dict  # type: ignore
        storage.save()
        FileStorage._FileStorage__objects = save  # type: ignore
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("hbnb.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    def test_get(self):
        """Test retrieving an existing object"""
        obj = BaseModel()
        obj.save()
        retrieved_obj = storage.get(BaseModel, obj.id)
        self.assertEqual(retrieved_obj, obj)

    def test_get_nonexistent_object(self):
        """Test retrieving a nonexistent object"""
        retrieved_obj = storage.get(BaseModel, "nonexistent_id")
        self.assertIsNone(retrieved_obj)

    def test_get_with_different_class(self):
        """Test retrieving an object with a different class"""
        obj = BaseModel()
        obj.save()
        retrieved_obj = storage.get(User, obj.id)
        self.assertIsNone(retrieved_obj)

    def test_get_with_invalid_id(self):
        """Test retrieving an object with an invalid id"""
        obj = BaseModel()
        obj.save()
        retrieved_obj = storage.get(BaseModel, 123)
        self.assertIsNone(retrieved_obj)

    def test_get_with_invalid_class(self):
        """Test retrieving an object with an invalid class"""
        obj = BaseModel()
        obj.save()
        retrieved_obj = storage.get(object, obj.id)
        self.assertIsNone(retrieved_obj)

    def test_count(self):
        """Test counting the number of objects in the database"""
        obj = BaseModel()
        user = User(email='', password='')
        obj.save()
        user.save()
        self.assertEqual(storage.count(), len(storage.all()))

    def test_count2(self):
        """Test the count method"""
        initial_count = storage.count()
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()
        new_count = storage.count()
        self.assertEqual(new_count, initial_count + 1)
        state_count = storage.count(State)
        self.assertGreaterEqual(state_count, 1)

    def test_count_with_class(self):
        """Test counting the number of objects of a specific class"""
        obj = BaseModel()
        obj.save()
        self.assertEqual(storage.count(BaseModel), len(storage.all(BaseModel)))

    def test_count_with_invalid_class(self):
        """Test counting the number of objects with an invalid class"""
        obj = BaseModel()
        obj.save()
        self.assertEqual(storage.count(object), 0)
