"""
    Hypothesis property tests for :class:`VSphereCredential`.

    Converted from the legacy ``unittest`` module
    ``ccai_tests.credentials.test_vsphere_credentials_properties`` during
    the Phase 7 unittest->testbase shift. The former ``TestCase`` method is
    preserved one-to-one as a module-level ``test_*`` function with identical
    logic and assertions.
"""

from ccai.testbase.properties import given
from ccai.testbase.properties import strategies as st

from ccai.credentials.vspherecredential import VSphereCredential


CATEGORIES = ["vm-venue", "vsphere-basic"]

_PRINTABLE = st.text(
    alphabet=st.characters(min_codepoint=33, max_codepoint=126),
    min_size=1, max_size=64,
)


@given(
    identifier=_PRINTABLE,
    username=_PRINTABLE,
    secrets=st.one_of(
        st.tuples(_PRINTABLE, st.none()),
        st.tuples(st.none(), _PRINTABLE),
        st.tuples(_PRINTABLE, _PRINTABLE),
    ),
)
def test_vsphere_credential_roundtrip(identifier, username, secrets) -> None:
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

    assert rebuilt.as_dict() == data
    assert rebuilt.username == cred.username
    assert rebuilt.password == cred.password
    assert rebuilt.sso_token == cred.sso_token
    return
