"""
    Testbase tests for :class:`SshCredential`.

    Converted from the legacy ``unittest`` module
    ``automojo_tests.credentials.test_sshcredential`` during the Phase 7
    unittest->testbase shift. Each former ``TestCase`` method is preserved
    one-to-one as a module-level ``test_*`` function with identical logic and
    assertions.
"""

from automojo.credentials.sshcredential import SshCredential
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "test-ssh"
CATEGORIES = ["ssh"]
USERNAME = "ubuntu"
PASSWORD = "secret"


def test_init_without_password_and_no_key_or_agent_raises() -> None:
    """
        Verifies a password-less credential without a key or agent triggers :class:`ConfigurationError`.
    """
    raised = False
    try:
        SshCredential(identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME)
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_init_with_password_and_both_keyfile_keyraw_raises() -> None:
    """
        Ensures providing both ``keyfile`` and ``keyraw`` raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        SshCredential(
            identifier=IDENTIFIER,
            categories=CATEGORIES,
            username=USERNAME,
            password=PASSWORD,
            keyfile="/some/path",
            keyraw="keydata",
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_init_without_password_and_allow_agent_ok() -> None:
    """
        Confirms allowing the agent permits password-less credentials.
    """
    cred = SshCredential(
        identifier=IDENTIFIER,
        categories=CATEGORIES,
        username=USERNAME,
        allow_agent=True,
    )
    assert cred.username == USERNAME
    return
