"""
    Hypothesis property tests for :class:`VSphereCredential`.
"""

import unittest

from ccai.testbase.properties import given
from ccai.testbase.properties import strategies as st

from ccai.credentials.vspherecredential import VSphereCredential


CATEGORIES = ["vm-venue", "vsphere-basic"]

_PRINTABLE = st.text(
    alphabet=st.characters(min_codepoint=33, max_codepoint=126),
    min_size=1, max_size=64,
)


class TestVSphereCredentialProperties(unittest.TestCase):

    @given(
        identifier=_PRINTABLE,
        username=_PRINTABLE,
        secrets=st.one_of(
            st.tuples(_PRINTABLE, st.none()),
            st.tuples(st.none(), _PRINTABLE),
            st.tuples(_PRINTABLE, _PRINTABLE),
        ),
    )
    def test_vsphere_credential_roundtrip(self, identifier, username, secrets):
        """
            Property test: serialise -> reconstruct -> equal across arbitrary
            valid inputs, exercising password-only, sso-token-only, and
            both-field states.
        """
        password, sso_token = secrets

        cred = VSphereCredential(
            identifier=identifier, categories=CATEGORIES,
            username=username, password=password, sso_token=sso_token,
        )
        data = cred.as_dict()

        rebuilt = VSphereCredential(
            identifier=data["identifier"], categories=data["categories"],
            username=data["username"], password=data["password"],
            sso_token=data["sso_token"], role=data["role"],
        )

        self.assertEqual(rebuilt.as_dict(), data)
        self.assertEqual(rebuilt.username, cred.username)
        self.assertEqual(rebuilt.password, cred.password)
        self.assertEqual(rebuilt.sso_token, cred.sso_token)


if __name__ == "__main__":
    unittest.main()
