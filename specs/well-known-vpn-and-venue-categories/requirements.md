# Requirements

## Introduction

The `well-known-vpn-and-venue-categories` feature extends
`automojo-credentials/wellknown.py` so the credential manager exposes
named categories that consumers can use to find credentials by
purpose without knowing the per-provider class names. Per §8
commitment "Credentials are values, not strings," the credential
manager is the single source of truth for credential lookup, and the
category vocabulary is the API.

The categories registered by this feature are:

- `vpn` — any mesh-VPN credential.
- `mesh` — alias of `vpn` for ergonomic search.
- `cloud-venue` — any public-cloud venue credential
  (AWS, Azure, GCP, DO, Hetzner, Linode, Oracle, Equinix, Vultr).
- `vm-venue` — any private-VM hypervisor credential
  (VSphere, Proxmox, libvirt, Xen, Hyper-V, Nutanix).
- `hpc-venue` — any HPC/AI-cloud credential
  (CoreWeave, Lambda Labs, Crusoe, Nebius, RunPod).

This spec adds the category constants and the lookup helpers; the
individual credential classes (in their own specs) reference the
constants when declaring their categories.

**See Also:** [tailscale-credentials](../tailscale-credentials/design.md),
[twingate-credentials](../twingate-credentials/design.md).

---

## Requirements

### Requirement 1: Category Constants

**User Story:** As a credential consumer, I want named constants for
the well-known categories so I never typo a string.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare the following string constants in
   `wellknown.py`:
   - `CATEGORY_VPN = "vpn"`
   - `CATEGORY_MESH = "mesh"`
   - `CATEGORY_CLOUD_VENUE = "cloud-venue"`
   - `CATEGORY_VM_VENUE = "vm-venue"`
   - `CATEGORY_HPC_VENUE = "hpc-venue"`
2. THE SYSTEM SHALL export them via `__all__`.

---

### Requirement 2: Provider-Category Mapping Registry

**User Story:** As a credential consumer, I want to query "which
credential classes belong to category X" so I can iterate without
hardcoding class names.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare a module-level mapping
   `WELL_KNOWN_CATEGORY_MEMBERSHIP: Dict[str, List[str]]` keyed by
   the category constant, mapping to a list of the per-provider
   category strings under that umbrella.
2. THE SYSTEM SHALL include at minimum:
   - `CATEGORY_VPN → ["tailscale-authkey", "tailscale-oauth",
     "twingate-service-account"]`
   - `CATEGORY_MESH → ["tailscale-authkey", "tailscale-oauth",
     "twingate-service-account"]`
   - `CATEGORY_CLOUD_VENUE → ["aws-access-key", ...]` populated as
     each venue credential spec lands.
   - `CATEGORY_VM_VENUE → []` populated as each VM-venue credential
     spec lands.
   - `CATEGORY_HPC_VENUE → []` populated as each HPC-venue
     credential spec lands.

---

### Requirement 3: Credential Manager Helper

**User Story:** As a control-plane implementer, I want a single
helper to get the first credential of a category from the singleton.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare
   `get_credentials_by_category(category: str) -> List[BaseCredential]`
   in `wellknown.py`, returning credentials of the given category
   from the `CredentialManagerSingleton`.
2. WHEN the category is one of the well-known umbrella constants
   (`vpn`, `mesh`, `cloud-venue`, `vm-venue`, `hpc-venue`) THE
   SYSTEM SHALL expand the request via
   `WELL_KNOWN_CATEGORY_MEMBERSHIP` and return the union of all
   per-provider matches.
3. WHEN the category is a per-provider category (e.g.
   `"tailscale-oauth"`) THE SYSTEM SHALL return only credentials
   tagged with that exact category.

---

### Requirement 4: Singleton Behaviour Preserved

**User Story:** As a downstream consumer, I want the existing
`CredentialManagerSingleton` semantics unchanged.

#### Acceptance Criteria

1. THE SYSTEM SHALL NOT modify the existing
   `CredentialManagerSingleton(credential_info, credential_uris)`
   signature or behaviour.
2. IF a caller invokes `get_credentials_by_category` before the
   singleton has been initialised THEN THE SYSTEM SHALL raise
   `SemanticError` with a message pointing to the initialisation
   call.
