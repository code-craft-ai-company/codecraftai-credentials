"""
    Testbase tests for :class:`VSphereCredential`.

    Converted from the legacy ``unittest`` module
    ``automojo_tests.credentials.test_vspherecredential`` during the Phase 7
    unittest->testbase shift. Each former ``TestCase`` method is preserved
    one-to-one as a module-level ``test_*`` function with identical logic and
    assertions.
"""

from automojo.credentials.vspherecredential import VSphereCredential
from automojo.credentials.wellknown import (
    CATEGORY_VM_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP
)
from automojo.errors.exceptions import ConfigurationError


IDENTIFIER = "vsphere-cred"
CATEGORIES = ["vm-venue", "vsphere-basic"]
USERNAME = "administrator@vsphere.local"
PASSWORD = "LetMeComeIn"
SSO_TOKEN = "abcdef0123456789ssotoken"


def test_construction_password_only() -> None:
    """
        Verifies a password-only credential constructs successfully.
    """
    cred = VSphereCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        username=USERNAME, password=PASSWORD,
    )
    assert cred.username == USERNAME
    assert cred.password == PASSWORD
    assert cred.sso_token is None
    return


def test_construction_sso_token_only() -> None:
    """
        Verifies an sso-token-only credential constructs successfully.
    """
    cred = VSphereCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        username=USERNAME, sso_token=SSO_TOKEN,
    )
    assert cred.username == USERNAME
    assert cred.password is None
    assert cred.sso_token == SSO_TOKEN
    return


def test_construction_both_fields() -> None:
    """
        Verifies a credential carrying both fields constructs successfully.
    """
    cred = VSphereCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        username=USERNAME, password=PASSWORD, sso_token=SSO_TOKEN,
    )
    assert cred.password == PASSWORD
    assert cred.sso_token == SSO_TOKEN
    return


def test_missing_category_raises() -> None:
    """
        Verifies a wrong category raises :class:`ConfigurationError`.
    """
    raised = False
    try:
        VSphereCredential(
            identifier=IDENTIFIER, categories=["basic"],
            username=USERNAME, password=PASSWORD,
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
        VSphereCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            username="", password=PASSWORD,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_missing_password_and_sso_token_raises() -> None:
    """
        Verifies a credential with neither password nor sso_token is rejected.
    """
    raised = False
    try:
        VSphereCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            username=USERNAME,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_empty_password_and_none_sso_token_raises() -> None:
    """
        Verifies an empty password with no sso_token is rejected.
    """
    raised = False
    try:
        VSphereCredential(
            identifier=IDENTIFIER, categories=CATEGORIES,
            username=USERNAME, password="", sso_token=None,
        )
    except ConfigurationError:
        raised = True

    assert raised
    return


def test_repr_redacts_secret_material() -> None:
    """
        Verifies password and sso_token never appear in the ``repr``.
    """
    cred = VSphereCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        username=USERNAME, password=PASSWORD, sso_token=SSO_TOKEN,
    )
    rendered = repr(cred)
    assert "VSphereCredential" in rendered
    assert PASSWORD not in rendered
    assert SSO_TOKEN not in rendered
    assert "***" in rendered
    return


def test_repr_shows_none_when_secrets_absent() -> None:
    """
        Verifies the ``repr`` shows None for an absent secret field.
    """
    cred = VSphereCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        username=USERNAME, password=PASSWORD,
    )
    rendered = repr(cred)
    assert "sso_token=None" in rendered
    return


def test_validate_reports_missing_username() -> None:
    """
        Verifies ``validate`` reports a missing username.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES,
                 "password": PASSWORD}
    errors, warnings = VSphereCredential.validate(cred_info)
    assert any("missing 'username'" in err for err in errors)
    return


def test_validate_reports_missing_credentials() -> None:
    """
        Verifies ``validate`` reports a missing password and sso_token.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES,
                 "username": USERNAME}
    errors, warnings = VSphereCredential.validate(cred_info)
    assert any("password" in err and "sso_token" in err
               for err in errors)
    return


def test_validate_ok_does_not_report_errors() -> None:
    """
        Verifies ``validate`` reports no errors for a complete credential.
    """
    cred_info = {"identifier": IDENTIFIER, "categories": CATEGORIES,
                 "username": USERNAME, "sso_token": SSO_TOKEN}
    errors, warnings = VSphereCredential.validate(cred_info)
    assert errors == []
    assert warnings == []
    return


def test_as_dict_roundtrips_none_fields() -> None:
    """
        Verifies ``as_dict`` carries None-valued fields losslessly.
    """
    cred = VSphereCredential(
        identifier=IDENTIFIER, categories=CATEGORIES,
        username=USERNAME, password=PASSWORD,
    )
    data = cred.as_dict()
    assert data["username"] == USERNAME
    assert data["password"] == PASSWORD
    assert data["sso_token"] is None
    return


def test_category_membership_registered() -> None:
    """
        Verifies the per-provider category is registered under the
        vm-venue umbrella.
    """
    vm_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_VM_VENUE]
    assert CATEGORY_VM_VENUE in vm_members
    return
