import unittest

from hypothesis import given, strategies as st

from ccai.credentials.twingateserviceaccountcredential import TwingateServiceAccountCredential
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "tg-prod"
CATEGORIES = ["twingate-service-account"]
API_TOKEN = "tg-svc-XXXX"
NETWORK_SLUG = "acme"


class TestTwingateServiceAccountCredential(unittest.TestCase):

    def test_construction_succeeds(self):
        """
            Verifies a complete credential constructs successfully.
        """
        cred = TwingateServiceAccountCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            api_token=API_TOKEN, network_slug=NETWORK_SLUG,
        )
        self.assertEqual(cred.api_token, API_TOKEN)
        self.assertEqual(cred.network_slug, NETWORK_SLUG)

    def test_missing_category_raises(self):
        """
            Verifies wrong category raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            TwingateServiceAccountCredential(
                identifier=IDENTIFIER, categories=["basic"],
                api_token=API_TOKEN, network_slug=NETWORK_SLUG,
            )

    def test_empty_api_token_raises(self):
        """
            Verifies an empty API token is rejected.
        """
        with self.assertRaises(ConfigurationError):
            TwingateServiceAccountCredential(
                identifier=IDENTIFIER, categories=CATEGORIES,
                api_token="", network_slug=NETWORK_SLUG,
            )

    def test_empty_network_slug_raises(self):
        """
            Verifies an empty network slug is rejected.
        """
        with self.assertRaises(ConfigurationError):
            TwingateServiceAccountCredential(
                identifier=IDENTIFIER, categories=CATEGORIES,
                api_token=API_TOKEN, network_slug="",
            )

    def test_network_slug_with_whitespace_raises(self):
        """
            Verifies a whitespace-containing slug is rejected.
        """
        with self.assertRaises(ConfigurationError):
            TwingateServiceAccountCredential(
                identifier=IDENTIFIER, categories=CATEGORIES,
                api_token=API_TOKEN, network_slug="bad slug",
            )

    def test_repr_redacts_token(self):
        """
            Verifies the API token value never appears in the ``repr``.
        """
        cred = TwingateServiceAccountCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            api_token=API_TOKEN, network_slug=NETWORK_SLUG,
        )
        rendered = repr(cred)
        self.assertIn("TwingateServiceAccountCredential", rendered)
        self.assertIn(IDENTIFIER, rendered)
        self.assertIn(NETWORK_SLUG, rendered)
        self.assertNotIn(API_TOKEN, rendered)
        self.assertIn("***", rendered)

    def test_validate_reports_each_failure(self):
        """
            Verifies ``validate`` reports each failure with a descriptive message.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "network_slug": "bad slug"}
        errors, warnings = TwingateServiceAccountCredential.validate(cred_info)
        self.assertTrue(any("missing 'api_token'" in err for err in errors))
        self.assertTrue(any("whitespace" in err for err in errors))

    def test_validate_ok_does_not_report_errors(self):
        """
            Verifies ``validate`` reports no errors for a complete credential.
        """
        cred_info = {
            "identifier": IDENTIFIER, "categories": CATEGORIES,
            "api_token": API_TOKEN, "network_slug": NETWORK_SLUG,
        }
        errors, warnings = TwingateServiceAccountCredential.validate(cred_info)
        self.assertEqual(errors, [])

    @given(
        identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        api_token=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
        network_slug=st.text(alphabet=st.characters(whitelist_categories=("Ll", "Lu", "Nd"), whitelist_characters="-_"), min_size=1, max_size=32),
    )
    def test_serialize_roundtrip(self, identifier, api_token, network_slug):
        """
            Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
        """
        cred = TwingateServiceAccountCredential(
            identifier=identifier, categories=CATEGORIES,
            api_token=api_token, network_slug=network_slug,
        )
        data = cred.as_dict()
        rebuilt = TwingateServiceAccountCredential(
            identifier=data["identifier"], categories=data["categories"],
            api_token=data["api_token"], network_slug=data["network_slug"],
            role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)
