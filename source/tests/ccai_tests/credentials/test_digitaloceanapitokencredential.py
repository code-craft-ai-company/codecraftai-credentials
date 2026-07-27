import unittest

from hypothesis import given, strategies as st

from ccai.credentials.digitaloceanapitokencredential import DigitalOceanApiTokenCredential
from ccai.credentials.wellknown import CATEGORY_CLOUD_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "digitalocean-token"
CATEGORIES = ["cloud-venue"]
TOKEN = "dop_v1_abc123"
SPACES_KEY = "DO00EXAMPLEACCESSKEY"
SPACES_SECRET = "example-spaces-secret-value"


class TestDigitalOceanApiTokenCredential(unittest.TestCase):

    def test_construction_succeeds(self):
        """
            Verifies a complete credential constructs successfully.
        """
        cred = DigitalOceanApiTokenCredential(
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
            DigitalOceanApiTokenCredential(
                identifier=IDENTIFIER, categories=["basic"], token=TOKEN,
            )

    def test_empty_token_raises(self):
        """
            Verifies an empty token is rejected.
        """
        with self.assertRaises(ConfigurationError):
            DigitalOceanApiTokenCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, token="",
            )

    def test_repr_redacts_token(self):
        """
            Verifies the token never appears in the ``repr``.
        """
        cred = DigitalOceanApiTokenCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
        )
        rendered = repr(cred)
        self.assertIn("DigitalOceanApiTokenCredential", rendered)
        self.assertNotIn(TOKEN, rendered)
        self.assertIn("***", rendered)

    def test_validate_reports_missing_token(self):
        """
            Verifies ``validate`` reports a missing token field.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = DigitalOceanApiTokenCredential.validate(cred_info)
        self.assertTrue(any("missing 'token'" in err for err in errors))

    def test_validate_ok_does_not_report_errors(self):
        """
            Verifies ``validate`` reports no errors for a complete credential.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "token": TOKEN}
        errors, warnings = DigitalOceanApiTokenCredential.validate(cred_info)
        self.assertEqual(errors, [])

    def test_as_dict_content(self):
        """
            Verifies ``as_dict`` carries all credential fields.
        """
        cred = DigitalOceanApiTokenCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
        )
        data = cred.as_dict()
        self.assertEqual(data["identifier"], IDENTIFIER)
        self.assertEqual(data["categories"], CATEGORIES)
        self.assertEqual(data["token"], TOKEN)
        self.assertEqual(data["role"], "priv")

    def test_spaces_keys_default_to_absent(self):
        """
            Verifies a credential without Spaces keys reports them as None.

            A credential that never touches buckets does not need them, so
            absence must be representable rather than an error.
        """
        cred = DigitalOceanApiTokenCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
        )
        self.assertIsNone(cred.spaces_access_key)
        self.assertIsNone(cred.spaces_secret_key)

    def test_spaces_keys_are_carried(self):
        """
            Verifies the S3-compatible Spaces key pair is carried.

            Spaces is authenticated with its own access-key pair; the
            personal-access token has no authority there.
        """
        cred = DigitalOceanApiTokenCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
            spaces_access_key=SPACES_KEY, spaces_secret_key=SPACES_SECRET,
        )
        self.assertEqual(cred.spaces_access_key, SPACES_KEY)
        self.assertEqual(cred.spaces_secret_key, SPACES_SECRET)

    def test_half_a_spaces_key_pair_raises(self):
        """
            Verifies half a Spaces key pair is refused at construction.

            Half a pair cannot authenticate a bucket operation, and accepting
            it would defer the failure to the first bucket call.
        """
        with self.assertRaises(ConfigurationError):
            DigitalOceanApiTokenCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
                spaces_access_key=SPACES_KEY,
            )
        with self.assertRaises(ConfigurationError):
            DigitalOceanApiTokenCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
                spaces_secret_key=SPACES_SECRET,
            )

    def test_validate_reports_half_a_spaces_key_pair(self):
        """
            Verifies ``validate`` reports an unpaired Spaces key.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES,
                     "token": TOKEN, "spaces_access_key": SPACES_KEY}
        errors, warnings = DigitalOceanApiTokenCredential.validate(cred_info)
        self.assertTrue(any("must be supplied as a pair" in err
                            for err in errors))

    def test_validate_accepts_a_complete_spaces_key_pair(self):
        """
            Verifies ``validate`` accepts a complete Spaces key pair.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES,
                     "token": TOKEN, "spaces_access_key": SPACES_KEY,
                     "spaces_secret_key": SPACES_SECRET}
        errors, warnings = DigitalOceanApiTokenCredential.validate(cred_info)
        self.assertEqual(errors, [])

    def test_as_dict_omits_absent_spaces_keys(self):
        """
            Verifies ``as_dict`` omits Spaces keys the credential does not carry.
        """
        cred = DigitalOceanApiTokenCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
        )
        data = cred.as_dict()
        self.assertNotIn("spaces_access_key", data)
        self.assertNotIn("spaces_secret_key", data)

    def test_as_dict_carries_spaces_keys(self):
        """
            Verifies ``as_dict`` round-trips the Spaces key pair.
        """
        cred = DigitalOceanApiTokenCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
            spaces_access_key=SPACES_KEY, spaces_secret_key=SPACES_SECRET,
        )
        data = cred.as_dict()
        self.assertEqual(data["spaces_access_key"], SPACES_KEY)
        self.assertEqual(data["spaces_secret_key"], SPACES_SECRET)

    def test_repr_redacts_spaces_keys(self):
        """
            Verifies the Spaces secret never appears in the ``repr``.
        """
        cred = DigitalOceanApiTokenCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
            spaces_access_key=SPACES_KEY, spaces_secret_key=SPACES_SECRET,
        )
        rendered = repr(cred)
        self.assertNotIn(SPACES_KEY, rendered)
        self.assertNotIn(SPACES_SECRET, rendered)

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
    def test_digitalocean_token_roundtrip(self, identifier, token):
        """
            Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
        """
        cred = DigitalOceanApiTokenCredential(
            identifier=identifier, categories=CATEGORIES, token=token,
        )
        data = cred.as_dict()
        rebuilt = DigitalOceanApiTokenCredential(
            identifier=data["identifier"], categories=data["categories"],
            token=data["token"], role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)


if __name__ == "__main__":
    unittest.main()
