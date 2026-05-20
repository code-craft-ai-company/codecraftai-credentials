import unittest

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


class TestWellKnownCategoryConstants(unittest.TestCase):

    def test_category_constants_exported(self):
        """
            Verifies all five umbrella constants are exported.
        """
        self.assertEqual(CATEGORY_VPN, "vpn")
        self.assertEqual(CATEGORY_MESH, "mesh")
        self.assertEqual(CATEGORY_CLOUD_VENUE, "cloud-venue")
        self.assertEqual(CATEGORY_VM_VENUE, "vm-venue")
        self.assertEqual(CATEGORY_HPC_VENUE, "hpc-venue")

    def test_constants_listed_in_all(self):
        """
            Verifies the constants are present in ``__all__``.
        """
        for name in [
            "CATEGORY_VPN", "CATEGORY_MESH", "CATEGORY_CLOUD_VENUE",
            "CATEGORY_VM_VENUE", "CATEGORY_HPC_VENUE",
            "WELL_KNOWN_CATEGORY_MEMBERSHIP",
            "CredentialManagerSingleton", "get_credentials_by_category",
        ]:
            self.assertIn(name, wellknown.__all__)

    def test_membership_seed_for_vpn(self):
        """
            Verifies the VPN umbrella includes the seeded per-provider categories.
        """
        vpn_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_VPN]
        self.assertIn("tailscale-authkey", vpn_members)
        self.assertIn("tailscale-oauth", vpn_members)
        self.assertIn("twingate-service-account", vpn_members)

    def test_membership_seed_for_mesh(self):
        """
            Verifies the mesh umbrella mirrors the VPN seed.
        """
        mesh_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_MESH]
        self.assertIn("tailscale-authkey", mesh_members)
        self.assertIn("tailscale-oauth", mesh_members)
        self.assertIn("twingate-service-account", mesh_members)

    def test_membership_seed_for_cloud_venue(self):
        """
            Verifies the cloud-venue umbrella includes existing AWS access keys.
        """
        cloud_members = WELL_KNOWN_CATEGORY_MEMBERSHIP[CATEGORY_CLOUD_VENUE]
        self.assertIn("aws-access-key", cloud_members)

    def test_membership_seed_for_venue_umbrellas_present(self):
        """
            Verifies the VM/HPC venue umbrellas are declared (possibly empty).
        """
        self.assertIn(CATEGORY_VM_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP)
        self.assertIn(CATEGORY_HPC_VENUE, WELL_KNOWN_CATEGORY_MEMBERSHIP)


class TestGetCredentialsByCategory(unittest.TestCase):

    def setUp(self):
        """
            Reset the singleton and load credentials for each test.
        """
        wellknown.CREDENTIAL_MANAGER_SINGLETON = None

    def tearDown(self):
        """
            Reset the singleton after each test.
        """
        wellknown.CREDENTIAL_MANAGER_SINGLETON = None

    def test_raises_when_singleton_uninitialised(self):
        """
            Verifies the helper raises :class:`SemanticError` before init.
        """
        with self.assertRaises(SemanticError):
            get_credentials_by_category(category="vpn")

    def test_umbrella_expansion_vpn(self):
        """
            Verifies the VPN umbrella expands to all three seeded providers.
        """
        CredentialManagerSingleton(credential_info=CREDENTIAL_INFO, credential_uris=["test"])
        matches = get_credentials_by_category(category=CATEGORY_VPN)
        identifiers = sorted(cred.identifier for cred in matches)
        self.assertEqual(identifiers, ["tg-prod", "ts-key", "ts-oauth"])

    def test_umbrella_expansion_cloud_venue(self):
        """
            Verifies the cloud-venue umbrella resolves to the AWS credential.
        """
        CredentialManagerSingleton(credential_info=CREDENTIAL_INFO, credential_uris=["test"])
        matches = get_credentials_by_category(category=CATEGORY_CLOUD_VENUE)
        identifiers = sorted(cred.identifier for cred in matches)
        self.assertEqual(identifiers, ["aws-cred"])

    def test_per_provider_lookup_returns_only_matching(self):
        """
            Verifies per-provider lookup returns only the exact-category credential.
        """
        CredentialManagerSingleton(credential_info=CREDENTIAL_INFO, credential_uris=["test"])
        matches = get_credentials_by_category(category="tailscale-oauth")
        identifiers = sorted(cred.identifier for cred in matches)
        self.assertEqual(identifiers, ["ts-oauth"])
