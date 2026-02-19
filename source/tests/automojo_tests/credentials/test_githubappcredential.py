import os
import tempfile
import unittest

from automojo.credentials.githubappcredential import GithubAppCredential
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "gh-app"
CATEGORIES = ["github-app"]
KEY = "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqh...\n-----END PRIVATE KEY-----\n"


class TestGithubAppCredential(unittest.TestCase):

    def _create_temp_keyfile(self) -> str:
        """
            Writes a temporary keyfile and registers cleanup.
        """
        handle = tempfile.NamedTemporaryFile(mode="w", delete=False)
        handle.write(KEY)
        handle.flush()
        handle.close()
        self.addCleanup(lambda: os.path.exists(handle.name) and os.unlink(handle.name))
        return handle.name

    def test_init_with_invalid_category_raises(self):
        """
            Ensures invalid categories raise :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            GithubAppCredential(identifier=IDENTIFIER, categories=["basic"], keys=[KEY])

    def test_init_with_no_key_material_raises(self):
        """
            Ensures lack of keys or keyfiles raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            GithubAppCredential(identifier=IDENTIFIER, categories=CATEGORIES)

    def test_init_with_keyfiles_loads_keys(self):
        """
            Verifies providing keyfiles loads the key contents.
        """
        keyfile = self._create_temp_keyfile()
        cred = GithubAppCredential(identifier=IDENTIFIER, categories=CATEGORIES, keyfiles=[keyfile])
        self.assertEqual(cred.keys, [KEY])

    def test_default_role_is_priv(self):
        """
            Confirms the default role is ``priv``.
        """
        cred = GithubAppCredential(identifier=IDENTIFIER, categories=CATEGORIES, keys=[KEY])
        self.assertEqual(cred.role, "priv")

    def test_as_dict_contains_fields(self):
        """
            Ensures ``as_dict`` includes keyfiles, explicit keys, and passwords.
        """
        keyfile = self._create_temp_keyfile()
        cred = GithubAppCredential(
            identifier=IDENTIFIER,
            categories=CATEGORIES,
            keyfiles=[keyfile],
            keypasswd=["pw"],
        )
        expected = {
            "identifier": IDENTIFIER,
            "categories": CATEGORIES,
            "role": "priv",
            "keyfiles": [keyfile],
            "keys": [],
            "keypasswd": ["pw"],
        }
        self.assertEqual(cred.as_dict(), expected)

    def test_validate_missing_keys_reports_error(self):
        """
            Ensures validation enforces keyfiles or keys presence.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = GithubAppCredential.validate(cred_info)
        self.assertIn("either 'keyfiles' or 'keys' must be provided in github-app credential.", errors)
        self.assertEqual(warnings, [])

    def test_validate_missing_keyfile_reports_error(self):
        """
            Ensures validation reports missing keyfiles.
        """
        cred_info = {
            "identifier": IDENTIFIER,
            "categories": CATEGORIES,
            "keyfiles": ["/nope.pem"],
        }
        errors, warnings = GithubAppCredential.validate(cred_info)
        self.assertTrue(any("specified keyfile" in err for err in errors))
        self.assertEqual(warnings, [])
