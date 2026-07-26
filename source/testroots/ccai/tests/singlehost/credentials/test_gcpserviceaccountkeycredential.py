"""
    Testbase tests for :class:`GcpServiceAccountKeyCredential`.

    Converted from the legacy ``unittest`` module
    ``ccai_tests.credentials.test_gcpserviceaccountkeycredential`` as part of
    the Phase 7 unittest -> testbase shift. Each former ``TestCase`` method is now
    a module-level ``test_*`` function with identical assertion behaviour.
"""

from ccai.testbase.properties import given
from ccai.testbase.properties import strategies as st

from ccai.credentials.gcpserviceaccountkeycredential import GcpServiceAccountKeyCredential
from ccai.credentials.wellknown import CATEGORY_CLOUD_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "gcp-sa"
CATEGORIES = ["cloud-venue"]
PROJECT_ID = "my-project"
CLIENT_EMAIL = "svc@my-project.iam.gserviceaccount.com"
PRIVATE_KEY_ID = "abcdef0123456789"
PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nMIIBVg\n-----END PRIVATE KEY-----\n"


def test_construction_succeeds() -> None:
    """
        Verifies a complete credential constructs successfully.
    """
    cred = GcpServiceAccountKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, project_id=PROJECT_ID,
        client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key=PRIVATE_KEY,
    )
    assert cred.project_id == PROJECT_ID
    assert cred.client_email == CLIENT_EMAIL
    assert cred.private_key_id == PRIVATE_KEY_ID
    assert cred.private_key == PRIVATE_KEY
    return


def test_token_uri_defaults_when_omitted() -> None:
    """
        Verifies ``token_uri`` is populated with the default when omitted.
    """
    cred = GcpServiceAccountKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, project_id=PROJECT_ID,
        client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key=PRIVATE_KEY,
    )
    assert cred.token_uri == GcpServiceAccountKeyCredential.DEFAULT_TOKEN_URI
    return


def test_token_uri_override_respected() -> None:
    """
        Verifies an explicit ``token_uri`` is retained.
    """
    custom = "https://example.test/token"
    cred = GcpServiceAccountKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, project_id=PROJECT_ID,
        client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key=PRIVATE_KEY,
        token_uri=custom,
    )
    assert cred.token_uri == custom
    return


def test_missing_category_raises() -> None:
    """
        Verifies wrong category raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        GcpServiceAccountKeyCredential(
            identifier=IDENTIFIER, categories=["basic"], project_id=PROJECT_ID,
            client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key=PRIVATE_KEY,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_project_id_raises() -> None:
    """
        Verifies an empty project id is rejected.
    """
    raised = False
    try:
        GcpServiceAccountKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, project_id="",
            client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key=PRIVATE_KEY,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_private_key_raises() -> None:
    """
        Verifies an empty private key is rejected.
    """
    raised = False
    try:
        GcpServiceAccountKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, project_id=PROJECT_ID,
            client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key="",
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_repr_redacts_key_material() -> None:
    """
        Verifies private key material never appears in the ``repr``.
    """
    cred = GcpServiceAccountKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, project_id=PROJECT_ID,
        client_email=CLIENT_EMAIL, private_key_id=PRIVATE_KEY_ID, private_key=PRIVATE_KEY,
    )
    rendered = repr(cred)
    assert "GcpServiceAccountKeyCredential" in rendered
    assert PRIVATE_KEY not in rendered
    assert PRIVATE_KEY_ID not in rendered
    assert "***" in rendered
    return


def test_validate_reports_each_missing_field() -> None:
    """
        Verifies ``validate`` reports each missing field.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = GcpServiceAccountKeyCredential.validate(cred_info)
    assert any("missing 'project_id'" in err for err in errors)
    assert any("missing 'client_email'" in err for err in errors)
    assert any("missing 'private_key_id'" in err for err in errors)
    assert any("missing 'private_key'" in err for err in errors)
    return


def test_category_membership_registered() -> None:
    """
        Verifies the per-provider category is registered under the cloud-venue umbrella.
    """
    cloud_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
    assert CATEGORY_CLOUD_VENUE in cloud_members
    return


@given(
    identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    project_id=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    client_email=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
    private_key_id=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48),
    private_key=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=128),
    token_uri=st.one_of(st.none(), st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64)),
)
def test_gcp_service_account_key_roundtrip(identifier, project_id, client_email, private_key_id, private_key, token_uri) -> None:
    """
        Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
    """
    cred = GcpServiceAccountKeyCredential(
        identifier=identifier, categories=CATEGORIES, project_id=project_id,
        client_email=client_email, private_key_id=private_key_id, private_key=private_key,
        token_uri=token_uri,
    )
    data = cred.as_dict()
    rebuilt = GcpServiceAccountKeyCredential(
        identifier=data["identifier"], categories=data["categories"], project_id=data["project_id"],
        client_email=data["client_email"], private_key_id=data["private_key_id"],
        private_key=data["private_key"], token_uri=data["token_uri"], role=data["role"],
    )
    assert rebuilt.as_dict() == data
    return
