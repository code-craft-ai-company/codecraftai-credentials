"""
    .. module:: venueregistry
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Registry that maps a venue credential ``provider`` discriminator to
                   its concrete credential class.

    The venue umbrella categories (``cloud-venue`` / ``vm-venue`` / ``hpc-venue``)
    are shared by many providers whose credential payloads can be structurally
    identical (for example DigitalOcean, Hetzner, Linode and Vultr all serialize
    as ``{category: cloud-venue, token: ...}``).  A credential definition therefore
    carries an explicit ``provider`` field so the :class:`CredentialManager` can
    dispatch to the correct concrete class.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Dict, Type

from ccai.credentials.basecredential import BaseCredential

from ccai.credentials.azuremanagedidentitycredential import AzureManagedIdentityCredential
from ccai.credentials.azureserviceprincipalcredential import AzureServicePrincipalCredential
from ccai.credentials.coreweaveapicredential import CoreweaveApiCredential
from ccai.credentials.crusoeapikeycredential import CrusoeApiKeyCredential
from ccai.credentials.digitaloceanapitokencredential import DigitalOceanApiTokenCredential
from ccai.credentials.equinixmetalapitokencredential import EquinixMetalApiTokenCredential
from ccai.credentials.gcpserviceaccountkeycredential import GcpServiceAccountKeyCredential
from ccai.credentials.gcpworkloadidentitycredential import GcpWorkloadIdentityCredential
from ccai.credentials.hetznerapitokencredential import HetznerApiTokenCredential
from ccai.credentials.lambdalabsapikeycredential import LambdalabsApiKeyCredential
from ccai.credentials.linodeapitokencredential import LinodeApiTokenCredential
from ccai.credentials.nebiusserviceaccountcredential import NebiusServiceAccountCredential
from ccai.credentials.nutanixprismcredential import NutanixPrismCredential
from ccai.credentials.oraclecloudapikeycredential import OracleCloudApiKeyCredential
from ccai.credentials.proxmoxapitokencredential import ProxmoxApiTokenCredential
from ccai.credentials.runpodapikeycredential import RunpodApiKeyCredential
from ccai.credentials.vspherecredential import VSphereCredential
from ccai.credentials.vultrapikeycredential import VultrApiKeyCredential


CATEGORY_CLOUD_VENUE = "cloud-venue"
CATEGORY_VM_VENUE = "vm-venue"
CATEGORY_HPC_VENUE = "hpc-venue"

VENUE_UMBRELLA_CATEGORIES = {
    CATEGORY_CLOUD_VENUE,
    CATEGORY_VM_VENUE,
    CATEGORY_HPC_VENUE,
}


# Maps the ``provider`` discriminator carried by a venue credential definition to
# the concrete credential class that should be constructed for it.
VENUE_PROVIDER_REGISTRY: Dict[str, Type[BaseCredential]] = {
    "azure-managed-identity": AzureManagedIdentityCredential,
    "azure-service-principal": AzureServicePrincipalCredential,
    "coreweave": CoreweaveApiCredential,
    "crusoe": CrusoeApiKeyCredential,
    "digitalocean": DigitalOceanApiTokenCredential,
    "equinix-metal": EquinixMetalApiTokenCredential,
    "gcp-service-account": GcpServiceAccountKeyCredential,
    "gcp-workload-identity": GcpWorkloadIdentityCredential,
    "hetzner": HetznerApiTokenCredential,
    "lambdalabs": LambdalabsApiKeyCredential,
    "linode": LinodeApiTokenCredential,
    "nebius": NebiusServiceAccountCredential,
    "nutanix-prism": NutanixPrismCredential,
    "oracle-cloud": OracleCloudApiKeyCredential,
    "proxmox": ProxmoxApiTokenCredential,
    "runpod": RunpodApiKeyCredential,
    "vsphere": VSphereCredential,
    "vultr": VultrApiKeyCredential,
}


def known_providers() -> str:
    """
        Returns a sorted, comma-joined list of the registered venue provider names,
        for use in error messages.

        :returns: The known provider discriminators as a display string.
    """
    rtnval = ", ".join(sorted(VENUE_PROVIDER_REGISTRY.keys()))
    return rtnval
