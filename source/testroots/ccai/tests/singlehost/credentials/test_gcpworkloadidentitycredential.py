"""
    Testbase tests for :class:`GcpWorkloadIdentityCredential`.

    Converted from the legacy ``unittest`` module
    ``ccai_tests.credentials.test_gcpworkloadidentitycredential`` as part of
    the Phase 7 unittest -> testbase shift. Each former ``TestCase`` method is
    now a module-level ``test_*`` function with identical assertion behaviour.
"""

from hypothesis import given, strategies as st

from ccai.credentials.gcpworkloadidentitycredential import GcpWorkloadIdentityCredential
from ccai.credentials.wellknown import CATEGORY_CLOUD_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "gcp-wif"
CATEGORIES = ["cloud-venue"]
AUDIENCE = "//iam.googleapis.com/projects/123/locations/global/workloadIdentityPools/pool/providers/provider"
SUBJECT_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:jwt"
SERVICE_ACCOUNT_EMAIL = "svc@my-project.iam.gserviceaccount.com"


def test_construction_succeeds() -> None:
    """
        Verifies a complete credential constructs successfully.
    """
    cred = GcpWorkloadIdentityCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, audience=AUDIENCE,
        subject_token_type=SUBJECT_TOKEN_TYPE, service_account_email=SERVICE_ACCOUNT_EMAIL,
    )
    assert cred.audience == AUDIENCE
    assert cred.subject_token_type == SUBJECT_TOKEN_TYPE
    assert cred.service_account_email == SERVICE_ACCOUNT_EMAIL
    return


def test_token_url_defaults_when_omitted() -> None:
    """
        Verifies ``token_url`` is populated with the default when omitted.
    """
    cred = GcpWorkloadIdentityCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, audience=AUDIENCE,
        subject_token_type=SUBJECT_TOKEN_TYPE, service_account_email=SERVICE_ACCOUNT_EMAIL,
    )
    assert cred.token_url == GcpWorkloadIdentityCredential.DEFAULT_TOKEN_URL
    return


def test_missing_category_raises() -> None:
    """
        Verifies wrong category raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        GcpWorkloadIdentityCredential(
            identifier=IDENTIFIER, categories=["basic"], audience=AUDIENCE,
            subject_token_type=SUBJECT_TOKEN_TYPE, service_account_email=SERVICE_ACCOUNT_EMAIL,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_audience_raises() -> None:
    """
        Verifies an empty audience is rejected.
    """
    raised = False
    try:
        GcpWorkloadIdentityCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, audience="",
            subject_token_type=SUBJECT_TOKEN_TYPE, service_account_email=SERVICE_ACCOUNT_EMAIL,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_service_account_email_raises() -> None:
    """
        Verifies an empty service account email is rejected.
    """
    raised = False
    try:
        GcpWorkloadIdentityCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, audience=AUDIENCE,
            subject_token_type=SUBJECT_TOKEN_TYPE, service_account_email="",
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_repr_contains_identifier() -> None:
    """
        Verifies the ``repr`` includes the identifier and class name.
    """
    cred = GcpWorkloadIdentityCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, audience=AUDIENCE,
        subject_token_type=SUBJECT_TOKEN_TYPE, service_account_email=SERVICE_ACCOUNT_EMAIL,
    )
    rendered = repr(cred)
    assert "GcpWorkloadIdentityCredential" in rendered
    assert IDENTIFIER in rendered
    return


def test_validate_reports_each_missing_field() -> None:
    """
        Verifies ``validate`` reports each missing field.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = GcpWorkloadIdentityCredential.validate(cred_info)
    assert any("missing 'audience'" in err for err in errors)
    assert any("missing 'subject_token_type'" in err for err in errors)
    assert any("missing 'service_account_email'" in err for err in errors)
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
    audience=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=96),
    subject_token_type=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48),
    service_account_email=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
    token_url=st.one_of(st.none(), st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64)),
)
def test_gcp_workload_identity_roundtrip(identifier, audience, subject_token_type, service_account_email, token_url) -> None:
    """
        Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
    """
    cred = GcpWorkloadIdentityCredential(
        identifier=identifier, categories=CATEGORIES, audience=audience,
        subject_token_type=subject_token_type, service_account_email=service_account_email,
        token_url=token_url,
    )
    data = cred.as_dict()
    rebuilt = GcpWorkloadIdentityCredential(
        identifier=data["identifier"], categories=data["categories"], audience=data["audience"],
        subject_token_type=data["subject_token_type"], service_account_email=data["service_account_email"],
        token_url=data["token_url"], role=data["role"],
    )
    assert rebuilt.as_dict() == data
    return
