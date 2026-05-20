import unittest

from hypothesis import given, strategies as st

from automojo.credentials.tailscaleoauthcredential import TailscaleOAuthCredential
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "ts-prov-oauth"
CATEGORIES = ["tailscale-oauth"]
CLIENT_ID = "ksXXXX"
CLIENT_SECRET = "tskey-client-secret-XXXX"


class TestTailscaleOAuthCredential(unittest.TestCase):

    def test_construction_succeeds(self):
        """
            Verifies a complete credential constructs successfully.
        """
        cred = TailscaleOAuthCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
            default_tags=["tag:lab"],
        )
        self.assertEqual(cred.client_id, CLIENT_ID)
        self.assertEqual(cred.client_secret, CLIENT_SECRET)
        self.assertEqual(cred.default_tags, ["tag:lab"])

    def test_missing_category_raises(self):
        """
            Verifies wrong category raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            TailscaleOAuthCredential(
                identifier=IDENTIFIER, categories=["basic"],
                client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
            )

    def test_empty_client_id_raises(self):
        """
            Verifies an empty client id is rejected.
        """
        with self.assertRaises(ConfigurationError):
            TailscaleOAuthCredential(
                identifier=IDENTIFIER, categories=CATEGORIES,
                client_id="", client_secret=CLIENT_SECRET,
            )

    def test_empty_client_secret_raises(self):
        """
            Verifies an empty client secret is rejected.
        """
        with self.assertRaises(ConfigurationError):
            TailscaleOAuthCredential(
                identifier=IDENTIFIER, categories=CATEGORIES,
                client_id=CLIENT_ID, client_secret="",
            )

    def test_default_tags_optional_defaults_to_empty_list(self):
        """
            Verifies ``default_tags`` defaults to an empty list when not provided.
        """
        cred = TailscaleOAuthCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
        )
        self.assertEqual(cred.default_tags, [])

    def test_repr_redacts_client_secret(self):
        """
            Verifies the client secret value never appears in the ``repr``.
        """
        cred = TailscaleOAuthCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
        )
        rendered = repr(cred)
        self.assertIn("TailscaleOAuthCredential", rendered)
        self.assertIn(IDENTIFIER, rendered)
        self.assertIn(CLIENT_ID, rendered)
        self.assertNotIn(CLIENT_SECRET, rendered)
        self.assertIn("***", rendered)

    def test_validate_missing_fields_reports_errors(self):
        """
            Verifies ``validate`` reports missing client id and client secret.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = TailscaleOAuthCredential.validate(cred_info)
        self.assertTrue(any("missing 'client_id'" in err for err in errors))
        self.assertTrue(any("missing 'client_secret'" in err for err in errors))

    def test_validate_ok_does_not_report_errors(self):
        """
            Verifies ``validate`` reports no errors for a complete credential.
        """
        cred_info = {
            "identifier": IDENTIFIER, "categories": CATEGORIES,
            "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        }
        errors, warnings = TailscaleOAuthCredential.validate(cred_info)
        self.assertEqual(errors, [])

    @given(
        identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        client_id=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        client_secret=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
        default_tags=st.lists(st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=16), max_size=5),
    )
    def test_serialize_roundtrip(self, identifier, client_id, client_secret, default_tags):
        """
            Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
        """
        cred = TailscaleOAuthCredential(
            identifier=identifier, categories=CATEGORIES,
            client_id=client_id, client_secret=client_secret, default_tags=default_tags,
        )
        data = cred.as_dict()
        rebuilt = TailscaleOAuthCredential(
            identifier=data["identifier"], categories=data["categories"],
            client_id=data["client_id"], client_secret=data["client_secret"],
            default_tags=data["default_tags"], role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)
