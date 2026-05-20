import unittest

from hypothesis import given, strategies as st

from automojo.credentials.tailscaleauthkeycredential import TailscaleAuthKeyCredential
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "ts-lab-key"
CATEGORIES = ["tailscale-authkey"]
AUTHKEY = "tskey-auth-AAAA-BBBB"


class TestTailscaleAuthKeyCredential(unittest.TestCase):

    def test_construction_succeeds(self):
        """
            Verifies a complete credential constructs successfully.
        """
        cred = TailscaleAuthKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, authkey=AUTHKEY,
            reusable=False, ephemeral=True, preauthorized=True,
        )
        self.assertEqual(cred.identifier, IDENTIFIER)
        self.assertEqual(cred.authkey, AUTHKEY)
        self.assertFalse(cred.reusable)
        self.assertTrue(cred.ephemeral)
        self.assertTrue(cred.preauthorized)

    def test_missing_category_raises(self):
        """
            Verifies wrong category raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            TailscaleAuthKeyCredential(identifier=IDENTIFIER, categories=["basic"], authkey=AUTHKEY)

    def test_empty_authkey_raises(self):
        """
            Verifies an empty authkey is rejected.
        """
        with self.assertRaises(ConfigurationError):
            TailscaleAuthKeyCredential(identifier=IDENTIFIER, categories=CATEGORIES, authkey="")

    def test_default_role_is_priv(self):
        """
            Confirms the default role is ``priv``.
        """
        cred = TailscaleAuthKeyCredential(identifier=IDENTIFIER, categories=CATEGORIES, authkey=AUTHKEY)
        self.assertEqual(cred.role, "priv")

    def test_categories_property_contains_tailscale_authkey(self):
        """
            Verifies the category membership is exposed on the instance.
        """
        cred = TailscaleAuthKeyCredential(identifier=IDENTIFIER, categories=CATEGORIES, authkey=AUTHKEY)
        self.assertIn("tailscale-authkey", cred.categories)

    def test_repr_redacts_secret(self):
        """
            Verifies the auth key value never appears in the ``repr``.
        """
        cred = TailscaleAuthKeyCredential(identifier=IDENTIFIER, categories=CATEGORIES, authkey=AUTHKEY)
        rendered = repr(cred)
        self.assertIn("TailscaleAuthKeyCredential", rendered)
        self.assertIn(IDENTIFIER, rendered)
        self.assertNotIn(AUTHKEY, rendered)
        self.assertIn("***", rendered)

    def test_validate_missing_authkey_reports_error(self):
        """
            Verifies ``validate`` reports a missing authkey.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = TailscaleAuthKeyCredential.validate(cred_info)
        self.assertTrue(any("missing 'authkey'" in err for err in errors))

    def test_validate_emits_production_warning(self):
        """
            Verifies ``validate`` always emits a warning recommending OAuth for production.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "authkey": AUTHKEY}
        errors, warnings = TailscaleAuthKeyCredential.validate(cred_info)
        self.assertEqual(errors, [])
        self.assertTrue(any("TailscaleOAuthCredential" in warn for warn in warnings))

    def test_as_dict_contains_fields(self):
        """
            Verifies ``as_dict`` round-trips all stored fields.
        """
        cred = TailscaleAuthKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, authkey=AUTHKEY,
            reusable=True, ephemeral=False, preauthorized=False,
        )
        data = cred.as_dict()
        self.assertEqual(data["identifier"], IDENTIFIER)
        self.assertEqual(data["categories"], CATEGORIES)
        self.assertEqual(data["authkey"], AUTHKEY)
        self.assertTrue(data["reusable"])
        self.assertFalse(data["ephemeral"])
        self.assertFalse(data["preauthorized"])

    @given(
        identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        authkey=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
        reusable=st.booleans(),
        ephemeral=st.booleans(),
        preauthorized=st.booleans(),
    )
    def test_serialize_roundtrip(self, identifier, authkey, reusable, ephemeral, preauthorized):
        """
            Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
        """
        cred = TailscaleAuthKeyCredential(
            identifier=identifier, categories=CATEGORIES, authkey=authkey,
            reusable=reusable, ephemeral=ephemeral, preauthorized=preauthorized,
        )
        data = cred.as_dict()
        rebuilt = TailscaleAuthKeyCredential(
            identifier=data["identifier"], categories=data["categories"], authkey=data["authkey"],
            reusable=data["reusable"], ephemeral=data["ephemeral"], preauthorized=data["preauthorized"],
            role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)
