import unittest

from hypothesis import given, strategies as st

from automojo.credentials.gcpworkloadidentitycredential import GcpWorkloadIdentityCredential
from automojo.credentials.wellknown import CATEGORY_CLOUD_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "gcp-wif"
CATEGORIES = ["cloud-venue"]
AUDIENCE = "//iam.googleapis.com/projects/123/locations/global/workloadIdentityPools/pool/providers/provider"
SUBJECT_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:jwt"
SERVICE_ACCOUNT_EMAIL = "svc@my-project.iam.gserviceaccount.com"


class TestGcpWorkloadIdentityCredential(unittest.TestCase):

    def test_construction_succeeds(self):
        """
            Verifies a complete credential constructs successfully.
        """
        cred = GcpWorkloadIdentityCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, audience=AUDIENCE,
            subject_token_type=SUBJECT_TOKEN_TYPE, service_account_email=SERVICE_ACCOUNT_EMAIL,
        )
        self.assertEqual(cred.audience, AUDIENCE)
        self.assertEqual(cred.subject_token_type, SUBJECT_TOKEN_TYPE)
        self.assertEqual(cred.service_account_email, SERVICE_ACCOUNT_EMAIL)

    def test_token_url_defaults_when_omitted(self):
        """
            Verifies ``token_url`` is populated with the default when omitted.
        """
        cred = GcpWorkloadIdentityCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, audience=AUDIENCE,
            subject_token_type=SUBJECT_TOKEN_TYPE, service_account_email=SERVICE_ACCOUNT_EMAIL,
        )
        self.assertEqual(cred.token_url, GcpWorkloadIdentityCredential.DEFAULT_TOKEN_URL)

    def test_missing_category_raises(self):
        """
            Verifies wrong category raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            GcpWorkloadIdentityCredential(
                identifier=IDENTIFIER, categories=["basic"], audience=AUDIENCE,
                subject_token_type=SUBJECT_TOKEN_TYPE, service_account_email=SERVICE_ACCOUNT_EMAIL,
            )

    def test_empty_audience_raises(self):
        """
            Verifies an empty audience is rejected.
        """
        with self.assertRaises(ConfigurationError):
            GcpWorkloadIdentityCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, audience="",
                subject_token_type=SUBJECT_TOKEN_TYPE, service_account_email=SERVICE_ACCOUNT_EMAIL,
            )

    def test_empty_service_account_email_raises(self):
        """
            Verifies an empty service account email is rejected.
        """
        with self.assertRaises(ConfigurationError):
            GcpWorkloadIdentityCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, audience=AUDIENCE,
                subject_token_type=SUBJECT_TOKEN_TYPE, service_account_email="",
            )

    def test_repr_contains_identifier(self):
        """
            Verifies the ``repr`` includes the identifier and class name.
        """
        cred = GcpWorkloadIdentityCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, audience=AUDIENCE,
            subject_token_type=SUBJECT_TOKEN_TYPE, service_account_email=SERVICE_ACCOUNT_EMAIL,
        )
        rendered = repr(cred)
        self.assertIn("GcpWorkloadIdentityCredential", rendered)
        self.assertIn(IDENTIFIER, rendered)

    def test_validate_reports_each_missing_field(self):
        """
            Verifies ``validate`` reports each missing field.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = GcpWorkloadIdentityCredential.validate(cred_info)
        self.assertTrue(any("missing 'audience'" in err for err in errors))
        self.assertTrue(any("missing 'subject_token_type'" in err for err in errors))
        self.assertTrue(any("missing 'service_account_email'" in err for err in errors))

    def test_category_membership_registered(self):
        """
            Verifies the per-provider category is registered under the cloud-venue umbrella.
        """
        cloud_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
        self.assertIn(CATEGORY_CLOUD_VENUE, cloud_members)

    @given(
        identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        audience=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=96),
        subject_token_type=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48),
        service_account_email=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
        token_url=st.one_of(st.none(), st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64)),
    )
    def test_gcp_workload_identity_roundtrip(self, identifier, audience, subject_token_type, service_account_email, token_url):
        """
            Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
        """
        cred = GcpWorkloadIdentityCredential(
            identifier=identifier, categories=CATEGORIES, audience=audience,
            subject_token_type=subject_token_type, service_account_email=service_account_email,
            token_url=token_url,
        )
        data = cred.as_dict()
        rebuilt = GcpWorkloadIdentityCredential(
            identifier=data["identifier"], categories=data["categories"], audience=data["audience"],
            subject_token_type=data["subject_token_type"], service_account_email=data["service_account_email"],
            token_url=data["token_url"], role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)
