# Design

## Overview

`well-known-vpn-and-venue-categories` extends
`codecraftai-credentials/source/packages/ccai/credentials/wellknown.py`
with five umbrella category constants (`vpn`, `mesh`, `cloud-venue`,
`vm-venue`, `hpc-venue`), a membership registry mapping each umbrella
to its per-provider categories, and a `get_credentials_by_category`
helper that the credential manager singleton can serve from.

The intent is to let consumers say "give me any VPN credential" or
"give me any cloud-venue credential" without knowing the credential
class names. This honours the §8 commitment "Credentials are values,
not strings."

The membership registry is *additive*. Each per-provider credential
spec (in this repository and elsewhere) lists itself under the right
umbrella. This module ships with the seed entries for the VPN
credentials (because those land in the same milestone) and empty
lists for the venue umbrellas.

**See Also:** [tailscale-credentials](../tailscale-credentials/design.md),
[twingate-credentials](../twingate-credentials/design.md).

---

## Architecture

```
+----------------------------------------+
| wellknown.py                           |
|                                        |
|  Category constants:                   |
|    CATEGORY_VPN, CATEGORY_MESH,        |
|    CATEGORY_CLOUD_VENUE,               |
|    CATEGORY_VM_VENUE,                  |
|    CATEGORY_HPC_VENUE                  |
|                                        |
|  WELL_KNOWN_CATEGORY_MEMBERSHIP:       |
|    {vpn: [tailscale-authkey, ...],     |
|     cloud-venue: [aws-access-key,...], |
|     ...}                               |
|                                        |
|  get_credentials_by_category(category) |
|    expands umbrella -> per-provider    |
|    fetches from CredentialManager-     |
|    Singleton                           |
+--------------------+-------------------+
                     |
                     v
+----------------------------------------+
| CredentialManagerSingleton             |
|   .get_by_categories([...])            |
+----------------------------------------+
```

---

## Data Model

```python
# wellknown.py additions

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
    CATEGORY_CLOUD_VENUE: [
        "aws-access-key",
        # populated as venue credential specs land:
        # "azure-service-principal", "gcp-service-account-key", ...
    ],
    CATEGORY_VM_VENUE: [
        # populated as VM-venue credential specs land:
        # "vsphere-basic", "proxmox-api-token", ...
    ],
    CATEGORY_HPC_VENUE: [
        # populated as HPC-venue credential specs land:
        # "coreweave-api", "lambdalabs-api-key", ...
    ],
}


def get_credentials_by_category(*, category: str) -> List[BaseCredential]:
    """
        Returns credentials matching the requested category. Umbrella
        categories are expanded via WELL_KNOWN_CATEGORY_MEMBERSHIP.

        :param category: Category constant or per-provider category string.

        :returns: List of matching BaseCredential instances.
        :raises: SemanticError when the singleton has not been initialised.
    """
    credmgr = _require_initialised_singleton()
    targets: List[str] = []
    if category in WELL_KNOWN_CATEGORY_MEMBERSHIP:
        targets = list(WELL_KNOWN_CATEGORY_MEMBERSHIP[category])
    else:
        targets = [category]
    rtnval = credmgr.get_credentials_by_categories(categories=targets)
    return rtnval


def _require_initialised_singleton() -> CredentialManager:
    global CREDENTIAL_MANAGER_SINGLETON
    if CREDENTIAL_MANAGER_SINGLETON is None:
        errmsg = (
            "CredentialManagerSingleton has not been initialised. "
            "Call CredentialManagerSingleton(credential_info, credential_uris) "
            "first."
        )
        raise SemanticError(errmsg)
    rtnval = CREDENTIAL_MANAGER_SINGLETON
    return rtnval
```

---

## Module Layout

```
codecraftai-credentials/source/packages/ccai/credentials/
  wellknown.py            (extended in place)
  credentialmanager.py    (existing — may need a get_credentials_by_categories
                           helper if not already present)
```

If `CredentialManager` does not yet expose
`get_credentials_by_categories(categories=...)`, add it alongside this
feature with the simple implementation
`[c for c in self._credentials if any(cat in c.categories for cat in categories)]`.

---

## See Also

- [tailscale-credentials](../tailscale-credentials/design.md) — seeds
  the `vpn` / `mesh` membership.
- [twingate-credentials](../twingate-credentials/design.md) — seeds
  the `vpn` / `mesh` membership.
- [vpn-control-plane-protocol](../../../codecraftai-interfaces/specs/vpn-control-plane-protocol/design.md)
  — the canonical consumer of `get_credentials_by_category("vpn")`.

---

## Testing Strategy

- **Constants exported test.** All five constants importable from
  `wellknown` and listed in `__all__`.
- **Membership seed test.** `WELL_KNOWN_CATEGORY_MEMBERSHIP["vpn"]`
  contains the three VPN per-provider categories.
- **Umbrella expansion test.** With a singleton populated by mixed
  credentials (Tailscale + AWS), `get_credentials_by_category(category="vpn")`
  returns only the Tailscale credential; `get_credentials_by_category(category="cloud-venue")`
  returns only the AWS credential.
- **Per-provider lookup test.** `get_credentials_by_category(category="tailscale-oauth")`
  returns only the OAuth credential, never the static-key credential.
- **Uninitialised singleton test.** Calling the helper before
  initialisation raises `SemanticError` with a descriptive message.
- **No property tests required** — the lookup is a small,
  declarative mapping; example-based coverage is sufficient.
