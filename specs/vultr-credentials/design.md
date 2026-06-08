# Design

## Overview

`VultrApiKeyCredential` is a thin `BaseCredential` subclass wrapping the vultr venue's API
authentication material.  The vultr venue provisioner consumes it via the
`cloud-venue` category filter.

See Also:
- `codecraftai-provisioning/specs/venue-vultr/design.md`
- `codecraftai-credentials/source/packages/ccai/credentials/awsaccesskeycredential.py`

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│        codecraftai-provisioning venue-vultr                     │
│   resolves credential by identifier                      │
└────────────────────────────┬─────────────────────────────┘
                             ▼
                    CredentialManager
                             │
                             ▼
        ┌─────────────────────────────────────────┐
        │     VultrApiKeyCredential                               │
        │     identifier / categories / token     │
        └─────────────────────────────────────────┘
                             │
                             ▼
                       BaseCredential
```

---

## Data Model

```python
class VultrApiKeyCredential(BaseCredential):

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
source/packages/ccai/credentials/
├── vultrapikeycredential.py
└── wellknown.py

source/testroots/testbase/ccai/tests/credentials/
├── test_vultrapikeycredential.py
└── test_vultr_credentials_properties.py
```

---

## Testing Strategy

Example-based tests cover: successful construction; `ConfigurationError` when
`categories` lacks `"cloud-venue"`; `ConfigurationError` on empty token; `validate()`
missing-field reporting; `as_dict()` completeness.

Property test (`hypothesis`):

- `test_vultr_token_roundtrip` — generates arbitrary non-empty token strings,
  constructs a credential, serialises via `as_dict()`, reconstructs, and asserts
  field-wise equality.
