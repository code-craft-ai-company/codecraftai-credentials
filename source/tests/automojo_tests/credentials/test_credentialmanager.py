
import unittest
from unittest.mock import MagicMock
import sys
import os

# Add source/packages to python path
sys.path.append(os.path.abspath("source/packages"))

# Mock dependencies if they are missing
if "automojo.errors.exceptions" not in sys.modules:
    errors_mock = MagicMock()
    class ConfigurationError(Exception):
        pass
    errors_mock.ConfigurationError = ConfigurationError
    sys.modules["automojo.errors"] = MagicMock()
    sys.modules["automojo.errors.exceptions"] = errors_mock

from automojo.credentials.credentialmanager import CredentialManager
from automojo.credentials.basiccredential import BasicCredential
from automojo.credentials.sshcredential import SshCredential
from automojo.errors.exceptions import ConfigurationError

class TestCredentialManager(unittest.TestCase):

    def setUp(self):
        self.cm = CredentialManager()

    def test_multi_category_is_basic_credential(self):
        """
        Verify that a multi-category credential (including ssh) is instantiated as a BasicCredential.
        Extra fields like 'keyfile' should be ignored and not cause validation errors.
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

if __name__ == '__main__':
    unittest.main()
