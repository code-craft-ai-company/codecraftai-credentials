"""
    Testbase tests for :class:`LambdalabsApiKeyCredential`.

    Converted from the legacy ``unittest`` module
    ``automojo_tests.credentials.test_lambdalabsapikeycredential`` as part of the
    Phase 7 unittest -> testbase shift. Each former ``TestCase`` method is now a
    module-level ``test_*`` function with identical assertion behaviour.
"""

from hypothesis import given, strategies as st

from automojo.credentials.lambdalabsapikeycredential import LambdalabsApiKeyCredential
from automojo.credentials.wellknown import CATEGORY_HPC_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "lambdalabs-key"
CATEGORIES = ["hpc-venue"]
TOKEN = "secret_lambdalabs_abc123"


def test_construction_succeeds() -> None:
    """
        Verifies a complete credential constructs successfully.
    """
    cred = LambdalabsApiKeyCredential(
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
        LambdalabsApiKeyCredential(
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
        LambdalabsApiKeyCredential(
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
    cred = LambdalabsApiKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
    )
    rendered = repr(cred)
    assert "LambdalabsApiKeyCredential" in rendered
    assert TOKEN not in rendered
    assert "***" in rendered
    return


def test_validate_reports_missing_token() -> None:
    """
        Verifies ``validate`` reports a missing token field.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = LambdalabsApiKeyCredential.validate(cred_info)
    assert any("missing 'token'" in err for err in errors)
    return


def test_validate_ok_does_not_report_errors() -> None:
    """
        Verifies ``validate`` reports no errors for a complete credential.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "token": TOKEN}
    errors, warnings = LambdalabsApiKeyCredential.validate(cred_info)
    assert errors == []
    return


def test_as_dict_content() -> None:
    """
        Verifies ``as_dict`` carries all credential fields.
    """
    cred = LambdalabsApiKeyCredential(
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
        Verifies the per-provider category is registered under the hpc-venue umbrella.
    """
    hpc_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_HPC_VENUE]
    assert CATEGORY_HPC_VENUE in hpc_members
    return


@given(
    identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    token=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=128),
)
def test_lambdalabs_token_roundtrip(identifier, token) -> None:
    """
        Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
    """
    cred = LambdalabsApiKeyCredential(
        identifier=identifier, categories=CATEGORIES, token=token,
    )
    data = cred.as_dict()
    rebuilt = LambdalabsApiKeyCredential(
        identifier=data["identifier"], categories=data["categories"],
        token=data["token"], role=data["role"],
    )
    assert rebuilt.as_dict() == data
    return
