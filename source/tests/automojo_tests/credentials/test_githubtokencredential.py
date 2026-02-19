import unittest

from automojo.credentials.githubtokencredential import GithubTokenCredential
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "gh-token"
CATEGORIES = ["github-token"]
TOKEN = "ghp_ABCD1234"


class TestGithubTokenCredential(unittest.TestCase):

    def test_init_with_invalid_category_raises(self):
        """
            Verifies invalid categories raise :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            GithubTokenCredential(identifier=IDENTIFIER, categories=["basic"], token=TOKEN)

    def test_init_with_empty_token_raises(self):
        """
            Ensures empty tokens are rejected.
        """
        with self.assertRaises(ConfigurationError):
            GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token="")

    def test_default_role_is_priv(self):
        """
            Confirms the default role is ``priv``.
        """
        cred = GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
        self.assertEqual(cred.role, "priv")

    def test_default_username_is_git(self):
        """
            Ensures the default username is ``git``.
        """
        cred = GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
        self.assertEqual(cred.username, "git")

    def test_token_property_returns_value(self):
        """
            Ensures the token accessor returns the configured value.
        """
        cred = GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
        self.assertEqual(cred.token, TOKEN)

    def test_username_property_returns_value(self):
        """
            Ensures the username accessor returns overrides when provided.
        """
        cred = GithubTokenCredential(
            identifier=IDENTIFIER,
            categories=CATEGORIES,
            token=TOKEN,
            username="octocat",
        )
        self.assertEqual(cred.username, "octocat")

    def test_as_dict_contains_fields(self):
        """
            Ensures ``as_dict`` includes the credential payload.
        """
        cred = GithubTokenCredential(
            identifier=IDENTIFIER,
            categories=CATEGORIES,
            token=TOKEN,
            username="octocat",
        )
        expected = {
            "identifier": IDENTIFIER,
            "categories": CATEGORIES,
            "role": "priv",
            "token": TOKEN,
            "username": "octocat",
        }
        self.assertEqual(cred.as_dict(), expected)

    def test_validate_missing_token_reports_error(self):
        """
            Ensures validation enforces token presence.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = GithubTokenCredential.validate(cred_info)
        self.assertTrue(any("missing 'token'" in err for err in errors))
        self.assertEqual(warnings, [])

    def test_validate_ok_does_not_raise(self):
        """
            Ensures a valid credential validates successfully.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "token": TOKEN}
        errors, warnings = GithubTokenCredential.validate(cred_info)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
