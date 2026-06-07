"""
    Testbase tests for :class:`AzureServicePrincipalCredential`.

    Converted from the legacy ``unittest`` module of the same name during the
    Phase 7 unittest->testbase shift. Each former ``TestCase`` method is now a
    module-level ``test_*`` function with an identical body.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

from hypothesis import given, strategies as st

from automojo.credentials.azureserviceprincipalcredential import AzureServicePrincipalCredential
from automojo.credentials.wellknown import CATEGORY_CLOUD_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "azure-sp"
CATEGORIES = ["cloud-venue"]
TENANT_ID = "11111111-1111-1111-1111-111111111111"
CLIENT_ID = "22222222-2222-2222-2222-222222222222"
CLIENT_SECRET = "@@&_LetMeComeIn"


def test_construction_succeeds() -> None:
    """
        Verifies a complete credential constructs successfully.
    """
    cred = AzureServicePrincipalCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    )
    assert cred.tenant_id == TENANT_ID
    assert cred.client_id == CLIENT_ID
    assert cred.client_secret == CLIENT_SECRET
    return


def test_missing_category_raises() -> None:
    """
        Verifies wrong category raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        AzureServicePrincipalCredential(
            identifier=IDENTIFIER, categories=["basic"],
            tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_tenant_id_raises() -> None:
    """
        Verifies an empty tenant id is rejected.
    """
    raised = False
    try:
        AzureServicePrincipalCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            tenant_id="", client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
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
        AzureServicePrincipalCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            tenant_id=TENANT_ID, client_id="", client_secret=CLIENT_SECRET,
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
        AzureServicePrincipalCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret="",
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_repr_redacts_secret() -> None:
    """
        Verifies the client secret value never appears in the ``repr``.
    """
    cred = AzureServicePrincipalCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    )
    rendered = repr(cred)
    assert "AzureServicePrincipalCredential" in rendered
    assert IDENTIFIER in rendered
    assert CLIENT_SECRET not in rendered
    assert "***" in rendered
    return


def test_validate_reports_each_missing_field() -> None:
    """
        Verifies ``validate`` reports each missing field.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = AzureServicePrincipalCredential.validate(cred_info)
    assert any("missing 'tenant_id'" in err for err in errors)
    assert any("missing 'client_id'" in err for err in errors)
    assert any("missing 'client_secret'" in err for err in errors)
    assert warnings == []
    return


def test_validate_ok_does_not_report_errors() -> None:
    """
        Verifies ``validate`` reports no errors for a complete credential.
    """
    cred_info = {
        "identifier": IDENTIFIER, "categories": CATEGORIES,
        "tenant_id": TENANT_ID, "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
    }
    errors, warnings = AzureServicePrincipalCredential.validate(cred_info)
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
        Verifies ``as_dict`` contains every constructor field.
    """
    cred = AzureServicePrincipalCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    )
    data = cred.as_dict()
    assert data["identifier"] == IDENTIFIER
    assert data["categories"] == CATEGORIES
    assert data["role"] == "priv"
    assert data["tenant_id"] == TENANT_ID
    assert data["client_id"] == CLIENT_ID
    assert data["client_secret"] == CLIENT_SECRET
    return


@given(
    identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    tenant_id=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48),
    client_id=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48),
    client_secret=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
)
def test_service_principal_roundtrip(identifier, tenant_id, client_id, client_secret) -> None:
    """
        Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
    """
    cred = AzureServicePrincipalCredential(
        identifier=identifier, categories=CATEGORIES,
        tenant_id=tenant_id, client_id=client_id, client_secret=client_secret,
    )
    data = cred.as_dict()
    rebuilt = AzureServicePrincipalCredential(
        identifier=data["identifier"], categories=data["categories"],
        tenant_id=data["tenant_id"], client_id=data["client_id"],
        client_secret=data["client_secret"], role=data["role"],
    )
    assert rebuilt.as_dict() == data
    return
