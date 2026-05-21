import unittest

from hypothesis import given, strategies as st

from automojo.credentials.proxmoxapitokencredential import ProxmoxApiTokenCredential
from automojo.credentials.wellknown import CATEGORY_VM_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "proxmox-token"
CATEGORIES = ["vm-venue"]
TOKEN_ID = "root@pam!automation"
SECRET = "11111111-2222-3333-4444-555555555555"


class TestProxmoxApiTokenCredential(unittest.TestCase):

    def test_construction_succeeds(self):
        """
            Verifies a complete credential constructs successfully.
        """
        cred = ProxmoxApiTokenCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token_id=TOKEN_ID, secret=SECRET,
        )
        self.assertEqual(cred.token_id, TOKEN_ID)
        self.assertEqual(cred.secret, SECRET)
        self.assertEqual(cred.identifier, IDENTIFIER)
        self.assertEqual(cred.categories, CATEGORIES)

    def test_missing_category_raises(self):
        """
            Verifies wrong category raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            ProxmoxApiTokenCredential(
                identifier=IDENTIFIER, categories=["basic"], token_id=TOKEN_ID, secret=SECRET,
            )

    def test_empty_token_id_raises(self):
        """
            Verifies an empty token_id is rejected.
        """
        with self.assertRaises(ConfigurationError):
            ProxmoxApiTokenCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, token_id="", secret=SECRET,
            )

    def test_empty_secret_raises(self):
        """
            Verifies an empty secret is rejected.
        """
        with self.assertRaises(ConfigurationError):
            ProxmoxApiTokenCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, token_id=TOKEN_ID, secret="",
            )

    def test_malformed_token_id_raises(self):
        """
            Verifies a token_id that does not match the required form is rejected.
        """
        with self.assertRaises(ConfigurationError):
            ProxmoxApiTokenCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, token_id="root-pam-automation",
                secret=SECRET,
            )

    def test_repr_redacts_secret(self):
        """
            Verifies the secret never appears in the ``repr``.
        """
        cred = ProxmoxApiTokenCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token_id=TOKEN_ID, secret=SECRET,
        )
        rendered = repr(cred)
        self.assertIn("ProxmoxApiTokenCredential", rendered)
        self.assertNotIn(SECRET, rendered)
        self.assertIn("***", rendered)

    def test_validate_reports_missing_fields(self):
        """
            Verifies ``validate`` reports missing token_id and secret fields.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = ProxmoxApiTokenCredential.validate(cred_info)
        self.assertTrue(any("missing 'token_id'" in err for err in errors))
        self.assertTrue(any("missing 'secret'" in err for err in errors))

    def test_validate_ok_does_not_report_errors(self):
        """
            Verifies ``validate`` reports no errors for a complete credential.
        """
        cred_info = {
            "identifier": IDENTIFIER, "categories": CATEGORIES,
            "token_id": TOKEN_ID, "secret": SECRET,
        }
        errors, warnings = ProxmoxApiTokenCredential.validate(cred_info)
        self.assertEqual(errors, [])

    def test_as_dict_content(self):
        """
            Verifies ``as_dict`` carries all credential fields.
        """
        cred = ProxmoxApiTokenCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token_id=TOKEN_ID, secret=SECRET,
        )
        data = cred.as_dict()
        self.assertEqual(data["identifier"], IDENTIFIER)
        self.assertEqual(data["categories"], CATEGORIES)
        self.assertEqual(data["token_id"], TOKEN_ID)
        self.assertEqual(data["secret"], SECRET)
        self.assertEqual(data["role"], "priv")

    def test_category_membership_registered(self):
        """
            Verifies the per-provider category is registered under the vm-venue umbrella.
        """
        members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_VM_VENUE]
        self.assertIn(CATEGORY_VM_VENUE, members)

    @given(
        identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        user=st.text(alphabet=st.characters(min_codepoint=97, max_codepoint=122), min_size=1, max_size=16),
        realm=st.text(alphabet=st.characters(min_codepoint=97, max_codepoint=122), min_size=1, max_size=16),
        tokenname=st.text(alphabet=st.characters(min_codepoint=97, max_codepoint=122), min_size=1, max_size=16),
        secret=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
    )
    def test_proxmox_credential_roundtrip(self, identifier, user, realm, tokenname, secret):
        """
            Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
        """
        token_id = "{}@{}!{}".format(user, realm, tokenname)
        cred = ProxmoxApiTokenCredential(
            identifier=identifier, categories=CATEGORIES, token_id=token_id, secret=secret,
        )
        data = cred.as_dict()
        rebuilt = ProxmoxApiTokenCredential(
            identifier=data["identifier"], categories=data["categories"],
            token_id=data["token_id"], secret=data["secret"], role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)


if __name__ == "__main__":
    unittest.main()
