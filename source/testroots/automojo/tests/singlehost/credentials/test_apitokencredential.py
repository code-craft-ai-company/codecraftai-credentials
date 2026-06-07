"""
    Tests for :class:`automojo.credentials.apitokencredential.ApiTokenCredential`.

    Converted from the original ``unittest.TestCase`` based module to the
    testbase module-level test-function format. Each test exercises construction
    validation, accessor behaviour, ``as_dict`` serialization, and the static
    ``validate`` helper of the API token credential type.
"""

from automojo.credentials.apitokencredential import ApiTokenCredential
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "jira-token"
CATEGORIES = ["api-token"]
TOKEN = "ABCD1234"


def test_init_with_invalid_category_raises() -> None:
    """
        Verifies invalid categories raise :class:`ConfigurationError`.
    """
    raised = False
    try:
        ApiTokenCredential(identifier=IDENTIFIER, categories=["basic"], token=TOKEN)
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_init_with_empty_token_raises() -> None:
    """
        Ensures an empty token value is rejected.
    """
    raised = False
    try:
        ApiTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token="")
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_init_with_none_token_raises() -> None:
    """
        Ensures ``None`` tokens are rejected.
    """
    raised = False
    try:
        ApiTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=None)
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_default_role_is_priv() -> None:
    """
        Confirms the default role is ``priv``.
    """
    cred = ApiTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
    assert cred.role == "priv"
    return


def test_token_property_returns_value() -> None:
    """
        Ensures the token accessor returns the configured value.
    """
    cred = ApiTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
    assert cred.token == TOKEN
    return


def test_as_dict_contains_fields() -> None:
    """
        Ensures ``as_dict`` contains the expected fields.
    """
    cred = ApiTokenCredential(identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN)
    expected = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "role": "priv",
        "token": TOKEN,
    }
    assert cred.as_dict() == expected
    return


def test_validate_missing_token_reports_error() -> None:
    """
        Checks validation catches a missing token entry.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = ApiTokenCredential.validate(cred_info)
    assert any("missing 'token'" in err for err in errors)
    assert warnings == []
    return


def test_validate_ok_does_not_raise() -> None:
    """
        Ensures a complete credential validates successfully.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "token": TOKEN}
    errors, warnings = ApiTokenCredential.validate(cred_info)
    assert errors == []
    assert warnings == []
    return
