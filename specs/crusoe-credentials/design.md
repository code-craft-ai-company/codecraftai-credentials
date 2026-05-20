# Design

## Overview

`CrusoeApiKeyCredential` is a `BaseCredential` subclass wrapping the two-field
Crusoe Cloud API credential (`access_key_id`, `secret`).  The Crusoe venue
provisioner consumes it via the `cloud-venue` (or `hpc-venue`) category filter.

See Also:
- `automojo-provisioning/specs/venue-crusoe/design.md`
- `automojo-credentials/source/packages/automojo/credentials/awsaccesskeycredential.py`

---

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│        automojo-provisioning venue-crusoe                  │
│   signs api.crusoecloud.com requests with the two fields   │
└────────────────────────────┬───────────────────────────────┘
                             ▼
                    CredentialManager
                             │
                             ▼
   ┌─────────────────────────────────────────────────────┐
   │   CrusoeApiKeyCredential                            │
   │   identifier / categories /                         │
   │   access_key_id / secret                            │
   └─────────────────────────────────────────────────────┘
                             │
                             ▼
                       BaseCredential
```

---

## Data Model

```python
class CrusoeApiKeyCredential(BaseCredential):

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        access_key_id: str,
        secret: str,
        role: Optional[str] = "priv",
    ) -> None: ...

    @property
    def access_key_id(self) -> str: ...
    @property
    def secret(self) -> str: ...

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]: ...

    def as_dict(self) -> Dict[str, Any]: ...
```

At least one of `"cloud-venue"` or `"hpc-venue"` must appear in `categories`.

---

## Module Layout

```
source/packages/automojo/credentials/
├── crusoeapikeycredential.py
└── wellknown.py

source/testroots/testbase/automojo/tests/credentials/
├── test_crusoeapikeycredential.py
└── test_crusoe_credentials_properties.py
```

---

## Testing Strategy

Example-based tests cover: successful construction; `ConfigurationError` when
neither category is present; `ConfigurationError` on empty `access_key_id` /
`secret`; `validate()` reports the right missing fields; `as_dict()` completeness.

Property test (`hypothesis`):

- `test_crusoe_credential_roundtrip` — generates `(access_key_id, secret)` pairs
  of non-empty strings; builds, serialises, reconstructs, and asserts field-wise
  equality.
