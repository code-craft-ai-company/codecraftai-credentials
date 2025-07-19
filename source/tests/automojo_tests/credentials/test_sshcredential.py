import unittest

from automojo.errors.exceptions import ConfigurationError
from automojo.credentials.sshcredential import SshCredential


class TestSshCredential(unittest.TestCase):

    def setUp(self):
        self.identifier = "test-ssh"
        self.categories = ["ssh"]
        self.username = "ubuntu"
        self.password = "secret"
        return

    def test_init_without_password_and_no_key_or_agent_raises(self):
        with self.assertRaises(ConfigurationError):
            SshCredential(
                identifier=self.identifier,
                categories=self.categories,
                username=self.username
            )
        return

    def test_init_with_password_and_both_keyfile_keyraw_raises(self):
        with self.assertRaises(ConfigurationError):
            SshCredential(
                identifier=self.identifier,
                categories=self.categories,
                username=self.username,
                password=self.password,
                keyfile="/some/path",
                keyraw="keydata"
            )
        return

    def test_init_without_password_and_allow_agent_ok(self):
        cred = SshCredential(
            identifier=self.identifier,
            categories=self.categories,
            username=self.username,
            allow_agent=True
        )
        self.assertEqual(cred.username, self.username)
        return


if __name__ == "__main__":
    unittest.main()
