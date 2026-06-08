import unittest

from ccai.credentials.wifichoicecredential import WifiChoiceCredential
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "my-wifi-networks"
CATEGORIES = ["wifi-choice"]
NETWORKS = [
    {"ssid": "AP1", "password": "pwd1"},
    {"ssid": "AP2", "password": "pwd2"},
]


class TestWifiChoiceCredential(unittest.TestCase):

    def test_init_with_invalid_category_raises(self):
        """
            Ensures invalid categories raise :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            WifiChoiceCredential(identifier=IDENTIFIER, categories=["basic"], networks=NETWORKS)

    def test_init_with_empty_networks_raises(self):
        """
            Ensures an empty networks list raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            WifiChoiceCredential(identifier=IDENTIFIER, categories=CATEGORIES, networks=[])

    def test_default_role_is_priv(self):
        """
            Confirms the default role is ``priv``.
        """
        cred = WifiChoiceCredential(identifier=IDENTIFIER, categories=CATEGORIES, networks=NETWORKS)
        self.assertEqual(cred.role, "priv")

    def test_networks_property_returns_value(self):
        """
            Ensures the networks accessor returns the configured networks.
        """
        cred = WifiChoiceCredential(identifier=IDENTIFIER, categories=CATEGORIES, networks=NETWORKS)
        self.assertEqual(cred.networks, NETWORKS)

    def test_as_dict_contains_fields(self):
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
        self.assertEqual(cred.as_dict(), expected)

    def test_validate_missing_networks_reports_error(self):
        """
            Ensures validation enforces the presence of network definitions.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = WifiChoiceCredential.validate(cred_info)
        self.assertTrue(any("missing 'networks'" in err for err in errors))
        self.assertEqual(warnings, [])

    def test_validate_empty_networks_raises(self):
        """
            Ensures validation detects empty network lists.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "networks": []}
        errors, warnings = WifiChoiceCredential.validate(cred_info)
        self.assertTrue(any("empty 'networks'" in err for err in errors))
        self.assertEqual(warnings, [])

    def test_validate_missing_network_fields_raises(self):
        """
            Ensures missing SSID and password entries are reported.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "networks": [{}]}
        errors, warnings = WifiChoiceCredential.validate(cred_info)
        self.assertTrue(any("missing the 'ssid'" in err for err in errors))
        self.assertTrue(any("missing the 'password'" in err for err in errors))
        self.assertEqual(warnings, [])

    def test_validate_ok_does_not_raise(self):
        """
            Ensures a valid credential validates without issues.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "networks": NETWORKS}
        errors, warnings = WifiChoiceCredential.validate(cred_info)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
