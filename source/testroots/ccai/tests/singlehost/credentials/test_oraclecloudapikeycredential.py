"""
    Testbase tests for :class:`OracleCloudApiKeyCredential`.

    Verifies construction, passphrase defaulting, category and OCID-prefix
    validation, empty private-key and fingerprint rejection, ``repr`` key-material
    redaction, ``validate`` reporting, well-known category membership registration,
    ``as_dict`` passphrase handling, and a serialize/deserialize roundtrip property
    test.
"""

from ccai.testbase.properties import given
from ccai.testbase.properties import strategies as st

from ccai.credentials.oraclecloudapikeycredential import OracleCloudApiKeyCredential
from ccai.credentials.wellknown import CATEGORY_CLOUD_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
from ccai.errors.exceptions import ConfigurationError


IDENTIFIER = "oci-key"
CATEGORIES = ["cloud-venue"]
TENANCY_OCID = "ocid1.tenancy.oc1..aaaatenancy"
USER_OCID = "ocid1.user.oc1..bbbbuser"
PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nMIIBVg\n-----END PRIVATE KEY-----\n"
FINGERPRINT = "aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99"


def test_construction_succeeds() -> None:
    """
        Verifies a complete credential constructs successfully.
    """
    cred = OracleCloudApiKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
        user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
    )
    assert cred.tenancy_ocid == TENANCY_OCID
    assert cred.user_ocid == USER_OCID
    assert cred.private_key == PRIVATE_KEY
    assert cred.fingerprint == FINGERPRINT
    assert cred.passphrase is None
    return


def test_passphrase_defaults_to_none() -> None:
    """
        Verifies an omitted passphrase defaults to None.
    """
    cred = OracleCloudApiKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
        user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
    )
    assert cred.passphrase is None
    return


def test_missing_category_raises() -> None:
    """
        Verifies wrong category raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        OracleCloudApiKeyCredential(
            identifier=IDENTIFIER, categories=["basic"], tenancy_ocid=TENANCY_OCID,
            user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
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
        OracleCloudApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
            user_ocid=USER_OCID, private_key="", fingerprint=FINGERPRINT,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_fingerprint_raises() -> None:
    """
        Verifies an empty fingerprint is rejected.
    """
    raised = False
    try:
        OracleCloudApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
            user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint="",
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_bad_tenancy_ocid_prefix_raises() -> None:
    """
        Verifies a tenancy OCID without the required prefix is rejected.
    """
    raised = False
    try:
        OracleCloudApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid="ocid1.user.oc1..wrong",
            user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_bad_user_ocid_prefix_raises() -> None:
    """
        Verifies a user OCID without the required prefix is rejected.
    """
    raised = False
    try:
        OracleCloudApiKeyCredential(
            identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
            user_ocid="ocid1.tenancy.oc1..wrong", private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_repr_redacts_key_material() -> None:
    """
        Verifies private key material never appears in the ``repr``.
    """
    cred = OracleCloudApiKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
        user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
        passphrase="topsecret",
    )
    rendered = repr(cred)
    assert "OracleCloudApiKeyCredential" in rendered
    assert PRIVATE_KEY not in rendered
    assert "topsecret" not in rendered
    assert "***" in rendered
    return


def test_repr_passphrase_none() -> None:
    """
        Verifies the ``repr`` shows None when there is no passphrase.
    """
    cred = OracleCloudApiKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
        user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
    )
    rendered = repr(cred)
    assert "passphrase=None" in rendered
    return


def test_validate_reports_each_missing_field() -> None:
    """
        Verifies ``validate`` reports each missing field.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES}
    errors, warnings = OracleCloudApiKeyCredential.validate(cred_info)
    assert any("missing 'tenancy_ocid'" in err for err in errors)
    assert any("missing 'user_ocid'" in err for err in errors)
    assert any("missing 'private_key'" in err for err in errors)
    assert any("missing 'fingerprint'" in err for err in errors)
    return


def test_validate_ok_does_not_report_errors() -> None:
    """
        Verifies ``validate`` reports no errors for a complete credential.
    """
    cred_info = {
        "identifier": IDENTIFIER, "categories": CATEGORIES, "tenancy_ocid": TENANCY_OCID,
        "user_ocid": USER_OCID, "private_key": PRIVATE_KEY, "fingerprint": FINGERPRINT,
    }
    errors, warnings = OracleCloudApiKeyCredential.validate(cred_info)
    assert errors == []
    return


def test_category_membership_registered() -> None:
    """
        Verifies the per-provider category is registered under the cloud-venue umbrella.
    """
    cloud_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
    assert CATEGORY_CLOUD_VENUE in cloud_members
    return


def test_as_dict_roundtrips_passphrase_none() -> None:
    """
        Verifies ``as_dict`` carries a None passphrase.
    """
    cred = OracleCloudApiKeyCredential(
        identifier=IDENTIFIER, categories=CATEGORIES, tenancy_ocid=TENANCY_OCID,
        user_ocid=USER_OCID, private_key=PRIVATE_KEY, fingerprint=FINGERPRINT,
    )
    data = cred.as_dict()
    assert data["passphrase"] is None
    return


@given(
    identifier=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=32),
    tenancy_suffix=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48),
    user_suffix=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48),
    private_key=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=128),
    fingerprint=st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64),
    passphrase=st.one_of(st.none(), st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=48)),
)
def test_oracle_credential_roundtrip(identifier: str, tenancy_suffix: str, user_suffix: str, private_key: str, fingerprint: str, passphrase: str) -> None:
    """
        Property test: serialize -> deserialize -> equal across arbitrary valid inputs.
    """
    tenancy_ocid = OracleCloudApiKeyCredential.TENANCY_OCID_PREFIX + tenancy_suffix
    user_ocid = OracleCloudApiKeyCredential.USER_OCID_PREFIX + user_suffix
    cred = OracleCloudApiKeyCredential(
        identifier=identifier, categories=CATEGORIES, tenancy_ocid=tenancy_ocid,
        user_ocid=user_ocid, private_key=private_key, fingerprint=fingerprint,
        passphrase=passphrase,
    )
    data = cred.as_dict()
    rebuilt = OracleCloudApiKeyCredential(
        identifier=data["identifier"], categories=data["categories"], tenancy_ocid=data["tenancy_ocid"],
        user_ocid=data["user_ocid"], private_key=data["private_key"], fingerprint=data["fingerprint"],
        passphrase=data["passphrase"], role=data["role"],
    )
    assert rebuilt.as_dict() == data
    return
