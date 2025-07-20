import automojo.testbase as testbase

from automojo.errors.exceptions import ConfigurationError
from automojo.credentials.basiccredential import BasicCredential

IDENTIFIER = "basic-login"
CATEGORIES = ["basic"]
USERNAME = "ubuntu"
PASSWORD = "secret"


def test_init_with_invalid_category_raises():
    try:
        BasicCredential(identifier=IDENTIFIER, categories=["ssh"], username=USERNAME, password=PASSWORD)
    except ConfigurationError:
        return
    raise AssertionError("ConfigurationError was not raised")


def test_init_with_empty_password_raises():
    try:
        BasicCredential(identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME, password="")
    except ConfigurationError:
        return
    raise AssertionError("ConfigurationError was not raised")


def test_init_with_none_password_raises():
    try:
        BasicCredential(identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME, password=None)
    except ConfigurationError:
        return
    raise AssertionError("ConfigurationError was not raised")


def test_username_property_returns_value():
    cred = BasicCredential(identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME, password=PASSWORD)
    testbase.assert_equal(cred.username, USERNAME)
    return


def test_as_dict_contains_fields():
    cred = BasicCredential(identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME, password=PASSWORD)
    expected = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "role": "priv",
        "username": USERNAME,
        "password": PASSWORD,
    }
    testbase.assert_equal(cred.as_dict(), expected)
    return


def test_validate_missing_username_reports_error():
    cred_info = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "password": PASSWORD,
    }
    errors, warnings = BasicCredential.validate(cred_info)
    testbase.assert_equal("missing 'username' in basic credential." in errors, True)
    testbase.assert_equal(len(warnings), 0)
    return


def test_validate_ok_does_not_raise():
    cred_info = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "username": USERNAME,
        "password": PASSWORD,
    }
    errors, warnings = BasicCredential.validate(cred_info)
    testbase.assert_equal(len(errors), 0)
    testbase.assert_equal(len(warnings), 0)
    return


if __name__ == "__main__":
    from automojo.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
