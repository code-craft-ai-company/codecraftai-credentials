import automojo.testbase as testbase

from automojo.errors.exceptions import ConfigurationError
from automojo.credentials.sshcredential import SshCredential

IDENTIFIER = "test-ssh"
CATEGORIES = ["ssh"]
USERNAME = "ubuntu"
PASSWORD = "secret"


def test_init_without_password_and_no_key_or_agent_raises():
    try:
        SshCredential(
            identifier=IDENTIFIER,
            categories=CATEGORIES,
            username=USERNAME,
        )
    except ConfigurationError:
        return
    raise AssertionError("ConfigurationError was not raised")


def test_init_with_password_and_both_keyfile_keyraw_raises():
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
        return
    raise AssertionError("ConfigurationError was not raised")


def test_init_without_password_and_allow_agent_ok():
    cred = SshCredential(
        identifier=IDENTIFIER,
        categories=CATEGORIES,
        username=USERNAME,
        allow_agent=True,
    )
    testbase.assert_equal(cred.username, USERNAME)
    return


if __name__ == "__main__":
    from automojo.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
