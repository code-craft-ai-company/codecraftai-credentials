"""
    Example-based unit tests for :class:`VSphereCredential`.
"""

import unittest

from automojo.credentials.vspherecredential import VSphereCredential
from automojo.credentials.wellknown import (
    CATEGORY_VM_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
)
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "vsphere-cred"
CATEGORIES = ["vm-venue", "vsphere-basic"]
USERNAME = "administrator@vsphere.local"
PASSWORD = "LetMeComeIn"
SSO_TOKEN = "abcdef0123456789ssotoken"


class TestVSphereCredential(unittest.TestCase):

    def test_construction_password_only(self):
        """
            Verifies a password-only credential constructs successfully.
        """
        cred = VSphereCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            username=USERNAME, password=PASSWORD,
        )
        self.assertEqual(cred.username, USERNAME)
        self.assertEqual(cred.password, PASSWORD)
        self.assertIsNone(cred.sso_token)

    def test_construction_sso_token_only(self):
        """
            Verifies an sso-token-only credential constructs successfully.
        """
        cred = VSphereCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            username=USERNAME, sso_token=SSO_TOKEN,
        )
        self.assertEqual(cred.username, USERNAME)
        self.assertIsNone(cred.password)
        self.assertEqual(cred.sso_token, SSO_TOKEN)

    def test_construction_both_fields(self):
        """
            Verifies a credential carrying both fields constructs successfully.
        """
        cred = VSphereCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            username=USERNAME, password=PASSWORD, sso_token=SSO_TOKEN,
        )
        self.assertEqual(cred.password, PASSWORD)
        self.assertEqual(cred.sso_token, SSO_TOKEN)

    def test_missing_category_raises(self):
        """
            Verifies a wrong category raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            VSphereCredential(
                identifier=IDENTIFIER, categories=["basic"],
                username=USERNAME, password=PASSWORD,
            )

    def test_empty_username_raises(self):
        """
            Verifies an empty username is rejected.
        """
        with self.assertRaises(ConfigurationError):
            VSphereCredential(
                identifier=IDENTIFIER, categories=CATEGORIES,
                username="", password=PASSWORD,
            )

    def test_missing_password_and_sso_token_raises(self):
        """
            Verifies a credential with neither password nor sso_token is rejected.
        """
        with self.assertRaises(ConfigurationError):
            VSphereCredential(
                identifier=IDENTIFIER, categories=CATEGORIES,
                username=USERNAME,
            )

    def test_empty_password_and_none_sso_token_raises(self):
        """
            Verifies an empty password with no sso_token is rejected.
        """
        with self.assertRaises(ConfigurationError):
            VSphereCredential(
                identifier=IDENTIFIER, categories=CATEGORIES,
                username=USERNAME, password="", sso_token=None,
            )

    def test_repr_redacts_secret_material(self):
        """
            Verifies password and sso_token never appear in the ``repr``.
        """
        cred = VSphereCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            username=USERNAME, password=PASSWORD, sso_token=SSO_TOKEN,
        )
        rendered = repr(cred)
        self.assertIn("VSphereCredential", rendered)
        self.assertNotIn(PASSWORD, rendered)
        self.assertNotIn(SSO_TOKEN, rendered)
        self.assertIn("***", rendered)

    def test_repr_shows_none_when_secrets_absent(self):
        """
            Verifies the ``repr`` shows None for an absent secret field.
        """
        cred = VSphereCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            username=USERNAME, password=PASSWORD,
        )
        rendered = repr(cred)
        self.assertIn("sso_token=None", rendered)

    def test_validate_reports_missing_username(self):
        """
            Verifies ``validate`` reports a missing username.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES,
                     "password": PASSWORD}
        errors, warnings = VSphereCredential.validate(cred_info)
        self.assertTrue(any("missing 'username'" in err for err in errors))

    def test_validate_reports_missing_credentials(self):
        """
            Verifies ``validate`` reports a missing password and sso_token.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES,
                     "username": USERNAME}
        errors, warnings = VSphereCredential.validate(cred_info)
        self.assertTrue(any("password" in err and "sso_token" in err
                            for err in errors))

    def test_validate_ok_does_not_report_errors(self):
        """
            Verifies ``validate`` reports no errors for a complete credential.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES,
                     "username": USERNAME, "sso_token": SSO_TOKEN}
        errors, warnings = VSphereCredential.validate(cred_info)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_as_dict_roundtrips_none_fields(self):
        """
            Verifies ``as_dict`` carries None-valued fields losslessly.
        """
        cred = VSphereCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            username=USERNAME, password=PASSWORD,
        )
        data = cred.as_dict()
        self.assertEqual(data["username"], USERNAME)
        self.assertEqual(data["password"], PASSWORD)
        self.assertIsNone(data["sso_token"])

    def test_category_membership_registered(self):
        """
            Verifies the per-provider category is registered under the
            vm-venue umbrella.
        """
        vm_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_VM_VENUE]
        self.assertIn("vsphere-basic", vm_members)


if __name__ == "__main__":
    unittest.main()
