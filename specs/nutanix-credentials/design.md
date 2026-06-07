# Design

## Overview

`NutanixPrismCredential` is a `BaseCredential` subclass wrapping Nutanix Prism
Central authentication: username + password plus the Prism Central endpoint URL.
The Nutanix venue provisioner consumes it via the `vm-venue` category filter.

See Also:
- `codecraftai-provisioning/specs/venue-nutanix/design.md`
- `codecraftai-credentials/source/packages/ccai/credentials/basiccredential.py`

---

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│        codecraftai-provisioning venue-nutanix                 │
│   POSTs to <endpoint>/api/nutanix/... with basic auth      │
└────────────────────────────┬───────────────────────────────┘
                             ▼
                    CredentialManager
                             │
                             ▼
   ┌─────────────────────────────────────────────────────┐
   │   NutanixPrismCredential                            │
   │   identifier / categories /                         │
   │   username / password / endpoint                    │
   └─────────────────────────────────────────────────────┘
                             │
                             ▼
                       BaseCredential
```

---

## Data Model

```python
class NutanixPrismCredential(BaseCredential):

    ALLOWED_ENDPOINT_PREFIXES = ("http://", "https://")

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        username: str,
        password: str,
        endpoint: str,
        role: Optional[str] = "priv",
    ) -> None: ...

    @property
    def username(self) -> str: ...
    @property
    def password(self) -> str: ...
    @property
    def endpoint(self) -> str: ...

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]: ...

    def as_dict(self) -> Dict[str, Any]: ...
```

Required category: `"vm-venue"`.

---

## Module Layout

```
source/packages/ccai/credentials/
├── nutanixprismcredential.py
└── wellknown.py

source/testroots/testbase/ccai/tests/credentials/
├── test_nutanixprismcredential.py
└── test_nutanix_credentials_properties.py
```

---

## Testing Strategy

Example-based tests cover: successful construction with both http and https
endpoints; `ConfigurationError` on missing `vm-venue` category; `ConfigurationError`
on empty fields; `ConfigurationError` on non-http(s) endpoint;
`validate()` reports missing fields; `as_dict()` completeness.

Property test (`hypothesis`):

- `test_nutanix_credential_roundtrip` — generates `(username, password,
  endpoint)` tuples where `endpoint` is composed as
  `"<scheme>://<host>:<port>"` with scheme drawn from `{http, https}` and other
  strings non-empty; builds, serialises, reconstructs, and asserts field-wise
  equality.
