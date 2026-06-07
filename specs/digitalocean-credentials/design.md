# Design

## Overview

`DigitalOceanApiTokenCredential` is a thin `BaseCredential` subclass wrapping a
DigitalOcean personal-access token.  The DigitalOcean venue provisioner consumes it
via the `cloud-venue` category filter and uses the `token` property as the bearer
credential for `pydo` / REST calls.

See Also:
- `codecraftai-provisioning/specs/venue-digitalocean/design.md`
- `codecraftai-credentials/source/packages/ccai/credentials/awsaccesskeycredential.py`

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│      codecraftai-provisioning venue-digitalocean           │
│   resolves credential by identifier and uses .token     │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
                    CredentialManager
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │   DigitalOceanApiTokenCredential       │
        │   identifier / categories / token      │
        └────────────────────────────────────────┘
                             │
                             ▼
                       BaseCredential
```

---

## Data Model

```python
class DigitalOceanApiTokenCredential(BaseCredential):

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
├── digitaloceanapitokencredential.py
└── wellknown.py

source/testroots/testbase/ccai/tests/credentials/
├── test_digitaloceanapitokencredential.py
└── test_digitalocean_credentials_properties.py
```

---

## Testing Strategy

Example-based tests cover:

- Successful construction.
- `ConfigurationError` when `categories` lacks `"cloud-venue"`.
- `ConfigurationError` on empty `token`.
- `validate()` reports the missing `token` field.
- `as_dict()` includes `token` plus inherited base-credential fields.

Property test (`hypothesis`):

- `test_digitalocean_token_roundtrip` — generates arbitrary non-empty token strings,
  constructs a credential, serialises via `as_dict()`, reconstructs, and asserts
  field-wise equality.
