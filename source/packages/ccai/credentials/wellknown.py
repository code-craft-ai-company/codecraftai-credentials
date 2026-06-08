
"""
    .. module:: wellknown
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that provides a singleton for the :class:`CredentialManager` and
                   declares the well-known credential category constants and umbrella
                   membership registry consumed by VPN and venue control planes.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Dict, List, Optional

from threading import RLock

from ccai.errors.exceptions import SemanticError

from ccai.credentials.basecredential import BaseCredential
from ccai.credentials.credentialmanager import CredentialManager


__all__ = [
    "CATEGORY_VPN",
    "CATEGORY_MESH",
    "CATEGORY_CLOUD_VENUE",
    "CATEGORY_VM_VENUE",
    "CATEGORY_HPC_VENUE",
    "WELL_KNOWN_CATEGORY_MEMBERSHIP",
    "CredentialManagerSingleton",
    "get_credentials_by_category",
]


CATEGORY_VPN = "vpn"
CATEGORY_MESH = "mesh"
CATEGORY_CLOUD_VENUE = "cloud-venue"
CATEGORY_VM_VENUE = "vm-venue"
CATEGORY_HPC_VENUE = "hpc-venue"


WELL_KNOWN_CATEGORY_MEMBERSHIP: Dict[str, List[str]] = {
    CATEGORY_VPN: [
        "tailscale-authkey",
        "tailscale-oauth",
        "twingate-service-account",
    ],
    CATEGORY_MESH: [
        "tailscale-authkey",
        "tailscale-oauth",
        "twingate-service-account",
    ],
    # The venue credential classes declare the umbrella category itself
    # (``cloud-venue`` / ``vm-venue`` / ``hpc-venue``) rather than a
    # per-provider string, so the umbrella entries must resolve to the
    # umbrella category. The two legacy cloud credential classes
    # (``AwsAccessKeyCredential``, ``AzureClientSecretCredential``) predate
    # that convention and declare per-provider strings, so those remain in
    # the cloud-venue membership list for backward compatibility.
    CATEGORY_CLOUD_VENUE: [
        CATEGORY_CLOUD_VENUE,
        "aws-access-key",
        "azure-client-secret",
    ],
    CATEGORY_VM_VENUE: [
        CATEGORY_VM_VENUE,
    ],
    CATEGORY_HPC_VENUE: [
        CATEGORY_HPC_VENUE,
    ],
}


CREDENTIAL_MANAGER_SINGLETON = None

SINGLETON_LOCK = RLock()


def CredentialManagerSingleton(credential_info: Optional[dict] = None, credential_uris: Optional[List[str]] = None) -> CredentialManager:
    """
        Instantiates and gets a global instance of the :class:`CredentialManager` class.  The
        :class:`CredentialManager` provides for management of credentials.

        :param credential_info: The credential information dictionary used on first call.
        :param credential_uris: The list of source URIs used on first call.

        :returns: The shared :class:`CredentialManager` instance.
        :raises: SemanticError when the first call omits ``credential_info`` or ``credential_uris``.
    """
    global CREDENTIAL_MANAGER_SINGLETON

    if CREDENTIAL_MANAGER_SINGLETON is None:

        if credential_info is None or credential_uris is None:
            errmsg = "The first call to create the CredentialManagerSingleton must include the credential_info and credential_uris parameters."
            raise SemanticError(errmsg)

        SINGLETON_LOCK.acquire()
        try:

            credmgr = CredentialManager()
            credmgr.load_credentials(credential_info, source_uris=credential_uris)
            CREDENTIAL_MANAGER_SINGLETON = credmgr

        finally:
            SINGLETON_LOCK.release()

    rtnval = CREDENTIAL_MANAGER_SINGLETON
    return rtnval


def _require_initialised_singleton() -> CredentialManager:
    """
        Returns the initialised :class:`CredentialManager` singleton.

        :returns: The shared :class:`CredentialManager` instance.
        :raises: SemanticError when the singleton has not been initialised.
    """
    global CREDENTIAL_MANAGER_SINGLETON

    if CREDENTIAL_MANAGER_SINGLETON is None:
        errmsg = (
            "CredentialManagerSingleton has not been initialised. "
            "Call CredentialManagerSingleton(credential_info, credential_uris) first."
        )
        raise SemanticError(errmsg)

    rtnval = CREDENTIAL_MANAGER_SINGLETON
    return rtnval


def get_credentials_by_category(*, category: str) -> List[BaseCredential]:
    """
        Returns credentials matching the requested category. Umbrella categories declared
        in :data:`WELL_KNOWN_CATEGORY_MEMBERSHIP` are expanded into their per-provider
        category list before lookup; per-provider categories are looked up directly.

        :param category: The well-known umbrella category constant or a per-provider category string.

        :returns: The list of matching :class:`BaseCredential` instances (possibly empty).
        :raises: SemanticError when the credential manager singleton has not been initialised.
    """
    credmgr = _require_initialised_singleton()

    targets: List[str] = []
    if category in WELL_KNOWN_CATEGORY_MEMBERSHIP:
        targets = list(WELL_KNOWN_CATEGORY_MEMBERSHIP[category])
    else:
        targets = [category]

    rtnval = credmgr.get_credentials_by_categories(categories=targets)
    return rtnval
