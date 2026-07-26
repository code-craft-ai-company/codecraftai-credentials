"""
    Testbase tests for :class:`CoreweaveApiCredential`.

    Verifies construction (with and without an organization_id), category and
    token validation, ``repr`` token redaction, ``validate`` reporting,
    ``as_dict`` content, well-known category membership registration, and a
    serialize/deserialize roundtrip property test.
"""

from ccai.testbase.properties import given
from ccai.testbase.properties import strategies as st

from ccai.credentials.coreweaveapicredential import CoreweaveApiCredential
from ccai.credentials.wellknown import CATEGORY_HPC_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "coreweave-token"
CATEGORIES = ["hpc-venue"]
TOKEN = "coreweave_abc123"
ORGANIZATION_ID = "org-12345"


def test_construction_without_organization_succeeds() -> None:
    """
        Verifies a credential constructs successfully without an organization_id.
    """
    cred = CoreweaveApiCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
    )
    assert cred.token == TOKEN
    assert cred.organization_id is None
    assert cred.identifier == IDENTIFIER
    assert cred.categories == CATEGORIES
    return


def test_construction_with_organization_succeeds() -> None:
    """
        Verifies a credential constructs successfully with an organization_id.
    """
    cred = CoreweaveApiCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
        organization_id=ORGANIZATION_ID,
    )
    assert cred.organization_id == ORGANIZATION_ID
    return


def test_missing_category_raises() -> None:
    """
        Verifies wrong category raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        CoreweaveApiCredential(
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
        CoreweaveApiCredential(
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
    cred = CoreweaveApiCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
        organization_id=ORGANIZATION_ID,
    )
    rendered = repr(cred)
    assert "CoreweaveApiCredential" in rendered
    assert TOKEN not in rendered
    assert "***" in rendered
    return


def test_validate_reports_missing_token() -> None:
    """
        Verifies ``validate`` reports a missing token field.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = CoreweaveApiCredential.validate(cred_info)
    assert any("missing 'token'" in err for err in errors)
    return


def test_validate_ok_does_not_report_errors() -> None:
    """
        Verifies ``validate`` reports no errors for a complete credential.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "token": TOKEN}
    errors, warnings = CoreweaveApiCredential.validate(cred_info)
    assert errors == []
    return


def test_as_dict_content_without_organization() -> None:
    """
        Verifies ``as_dict`` carries all credential fields with organization_id None.
    """
    cred = CoreweaveApiCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
    )
    data = cred.as_dict()
    assert data["identifier"] == IDENTIFIER
    assert data["categories"] == CATEGORIES
    assert data["token"] == TOKEN
    assert data["organization_id"] is None
    assert data["role"] == "priv"
    return


def test_as_dict_content_with_organization() -> None:
    """
        Verifies ``as_dict`` carries a non-empty organization_id.
    """
    cred = CoreweaveApiCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, token=TOKEN,
        organization_id=ORGANIZATION_ID,
    )
    data = cred.as_dict()
    assert data["organization_id"] == ORGANIZATION_ID
    return


def test_category_membership_registered() -> None:
    """
        Verifies the per-provider category is registered under the hpc-venue umbrella.
    """
    members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_HPC_VENUE]
    assert CATEGORY_HPC_VENUE in members
    return


@given(
    identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    token=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=128),
    organization_id=st.one_of(
        st.none(),
        st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
    ),
)
def test_coreweave_credential_roundtrip(identifier: str, token: str, organization_id: str) -> None:
    """
        Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
    """
    cred = CoreweaveApiCredential(
        identifier=identifier, categories=CATEGORIES, token=token,
        organization_id=organization_id,
    )
    data = cred.as_dict()
    rebuilt = CoreweaveApiCredential(
        identifier=data["identifier"], categories=data["categories"],
        token=data["token"], organization_id=data["organization_id"],
        role=data["role"],
    )
    assert rebuilt.as_dict() == data
    return
