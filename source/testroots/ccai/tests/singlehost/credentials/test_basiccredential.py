"""
    Testbase tests for :class:`BasicCredential`.

    Converted from the legacy ``unittest`` module
    ``ccai_tests.credentials.test_basiccredential`` during the Phase 7
    unittest->testbase shift. Each former ``TestCase`` method is preserved
    one-to-one as a module-level ``test_*`` function with identical logic and
    assertions.
"""

from ccai.credentials.basiccredential import BasicCredential
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "basic-login"
CATEGORIES = ["basic"]
USERNAME = "ubuntu"
PASSWORD = "secret"


def test_init_with_invalid_category_raises() -> None:
    """
        Verifies invalid categories trigger a :class:`ConfigurationError`.
    """
    raised = False
    try:
        BasicCredential(
            identifier=IDENTIFIER,
            categories=["ssh"],
            username=USERNAME,
            password=PASSWORD,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_init_with_empty_password_raises() -> None:
    """
        Verifies an empty password is rejected.
    """
    raised = False
    try:
        BasicCredential(
            identifier=IDENTIFIER,
            categories=CATEGORIES,
            username=USERNAME,
            password="",
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_init_with_none_password_raises() -> None:
    """
        Verifies a ``None`` password is rejected.
    """
    raised = False
    try:
        BasicCredential(
            identifier=IDENTIFIER,
            categories=CATEGORIES,
            username=USERNAME,
            password=None,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_username_property_returns_value() -> None:
    """
        Ensures the username accessor returns the configured username.
    """
    cred = BasicCredential(
        identifier=IDENTIFIER,
        categories=CATEGORIES,
        username=USERNAME,
        password=PASSWORD,
    )
    assert cred.username == USERNAME
    return


def test_as_dict_contains_fields() -> None:
    """
        Ensures ``as_dict`` includes all expected fields.
    """
    cred = BasicCredential(
        identifier=IDENTIFIER,
        categories=CATEGORIES,
        username=USERNAME,
        password=PASSWORD,
    )
    expected = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "role": "priv",
        "username": USERNAME,
        "password": PASSWORD,
    }
    assert cred.as_dict() == expected
    return


def test_validate_missing_username_reports_error() -> None:
    """
        Validates username presence is enforced.
    """
    cred_info = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "password": PASSWORD,
    }
    errors, warnings = BasicCredential.validate(cred_info)
    assert any("missing 'username'" in err for err in errors)
    assert warnings == []
    return


def test_validate_ok_does_not_raise() -> None:
    """
        Ensures a complete credential validates without issues.
    """
    cred_info = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "username": USERNAME,
        "password": PASSWORD,
    }
    errors, warnings = BasicCredential.validate(cred_info)
    assert errors == []
    assert warnings == []
    return
