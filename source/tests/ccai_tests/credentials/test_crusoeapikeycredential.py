import unittest

from ccai.testbase.properties import given
from ccai.testbase.properties import strategies as st

from ccai.credentials.crusoeapikeycredential import CrusoeApiKeyCredential
from ccai.credentials.wellknown import (
    CATEGORY_CLOUD_VENUE,
    CATEGORY_HPC_VENUE,
    WELL_KNOWN_CATEGORY_MEMBERSHIP,
)
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "crusoe-key"
CATEGORIES = ["hpc-venue"]
ACCESS_KEY_ID = "crusoe-access-key-abc"
SECRET = "crusoe-secret-xyz"


class TestCrusoeApiKeyCredential(unittest.TestCase):

    def test_construction_succeeds(self):
        """
            Verifies a complete credential constructs successfully.
        """
        cred = CrusoeApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            access_key_id=ACCESS_KEY_ID, secret=SECRET,
        )
        self.assertEqual(cred.access_key_id, ACCESS_KEY_ID)
        self.assertEqual(cred.secret, SECRET)

    def test_construction_succeeds_with_cloud_venue(self):
        """
            Verifies the cloud-venue category alone is accepted.
        """
        cred = CrusoeApiKeyCredential(
            identifier=IDENTIFIER, categories=["cloud-venue"],
            access_key_id=ACCESS_KEY_ID, secret=SECRET,
        )
        self.assertEqual(cred.access_key_id, ACCESS_KEY_ID)

    def test_missing_category_raises(self):
        """
            Verifies neither category present raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            CrusoeApiKeyCredential(
                identifier=IDENTIFIER, categories=["basic"],
                access_key_id=ACCESS_KEY_ID, secret=SECRET,
            )

    def test_empty_access_key_id_raises(self):
        """
            Verifies an empty access_key_id is rejected.
        """
        with self.assertRaises(ConfigurationError):
            CrusoeApiKeyCredential(
                identifier=IDENTIFIER, categories=CATEGORIES,
                access_key_id="", secret=SECRET,
            )

    def test_empty_secret_raises(self):
        """
            Verifies an empty secret is rejected.
        """
        with self.assertRaises(ConfigurationError):
            CrusoeApiKeyCredential(
                identifier=IDENTIFIER, categories=CATEGORIES,
                access_key_id=ACCESS_KEY_ID, secret="",
            )

    def test_repr_redacts_secret(self):
        """
            Verifies the secret never appears in the ``repr``.
        """
        cred = CrusoeApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            access_key_id=ACCESS_KEY_ID, secret=SECRET,
        )
        rendered = repr(cred)
        self.assertIn("CrusoeApiKeyCredential", rendered)
        self.assertNotIn(SECRET, rendered)
        self.assertIn("***", rendered)

    def test_validate_reports_each_missing_field(self):
        """
            Verifies ``validate`` reports each missing field.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = CrusoeApiKeyCredential.validate(cred_info)
        self.assertTrue(any("missing 'access_key_id'" in err for err in errors))
        self.assertTrue(any("missing 'secret'" in err for err in errors))

    def test_validate_ok_does_not_report_errors(self):
        """
            Verifies ``validate`` reports no errors for a complete credential.
        """
        cred_info = {
            "identifier": IDENTIFIER, "categories": CATEGORIES,
            "access_key_id": ACCESS_KEY_ID, "secret": SECRET,
        }
        errors, warnings = CrusoeApiKeyCredential.validate(cred_info)
        self.assertEqual(errors, [])

    def test_as_dict_content(self):
        """
            Verifies ``as_dict`` carries all credential fields.
        """
        cred = CrusoeApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            access_key_id=ACCESS_KEY_ID, secret=SECRET,
        )
        data = cred.as_dict()
        self.assertEqual(data["identifier"], IDENTIFIER)
        self.assertEqual(data["categories"], CATEGORIES)
        self.assertEqual(data["access_key_id"], ACCESS_KEY_ID)
        self.assertEqual(data["secret"], SECRET)
        self.assertEqual(data["role"], "priv")

    def test_category_membership_registered(self):
        """
            Verifies the per-provider category is registered under both umbrellas.
        """
        hpc_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_HPC_VENUE]
        cloud_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
        self.assertIn(CATEGORY_HPC_VENUE, hpc_members)
        self.assertIn(CATEGORY_CLOUD_VENUE, cloud_members)

    @given(
        identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        access_key_id=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
        secret=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=128),
    )
    def test_crusoe_credential_roundtrip(self, identifier, access_key_id, secret):
        """
            Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
        """
        cred = CrusoeApiKeyCredential(
            identifier=identifier, categories=CATEGORIES,
            access_key_id=access_key_id, secret=secret,
        )
        data = cred.as_dict()
        rebuilt = CrusoeApiKeyCredential(
            identifier=data["identifier"], categories=data["categories"],
            access_key_id=data["access_key_id"], secret=data["secret"], role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)


if __name__ == "__main__":
    unittest.main()
