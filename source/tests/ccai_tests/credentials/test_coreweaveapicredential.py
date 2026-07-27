import unittest

from hypothesis import given, strategies as st

from ccai.credentials.coreweaveapicredential import CoreweaveApiCredential
from ccai.credentials.wellknown import CATEGORY_HPC_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "coreweave-token"
CATEGORIES = ["hpc-venue"]
TOKEN = "coreweave_abc123"
ORGANIZATION_ID = "org-12345"


class TestCoreweaveApiCredential(unittest.TestCase):

    def test_construction_without_organization_succeeds(self):
        """
            Verifies a credential constructs successfully without an organization_id.
        """
        cred = CoreweaveApiCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
        )
        self.assertEqual(cred.token, TOKEN)
        self.assertIsNone(cred.organization_id)
        self.assertEqual(cred.identifier, IDENTIFIER)
        self.assertEqual(cred.categories, CATEGORIES)

    def test_construction_with_organization_succeeds(self):
        """
            Verifies a credential constructs successfully with an organization_id.
        """
        cred = CoreweaveApiCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
            organization_id=ORGANIZATION_ID,
        )
        self.assertEqual(cred.organization_id, ORGANIZATION_ID)

    def test_missing_category_raises(self):
        """
            Verifies wrong category raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            CoreweaveApiCredential(
                identifier=IDENTIFIER, categories=["basic"], token=TOKEN,
            )

    def test_empty_token_raises(self):
        """
            Verifies an empty token is rejected.
        """
        with self.assertRaises(ConfigurationError):
            CoreweaveApiCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, token="",
            )

    def test_repr_redacts_token(self):
        """
            Verifies the token never appears in the ``repr``.
        """
        cred = CoreweaveApiCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
            organization_id=ORGANIZATION_ID,
        )
        rendered = repr(cred)
        self.assertIn("CoreweaveApiCredential", rendered)
        self.assertNotIn(TOKEN, rendered)
        self.assertIn("***", rendered)

    def test_validate_reports_missing_token(self):
        """
            Verifies ``validate`` reports a missing token field.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = CoreweaveApiCredential.validate(cred_info)
        self.assertTrue(any("missing 'token'" in err for err in errors))

    def test_validate_ok_does_not_report_errors(self):
        """
            Verifies ``validate`` reports no errors for a complete credential.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "token": TOKEN}
        errors, warnings = CoreweaveApiCredential.validate(cred_info)
        self.assertEqual(errors, [])

    def test_as_dict_content_without_organization(self):
        """
            Verifies ``as_dict`` carries all credential fields with organization_id None.
        """
        cred = CoreweaveApiCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
        )
        data = cred.as_dict()
        self.assertEqual(data["identifier"], IDENTIFIER)
        self.assertEqual(data["categories"], CATEGORIES)
        self.assertEqual(data["token"], TOKEN)
        self.assertIsNone(data["organization_id"])
        self.assertEqual(data["role"], "priv")

    def test_as_dict_content_with_organization(self):
        """
            Verifies ``as_dict`` carries a non-empty organization_id.
        """
        cred = CoreweaveApiCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
            organization_id=ORGANIZATION_ID,
        )
        data = cred.as_dict()
        self.assertEqual(data["organization_id"], ORGANIZATION_ID)

    def test_category_membership_registered(self):
        """
            Verifies the per-provider category is registered under the hpc-venue umbrella.
        """
        members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_HPC_VENUE]
        self.assertIn(CATEGORY_HPC_VENUE, members)

    @given(
        identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        token=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=128),
        organization_id=st.one_of(
            st.none(),
            st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
        ),
    )
    def test_coreweave_credential_roundtrip(self, identifier, token, organization_id):
        """
            Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
        """
        cred = CoreweaveApiCredential(
            identifier=identifier, categories=CATEGORIES, token=token,
            organization_id=organization_id,
        )
        data = cred.as_dict()
        rebuilt = CoreweaveApiCredential(
            identifier=data["identifier"], categories=data["categories"],
            token=data["token"], organization_id=data["organization_id"],
            role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)


if __name__ == "__main__":
    unittest.main()
