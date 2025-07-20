import automojo.testbase as testbase

from automojo.errors.exceptions import ConfigurationError
from automojo.credentials.wifichoicecredential import WifiChoiceCredential

IDENTIFIER = "my-wifi-networks"
CATEGORIES = ["wifi-choice"]
NETWORKS = [
    {"ssid": "AP1", "password": "pwd1"},
    {"ssid": "AP2", "password": "pwd2"},
]


def test_init_with_invalid_category_raises():
    try:
        WifiChoiceCredential(identifier=IDENTIFIER, categories=["basic"], networks=NETWORKS)
    except ConfigurationError:
        return
    raise AssertionError("ConfigurationError was not raised")


def test_init_with_empty_networks_raises():
    try:
        WifiChoiceCredential(identifier=IDENTIFIER, categories=CATEGORIES, networks=[])
    except ConfigurationError:
        return
    raise AssertionError("ConfigurationError was not raised")


def test_default_role_is_priv():
    cred = WifiChoiceCredential(identifier=IDENTIFIER, categories=CATEGORIES, networks=NETWORKS)
    testbase.assert_equal(cred.role, "priv")
    return


def test_networks_property_returns_value():
    cred = WifiChoiceCredential(identifier=IDENTIFIER, categories=CATEGORIES, networks=NETWORKS)
    testbase.assert_equal(cred.networks, NETWORKS)
    return


def test_as_dict_contains_fields():
    cred = WifiChoiceCredential(identifier=IDENTIFIER, categories=CATEGORIES, networks=NETWORKS)
    expected = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "role": "priv",
        "networks": NETWORKS,
    }
    testbase.assert_equal(cred.as_dict(), expected)
    return


def test_validate_missing_networks_reports_error():
    cred_info = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
    }
    errors, warnings = WifiChoiceCredential.validate(cred_info)
    testbase.assert_equal("missing 'networks' field on wifi-choice credential." in errors, True)
    testbase.assert_equal(len(warnings), 0)
    return


def test_validate_empty_networks_raises():
    cred_info = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "networks": [],
    }
    errors, warnings = WifiChoiceCredential.validate(cred_info)
    testbase.assert_equal("empty 'networks' field on wifi-choice credential." in errors, True)
    testbase.assert_equal(len(warnings), 0)
    return


def test_validate_missing_network_fields_raises():
    cred_info = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "networks": [{}],
    }
    errors, warnings = WifiChoiceCredential.validate(cred_info)
    found_ssid = any("missing the 'ssid' field" in err for err in errors)
    found_pass = any("missing the 'password' field" in err for err in errors)
    testbase.assert_equal(found_ssid, True)
    testbase.assert_equal(found_pass, True)
    testbase.assert_equal(len(warnings), 0)
    return


def test_validate_ok_does_not_raise():
    cred_info = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "networks": NETWORKS,
    }
    errors, warnings = WifiChoiceCredential.validate(cred_info)
    testbase.assert_equal(len(errors), 0)
    testbase.assert_equal(len(warnings), 0)
    return


if __name__ == "__main__":
    from automojo.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
