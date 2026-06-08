"""
    Testbase module verifying the behaviour of :class:`GithubAppCredential`.

    Covers construction validation, default role assignment, dictionary
    serialization, and the static ``validate`` routine.
"""

import os
import tempfile

from ccai.credentials.githubappcredential import GithubAppCredential
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "gh-app"
CATEGORIES = ["github-app"]
KEY = "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqh...\n-----END PRIVATE KEY-----\n"


def _create_temp_keyfile() -> str:
    """
        Writes a temporary keyfile and returns its path.

        :returns: The filesystem path to the temporary keyfile.
    """
    handle = tempfile.NamedTemporaryFile(mode="w", delete=False)
    handle.write(KEY)
    handle.flush()
    handle.close()
    rtnval = handle.name
    return rtnval


def test_init_with_invalid_category_raises() -> None:
    """
        Ensures invalid categories raise :class:`ConfigurationError`.
    """
    raised = False
    try:
        GithubAppCredential(identifier=IDENTIFIER, categories=["basic"], keys=[KEY])
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_init_with_no_key_material_raises() -> None:
    """
        Ensures lack of keys or keyfiles raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        GithubAppCredential(identifier=IDENTIFIER, categories=CATEGORIES)
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_init_with_keyfiles_loads_keys() -> None:
    """
        Verifies providing keyfiles loads the key contents.
    """
    keyfile = _create_temp_keyfile()
    try:
        cred = GithubAppCredential(identifier=IDENTIFIER, categories=CATEGORIES, keyfiles=[keyfile])
        assert cred.keys == [KEY]
    finally:
        if os.path.exists(keyfile):
            os.unlink(keyfile)

    return


def test_default_role_is_priv() -> None:
    """
        Confirms the default role is ``priv``.
    """
    cred = GithubAppCredential(identifier=IDENTIFIER, categories=CATEGORIES, keys=[KEY])
    assert cred.role == "priv"
    return


def test_as_dict_contains_fields() -> None:
    """
        Ensures ``as_dict`` includes keyfiles, explicit keys, and passwords.
    """
    keyfile = _create_temp_keyfile()
    try:
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
        assert cred.as_dict() == expected
    finally:
        if os.path.exists(keyfile):
            os.unlink(keyfile)

    return


def test_validate_missing_keys_reports_error() -> None:
    """
        Ensures validation enforces keyfiles or keys presence.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = GithubAppCredential.validate(cred_info)
    assert "either 'keyfiles' or 'keys' must be provided in github-app credential." in errors
    assert warnings == []
    return


def test_validate_missing_keyfile_reports_error() -> None:
    """
        Ensures validation reports missing keyfiles.
    """
    cred_info = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "keyfiles": ["/nope.pem"],
    }
    errors, warnings = GithubAppCredential.validate(cred_info)
    assert any("specified keyfile" in err for err in errors)
    assert warnings == []
    return
