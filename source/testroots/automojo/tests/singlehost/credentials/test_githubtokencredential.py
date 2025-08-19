import automojo.testbase as testbase

from automojo.errors.exceptions import ConfigurationError
from automojo.credentials.githubtokencredential import GithubTokenCredential


IDENTIFIER = "gh-token"
CATEGORIES = ["github-token"]
TOKEN = "ghp_ABCD1234"


def test_init_with_invalid_category_raises():
    try:
        GithubTokenCredential(identifier=IDENTIFIER, categories=["basic"], token=TOKEN)
    except ConfigurationError:
        return
    raise AssertionError("ConfigurationError was not raised")


def test_init_with_empty_token_raises():
    try:
        GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token="")
    except ConfigurationError:
        return
    raise AssertionError("ConfigurationError was not raised")


def test_default_role_is_priv():
    cred = GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
    testbase.assert_equal(cred.role, "priv")
    return


def test_default_username_is_git():
    cred = GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
    testbase.assert_equal(cred.username, "git")
    return


def test_token_property_returns_value():
    cred = GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
    testbase.assert_equal(cred.token, TOKEN)
    return


def test_username_property_returns_value():
    cred = GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN, username="octocat")
    testbase.assert_equal(cred.username, "octocat")
    return


def test_as_dict_contains_fields():
    cred = GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN, username="octocat")
    expected = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "role": "priv",
        "token": TOKEN,
        "username": "octocat",
    }
    testbase.assert_equal(cred.as_dict(), expected)
    return


def test_validate_missing_token_reports_error():
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = GithubTokenCredential.validate(cred_info)
    testbase.assert_equal("missing 'token' in github token credential." in errors, True)
    testbase.assert_equal(len(warnings), 0)
    return


def test_validate_ok_does_not_raise():
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "token": TOKEN}
    errors, warnings = GithubTokenCredential.validate(cred_info)
    testbase.assert_equal(len(errors), 0)
    testbase.assert_equal(len(warnings), 0)
    return


if __name__ == "__main__":
    from automojo.testbase.entrypoints import generic_test_entrypoint

    generic_test_entrypoint()

