"""
    Testbase tests for :class:`AzureManagedIdentityCredential`.

    Converted from the legacy ``unittest`` module to the testbase
    module-level function format as part of the Phase 7 unittest->testbase
    shift. Behaviour is preserved 1:1 with the original test methods.
"""

from ccai.testbase.properties import assume, given
from ccai.testbase.properties import strategies as st

from ccai.credentials.azuremanagedidentitycredential import AzureManagedIdentityCredential
from ccai.credentials.wellknown import CATEGORY_CLOUD_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "azure-mi"
CATEGORIES = ["cloud-venue"]
CLIENT_ID = "33333333-3333-3333-3333-333333333333"
RESOURCE_ID = "/subscriptions/abc/resourcegroups/rg/providers/Microsoft.ManagedIdentity/userAssignedIdentities/mi"


def test_construction_with_client_id_succeeds() -> None:
    """
        Verifies construction with only a client id succeeds.
    """
    cred = AzureManagedIdentityCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, client_id=CLIENT_ID,
    )
    assert cred.client_id == CLIENT_ID
    assert cred.resource_id is None
    return


def test_construction_with_resource_id_succeeds() -> None:
    """
        Verifies construction with only a resource id succeeds.
    """
    cred = AzureManagedIdentityCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, resource_id=RESOURCE_ID,
    )
    assert cred.client_id is None
    assert cred.resource_id == RESOURCE_ID
    return


def test_construction_with_both_selectors_succeeds() -> None:
    """
        Verifies construction with both selectors succeeds.
    """
    cred = AzureManagedIdentityCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, client_id=CLIENT_ID, resource_id=RESOURCE_ID,
    )
    assert cred.client_id == CLIENT_ID
    assert cred.resource_id == RESOURCE_ID
    return


def test_missing_category_raises() -> None:
    """
        Verifies wrong category raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        AzureManagedIdentityCredential(
            identifier=IDENTIFIER, categories=["basic"], client_id=CLIENT_ID,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_both_selectors_none_raises() -> None:
    """
        Verifies omitting both selectors raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        AzureManagedIdentityCredential(identifier=IDENTIFIER, categories=CATEGORIES)
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_repr_contains_identifier() -> None:
    """
        Verifies the ``repr`` includes the identifier and class name.
    """
    cred = AzureManagedIdentityCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, client_id=CLIENT_ID,
    )
    rendered = repr(cred)
    assert "AzureManagedIdentityCredential" in rendered
    assert IDENTIFIER in rendered
    return


def test_validate_missing_both_reports_error() -> None:
    """
        Verifies ``validate`` reports an error when both selectors are missing.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = AzureManagedIdentityCredential.validate(cred_info)
    assert any("at least one of 'client_id' or 'resource_id'" in err for err in errors)
    return


def test_validate_ok_does_not_report_errors() -> None:
    """
        Verifies ``validate`` reports no errors when a selector is present.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES, "client_id": CLIENT_ID}
    errors, warnings = AzureManagedIdentityCredential.validate(cred_info)
    assert errors == []
    assert warnings == []
    return


def test_category_membership_registered() -> None:
    """
        Verifies the per-provider category is registered under the cloud-venue umbrella.
    """
    cloud_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
    assert CATEGORY_CLOUD_VENUE in cloud_members
    return


def test_as_dict_contains_fields() -> None:
    """
        Verifies ``as_dict`` contains both selectors and base fields.
    """
    cred = AzureManagedIdentityCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, client_id=CLIENT_ID,
    )
    data = cred.as_dict()
    assert data["identifier"] == IDENTIFIER
    assert data["client_id"] == CLIENT_ID
    assert data["resource_id"] is None
    return


@given(
    identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    client_id=st.one_of(st.none(), st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48)),
    resource_id=st.one_of(st.none(), st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=80)),
)
def test_managed_identity_roundtrip(identifier: str, client_id: str, resource_id: str) -> None:
    """
        Property test: serialize -> deserialize -> equal for selector combinations.
    """
    assume(client_id is not None or resource_id is not None)
    cred = AzureManagedIdentityCredential(
        identifier=identifier, categories=CATEGORIES, client_id=client_id, resource_id=resource_id,
    )
    data = cred.as_dict()
    rebuilt = AzureManagedIdentityCredential(
        identifier=data["identifier"], categories=data["categories"],
        client_id=data["client_id"], resource_id=data["resource_id"], role=data["role"],
    )
    assert rebuilt.as_dict() == data
    return
