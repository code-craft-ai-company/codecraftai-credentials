import unittest

from ccai.credentials.apitokencredential import ApiTokenCredential
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "jira-token"
CATEGORIES = ["api-token"]
TOKEN = "ABCD1234"


class TestApiTokenCredential(unittest.TestCase):

    def test_init_with_invalid_category_raises(self):
        """
            Verifies invalid categories raise :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            ApiTokenCredential(identifier=IDENTIFIER, categories=["basic"], token=TOKEN)

    def test_init_with_empty_token_raises(self):
        """
            Ensures an empty token value is rejected.
        """
        with self.assertRaises(ConfigurationError):
            ApiTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token="")

    def test_init_with_none_token_raises(self):
        """
            Ensures ``None`` tokens are rejected.
        """
        with self.assertRaises(ConfigurationError):
            ApiTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=None)

    def test_default_role_is_priv(self):
        """
            Confirms the default role is ``priv``.
        """
        cred = ApiTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
        self.assertEqual(cred.role, "priv")

    def test_token_property_returns_value(self):
        """
            Ensures the token accessor returns the configured value.
        """
        cred = ApiTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
        self.assertEqual(cred.token, TOKEN)

    def test_as_dict_contains_fields(self):
        """
            Ensures ``as_dict`` contains the expected fields.
        """
        cred = ApiTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
        expected = {
            "identifier": IDENTIFIER,
            "categories": CATEGORIES,
            "role": "priv",
            "token": TOKEN,
        }
        self.assertEqual(cred.as_dict(), expected)

    def test_validate_missing_token_reports_error(self):
        """
            Checks validation catches a missing token entry.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = ApiTokenCredential.validate(cred_info)
        self.assertTrue(any("missing 'token'" in err for err in errors))
        self.assertEqual(warnings, [])

    def test_validate_ok_does_not_raise(self):
        """
            Ensures a complete credential validates successfully.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "token": TOKEN}
        errors, warnings = ApiTokenCredential.validate(cred_info)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
