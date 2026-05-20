# Design

## Overview

`ProxmoxApiTokenCredential` is a `BaseCredential` subclass wrapping a Proxmox
API token (token id + secret).  The Proxmox venue provisioner consumes it via the
`vm-venue` category filter; the token id carries the `<user>@<realm>!<tokenname>`
form that Proxmox requires in the `Authorization: PVEAPIToken=` header.

See Also:
- `automojo-provisioning/specs/venue-proxmox/design.md`
- `automojo-credentials/source/packages/automojo/credentials/awsaccesskeycredential.py`

---

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│        automojo-provisioning venue-proxmox                 │
│   sends `PVEAPIToken=<token_id>=<secret>` header           │
└────────────────────────────┬───────────────────────────────┘
                             ▼
                    CredentialManager
                             │
                             ▼
   ┌─────────────────────────────────────────────────────┐
   │   ProxmoxApiTokenCredential                         │
   │   identifier / categories /                         │
   │   token_id / secret                                 │
   └─────────────────────────────────────────────────────┘
                             │
                             ▼
                       BaseCredential
```

---

## Data Model

```python
class ProxmoxApiTokenCredential(BaseCredential):

    TOKEN_ID_PATTERN = r"^[^@!]+@[^@!]+![^@!]+$"

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        token_id: str,
        secret: str,
        role: Optional[str] = "priv",
    ) -> None: ...

    @property
    def token_id(self) -> str: ...
    @property
    def secret(self) -> str: ...

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]: ...

    def as_dict(self) -> Dict[str, Any]: ...
```

Required category: `"vm-venue"`.  Token id must match
`<user>@<realm>!<tokenname>`.

---

## Module Layout

```
source/packages/automojo/credentials/
├── proxmoxapitokencredential.py
└── wellknown.py

source/testroots/testbase/automojo/tests/credentials/
├── test_proxmoxapitokencredential.py
└── test_proxmox_credentials_properties.py
```

---

## Testing Strategy

Example-based tests cover: successful construction; `ConfigurationError` on
missing `vm-venue` category; `ConfigurationError` on empty fields;
`ConfigurationError` on malformed `token_id`; `validate()` reports missing
fields; `as_dict()` completeness.

Property test (`hypothesis`):

- `test_proxmox_credential_roundtrip` — generates `(token_id, secret)` pairs
  where `token_id` is composed from random non-`@`/non-`!` strings joined as
  `<user>@<realm>!<tokenname>` and `secret` is a non-empty string; builds,
  serialises, reconstructs, and asserts field-wise equality.
