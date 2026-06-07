"""
    Tests for :class:`automojo.credentials.githubtokencredential.GithubTokenCredential`.

    Converted from the original ``unittest.TestCase`` based module to the
    testbase module-level test-function format. Each test exercises construction
    validation, accessor behaviour, ``as_dict`` serialization, and the static
    ``validate`` helper of the GitHub token credential type.
"""

from automojo.credentials.githubtokencredential import GithubTokenCredential
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "gh-token"
CATEGORIES = ["github-token"]
TOKEN = "ghp_ABCD1234"


def test_init_with_invalid_category_raises() -> None:
    """
        Verifies invalid categories raise :class:`ConfigurationError`.
    """
    raised = False
    try:
        GithubTokenCredential(identifier=IDENTIFIER, categories=["basic"], token=TOKEN)
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_init_with_empty_token_raises() -> None:
    """
        Ensures empty tokens are rejected.
    """
    raised = False
    try:
        GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token="")
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_default_role_is_priv() -> None:
    """
        Confirms the default role is ``priv``.
    """
    cred = GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
    assert cred.role == "priv"
    return


def test_default_username_is_git() -> None:
    """
        Ensures the default username is ``git``.
    """
    cred = GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
    assert cred.username == "git"
    return


def test_token_property_returns_value() -> None:
    """
        Ensures the token accessor returns the configured value.
    """
    cred = GithubTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
    assert cred.token == TOKEN
    return


def test_username_property_returns_value() -> None:
    """
        Ensures the username accessor returns overrides when provided.
    """
    cred = GithubTokenCredential(
        identifier=IDENTIFIER,
        categories=CATEGORIES,
        token=TOKEN,
        username="octocat",
    )
    assert cred.username == "octocat"
    return


def test_as_dict_contains_fields() -> None:
    """
        Ensures ``as_dict`` includes the credential payload.
    """
    cred = GithubTokenCredential(
        identifier=IDENTIFIER,
        categories=CATEGORIES,
        token=TOKEN,
        username="octocat",
    )
    expected = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "role": "priv",
        "token": TOKEN,
        "username": "octocat",
    }
    assert cred.as_dict() == expected
    return


def test_validate_missing_token_reports_error() -> None:
    """
        Ensures validation enforces token presence.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = GithubTokenCredential.validate(cred_info)
    assert any("missing 'token'" in err for err in errors)
    assert warnings == []
    return


def test_validate_ok_does_not_raise() -> None:
    """
        Ensures a valid credential validates successfully.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "token": TOKEN}
    errors, warnings = GithubTokenCredential.validate(cred_info)
    assert errors == []
    assert warnings == []
    return
