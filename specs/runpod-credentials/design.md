# Design

## Overview

`RunpodApiKeyCredential` is a thin `BaseCredential` subclass wrapping the runpod venue's API
authentication material.  The runpod venue provisioner consumes it via the
`hpc-venue` category filter.

See Also:
- `codecraftai-provisioning/specs/venue-runpod/design.md`
- `codecraftai-credentials/source/packages/ccai/credentials/awsaccesskeycredential.py`

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│        codecraftai-provisioning venue-runpod                     │
│   resolves credential by identifier                      │
└────────────────────────────┬─────────────────────────────┘
                             ▼
                    CredentialManager
                             │
                             ▼
        ┌─────────────────────────────────────────┐
        │     RunpodApiKeyCredential                               │
        │     identifier / categories / token     │
        └─────────────────────────────────────────┘
                             │
                             ▼
                       BaseCredential
```

---

## Data Model

```python
class RunpodApiKeyCredential(BaseCredential):

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
source/packages/ccai/credentials/
├── runpodapikeycredential.py
└── wellknown.py

source/testroots/testbase/ccai/tests/credentials/
├── test_runpodapikeycredential.py
└── test_runpod_credentials_properties.py
```

---

## Testing Strategy

Example-based tests cover: successful construction; `ConfigurationError` when
`categories` lacks `"hpc-venue"`; `ConfigurationError` on empty token; `validate()`
missing-field reporting; `as_dict()` completeness.

Property test (`hypothesis`):

- `test_runpod_token_roundtrip` — generates arbitrary non-empty token strings,
  constructs a credential, serialises via `as_dict()`, reconstructs, and asserts
  field-wise equality.
