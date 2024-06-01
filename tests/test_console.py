#!/usr/bin/python3
"""Unittest for console.py"""
import os
import pep8
import hashlib
import console
import unittest
from io import StringIO
from unittest.mock import patch
from models import storage, storage_type
from console import HBNBCommand, error_messages


class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""

    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None, "console.py needs a docstring")
        self.assertTrue(
            len(console.__doc__) >= 1, "console.py needs a docstring"
        )

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(
            HBNBCommand.__doc__, None, "HBNBCommand class needs a docstring"
        )
        self.assertTrue(
            len(HBNBCommand.__doc__) >= 1 if HBNBCommand.__doc__ else False,
            "HBNBCommand class needs a docstring",
        )


class TestConsoleExitOp(unittest.TestCase):
    """Testing the exit methods of the console."""

    def test_quit(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "quit"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue()
        self.assertEqual(output, "")

    def test_EOF(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "EOF"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue()
        self.assertEqual(output, "\n")


class TestUser(unittest.TestCase):
    """Testing the User"""

    @classmethod
    def setUpClass(cls):
        from models.user import User

        cls.model = User
        cls.c_name = "User"

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("hbnb.json"):
            os.remove("hbnb.json")
        storage.close()

    @unittest.skipIf(storage_type == "db", "Skip for testing db storage")
    def test_create(self):
        """Test the create method using the <method> <class> formate."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "create {}".format(self.c_name)
            HBNBCommand().onecmd(cmd)
            obj_id = mock_stdout.getvalue().strip()
        self.assertIsInstance(obj_id, str)
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(obj_id, uuid_pattern)
        self.assertIn(
            "{}.{}".format(self.c_name, obj_id), storage.all().keys()
        )

    def test_create_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "create"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_c_name"]
        self.assertEqual(output, expected)

    def test_create_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "create base"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_create_with_params(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "create {} email=x@g.c password=123".format(self.c_name)
            HBNBCommand().onecmd(cmd)
            obj_id = mock_stdout.getvalue().strip()
        key = "{}.{}".format(self.c_name, obj_id)
        self.assertIn(key, storage.all().keys())

    def test_create_with_quote_in_param(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = 'create {} email="xx" password="123"'.format(self.c_name)
            HBNBCommand().onecmd(cmd)
            obj_id = mock_stdout.getvalue().strip()
        key = "{}.{}".format(self.c_name, obj_id)
        self.assertIn(key, storage.all().keys())
        obj = storage.all()[key]
        self.assertEqual(obj.__dict__["email"], "xx")
        self.assertIn("email", obj.__dict__.keys())
        self.assertIn("password", obj.__dict__.keys())
        hashed_pass = hashlib.md5("123".encode()).hexdigest()
        self.assertEqual(obj.__dict__["password"], hashed_pass)

    def test_create_params_with_underscore_value(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "create {} email=xx password=123 first_name=xx_cc"
            HBNBCommand().onecmd(cmd.format(self.c_name))
            obj_id = mock_stdout.getvalue().strip()
        key = "{}.{}".format(self.c_name, obj_id)
        self.assertIn(key, storage.all(self.model).keys())
        obj = storage.all(self.model)[key]
        self.assertEqual(obj.__dict__["first_name"], "xx cc")
        self.assertIn("first_name", obj.__dict__.keys())

    def test_show(self):
        obj = self.model(email='x@g.c', password='123')
        obj.save()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "show {} {}".format(self.c_name, obj.id)
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "show"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_c_name"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "show base"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "show {} 123".format(self.c_name)
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "update {} {} name 'xxx'".format(self.c_name, obj.id)
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "")
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()):
            cmd = "update {} {} age=20 name=xxx".format(self.c_name, obj.id)
            HBNBCommand().onecmd(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_dict(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            data = {"email": "x@g.c"}
            cmd = "update {} {} {}".format(self.c_name, obj.id, data)
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "")
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "x@g.c")

    def test_update_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "update"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_c_name"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "update base"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "update {}".format(self.c_name)
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "update {} 123 age 20".format(self.c_name)
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "update {} {} ".format(self.c_name, obj.id)
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "update {} {} name".format(self.c_name, obj.id)
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_value"]
        self.assertEqual(output, expected)

    def test_destroy(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()):
            cmd = "destroy {} {}".format(self.c_name, obj.id)
            HBNBCommand().onecmd(cmd)
        key = "{}.{}".format(self.c_name, obj.id)
        self.assertNotIn(key, storage.all().keys())

    def test_destroy_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "destroy"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_c_name"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "destroy base"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "destroy {}".format(self.c_name)
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "destroy {} 123".format(self.c_name)
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_do_all(self):
        obj = self.model(email="test@all.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "all"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        self.assertIn(obj.__str__(), output)

    def test_do_all_with_clsname(self):
        obj = self.model(email="est@all.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "all {}".format(self.c_name)
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        self.assertIn(obj.__str__(), output)

    def test_do_all_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "all base"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "count {}".format(self.c_name)
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue()
        count = 0
        for _ in storage.all(self.c_name).values():
            count += 1
        self.assertEqual(int(output), count)

    def test_count_with_all(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "count all"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue()
        count = 0
        for _ in storage.all().values():
            count += 1
        self.assertEqual(int(output), count)

    def test_count_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "count"
            HBNBCommand().onecmd(cmd)
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_c_name"]
        self.assertEqual(output, expected)


class TestUserDotNotation(unittest.TestCase):
    """Testing with the method.notation formate"""

    @classmethod
    def setUpClass(cls):
        from models.user import User

        cls.model = User
        cls.c_name = 'User'

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("hbnb.json"):
            os.remove("hbnb.json")
        storage.close()

    def test_invalid_method(self):
        """Test invalid method output message"""
        method_name = "invalid_method"
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "{}.{}()".format(self.c_name, method_name)
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd))
            output = mock_stdout.getvalue().strip()
        expected = '{}: {} **'.format(error_messages["no_method"], method_name)
        self.assertEqual(output, expected)

    @unittest.skipIf(storage_type == "db", "Skip for testing db storage")
    def test_create(self):
        """Test the create method using the <class>.<method>() formate."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "{}.create()".format(self.c_name)
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd))
            obj_id = mock_stdout.getvalue().strip()
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(obj_id, uuid_pattern)
        self.assertIn(
            "{}.{}".format(self.c_name, obj_id), storage.all().keys()
        )

    def test_create_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "base.create()"
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd))
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "{}.show({})"
            HBNBCommand().onecmd(
                HBNBCommand().precmd(cmd.format(self.c_name, obj.id))
            )
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "base.show()"
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd))
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "{}.show()".format(self.c_name)
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd))
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "{}.show(1)"
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd.format(self.c_name)))
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()):
            cmd = "{}.update({}, name xxx)"
            HBNBCommand().onecmd(
                HBNBCommand().precmd(cmd.format(self.c_name, obj.id))
            )
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()):
            cmd = "{}.update({}, age 20, name xxx)"
            HBNBCommand().onecmd(
                HBNBCommand().precmd(cmd.format(self.c_name, obj.id))
            )
        self.assertIn("age", obj.__dict__.keys())
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_dict(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()):
            data = {"email": "g@g.c"}
            cmd = "{}.update({}, {})"
            HBNBCommand().onecmd(
                HBNBCommand().precmd(cmd.format(self.c_name, obj.id, data))
            )
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "g@g.c")

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "user.update()"
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd))
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "{}.update()"
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd.format(self.c_name)))
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "{}.update(123, age 20)"
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd.format(self.c_name)))
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "{}.update({}, '')"
            HBNBCommand().onecmd(
                HBNBCommand().precmd(cmd.format(self.c_name, obj.id))
            )
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = self.model(email="x@x.com", password="123")
        obj.save()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "{}.update({}, age)"
            HBNBCommand().onecmd(
                HBNBCommand().precmd(cmd.format(self.c_name, obj.id))
            )
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_value"]
        self.assertEqual(output, expected)

    def do_all(self):

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "{}.count()".format(self.c_name)
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd))
            output = mock_stdout.getvalue()
        count = 0
        for _ in storage.all(self.c_name).values():
            count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = self.model(email="x@x.com", password="123")
        with patch('sys.stdout', new=StringIO()):
            cmd = "{}.destroy({})"
            HBNBCommand().onecmd(
                HBNBCommand().precmd(cmd.format(self.c_name, obj.id))
            )
        key = "{}.{}".format(self.c_name, obj.id)
        self.assertNotIn(key, storage.all().keys())

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "user.destroy()"
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd))
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "{}.destroy()"
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd.format(self.c_name)))
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            cmd = "{}.destroy(123)"
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd.format(self.c_name)))
            output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
