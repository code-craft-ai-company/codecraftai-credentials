import unittest

from ccai.testbase.properties import given
from ccai.testbase.properties import strategies as st

from ccai.credentials.nutanixprismcredential import NutanixPrismCredential
from ccai.credentials.wellknown import CATEGORY_VM_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "nutanix-prism"
CATEGORIES = ["vm-venue"]
USERNAME = "admin"
PASSWORD = "supersecret"
ENDPOINT = "https://prism.example.com:9440"


class TestNutanixPrismCredential(unittest.TestCase):

    def test_construction_https_succeeds(self):
        """
            Verifies a credential constructs successfully with an https endpoint.
        """
        cred = NutanixPrismCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME,
            password=PASSWORD, endpoint=ENDPOINT,
        )
        self.assertEqual(cred.username, USERNAME)
        self.assertEqual(cred.password, PASSWORD)
        self.assertEqual(cred.endpoint, ENDPOINT)

    def test_construction_http_succeeds(self):
        """
            Verifies a credential constructs successfully with an http endpoint.
        """
        cred = NutanixPrismCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME,
            password=PASSWORD, endpoint="http://prism.example.com:9440",
        )
        self.assertEqual(cred.endpoint, "http://prism.example.com:9440")

    def test_missing_category_raises(self):
        """
            Verifies wrong category raises :class:`ConfigurationError`.
        """
        with self.assertRaises(ConfigurationError):
            NutanixPrismCredential(
                identifier=IDENTIFIER, categories=["basic"], username=USERNAME,
                password=PASSWORD, endpoint=ENDPOINT,
            )

    def test_empty_username_raises(self):
        """
            Verifies an empty username is rejected.
        """
        with self.assertRaises(ConfigurationError):
            NutanixPrismCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, username="",
                password=PASSWORD, endpoint=ENDPOINT,
            )

    def test_empty_password_raises(self):
        """
            Verifies an empty password is rejected.
        """
        with self.assertRaises(ConfigurationError):
            NutanixPrismCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME,
                password="", endpoint=ENDPOINT,
            )

    def test_non_http_endpoint_raises(self):
        """
            Verifies a non-http(s) endpoint is rejected.
        """
        with self.assertRaises(ConfigurationError):
            NutanixPrismCredential(
                identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME,
                password=PASSWORD, endpoint="ftp://prism.example.com",
            )

    def test_repr_redacts_password(self):
        """
            Verifies the password never appears in the ``repr``.
        """
        cred = NutanixPrismCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME,
            password=PASSWORD, endpoint=ENDPOINT,
        )
        rendered = repr(cred)
        self.assertIn("NutanixPrismCredential", rendered)
        self.assertNotIn(PASSWORD, rendered)
        self.assertIn("***", rendered)

    def test_validate_reports_missing_fields(self):
        """
            Verifies ``validate`` reports missing username, password and endpoint fields.
        """
        cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
        errors, warnings = NutanixPrismCredential.validate(cred_info)
        self.assertTrue(any("missing 'username'" in err for err in errors))
        self.assertTrue(any("missing 'password'" in err for err in errors))
        self.assertTrue(any("missing 'endpoint'" in err for err in errors))

    def test_validate_ok_does_not_report_errors(self):
        """
            Verifies ``validate`` reports no errors for a complete credential.
        """
        cred_info = {
            "identifier": IDENTIFIER, "categories": CATEGORIES,
            "username": USERNAME, "password": PASSWORD, "endpoint": ENDPOINT,
        }
        errors, warnings = NutanixPrismCredential.validate(cred_info)
        self.assertEqual(errors, [])

    def test_as_dict_content(self):
        """
            Verifies ``as_dict`` carries all credential fields.
        """
        cred = NutanixPrismCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME,
            password=PASSWORD, endpoint=ENDPOINT,
        )
        data = cred.as_dict()
        self.assertEqual(data["identifier"], IDENTIFIER)
        self.assertEqual(data["categories"], CATEGORIES)
        self.assertEqual(data["username"], USERNAME)
        self.assertEqual(data["password"], PASSWORD)
        self.assertEqual(data["endpoint"], ENDPOINT)
        self.assertEqual(data["role"], "priv")

    def test_category_membership_registered(self):
        """
            Verifies the per-provider category is registered under the vm-venue umbrella.
        """
        members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_VM_VENUE]
        self.assertIn(CATEGORY_VM_VENUE, members)

    @given(
        identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        username=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
        password=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
        scheme=st.sampled_from(["http", "https"]),
        host=st.text(alphabet=st.characters(min_codepoint=97, max_codepoint=122), min_size=1, max_size=24),
        port=st.integers(min_value=1, max_value=65535),
    )
    def test_nutanix_credential_roundtrip(self, identifier, username, password, scheme, host, port):
        """
            Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
        """
        endpoint = "{}://{}:{}".format(scheme, host, port)
        cred = NutanixPrismCredential(
            identifier=identifier, categories=CATEGORIES, username=username,
            password=password, endpoint=endpoint,
        )
        data = cred.as_dict()
        rebuilt = NutanixPrismCredential(
            identifier=data["identifier"], categories=data["categories"],
            username=data["username"], password=data["password"],
            endpoint=data["endpoint"], role=data["role"],
        )
        self.assertEqual(rebuilt.as_dict(), data)


if __name__ == "__main__":
    unittest.main()
