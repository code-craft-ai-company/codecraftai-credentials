import unittest

from automojo.errors.exceptions import ConfigurationError
from automojo.credentials.basiccredential import BasicCredential


class TestBasicCredential(unittest.TestCase):

    def setUp(self):
        self.identifier = "basic-login"
        self.categories = ["basic"]
        self.username = "ubuntu"
        self.password = "secret"
        return

    def test_init_with_invalid_category_raises(self):
        with self.assertRaises(ConfigurationError):
            BasicCredential(identifier=self.identifier, categories=["ssh"], username=self.username, password=self.password)

    def test_init_with_empty_password_raises(self):
        with self.assertRaises(ConfigurationError):
            BasicCredential(identifier=self.identifier, categories=self.categories, username=self.username, password="")

    def test_init_with_none_password_raises(self):
        with self.assertRaises(ConfigurationError):
            BasicCredential(identifier=self.identifier, categories=self.categories, username=self.username, password=None)

    def test_username_property_returns_value(self):
        cred = BasicCredential(identifier=self.identifier, categories=self.categories, username=self.username, password=self.password)
        self.assertEqual(cred.username, self.username)

    def test_as_dict_contains_fields(self):
        cred = BasicCredential(identifier=self.identifier, categories=self.categories, username=self.username, password=self.password)
        expected = {
            "identifier": self.identifier,
            "categories": self.categories,
            "role": "priv",
            "username": self.username,
            "password": self.password,
        }
        self.assertEqual(cred.as_dict(), expected)

    def test_validate_missing_username_reports_error(self):
        cred_info = {
            "identifier": self.identifier,
            "categories": self.categories,
            "password": self.password,
        }
        errors, warnings = BasicCredential.validate(cred_info)
        self.assertIn("missing 'username' in basic credential.", errors)
        self.assertEqual(len(warnings), 0)

    def test_validate_ok_does_not_raise(self):
        cred_info = {
            "identifier": self.identifier,
            "categories": self.categories,
            "username": self.username,
            "password": self.password,
        }
        errors, warnings = BasicCredential.validate(cred_info)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)


if __name__ == "__main__":
    unittest.main()
