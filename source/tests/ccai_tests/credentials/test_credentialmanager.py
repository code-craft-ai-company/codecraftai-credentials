import unittest

from ccai.credentials.credentialmanager import CredentialManager
from ccai.credentials.basiccredential import BasicCredential
from ccai.credentials.sshcredential import SshCredential


class TestCredentialManager(unittest.TestCase):

    def setUp(self):
        self.cm = CredentialManager()

    def test_multi_category_is_basic_credential(self):
        """
            Verifies that a multi-category credential (including ssh) is instantiated as a
            :class:`BasicCredential` and ignores unsupported key-specific fields.
        """
        creds = {
            "credentials": [
                {
                    "identifier": "test-multi",
                    "categories": ["ssh", "basic"],
                    "username": "user",
                    "password": "password",
                    "keyfile": "/non/existent/file"
                }
            ]
        }

        # This should NOT raise ConfigurationError.
        self.cm.load_credentials(creds)

        # Verify the credential object
        cred = self.cm.lookup_credential("test-multi")
        self.assertIsInstance(cred, BasicCredential)
        self.assertNotIsInstance(cred, SshCredential)

        # Verify it has correct attributes
        self.assertEqual(cred.username, "user")
        self.assertEqual(cred.password, "password")
        self.assertEqual(cred.categories, ["ssh", "basic"])

        # Verify it does NOT have keyfile attribute (BasicCredential doesn't have it)
        self.assertFalse(hasattr(cred, "keyfile"))
