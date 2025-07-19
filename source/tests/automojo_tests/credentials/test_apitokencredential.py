import unittest

from automojo.errors.exceptions import ConfigurationError
from automojo.credentials.apitokencredential import ApiTokenCredential

class TestApiTokenCredential(unittest.TestCase):

    def setUp(self):
        self.identifier = "jira-token"
        self.categories = ["api-token"]
        self.token = "ABCD1234"
        return

    def test_init_with_invalid_category_raises(self):
        with self.assertRaises(ConfigurationError):
            ApiTokenCredential(identifier=self.identifier, categories=["basic"], token=self.token)

    def test_init_with_empty_token_raises(self):
        with self.assertRaises(ConfigurationError):
            ApiTokenCredential(identifier=self.identifier, categories=self.categories, token="")

    def test_init_with_none_token_raises(self):
        with self.assertRaises(ConfigurationError):
            ApiTokenCredential(identifier=self.identifier, categories=self.categories, token=None)

    def test_default_role_is_priv(self):
        cred = ApiTokenCredential(identifier=self.identifier, categories=self.categories, token=self.token)
        self.assertEqual(cred.role, "priv")

    def test_token_property_returns_value(self):
        cred = ApiTokenCredential(identifier=self.identifier, categories=self.categories, token=self.token)
        self.assertEqual(cred.token, self.token)

    def test_as_dict_contains_fields(self):
        cred = ApiTokenCredential(identifier=self.identifier, categories=self.categories, token=self.token)
        expected = {
            "identifier": self.identifier,
            "categories": self.categories,
            "role": "priv",
            "token": self.token,
        }
        self.assertEqual(cred.as_dict(), expected)

    def test_validate_missing_token_raises(self):
        cred_info = {"identifier": self.identifier, "categories": self.categories}
        with self.assertRaises(ConfigurationError) as cm:
            ApiTokenCredential.validate(cred_info)
        msg = str(cm.exception)
        self.assertIn("missing 'token' in api token credential", msg)
        self.assertIn(self.identifier, msg)

    def test_validate_ok_does_not_raise(self):
        cred_info = {
            "identifier": self.identifier,
            "categories": self.categories,
            "token": self.token,
        }
        try:
            ApiTokenCredential.validate(cred_info)
        except ConfigurationError as exc:
            self.fail(f"validate raised unexpectedly: {exc}")


if __name__ == "__main__":
    unittest.main()
