"""
    Tests for :class:`automojo.credentials.wifichoicecredential.WifiChoiceCredential`.

    Converted from the original ``unittest.TestCase`` based module to the
    testbase module-level test-function format. Each test exercises construction
    validation, the default role, the networks accessor, ``as_dict``
    serialization, and the static ``validate`` helper for the Wi-Fi choice
    credential type.
"""

from automojo.credentials.wifichoicecredential import WifiChoiceCredential
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "my-wifi-networks"
CATEGORIES = ["wifi-choice"]
NETWORKS = [
    {"ssid": "AP1", "password": "pwd1"},
    {"ssid": "AP2", "password": "pwd2"},
]


def test_init_with_invalid_category_raises() -> None:
    """
        Ensures invalid categories raise :class:`ConfigurationError`.
    """
    raised = False
    try:
        WifiChoiceCredential(identifier=IDENTIFIER, categories=["basic"], networks=NETWORKS)
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_init_with_empty_networks_raises() -> None:
    """
        Ensures an empty networks list raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        WifiChoiceCredential(identifier=IDENTIFIER, categories=CATEGORIES, networks=[])
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_default_role_is_priv() -> None:
    """
        Confirms the default role is ``priv``.
    """
    cred = WifiChoiceCredential(identifier=IDENTIFIER, categories=CATEGORIES, networks=NETWORKS)
    assert cred.role == "priv"
    return


def test_networks_property_returns_value() -> None:
    """
        Ensures the networks accessor returns the configured networks.
    """
    cred = WifiChoiceCredential(identifier=IDENTIFIER, categories=CATEGORIES, networks=NETWORKS)
    assert cred.networks == NETWORKS
    return


def test_as_dict_contains_fields() -> None:
    """
        Ensures ``as_dict`` includes the networks payload.
    """
    cred = WifiChoiceCredential(identifier=IDENTIFIER, categories=CATEGORIES, networks=NETWORKS)
    expected = {
        "identifier": IDENTIFIER,
        "categories": CATEGORIES,
        "role": "priv",
        "networks": NETWORKS,
    }
    assert cred.as_dict() == expected
    return


def test_validate_missing_networks_reports_error() -> None:
    """
        Ensures validation enforces the presence of network definitions.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = WifiChoiceCredential.validate(cred_info)
    assert any("missing 'networks'" in err for err in errors)
    assert warnings == []
    return


def test_validate_empty_networks_raises() -> None:
    """
        Ensures validation detects empty network lists.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "networks": []}
    errors, warnings = WifiChoiceCredential.validate(cred_info)
    assert any("empty 'networks'" in err for err in errors)
    assert warnings == []
    return


def test_validate_missing_network_fields_raises() -> None:
    """
        Ensures missing SSID and password entries are reported.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "networks": [{}]}
    errors, warnings = WifiChoiceCredential.validate(cred_info)
    assert any("missing the 'ssid'" in err for err in errors)
    assert any("missing the 'password'" in err for err in errors)
    assert warnings == []
    return


def test_validate_ok_does_not_raise() -> None:
    """
        Ensures a valid credential validates without issues.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "networks": NETWORKS}
    errors, warnings = WifiChoiceCredential.validate(cred_info)
    assert errors == []
    assert warnings == []
    return
