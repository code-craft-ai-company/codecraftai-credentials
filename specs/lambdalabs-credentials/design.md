# Design

## Overview

`LambdalabsApiKeyCredential` is a thin `BaseCredential` subclass wrapping the lambdalabs venue's API
authentication material.  The lambdalabs venue provisioner consumes it via the
`hpc-venue` category filter.

See Also:
- `automojo-provisioning/specs/venue-lambdalabs/design.md`
- `automojo-credentials/source/packages/automojo/credentials/awsaccesskeycredential.py`

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│        automojo-provisioning venue-lambdalabs                     │
│   resolves credential by identifier                      │
└────────────────────────────┬─────────────────────────────┘
                             ▼
                    CredentialManager
                             │
                             ▼
        ┌─────────────────────────────────────────┐
        │     LambdalabsApiKeyCredential                               │
        │     identifier / categories / token     │
        └─────────────────────────────────────────┘
                             │
                             ▼
                       BaseCredential
```

---

## Data Model

```python
class LambdalabsApiKeyCredential(BaseCredential):

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

Required category: `"hpc-venue"`.

---

## Module Layout

```
source/packages/automojo/credentials/
├── lambdalabsapikeycredential.py
└── wellknown.py

source/testroots/testbase/automojo/tests/credentials/
├── test_lambdalabsapikeycredential.py
└── test_lambdalabs_credentials_properties.py
```

---

## Testing Strategy

Example-based tests cover: successful construction; `ConfigurationError` when
`categories` lacks `"hpc-venue"`; `ConfigurationError` on empty token; `validate()`
missing-field reporting; `as_dict()` completeness.

Property test (`hypothesis`):

- `test_lambdalabs_token_roundtrip` — generates arbitrary non-empty token strings,
  constructs a credential, serialises via `as_dict()`, reconstructs, and asserts
  field-wise equality.
