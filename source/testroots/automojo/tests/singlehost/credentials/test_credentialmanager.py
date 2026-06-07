"""
    Testbase tests for :class:`CredentialManager`.

    Verifies multi-category credential loading behaviour, ensuring that a
    credential declaring multiple categories (including ``ssh``) is
    instantiated as a :class:`BasicCredential` and that unsupported
    key-specific fields are ignored.
"""

from automojo.credentials.credentialmanager import CredentialManager
from automojo.credentials.basiccredential import BasicCredential
from automojo.credentials.sshcredential import SshCredential


def _setup_credential_manager() -> CredentialManager:
    """
        Replicates the original ``setUp`` by creating a fresh
        :class:`CredentialManager` instance for use by a single test.

        :returns: A newly constructed :class:`CredentialManager`.
    """
    cm = CredentialManager()
    return cm


def test_multi_category_is_basic_credential() -> None:
    """
        Verifies that a multi-category credential (including ssh) is instantiated as a
        :class:`BasicCredential` and ignores unsupported key-specific fields.
    """
    cm = _setup_credential_manager()

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
    cm.load_credentials(creds)

    # Verify the credential object
    cred = cm.lookup_credential("test-multi")
    assert isinstance(cred, BasicCredential)
    assert not isinstance(cred, SshCredential)

    # Verify it has correct attributes
    assert cred.username == "user"
    assert cred.password == "password"
    assert cred.categories == ["ssh", "basic"]

    # Verify it does NOT have keyfile attribute (BasicCredential doesn't have it)
    assert not hasattr(cred, "keyfile")

    return
