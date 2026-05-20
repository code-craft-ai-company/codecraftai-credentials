# Design

## Overview

`EquinixMetalApiTokenCredential` is a thin `BaseCredential` subclass wrapping the equinix venue's API
authentication material.  The equinix venue provisioner consumes it via the
`cloud-venue` category filter.

See Also:
- `automojo-provisioning/specs/venue-equinix-metal/design.md`
- `automojo-credentials/source/packages/automojo/credentials/awsaccesskeycredential.py`

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│        automojo-provisioning venue-equinix-metal                     │
│   resolves credential by identifier                      │
└────────────────────────────┬─────────────────────────────┘
                             ▼
                    CredentialManager
                             │
                             ▼
        ┌─────────────────────────────────────────┐
        │     EquinixMetalApiTokenCredential                               │
        │     identifier / categories / token     │
        └─────────────────────────────────────────┘
                             │
                             ▼
                       BaseCredential
```

---

## Data Model

```python
class EquinixMetalApiTokenCredential(BaseCredential):

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        token: str,
        role: Optional[str] = "priv",
    ) -> None: ...

    @property
    def token(self) -> str: ...

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]: ...

    def as_dict(self) -> Dict[str, Any]: ...
```

Required category: `"cloud-venue"`.

---

## Module Layout

```
source/packages/automojo/credentials/
├── equinixmetalapitokencredential.py
└── wellknown.py

source/testroots/testbase/automojo/tests/credentials/
├── test_equinixmetalapitokencredential.py
└── test_equinix_credentials_properties.py
```

---

## Testing Strategy

Example-based tests cover: successful construction; `ConfigurationError` when
`categories` lacks `"cloud-venue"`; `ConfigurationError` on empty token; `validate()`
missing-field reporting; `as_dict()` completeness.

Property test (`hypothesis`):

- `test_equinix_token_roundtrip` — generates arbitrary non-empty token strings,
  constructs a credential, serialises via `as_dict()`, reconstructs, and asserts
  field-wise equality.
