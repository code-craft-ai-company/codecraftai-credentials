"""
    Testbase tests for :class:`ProxmoxApiTokenCredential` covering
    construction, validation, redaction, serialization, category membership,
    and a property-based serialize/deserialize roundtrip.
"""

from hypothesis import given, strategies as st

from ccai.credentials.proxmoxapitokencredential import ProxmoxApiTokenCredential
from ccai.credentials.wellknown import CATEGORY_VM_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "proxmox-token"
CATEGORIES = ["vm-venue"]
TOKEN_ID = "root@pam!automation"
SECRET = "11111111-2222-3333-4444-555555555555"


def test_construction_succeeds() -> None:
    """
        Verifies a complete credential constructs successfully.
    """
    cred = ProxmoxApiTokenCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, token_id=TOKEN_ID, secret=SECRET,
    )
    assert cred.token_id == TOKEN_ID
    assert cred.secret == SECRET
    assert cred.identifier == IDENTIFIER
    assert cred.categories == CATEGORIES
    return


def test_missing_category_raises() -> None:
    """
        Verifies wrong category raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        ProxmoxApiTokenCredential(
            identifier=IDENTIFIER, categories=["basic"], token_id=TOKEN_ID, secret=SECRET,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_token_id_raises() -> None:
    """
        Verifies an empty token_id is rejected.
    """
    raised = False
    try:
        ProxmoxApiTokenCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token_id="", secret=SECRET,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_secret_raises() -> None:
    """
        Verifies an empty secret is rejected.
    """
    raised = False
    try:
        ProxmoxApiTokenCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token_id=TOKEN_ID, secret="",
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_malformed_token_id_raises() -> None:
    """
        Verifies a token_id that does not match the required form is rejected.
    """
    raised = False
    try:
        ProxmoxApiTokenCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token_id="root-pam-automation",
            secret=SECRET,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_repr_redacts_secret() -> None:
    """
        Verifies the secret never appears in the ``repr``.
    """
    cred = ProxmoxApiTokenCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, token_id=TOKEN_ID, secret=SECRET,
    )
    rendered = repr(cred)
    assert "ProxmoxApiTokenCredential" in rendered
    assert SECRET not in rendered
    assert "***" in rendered
    return


def test_validate_reports_missing_fields() -> None:
    """
        Verifies ``validate`` reports missing token_id and secret fields.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = ProxmoxApiTokenCredential.validate(cred_info)
    assert any("missing 'token_id'" in err for err in errors)
    assert any("missing 'secret'" in err for err in errors)
    return


def test_validate_ok_does_not_report_errors() -> None:
    """
        Verifies ``validate`` reports no errors for a complete credential.
    """
    cred_info = {
        "identifier": IDENTIFIER, "categories": CATEGORIES,
        "token_id": TOKEN_ID, "secret": SECRET,
    }
    errors, warnings = ProxmoxApiTokenCredential.validate(cred_info)
    assert errors == []
    return


def test_as_dict_content() -> None:
    """
        Verifies ``as_dict`` carries all credential fields.
    """
    cred = ProxmoxApiTokenCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, token_id=TOKEN_ID, secret=SECRET,
    )
    data = cred.as_dict()
    assert data["identifier"] == IDENTIFIER
    assert data["categories"] == CATEGORIES
    assert data["token_id"] == TOKEN_ID
    assert data["secret"] == SECRET
    assert data["role"] == "priv"
    return


def test_category_membership_registered() -> None:
    """
        Verifies the per-provider category is registered under the vm-venue umbrella.
    """
    members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_VM_VENUE]
    assert CATEGORY_VM_VENUE in members
    return


@given(
    identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    user=st.text(alphabet=st.characters(min_codepoint=97, max_codepoint=122), min_size=1, max_size=16),
    realm=st.text(alphabet=st.characters(min_codepoint=97, max_codepoint=122), min_size=1, max_size=16),
    tokenname=st.text(alphabet=st.characters(min_codepoint=97, max_codepoint=122), min_size=1, max_size=16),
    secret=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
)
def test_proxmox_credential_roundtrip(
    identifier: str, user: str, realm: str, tokenname: str, secret: str,
) -> None:
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
    assert rebuilt.as_dict() == data
    return
