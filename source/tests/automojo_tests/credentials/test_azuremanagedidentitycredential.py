import unittest

from hypothesis import assume, given, strategies as st

from automojo.credentials.azuremanagedidentitycredential import AzureManagedIdentityCredential
from automojo.credentials.wellknown import CATEGORY_CLOUD_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "azure-mi"
CATEGORIES = ["cloud-venue"]
CLIENT_ID = "33333333-3333-3333-3333-333333333333"
RESOURCE_ID = "/subscriptions/abc/resourcegroups/rg/providers/Microsoft.ManagedIdentity/userAssignedIdentities/mi"


class TestAzureManagedIdentityCredential(unittest.TestCase):

    def test_construction_with_client_id_succeeds(self):
        """
            Verifies construction with only a client id succeeds.
        """
        cred = AzureManagedIdentityCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, client_id=CLIENT_ID,
        )
        self.assertEqual(cred.client_id, CLIENT_ID)
        self.assertIsNone(cred.resource_id)

    def test_construction_with_resource_id_succeeds(self):
        """
            Verifies construction with only a resource id succeeds.
        """
        cred = AzureManagedIdentityCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, resource_id=RESOURCE_ID,
        )
        self.assertIsNone(cred.client_id)
        self.assertEqual(cred.resource_id, RESOURCE_ID)

    def test_construction_with_both_selectors_succeeds(self):
        """
            Verifies construction with both selectors succeeds.
        """
        cred = AzureManagedIdentityCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, client_id=CLIENT_ID, resource_id=RESOURCE_ID,
        )
        self.assertEqual(cred.client_id, CLIENT_ID)
        self.assertEqual(cred.resource_id, RESOURCE_ID)

    def test_missing_category_raises(self):
        """
            Verifies wrong category raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            AzureManagedIdentityCredential(
                identifier=IDENTIFIER, categories=["basic"], client_id=CLIENT_ID,
            )

    def test_both_selectors_none_raises(self):
        """
            Verifies omitting both selectors raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            AzureManagedIdentityCredential(identifier=IDENTIFIER, categories=CATEGORIES)

    def test_repr_contains_identifier(self):
        """
            Verifies the ``repr`` includes the identifier and class name.
        """
        cred = AzureManagedIdentityCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, client_id=CLIENT_ID,
        )
        rendered = repr(cred)
        self.assertIn("AzureManagedIdentityCredential", rendered)
        self.assertIn(IDENTIFIER, rendered)

    def test_validate_missing_both_reports_error(self):
        """
            Verifies ``validate`` reports an error when both selectors are missing.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = AzureManagedIdentityCredential.validate(cred_info)
        self.assertTrue(any("at least one of 'client_id' or 'resource_id'" in err for err in errors))

    def test_validate_ok_does_not_report_errors(self):
        """
            Verifies ``validate`` reports no errors when a selector is present.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "client_id": CLIENT_ID}
        errors, warnings = AzureManagedIdentityCredential.validate(cred_info)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_category_membership_registered(self):
        """
            Verifies the per-provider category is registered under the cloud-venue umbrella.
        """
        cloud_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
        self.assertIn("azure-managed-identity", cloud_members)

    def test_as_dict_contains_fields(self):
        """
            Verifies ``as_dict`` contains both selectors and base fields.
        """
        cred = AzureManagedIdentityCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, client_id=CLIENT_ID,
        )
        data = cred.as_dict()
        self.assertEqual(data["identifier"], IDENTIFIER)
        self.assertEqual(data["client_id"], CLIENT_ID)
        self.assertIsNone(data["resource_id"])

    @given(
        identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        client_id=st.one_of(st.none(), st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48)),
        resource_id=st.one_of(st.none(), st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=80)),
    )
    def test_managed_identity_roundtrip(self, identifier, client_id, resource_id):
        """
            Property test: serialize -> deserialize -> equal for selector combinations.
        """
        assume(client_id is not None or resource_id is not None)
        cred = AzureManagedIdentityCredential(
            identifier=identifier, categories=CATEGORIES, client_id=client_id, resource_id=resource_id,
        )
        data = cred.as_dict()
        rebuilt = AzureManagedIdentityCredential(
            identifier=data["identifier"], categories=data["categories"],
            client_id=data["client_id"], resource_id=data["resource_id"], role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)
