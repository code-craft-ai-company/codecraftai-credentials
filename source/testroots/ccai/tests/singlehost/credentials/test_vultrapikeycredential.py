"""
    Testbase tests for :class:`VultrApiKeyCredential`.

    Converted from the legacy ``unittest`` module to the testbase
    module-level ``test_*`` function format as part of the Phase 7
    unittest->testbase shift. Behaviour is preserved one-to-one with the
    original test methods.
"""

from hypothesis import given, strategies as st

from ccai.credentials.vultrapikeycredential import VultrApiKeyCredential
from ccai.credentials.wellknown import CATEGORY_CLOUD_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "vultr-key"
CATEGORIES = ["cloud-venue"]
TOKEN = "vultr_abc123"


def test_construction_succeeds() -> None:
    """
        Verifies a complete credential constructs successfully.
    """
    cred = VultrApiKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
    )
    assert cred.token == TOKEN
    assert cred.identifier == IDENTIFIER
    assert cred.categories == CATEGORIES
    return


def test_missing_category_raises() -> None:
    """
        Verifies wrong category raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        VultrApiKeyCredential(
            identifier=IDENTIFIER, categories=["basic"], token=TOKEN,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_token_raises() -> None:
    """
        Verifies an empty token is rejected.
    """
    raised = False
    try:
        VultrApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, token="",
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_repr_redacts_token() -> None:
    """
        Verifies the token never appears in the ``repr``.
    """
    cred = VultrApiKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
    )
    rendered = repr(cred)
    assert "VultrApiKeyCredential" in rendered
    assert TOKEN not in rendered
    assert "***" in rendered
    return


def test_validate_reports_missing_token() -> None:
    """
        Verifies ``validate`` reports a missing token field.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = VultrApiKeyCredential.validate(cred_info)
    assert any("missing 'token'" in err for err in errors)
    return


def test_validate_ok_does_not_report_errors() -> None:
    """
        Verifies ``validate`` reports no errors for a complete credential.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "token": TOKEN}
    errors, warnings = VultrApiKeyCredential.validate(cred_info)
    assert errors == []
    return


def test_as_dict_content() -> None:
    """
        Verifies ``as_dict`` carries all credential fields.
    """
    cred = VultrApiKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
    )
    data = cred.as_dict()
    assert data["identifier"] == IDENTIFIER
    assert data["categories"] == CATEGORIES
    assert data["token"] == TOKEN
    assert data["role"] == "priv"
    return


def test_category_membership_registered() -> None:
    """
        Verifies the per-provider category is registered under the cloud-venue umbrella.
    """
    members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
    assert CATEGORY_CLOUD_VENUE in members
    return


@given(
    identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    token=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=128),
)
def test_vultr_token_roundtrip(identifier: str, token: str) -> None:
    """
        Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
    """
    cred = VultrApiKeyCredential(
        identifier=identifier, categories=CATEGORIES, token=token,
    )
    data = cred.as_dict()
    rebuilt = VultrApiKeyCredential(
        identifier=data["identifier"], categories=data["categories"],
        token=data["token"], role=data["role"],
    )
    assert rebuilt.as_dict() == data
    return
