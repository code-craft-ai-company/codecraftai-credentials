import unittest

from automojo.credentials.sshcredential import SshCredential
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "test-ssh"
CATEGORIES = ["ssh"]
USERNAME = "ubuntu"
PASSWORD = "secret"


class TestSshCredential(unittest.TestCase):

    def test_init_without_password_and_no_key_or_agent_raises(self):
        """
            Verifies a password-less credential without a key or agent triggers :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            SshCredential(identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME)

    def test_init_with_password_and_both_keyfile_keyraw_raises(self):
        """
            Ensures providing both ``keyfile`` and ``keyraw`` raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            SshCredential(
                identifier=IDENTIFIER,
                categories=CATEGORIES,
                username=USERNAME,
                password=PASSWORD,
                keyfile="/some/path",
                keyraw="keydata",
            )

    def test_init_without_password_and_allow_agent_ok(self):
        """
            Confirms allowing the agent permits password-less credentials.
        """
        cred = SshCredential(
            identifier=IDENTIFIER,
            categories=CATEGORIES,
            username=USERNAME,
            allow_agent=True,
        )
        self.assertEqual(cred.username, USERNAME)
