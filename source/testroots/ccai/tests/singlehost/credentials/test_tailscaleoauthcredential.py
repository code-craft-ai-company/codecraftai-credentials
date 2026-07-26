"""
    Tests for :class:`ccai.credentials.tailscaleoauthcredential.TailscaleOAuthCredential`.

    Converted from the original ``unittest.TestCase`` based module to the
    testbase module-level test-function format. Each test exercises construction
    validation, the secret-redacting ``repr``, ``as_dict`` serialization, and the
    static ``validate`` helper of the Tailscale OAuth credential type. A
    hypothesis property test verifies serialize/deserialize round-trip identity.
"""

from ccai.testbase.properties import given
from ccai.testbase.properties import strategies as st

from ccai.credentials.tailscaleoauthcredential import TailscaleOAuthCredential
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "ts-prov-oauth"
CATEGORIES = ["tailscale-oauth"]
CLIENT_ID = "ksXXXX"
CLIENT_SECRET = "tskey-client-secret-XXXX"


def test_construction_succeeds() -> None:
    """
        Verifies a complete credential constructs successfully.
    """
    cred = TailscaleOAuthCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
        default_tags=["tag:lab"],
    )
    assert cred.client_id == CLIENT_ID
    assert cred.client_secret == CLIENT_SECRET
    assert cred.default_tags == ["tag:lab"]
    return


def test_missing_category_raises() -> None:
    """
        Verifies wrong category raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        TailscaleOAuthCredential(
            identifier=IDENTIFIER, categories=["basic"],
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_client_id_raises() -> None:
    """
        Verifies an empty client id is rejected.
    """
    raised = False
    try:
        TailscaleOAuthCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            client_id="", client_secret=CLIENT_SECRET,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_client_secret_raises() -> None:
    """
        Verifies an empty client secret is rejected.
    """
    raised = False
    try:
        TailscaleOAuthCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            client_id=CLIENT_ID, client_secret="",
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_default_tags_optional_defaults_to_empty_list() -> None:
    """
        Verifies ``default_tags`` defaults to an empty list when not provided.
    """
    cred = TailscaleOAuthCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    )
    assert cred.default_tags == []
    return


def test_repr_redacts_client_secret() -> None:
    """
        Verifies the client secret value never appears in the ``repr``.
    """
    cred = TailscaleOAuthCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    )
    rendered = repr(cred)
    assert "TailscaleOAuthCredential" in rendered
    assert IDENTIFIER in rendered
    assert CLIENT_ID in rendered
    assert CLIENT_SECRET not in rendered
    assert "***" in rendered
    return


def test_validate_missing_fields_reports_errors() -> None:
    """
        Verifies ``validate`` reports missing client id and client secret.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = TailscaleOAuthCredential.validate(cred_info)
    assert any("missing 'client_id'" in err for err in errors)
    assert any("missing 'client_secret'" in err for err in errors)
    return


def test_validate_ok_does_not_report_errors() -> None:
    """
        Verifies ``validate`` reports no errors for a complete credential.
    """
    cred_info = {
        "identifier": IDENTIFIER, "categories": CATEGORIES,
        "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
    }
    errors, warnings = TailscaleOAuthCredential.validate(cred_info)
    assert errors == []
    return


@given(
    identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    client_id=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    client_secret=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
    default_tags=st.lists(st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=16), max_size=5),
)
def test_serialize_roundtrip(identifier, client_id, client_secret, default_tags) -> None:
    """
        Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
    """
    cred = TailscaleOAuthCredential(
        identifier=identifier, categories=CATEGORIES,
        client_id=client_id, client_secret=client_secret, default_tags=default_tags,
    )
    data = cred.as_dict()
    rebuilt = TailscaleOAuthCredential(
        identifier=data["identifier"], categories=data["categories"],
        client_id=data["client_id"], client_secret=data["client_secret"],
        default_tags=data["default_tags"], role=data["role"],
    )
    assert rebuilt.as_dict() == data
    return
