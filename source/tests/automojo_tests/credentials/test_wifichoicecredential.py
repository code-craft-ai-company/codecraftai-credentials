import unittest

from automojo.errors.exceptions import ConfigurationError
from automojo.credentials.wifichoicecredential import WifiChoiceCredential


class TestWifiChoiceCredential(unittest.TestCase):

    def setUp(self):
        self.identifier = "my-wifi-networks"
        self.categories = ["wifi-choice"]
        self.networks = [
            {"ssid": "AP1", "password": "pwd1"},
            {"ssid": "AP2", "password": "pwd2"},
        ]
        return

    def test_init_with_invalid_category_raises(self):
        with self.assertRaises(ConfigurationError):
            WifiChoiceCredential(identifier=self.identifier, categories=["basic"], networks=self.networks)

    def test_init_with_empty_networks_raises(self):
        with self.assertRaises(ConfigurationError):
            WifiChoiceCredential(identifier=self.identifier, categories=self.categories, networks=[])

    def test_default_role_is_priv(self):
        cred = WifiChoiceCredential(identifier=self.identifier, categories=self.categories, networks=self.networks)
        self.assertEqual(cred.role, "priv")

    def test_networks_property_returns_value(self):
        cred = WifiChoiceCredential(identifier=self.identifier, categories=self.categories, networks=self.networks)
        self.assertEqual(cred.networks, self.networks)

    def test_as_dict_contains_fields(self):
        cred = WifiChoiceCredential(identifier=self.identifier, categories=self.categories, networks=self.networks)
        expected = {
            "identifier": self.identifier,
            "categories": self.categories,
            "role": "priv",
            "networks": self.networks,
        }
        self.assertEqual(cred.as_dict(), expected)

    def test_validate_missing_networks_reports_error(self):
        cred_info = {
            "identifier": self.identifier,
            "categories": self.categories,
        }
        errors, warnings = WifiChoiceCredential.validate(cred_info)
        self.assertIn("missing 'networks' field on wifi-choice credential.", errors)
        self.assertEqual(len(warnings), 0)

    def test_validate_empty_networks_raises(self):
        cred_info = {
            "identifier": self.identifier,
            "categories": self.categories,
            "networks": [],
        }
        errors, warnings = WifiChoiceCredential.validate(cred_info)
        self.assertIn("empty 'networks' field on wifi-choice credential.", errors)
        self.assertEqual(len(warnings), 0)

    def test_validate_missing_network_fields_raises(self):
        cred_info = {
            "identifier": self.identifier,
            "categories": self.categories,
            "networks": [{}],
        }
        errors, warnings = WifiChoiceCredential.validate(cred_info)
        self.assertTrue(any("missing the 'ssid' field" in err for err in errors))
        self.assertTrue(any("missing the 'password' field" in err for err in errors))
        self.assertEqual(len(warnings), 0)

    def test_validate_ok_does_not_raise(self):
        cred_info = {
            "identifier": self.identifier,
            "categories": self.categories,
            "networks": self.networks,
        }
        errors, warnings = WifiChoiceCredential.validate(cred_info)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)


if __name__ == "__main__":
    unittest.main()
