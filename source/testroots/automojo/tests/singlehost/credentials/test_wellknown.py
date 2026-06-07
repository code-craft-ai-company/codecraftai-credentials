"""
    Testbase tests for the well-known credential category umbrella support.

    Verifies that the umbrella category constants are exported and listed in
    ``__all__``, that the seeded membership map wires the per-provider
    categories under the correct umbrellas, and that
    :func:`get_credentials_by_category` performs umbrella expansion, exact
    per-provider lookup, and umbrella-self-declaration resolution.
"""

from automojo.errors.exceptions import SemanticError

from automojo.credentials import wellknown
from automojo.credentials.wellknown import (
    CATEGORY_VPN,
    CATEGORY_MESH,
    CATEGORY_CLOUD_VENUE,
    CATEGORY_VM_VENUE,
    CATEGORY_HPC_VENUE,
    WELL_KNOWN_CATEGORY_MEMBERSHIP,
    CredentialManagerSingleton,
    get_credentials_by_category,
)


CREDENTIAL_INFO = {
    "credentials": [
        {
            "identifier": "ts-key",
            "category": "tailscale-authkey",
            "authkey": "tskey-auth-AAAA",
        },
        {
            "identifier": "ts-oauth",
            "category": "tailscale-oauth",
            "client_id": "ksXXXX",
            "client_secret": "secret-XXXX",
        },
        {
            "identifier": "tg-prod",
            "category": "twingate-service-account",
            "api_token": "tg-svc-XXXX",
            "network_slug": "acme",
        },
        {
            "identifier": "aws-cred",
            "category": "aws-access-key",
            "keyid": "AKIAFAKE",
            "secret": "secret-aws",
        },
    ]
}


def _setup_singleton_reset() -> None:
    """
        Replicates the original ``setUp`` by resetting the credential manager
        singleton before a single test executes so that tests remain isolated.
    """
    wellknown.CREDENTIAL_MANAGER_SINGLETON = None
    return


def _teardown_singleton_reset() -> None:
    """
        Replicates the original ``tearDown`` by resetting the credential
        manager singleton after a single test executes.
    """
    wellknown.CREDENTIAL_MANAGER_SINGLETON = None
    return


def test_category_constants_exported() -> None:
    """
        Verifies all five umbrella constants are exported.
    """
    assert CATEGORY_VPN == "vpn"
    assert CATEGORY_MESH == "mesh"
    assert CATEGORY_CLOUD_VENUE == "cloud-venue"
    assert CATEGORY_VM_VENUE == "vm-venue"
    assert CATEGORY_HPC_VENUE == "hpc-venue"
    return


def test_constants_listed_in_all() -> None:
    """
        Verifies the constants are present in ``__all__``.
    """
    for name in [
        "CATEGORY_VPN", "CATEGORY_MESH", "CATEGORY_CLOUD_VENUE",
        "CATEGORY_VM_VENUE", "CATEGORY_HPC_VENUE",
        "WELL_KNOWN_CATEGORY_MEMBERSHIP",
        "CredentialManagerSingleton", "get_credentials_by_category",
    ]:
        assert name in wellknown.__all__
    return


def test_membership_seed_for_vpn() -> None:
    """
        Verifies the VPN umbrella includes the seeded per-provider categories.
    """
    vpn_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_VPN]
    assert "tailscale-authkey" in vpn_members
    assert "tailscale-oauth" in vpn_members
    assert "twingate-service-account" in vpn_members
    return


def test_membership_seed_for_mesh() -> None:
    """
        Verifies the mesh umbrella mirrors the VPN seed.
    """
    mesh_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_MESH]
    assert "tailscale-authkey" in mesh_members
    assert "tailscale-oauth" in mesh_members
    assert "twingate-service-account" in mesh_members
    return


def test_membership_seed_for_cloud_venue() -> None:
    """
        Verifies the cloud-venue umbrella includes existing AWS access keys.
    """
    cloud_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
    assert "aws-access-key" in cloud_members
    return


def test_membership_seed_for_venue_umbrellas_present() -> None:
    """
        Verifies the VM/HPC venue umbrellas are declared (possibly empty).
    """
    assert CATEGORY_VM_VENUE in WELL_KNOWN_CATEGORY_MEMBERSHIP
    assert CATEGORY_HPC_VENUE in WELL_KNOWN_CATEGORY_MEMBERSHIP
    return


def test_raises_when_singleton_uninitialised() -> None:
    """
        Verifies the helper raises :class:`SemanticError` before init.
    """
    _setup_singleton_reset()
    try:
        raised = False
        try:
            get_credentials_by_category(category="vpn")
        except SemanticError:
            raised = True
        assert raised
    finally:
        _teardown_singleton_reset()
    return


def test_umbrella_expansion_vpn() -> None:
    """
        Verifies the VPN umbrella expands to all three seeded providers.
    """
    _setup_singleton_reset()
    try:
        CredentialManagerSingleton(credential_info=CREDENTIAL_INFO, credential_uris=["test"])
        matches = get_credentials_by_category(category=CATEGORY_VPN)
        identifiers = sorted(cred.identifier for cred in matches)
        assert identifiers == ["tg-prod", "ts-key", "ts-oauth"]
    finally:
        _teardown_singleton_reset()
    return


def test_umbrella_expansion_cloud_venue() -> None:
    """
        Verifies the cloud-venue umbrella resolves to the AWS credential.
    """
    _setup_singleton_reset()
    try:
        CredentialManagerSingleton(credential_info=CREDENTIAL_INFO, credential_uris=["test"])
        matches = get_credentials_by_category(category=CATEGORY_CLOUD_VENUE)
        identifiers = sorted(cred.identifier for cred in matches)
        assert identifiers == ["aws-cred"]
    finally:
        _teardown_singleton_reset()
    return


def test_per_provider_lookup_returns_only_matching() -> None:
    """
        Verifies per-provider lookup returns only the exact-category credential.
    """
    _setup_singleton_reset()
    try:
        CredentialManagerSingleton(credential_info=CREDENTIAL_INFO, credential_uris=["test"])
        matches = get_credentials_by_category(category="tailscale-oauth")
        identifiers = sorted(cred.identifier for cred in matches)
        assert identifiers == ["ts-oauth"]
    finally:
        _teardown_singleton_reset()
    return


def test_umbrella_expansion_matches_umbrella_declaring_credential() -> None:
    """
        Verifies the cloud-venue umbrella resolves credentials that
        declare the umbrella category itself (the convention used by the
        venue credential classes), not only the legacy per-provider
        strings. This is the F-H4 regression guard.
    """
    _setup_singleton_reset()
    try:
        from automojo.credentials.digitaloceanapitokencredential import (
            DigitalOceanApiTokenCredential,
        )

        credmgr = CredentialManagerSingleton(credential_info=CREDENTIAL_INFO,
                                             credential_uris=["test"])
        do_cred = DigitalOceanApiTokenCredential(
            identifier="do-cred", categories=["cloud-venue"],
            token="do-token-XXXX")
        credmgr._credentials["do-cred"] = do_cred

        matches = get_credentials_by_category(category=CATEGORY_CLOUD_VENUE)
        identifiers = sorted(cred.identifier for cred in matches)
        assert identifiers == ["aws-cred", "do-cred"]
    finally:
        _teardown_singleton_reset()
    return
