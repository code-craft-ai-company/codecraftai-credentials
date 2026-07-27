import unittest

from hypothesis import given, strategies as st

from ccai.credentials.oraclecloudapikeycredential import OracleCloudApiKeyCredential
from ccai.credentials.wellknown import CATEGORY_CLOUD_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "oci-key"
CATEGORIES = ["cloud-venue"]
TENANCY_OCID = "ocid1.tenancy.oc1..aaaatenancy"
USER_OCID = "ocid1.user.oc1..bbbbuser"
PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nMIIBVg\n-----END PRIVATE KEY-----\n"
FINGERPRINT = "aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99"


class TestOracleCloudApiKeyCredential(unittest.TestCase):

    def test_construction_succeeds(self):
        """
            Verifies a complete credential constructs successfully.
        """
        cred = OracleCloudApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
            user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
        )
        self.assertEqual(cred.tenancy_ocid, TENANCY_OCID)
        self.assertEqual(cred.user_ocid, USER_OCID)
        self.assertEqual(cred.private_key, PRIVATE_KEY)
        self.assertEqual(cred.fingerprint, FINGERPRINT)
        self.assertIsNone(cred.passphrase)

    def test_passphrase_defaults_to_none(self):
        """
            Verifies an omitted passphrase defaults to None.
        """
        cred = OracleCloudApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
            user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
        )
        self.assertIsNone(cred.passphrase)

    def test_missing_category_raises(self):
        """
            Verifies wrong category raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            OracleCloudApiKeyCredential(
                identifier=IDENTIFIER, categories=["basic"], tenancy_ocid=TENANCY_OCID,
                user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
            )

    def test_empty_private_key_raises(self):
        """
            Verifies an empty private key is rejected.
        """
        with self.assertRaises(ConfigurationError):
            OracleCloudApiKeyCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
                user_ocid=USER_OCID, private_key="", fingerprint=FINGERPRINT,
            )

    def test_empty_fingerprint_raises(self):
        """
            Verifies an empty fingerprint is rejected.
        """
        with self.assertRaises(ConfigurationError):
            OracleCloudApiKeyCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
                user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint="",
            )

    def test_bad_tenancy_ocid_prefix_raises(self):
        """
            Verifies a tenancy OCID without the required prefix is rejected.
        """
        with self.assertRaises(ConfigurationError):
            OracleCloudApiKeyCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid="ocid1.user.oc1..wrong",
                user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
            )

    def test_bad_user_ocid_prefix_raises(self):
        """
            Verifies a user OCID without the required prefix is rejected.
        """
        with self.assertRaises(ConfigurationError):
            OracleCloudApiKeyCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
                user_ocid="ocid1.tenancy.oc1..wrong", private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
            )

    def test_repr_redacts_key_material(self):
        """
            Verifies private key material never appears in the ``repr``.
        """
        cred = OracleCloudApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
            user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
            passphrase="topsecret",
        )
        rendered = repr(cred)
        self.assertIn("OracleCloudApiKeyCredential", rendered)
        self.assertNotIn(PRIVATE_KEY, rendered)
        self.assertNotIn("topsecret", rendered)
        self.assertIn("***", rendered)

    def test_repr_passphrase_none(self):
        """
            Verifies the ``repr`` shows None when there is no passphrase.
        """
        cred = OracleCloudApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
            user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
        )
        rendered = repr(cred)
        self.assertIn("passphrase=None", rendered)

    def test_validate_reports_each_missing_field(self):
        """
            Verifies ``validate`` reports each missing field.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = OracleCloudApiKeyCredential.validate(cred_info)
        self.assertTrue(any("missing 'tenancy_ocid'" in err for err in errors))
        self.assertTrue(any("missing 'user_ocid'" in err for err in errors))
        self.assertTrue(any("missing 'private_key'" in err for err in errors))
        self.assertTrue(any("missing 'fingerprint'" in err for err in errors))

    def test_validate_ok_does_not_report_errors(self):
        """
            Verifies ``validate`` reports no errors for a complete credential.
        """
        cred_info = {
            "identifier": IDENTIFIER, "categories": CATEGORIES, "tenancy_ocid": TENANCY_OCID,
            "user_ocid": USER_OCID, "private_key": PRIVATE_KEY, "fingerprint": FINGERPRINT,
        }
        errors, warnings = OracleCloudApiKeyCredential.validate(cred_info)
        self.assertEqual(errors, [])

    def test_category_membership_registered(self):
        """
            Verifies the per-provider category is registered under the cloud-venue umbrella.
        """
        cloud_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
        self.assertIn(CATEGORY_CLOUD_VENUE, cloud_members)

    def test_as_dict_roundtrips_passphrase_none(self):
        """
            Verifies ``as_dict`` carries a None passphrase.
        """
        cred = OracleCloudApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
            user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
        )
        data = cred.as_dict()
        self.assertIsNone(data["passphrase"])

    @given(
        identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        tenancy_suffix=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48),
        user_suffix=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48),
        private_key=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=128),
        fingerprint=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
        passphrase=st.one_of(st.none(), st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48)),
    )
    def test_oracle_credential_roundtrip(self, identifier, tenancy_suffix, user_suffix, private_key, fingerprint, passphrase):
        """
            Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
        """
        tenancy_ocid = OracleCloudApiKeyCredential.TENANCY_OCID_PREFIX + tenancy_suffix
        user_ocid = OracleCloudApiKeyCredential.USER_OCID_PREFIX + user_suffix
        cred = OracleCloudApiKeyCredential(
            identifier=identifier, categories=CATEGORIES, tenancy_ocid=tenancy_ocid,
            user_ocid=user_ocid, private_key=private_key, fingerprint=fingerprint,
            passphrase=passphrase,
        )
        data = cred.as_dict()
        rebuilt = OracleCloudApiKeyCredential(
            identifier=data["identifier"], categories=data["categories"], tenancy_ocid=data["tenancy_ocid"],
            user_ocid=data["user_ocid"], private_key=data["private_key"], fingerprint=data["fingerprint"],
            passphrase=data["passphrase"], role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)
