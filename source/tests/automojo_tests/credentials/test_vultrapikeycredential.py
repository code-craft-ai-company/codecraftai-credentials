import unittest

from hypothesis import given, strategies as st

from automojo.credentials.vultrapikeycredential import VultrApiKeyCredential
from automojo.credentials.wellknown import CATEGORY_CLOUD_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "vultr-key"
CATEGORIES = ["cloud-venue"]
TOKEN = "vultr_abc123"


class TestVultrApiKeyCredential(unittest.TestCase):

    def test_construction_succeeds(self):
        """
            Verifies a complete credential constructs successfully.
        """
        cred = VultrApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
        )
        self.assertEqual(cred.token, TOKEN)
        self.assertEqual(cred.identifier, IDENTIFIER)
        self.assertEqual(cred.categories, CATEGORIES)

    def test_missing_category_raises(self):
        """
            Verifies wrong category raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            VultrApiKeyCredential(
                identifier=IDENTIFIER, categories=["basic"], token=TOKEN,
            )

    def test_empty_token_raises(self):
        """
            Verifies an empty token is rejected.
        """
        with self.assertRaises(ConfigurationError):
            VultrApiKeyCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, token="",
            )

    def test_repr_redacts_token(self):
        """
            Verifies the token never appears in the ``repr``.
        """
        cred = VultrApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
        )
        rendered = repr(cred)
        self.assertIn("VultrApiKeyCredential", rendered)
        self.assertNotIn(TOKEN, rendered)
        self.assertIn("***", rendered)

    def test_validate_reports_missing_token(self):
        """
            Verifies ``validate`` reports a missing token field.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = VultrApiKeyCredential.validate(cred_info)
        self.assertTrue(any("missing 'token'" in err for err in errors))

    def test_validate_ok_does_not_report_errors(self):
        """
            Verifies ``validate`` reports no errors for a complete credential.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "token": TOKEN}
        errors, warnings = VultrApiKeyCredential.validate(cred_info)
        self.assertEqual(errors, [])

    def test_as_dict_content(self):
        """
            Verifies ``as_dict`` carries all credential fields.
        """
        cred = VultrApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
        )
        data = cred.as_dict()
        self.assertEqual(data["identifier"], IDENTIFIER)
        self.assertEqual(data["categories"], CATEGORIES)
        self.assertEqual(data["token"], TOKEN)
        self.assertEqual(data["role"], "priv")

    def test_category_membership_registered(self):
        """
            Verifies the per-provider category is registered under the cloud-venue umbrella.
        """
        members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
        self.assertIn(CATEGORY_CLOUD_VENUE, members)

    @given(
        identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        token=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=128),
    )
    def test_vultr_token_roundtrip(self, identifier, token):
        """
            Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
        """
        cred = VultrApiKeyCredential(
            identifier=identifier, categories=CATEGORIES, token=token,
        )
        data = cred.as_dict()
        rebuilt = VultrApiKeyCredential(
            identifier=data["identifier"], categories=data["categories"],
            token=data["token"], role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)


if __name__ == "__main__":
    unittest.main()
