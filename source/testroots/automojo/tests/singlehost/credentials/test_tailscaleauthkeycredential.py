"""
    Tests for :class:`automojo.credentials.tailscaleauthkeycredential.TailscaleAuthKeyCredential`.

    Converted from the original ``unittest.TestCase`` based module to the
    testbase module-level test-function format. Each test exercises construction
    validation, accessor behaviour, secret redaction in ``repr``, ``as_dict``
    serialization, the static ``validate`` helper, and a serialize/deserialize
    roundtrip property test for the Tailscale auth-key credential type.
"""

from hypothesis import given, strategies as st

from automojo.credentials.tailscaleauthkeycredential import TailscaleAuthKeyCredential
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "ts-lab-key"
CATEGORIES = ["tailscale-authkey"]
AUTHKEY = "tskey-auth-AAAA-BBBB"


def test_construction_succeeds() -> None:
    """
        Verifies a complete credential constructs successfully.
    """
    cred = TailscaleAuthKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, authkey=AUTHKEY,
        reusable=False, ephemeral=True, preauthorized=True,
    )
    assert cred.identifier == IDENTIFIER
    assert cred.authkey == AUTHKEY
    assert not cred.reusable
    assert cred.ephemeral
    assert cred.preauthorized
    return


def test_missing_category_raises() -> None:
    """
        Verifies wrong category raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        TailscaleAuthKeyCredential(identifier=IDENTIFIER, categories=["basic"], authkey=AUTHKEY)
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_authkey_raises() -> None:
    """
        Verifies an empty authkey is rejected.
    """
    raised = False
    try:
        TailscaleAuthKeyCredential(identifier=IDENTIFIER, categories=CATEGORIES, authkey="")
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_default_role_is_priv() -> None:
    """
        Confirms the default role is ``priv``.
    """
    cred = TailscaleAuthKeyCredential(identifier=IDENTIFIER, categories=CATEGORIES, authkey=AUTHKEY)
    assert cred.role == "priv"
    return


def test_categories_property_contains_tailscale_authkey() -> None:
    """
        Verifies the category membership is exposed on the instance.
    """
    cred = TailscaleAuthKeyCredential(identifier=IDENTIFIER, categories=CATEGORIES, authkey=AUTHKEY)
    assert "tailscale-authkey" in cred.categories
    return


def test_repr_redacts_secret() -> None:
    """
        Verifies the auth key value never appears in the ``repr``.
    """
    cred = TailscaleAuthKeyCredential(identifier=IDENTIFIER, categories=CATEGORIES, authkey=AUTHKEY)
    rendered = repr(cred)
    assert "TailscaleAuthKeyCredential" in rendered
    assert IDENTIFIER in rendered
    assert AUTHKEY not in rendered
    assert "***" in rendered
    return


def test_validate_missing_authkey_reports_error() -> None:
    """
        Verifies ``validate`` reports a missing authkey.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = TailscaleAuthKeyCredential.validate(cred_info)
    assert any("missing 'authkey'" in err for err in errors)
    return


def test_validate_emits_production_warning() -> None:
    """
        Verifies ``validate`` always emits a warning recommending OAuth for production.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "authkey": AUTHKEY}
    errors, warnings = TailscaleAuthKeyCredential.validate(cred_info)
    assert errors == []
    assert any("TailscaleOAuthCredential" in warn for warn in warnings)
    return


def test_as_dict_contains_fields() -> None:
    """
        Verifies ``as_dict`` round-trips all stored fields.
    """
    cred = TailscaleAuthKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, authkey=AUTHKEY,
        reusable=True, ephemeral=False, preauthorized=False,
    )
    data = cred.as_dict()
    assert data["identifier"] == IDENTIFIER
    assert data["categories"] == CATEGORIES
    assert data["authkey"] == AUTHKEY
    assert data["reusable"]
    assert not data["ephemeral"]
    assert not data["preauthorized"]
    return


@given(
    identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    authkey=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
    reusable=st.booleans(),
    ephemeral=st.booleans(),
    preauthorized=st.booleans(),
)
def test_serialize_roundtrip(identifier: str, authkey: str, reusable: bool, ephemeral: bool, preauthorized: bool) -> None:
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
    assert rebuilt.as_dict() == data
    return
