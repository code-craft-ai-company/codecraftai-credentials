import os
import tempfile

import automojo.testbase as testbase

from automojo.errors.exceptions import ConfigurationError
from automojo.credentials.githubappcredential import GithubAppCredential

IDENTIFIER = "gh-app"
CATEGORIES = ["github-app"]
KEY = "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqh...\n-----END PRIVATE KEY-----\n"


def test_init_with_invalid_category_raises():
    try:
        GithubAppCredential(identifier=IDENTIFIER, categories=["basic"], keys=[KEY])
    except ConfigurationError:
        return
    raise AssertionError("ConfigurationError was not raised")


def test_init_with_no_key_material_raises():
    try:
        GithubAppCredential(identifier=IDENTIFIER, categories=CATEGORIES)
    except ConfigurationError:
        return
    raise AssertionError("ConfigurationError was not raised")


def test_init_with_keyfiles_loads_keys():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as kf:
        kf.write(KEY)
        kf.flush()
        kfpath = kf.name
    try:
        cred = GithubAppCredential(identifier=IDENTIFIER, categories=CATEGORIES, keyfiles=[kfpath])
        testbase.assert_equal(len(cred.keys) == 1 and cred.keys[0] == KEY, True)
    finally:
        os.unlink(kfpath)
    return


def test_default_role_is_priv():
    cred = GithubAppCredential(identifier=IDENTIFIER, categories=CATEGORIES, keys=[KEY])
    testbase.assert_equal(cred.role, "priv")
    return


def test_as_dict_contains_fields():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as kf:
        kf.write(KEY)
        kf.flush()
        kfpath = kf.name
    try:
        cred = GithubAppCredential(identifier=IDENTIFIER, categories=CATEGORIES, keyfiles=[kfpath], keypasswd=["pw"])
        expected = {
            "identifier": IDENTIFIER,
            "categories": CATEGORIES,
            "role": "priv",
            "keyfiles": [kfpath],
            "keys": [KEY],
            "keypasswd": ["pw"],
        }
        testbase.assert_equal(cred.as_dict(), expected)
    finally:
        os.unlink(kfpath)
    return


def test_validate_missing_keys_reports_error():
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = GithubAppCredential.validate(cred_info)
    testbase.assert_equal("either 'keyfiles' or 'keys' must be provided in github-app credential." in errors, True)
    testbase.assert_equal(len(warnings), 0)
    return


def test_validate_missing_keyfile_reports_error():
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "keyfiles": ["/nope.pem"]}
    errors, warnings = GithubAppCredential.validate(cred_info)
    testbase.assert_equal("specified keyfile" in errors[0], True)
    testbase.assert_equal(len(warnings), 0)
    return


if __name__ == "__main__":
    from automojo.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
