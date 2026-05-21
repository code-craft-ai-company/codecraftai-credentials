import unittest

from hypothesis import given, strategies as st

from automojo.credentials.gcpserviceaccountkeycredential import GcpServiceAccountKeyCredential
from automojo.credentials.wellknown import CATEGORY_CLOUD_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "gcp-sa"
CATEGORIES = ["cloud-venue"]
PROJECT_ID = "my-project"
CLIENT_EMAIL = "svc@my-project.iam.gserviceaccount.com"
PRIVATE_KEY_ID = "abcdef0123456789"
PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nMIIBVg\n-----END PRIVATE KEY-----\n"


class TestGcpServiceAccountKeyCredential(unittest.TestCase):

    def test_construction_succeeds(self):
        """
            Verifies a complete credential constructs successfully.
        """
        cred = GcpServiceAccountKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, project_id=PROJECT_ID,
            client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key=PRIVATE_KEY,
        )
        self.assertEqual(cred.project_id, PROJECT_ID)
        self.assertEqual(cred.client_email, CLIENT_EMAIL)
        self.assertEqual(cred.private_key_id, PRIVATE_KEY_ID)
        self.assertEqual(cred.private_key, PRIVATE_KEY)

    def test_token_uri_defaults_when_omitted(self):
        """
            Verifies ``token_uri`` is populated with the default when omitted.
        """
        cred = GcpServiceAccountKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, project_id=PROJECT_ID,
            client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key=PRIVATE_KEY,
        )
        self.assertEqual(cred.token_uri, GcpServiceAccountKeyCredential.DEFAULT_TOKEN_URI)

    def test_token_uri_override_respected(self):
        """
            Verifies an explicit ``token_uri`` is retained.
        """
        custom = "https://example.test/token"
        cred = GcpServiceAccountKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, project_id=PROJECT_ID,
            client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key=PRIVATE_KEY,
            token_uri=custom,
        )
        self.assertEqual(cred.token_uri, custom)

    def test_missing_category_raises(self):
        """
            Verifies wrong category raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            GcpServiceAccountKeyCredential(
                identifier=IDENTIFIER, categories=["basic"], project_id=PROJECT_ID,
                client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key=PRIVATE_KEY,
            )

    def test_empty_project_id_raises(self):
        """
            Verifies an empty project id is rejected.
        """
        with self.assertRaises(ConfigurationError):
            GcpServiceAccountKeyCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, project_id="",
                client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key=PRIVATE_KEY,
            )

    def test_empty_private_key_raises(self):
        """
            Verifies an empty private key is rejected.
        """
        with self.assertRaises(ConfigurationError):
            GcpServiceAccountKeyCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, project_id=PROJECT_ID,
                client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key="",
            )

    def test_repr_redacts_key_material(self):
        """
            Verifies private key material never appears in the ``repr``.
        """
        cred = GcpServiceAccountKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, project_id=PROJECT_ID,
            client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key=PRIVATE_KEY,
        )
        rendered = repr(cred)
        self.assertIn("GcpServiceAccountKeyCredential", rendered)
        self.assertNotIn(PRIVATE_KEY, rendered)
        self.assertNotIn(PRIVATE_KEY_ID, rendered)
        self.assertIn("***", rendered)

    def test_validate_reports_each_missing_field(self):
        """
            Verifies ``validate`` reports each missing field.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = GcpServiceAccountKeyCredential.validate(cred_info)
        self.assertTrue(any("missing 'project_id'" in err for err in errors))
        self.assertTrue(any("missing 'client_email'" in err for err in errors))
        self.assertTrue(any("missing 'private_key_id'" in err for err in errors))
        self.assertTrue(any("missing 'private_key'" in err for err in errors))

    def test_category_membership_registered(self):
        """
            Verifies the per-provider category is registered under the cloud-venue umbrella.
        """
        cloud_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
        self.assertIn(CATEGORY_CLOUD_VENUE, cloud_members)

    @given(
        identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        project_id=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        client_email=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
        private_key_id=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48),
        private_key=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=128),
        token_uri=st.one_of(st.none(), st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64)),
    )
    def test_gcp_service_account_key_roundtrip(self, identifier, project_id, client_email, private_key_id, private_key, token_uri):
        """
            Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
        """
        cred = GcpServiceAccountKeyCredential(
            identifier=identifier, categories=CATEGORIES, project_id=project_id,
            client_email=client_email, private_key_id=private_key_id, private_key=private_key,
            token_uri=token_uri,
        )
        data = cred.as_dict()
        rebuilt = GcpServiceAccountKeyCredential(
            identifier=data["identifier"], categories=data["categories"], project_id=data["project_id"],
            client_email=data["client_email"], private_key_id=data["private_key_id"],
            private_key=data["private_key"], token_uri=data["token_uri"], role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)
