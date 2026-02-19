import unittest

from automojo.credentials.basiccredential import BasicCredential
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "basic-login"
CATEGORIES = ["basic"]
USERNAME = "ubuntu"
PASSWORD = "secret"


class TestBasicCredential(unittest.TestCase):

    def test_init_with_invalid_category_raises(self):
        """
            Verifies invalid categories trigger a :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            BasicCredential(
                identifier=IDENTIFIER,
                categories=["ssh"],
                username=USERNAME,
                password=PASSWORD,
            )

    def test_init_with_empty_password_raises(self):
        """
            Verifies an empty password is rejected.
        """
        with self.assertRaises(ConfigurationError):
            BasicCredential(
                identifier=IDENTIFIER,
                categories=CATEGORIES,
                username=USERNAME,
                password="",
            )

    def test_init_with_none_password_raises(self):
        """
            Verifies a ``None`` password is rejected.
        """
        with self.assertRaises(ConfigurationError):
            BasicCredential(
                identifier=IDENTIFIER,
                categories=CATEGORIES,
                username=USERNAME,
                password=None,
            )

    def test_username_property_returns_value(self):
        """
            Ensures the username accessor returns the configured username.
        """
        cred = BasicCredential(
            identifier=IDENTIFIER,
            categories=CATEGORIES,
            username=USERNAME,
            password=PASSWORD,
        )
        self.assertEqual(cred.username, USERNAME)

    def test_as_dict_contains_fields(self):
        """
            Ensures ``as_dict`` includes all expected fields.
        """
        cred = BasicCredential(
            identifier=IDENTIFIER,
            categories=CATEGORIES,
            username=USERNAME,
            password=PASSWORD,
        )
        expected = {
            "identifier": IDENTIFIER,
            "categories": CATEGORIES,
            "role": "priv",
            "username": USERNAME,
            "password": PASSWORD,
        }
        self.assertEqual(cred.as_dict(), expected)

    def test_validate_missing_username_reports_error(self):
        """
            Validates username presence is enforced.
        """
        cred_info = {
            "identifier": IDENTIFIER,
            "categories": CATEGORIES,
            "password": PASSWORD,
        }
        errors, warnings = BasicCredential.validate(cred_info)
        self.assertTrue(any("missing 'username'" in err for err in errors))
        self.assertEqual(warnings, [])

    def test_validate_ok_does_not_raise(self):
        """
            Ensures a complete credential validates without issues.
        """
        cred_info = {
            "identifier": IDENTIFIER,
            "categories": CATEGORIES,
            "username": USERNAME,
            "password": PASSWORD,
        }
        errors, warnings = BasicCredential.validate(cred_info)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
