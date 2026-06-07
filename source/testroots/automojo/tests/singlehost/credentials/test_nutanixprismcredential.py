"""
    Testbase tests for :class:`NutanixPrismCredential`.

    Verifies construction (with http and https endpoints), category and field
    validation, non-http(s) endpoint rejection, ``repr`` password redaction,
    ``validate`` reporting, ``as_dict`` content, well-known category membership
    registration, and a serialize/deserialize roundtrip property test.
"""

from hypothesis import given, strategies as st

from automojo.credentials.nutanixprismcredential import NutanixPrismCredential
from automojo.credentials.wellknown import CATEGORY_VM_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "nutanix-prism"
CATEGORIES = ["vm-venue"]
USERNAME = "admin"
PASSWORD = "supersecret"
ENDPOINT = "https://prism.example.com:9440"


def test_construction_https_succeeds() -> None:
    """
        Verifies a credential constructs successfully with an https endpoint.
    """
    cred = NutanixPrismCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME,
        password=PASSWORD, endpoint=ENDPOINT,
    )
    assert cred.username == USERNAME
    assert cred.password == PASSWORD
    assert cred.endpoint == ENDPOINT
    return


def test_construction_http_succeeds() -> None:
    """
        Verifies a credential constructs successfully with an http endpoint.
    """
    cred = NutanixPrismCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME,
        password=PASSWORD, endpoint="http://prism.example.com:9440",
    )
    assert cred.endpoint == "http://prism.example.com:9440"
    return


def test_missing_category_raises() -> None:
    """
        Verifies wrong category raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        NutanixPrismCredential(
            identifier=IDENTIFIER, categories=["basic"], username=USERNAME,
            password=PASSWORD, endpoint=ENDPOINT,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_username_raises() -> None:
    """
        Verifies an empty username is rejected.
    """
    raised = False
    try:
        NutanixPrismCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, username="",
            password=PASSWORD, endpoint=ENDPOINT,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_password_raises() -> None:
    """
        Verifies an empty password is rejected.
    """
    raised = False
    try:
        NutanixPrismCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME,
            password="", endpoint=ENDPOINT,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_non_http_endpoint_raises() -> None:
    """
        Verifies a non-http(s) endpoint is rejected.
    """
    raised = False
    try:
        NutanixPrismCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME,
            password=PASSWORD, endpoint="ftp://prism.example.com",
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_repr_redacts_password() -> None:
    """
        Verifies the password never appears in the ``repr``.
    """
    cred = NutanixPrismCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME,
        password=PASSWORD, endpoint=ENDPOINT,
    )
    rendered = repr(cred)
    assert "NutanixPrismCredential" in rendered
    assert PASSWORD not in rendered
    assert "***" in rendered
    return


def test_validate_reports_missing_fields() -> None:
    """
        Verifies ``validate`` reports missing username, password and endpoint fields.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = NutanixPrismCredential.validate(cred_info)
    assert any("missing 'username'" in err for err in errors)
    assert any("missing 'password'" in err for err in errors)
    assert any("missing 'endpoint'" in err for err in errors)
    return


def test_validate_ok_does_not_report_errors() -> None:
    """
        Verifies ``validate`` reports no errors for a complete credential.
    """
    cred_info = {
        "identifier": IDENTIFIER, "categories": CATEGORIES,
        "username": USERNAME, "password": PASSWORD, "endpoint": ENDPOINT,
    }
    errors, warnings = NutanixPrismCredential.validate(cred_info)
    assert errors == []
    return


def test_as_dict_content() -> None:
    """
        Verifies ``as_dict`` carries all credential fields.
    """
    cred = NutanixPrismCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, username=USERNAME,
        password=PASSWORD, endpoint=ENDPOINT,
    )
    data = cred.as_dict()
    assert data["identifier"] == IDENTIFIER
    assert data["categories"] == CATEGORIES
    assert data["username"] == USERNAME
    assert data["password"] == PASSWORD
    assert data["endpoint"] == ENDPOINT
    assert data["role"] == "priv"
    return


def test_category_membership_registered() -> None:
    """
        Verifies the per-provider category is registered under the vm-venue umbrella.
    """
    members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_VM_VENUE]
    assert CATEGORY_VM_VENUE in members
    return


@given(
    identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    username=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    password=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
    scheme=st.sampled_from(["http", "https"]),
    host=st.text(alphabet=st.characters(min_codepoint=97, max_codepoint=122), min_size=1, max_size=24),
    port=st.integers(min_value=1, max_value=65535),
)
def test_nutanix_credential_roundtrip(identifier: str, username: str, password: str, scheme: str, host: str, port: int) -> None:
    """
        Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
    """
    endpoint = "{}://{}:{}".format(scheme, host, port)
    cred = NutanixPrismCredential(
        identifier=identifier, categories=CATEGORIES, username=username,
        password=password, endpoint=endpoint,
    )
    data = cred.as_dict()
    rebuilt = NutanixPrismCredential(
        identifier=data["identifier"], categories=data["categories"],
        username=data["username"], password=data["password"],
        endpoint=data["endpoint"], role=data["role"],
    )
    assert rebuilt.as_dict() == data
    return
