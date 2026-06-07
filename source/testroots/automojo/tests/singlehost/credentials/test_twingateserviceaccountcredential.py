"""
    Testbase tests for :class:`TwingateServiceAccountCredential`.

    Converted from the legacy ``unittest`` module during the Phase 7
    ``unittest`` -> ``testbase`` shift. Each original ``TestCase`` method is
    preserved one-to-one as a module-level ``test_*`` function with identical
    assertion behaviour.
"""

from hypothesis import given, strategies as st

from automojo.credentials.twingateserviceaccountcredential import TwingateServiceAccountCredential
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "tg-prod"
CATEGORIES = ["twingate-service-account"]
API_TOKEN = "tg-svc-XXXX"
NETWORK_SLUG = "acme"


def test_construction_succeeds() -> None:
    """
        Verifies a complete credential constructs successfully.
    """
    cred = TwingateServiceAccountCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        api_token=API_TOKEN, network_slug=NETWORK_SLUG,
    )
    assert cred.api_token == API_TOKEN
    assert cred.network_slug == NETWORK_SLUG
    return


def test_missing_category_raises() -> None:
    """
        Verifies wrong category raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        TwingateServiceAccountCredential(
            identifier=IDENTIFIER, categories=["basic"],
            api_token=API_TOKEN, network_slug=NETWORK_SLUG,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_api_token_raises() -> None:
    """
        Verifies an empty API token is rejected.
    """
    raised = False
    try:
        TwingateServiceAccountCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            api_token="", network_slug=NETWORK_SLUG,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_network_slug_raises() -> None:
    """
        Verifies an empty network slug is rejected.
    """
    raised = False
    try:
        TwingateServiceAccountCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            api_token=API_TOKEN, network_slug="",
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_network_slug_with_whitespace_raises() -> None:
    """
        Verifies a whitespace-containing slug is rejected.
    """
    raised = False
    try:
        TwingateServiceAccountCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            api_token=API_TOKEN, network_slug="bad slug",
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_repr_redacts_token() -> None:
    """
        Verifies the API token value never appears in the ``repr``.
    """
    cred = TwingateServiceAccountCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        api_token=API_TOKEN, network_slug=NETWORK_SLUG,
    )
    rendered = repr(cred)
    assert "TwingateServiceAccountCredential" in rendered
    assert IDENTIFIER in rendered
    assert NETWORK_SLUG in rendered
    assert API_TOKEN not in rendered
    assert "***" in rendered
    return


def test_validate_reports_each_failure() -> None:
    """
        Verifies ``validate`` reports each failure with a descriptive message.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "network_slug": "bad slug"}
    errors, warnings = TwingateServiceAccountCredential.validate(cred_info)
    assert any("missing 'api_token'" in err for err in errors)
    assert any("whitespace" in err for err in errors)
    return


def test_validate_ok_does_not_report_errors() -> None:
    """
        Verifies ``validate`` reports no errors for a complete credential.
    """
    cred_info = {
        "identifier": IDENTIFIER, "categories": CATEGORIES,
        "api_token": API_TOKEN, "network_slug": NETWORK_SLUG,
    }
    errors, warnings = TwingateServiceAccountCredential.validate(cred_info)
    assert errors == []
    return


@given(
    identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    api_token=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
    network_slug=st.text(alphabet=st.characters(whitelist_categories=("Ll", "Lu", "Nd"), whitelist_characters="-_"), min_size=1, max_size=32),
)
def test_serialize_roundtrip(identifier: str, api_token: str, network_slug: str) -> None:
    """
        Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
    """
    cred = TwingateServiceAccountCredential(
        identifier=identifier, categories=CATEGORIES,
        api_token=api_token, network_slug=network_slug,
    )
    data = cred.as_dict()
    rebuilt = TwingateServiceAccountCredential(
        identifier=data["identifier"], categories=data["categories"],
        api_token=data["api_token"], network_slug=data["network_slug"],
        role=data["role"],
    )
    assert rebuilt.as_dict() == data
    return
