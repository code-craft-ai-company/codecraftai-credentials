"""
    Testbase tests for :class:`CrusoeApiKeyCredential`.

    Converted from the legacy ``unittest`` module
    ``automojo_tests.credentials.test_crusoeapikeycredential`` as part of the
    Phase 7 unittest -> testbase shift. Each former ``TestCase`` method is now a
    module-level ``test_*`` function with identical assertion behaviour.
"""

from hypothesis import given, strategies as st

from automojo.credentials.crusoeapikeycredential import CrusoeApiKeyCredential
from automojo.credentials.wellknown import (
    CATEGORY_CLOUD_VENUE,
    CATEGORY_HPC_VENUE,
    WELL_KNOWN_CATEGORY_MEMBERSHIP,
)
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "crusoe-key"
CATEGORIES = ["hpc-venue"]
ACCESS_KEY_ID = "crusoe-access-key-abc"
SECRET = "crusoe-secret-xyz"


def test_construction_succeeds() -> None:
    """
        Verifies a complete credential constructs successfully.
    """
    cred = CrusoeApiKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        access_key_id=ACCESS_KEY_ID, secret=SECRET,
    )
    assert cred.access_key_id == ACCESS_KEY_ID
    assert cred.secret == SECRET
    return


def test_construction_succeeds_with_cloud_venue() -> None:
    """
        Verifies the cloud-venue category alone is accepted.
    """
    cred = CrusoeApiKeyCredential(
        identifier=IDENTIFIER, categories=["cloud-venue"],
        access_key_id=ACCESS_KEY_ID, secret=SECRET,
    )
    assert cred.access_key_id == ACCESS_KEY_ID
    return


def test_missing_category_raises() -> None:
    """
        Verifies neither category present raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        CrusoeApiKeyCredential(
            identifier=IDENTIFIER, categories=["basic"],
            access_key_id=ACCESS_KEY_ID, secret=SECRET,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_access_key_id_raises() -> None:
    """
        Verifies an empty access_key_id is rejected.
    """
    raised = False
    try:
        CrusoeApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            access_key_id="", secret=SECRET,
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
        CrusoeApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            access_key_id=ACCESS_KEY_ID, secret="",
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_repr_redacts_secret() -> None:
    """
        Verifies the secret never appears in the ``repr``.
    """
    cred = CrusoeApiKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        access_key_id=ACCESS_KEY_ID, secret=SECRET,
    )
    rendered = repr(cred)
    assert "CrusoeApiKeyCredential" in rendered
    assert SECRET not in rendered
    assert "***" in rendered
    return


def test_validate_reports_each_missing_field() -> None:
    """
        Verifies ``validate`` reports each missing field.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = CrusoeApiKeyCredential.validate(cred_info)
    assert any("missing 'access_key_id'" in err for err in errors)
    assert any("missing 'secret'" in err for err in errors)
    return


def test_validate_ok_does_not_report_errors() -> None:
    """
        Verifies ``validate`` reports no errors for a complete credential.
    """
    cred_info = {
        "identifier": IDENTIFIER, "categories": CATEGORIES,
        "access_key_id": ACCESS_KEY_ID, "secret": SECRET,
    }
    errors, warnings = CrusoeApiKeyCredential.validate(cred_info)
    assert errors == []
    return


def test_as_dict_content() -> None:
    """
        Verifies ``as_dict`` carries all credential fields.
    """
    cred = CrusoeApiKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        access_key_id=ACCESS_KEY_ID, secret=SECRET,
    )
    data = cred.as_dict()
    assert data["identifier"] == IDENTIFIER
    assert data["categories"] == CATEGORIES
    assert data["access_key_id"] == ACCESS_KEY_ID
    assert data["secret"] == SECRET
    assert data["role"] == "priv"
    return


def test_category_membership_registered() -> None:
    """
        Verifies the per-provider category is registered under both umbrellas.
    """
    hpc_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_HPC_VENUE]
    cloud_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
    assert CATEGORY_HPC_VENUE in hpc_members
    assert CATEGORY_CLOUD_VENUE in cloud_members
    return


@given(
    identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    access_key_id=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
    secret=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=128),
)
def test_crusoe_credential_roundtrip(identifier, access_key_id, secret) -> None:
    """
        Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
    """
    cred = CrusoeApiKeyCredential(
        identifier=identifier, categories=CATEGORIES,
        access_key_id=access_key_id, secret=secret,
    )
    data = cred.as_dict()
    rebuilt = CrusoeApiKeyCredential(
        identifier=data["identifier"], categories=data["categories"],
        access_key_id=data["access_key_id"], secret=data["secret"], role=data["role"],
    )
    assert rebuilt.as_dict() == data
    return
