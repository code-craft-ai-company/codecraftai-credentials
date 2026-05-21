import unittest

from hypothesis import given, strategies as st

from automojo.credentials.azureserviceprincipalcredential import AzureServicePrincipalCredential
from automojo.credentials.wellknown import CATEGORY_CLOUD_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "azure-sp"
CATEGORIES = ["cloud-venue"]
TENANT_ID = "11111111-1111-1111-1111-111111111111"
CLIENT_ID = "22222222-2222-2222-2222-222222222222"
CLIENT_SECRET = "@@&_LetMeComeIn"


class TestAzureServicePrincipalCredential(unittest.TestCase):

    def test_construction_succeeds(self):
        """
            Verifies a complete credential constructs successfully.
        """
        cred = AzureServicePrincipalCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
        )
        self.assertEqual(cred.tenant_id, TENANT_ID)
        self.assertEqual(cred.client_id, CLIENT_ID)
        self.assertEqual(cred.client_secret, CLIENT_SECRET)

    def test_missing_category_raises(self):
        """
            Verifies wrong category raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            AzureServicePrincipalCredential(
                identifier=IDENTIFIER, categories=["basic"],
                tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
            )

    def test_empty_tenant_id_raises(self):
        """
            Verifies an empty tenant id is rejected.
        """
        with self.assertRaises(ConfigurationError):
            AzureServicePrincipalCredential(
                identifier=IDENTIFIER, categories=CATEGORIES,
                tenant_id="", client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
            )

    def test_empty_client_id_raises(self):
        """
            Verifies an empty client id is rejected.
        """
        with self.assertRaises(ConfigurationError):
            AzureServicePrincipalCredential(
                identifier=IDENTIFIER, categories=CATEGORIES,
                tenant_id=TENANT_ID, client_id="", client_secret=CLIENT_SECRET,
            )

    def test_empty_client_secret_raises(self):
        """
            Verifies an empty client secret is rejected.
        """
        with self.assertRaises(ConfigurationError):
            AzureServicePrincipalCredential(
                identifier=IDENTIFIER, categories=CATEGORIES,
                tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret="",
            )

    def test_repr_redacts_secret(self):
        """
            Verifies the client secret value never appears in the ``repr``.
        """
        cred = AzureServicePrincipalCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
        )
        rendered = repr(cred)
        self.assertIn("AzureServicePrincipalCredential", rendered)
        self.assertIn(IDENTIFIER, rendered)
        self.assertNotIn(CLIENT_SECRET, rendered)
        self.assertIn("***", rendered)

    def test_validate_reports_each_missing_field(self):
        """
            Verifies ``validate`` reports each missing field.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = AzureServicePrincipalCredential.validate(cred_info)
        self.assertTrue(any("missing 'tenant_id'" in err for err in errors))
        self.assertTrue(any("missing 'client_id'" in err for err in errors))
        self.assertTrue(any("missing 'client_secret'" in err for err in errors))
        self.assertEqual(warnings, [])

    def test_validate_ok_does_not_report_errors(self):
        """
            Verifies ``validate`` reports no errors for a complete credential.
        """
        cred_info = {
            "identifier": IDENTIFIER, "categories": CATEGORIES,
            "tenant_id": TENANT_ID, "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        }
        errors, warnings = AzureServicePrincipalCredential.validate(cred_info)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_category_membership_registered(self):
        """
            Verifies the per-provider category is registered under the cloud-venue umbrella.
        """
        cloud_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
        self.assertIn(CATEGORY_CLOUD_VENUE, cloud_members)

    def test_as_dict_contains_fields(self):
        """
            Verifies ``as_dict`` contains every constructor field.
        """
        cred = AzureServicePrincipalCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
        )
        data = cred.as_dict()
        self.assertEqual(data["identifier"], IDENTIFIER)
        self.assertEqual(data["categories"], CATEGORIES)
        self.assertEqual(data["role"], "priv")
        self.assertEqual(data["tenant_id"], TENANT_ID)
        self.assertEqual(data["client_id"], CLIENT_ID)
        self.assertEqual(data["client_secret"], CLIENT_SECRET)

    @given(
        identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        tenant_id=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48),
        client_id=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48),
        client_secret=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
    )
    def test_service_principal_roundtrip(self, identifier, tenant_id, client_id, client_secret):
        """
            Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
        """
        cred = AzureServicePrincipalCredential(
            identifier=identifier, categories=CATEGORIES,
            tenant_id=tenant_id, client_id=client_id, client_secret=client_secret,
        )
        data = cred.as_dict()
        rebuilt = AzureServicePrincipalCredential(
            identifier=data["identifier"], categories=data["categories"],
            tenant_id=data["tenant_id"], client_id=data["client_id"],
            client_secret=data["client_secret"], role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)
