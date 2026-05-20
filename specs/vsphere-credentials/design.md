# Design

## Overview

`VSphereCredential` is a `BaseCredential` subclass wrapping VSphere SSO/basic
authentication material (username + password and/or an SSO token).  It replaces
the current pattern of overloading `BasicCredential` for VSphere with a typed
class registered under the `vm-venue` category.

See Also:
- `automojo-provisioning/specs/venue-vsphere/design.md`
- `automojo-interop-vsphere/specs/vsphere-client-rest-base/design.md`
- `automojo-credentials/source/packages/automojo/credentials/basiccredential.py`

---

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│        automojo-interop-vsphere VSphereClient              │
│   _authenticate(...) consumes (username, password|token)   │
└────────────────────────────┬───────────────────────────────┘
                             ▼
                    CredentialManager
                             │
                             ▼
   ┌─────────────────────────────────────────────────────┐
   │   VSphereCredential                                 │
   │   identifier / categories /                         │
   │   username / password? / sso_token?                 │
   └─────────────────────────────────────────────────────┘
                             │
                             ▼
                       BaseCredential
```

---

## Data Model

```python
class VSphereCredential(BaseCredential):

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        username: str,
        password: Optional[str] = None,
        sso_token: Optional[str] = None,
        role: Optional[str] = "priv",
    ) -> None: ...

    @property
    def username(self) -> str: ...
    @property
    def password(self) -> Optional[str]: ...
    @property
    def sso_token(self) -> Optional[str]: ...

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]: ...

    def as_dict(self) -> Dict[str, Any]: ...
```

Required category: `"vm-venue"`.  Exactly one of `password` or `sso_token` must be
non-empty; both may be present (the interop client prefers `sso_token` when both
are set).

---

## Module Layout

```
source/packages/automojo/credentials/
├── vspherecredential.py
└── wellknown.py

source/testroots/testbase/automojo/tests/credentials/
├── test_vspherecredential.py
└── test_vsphere_credentials_properties.py
```

---

## Testing Strategy

Example-based tests cover: construction with password-only; construction with
sso-token-only; construction with both fields populated; `ConfigurationError`
when `categories` lacks `vm-venue`; `ConfigurationError` on empty `username`;
`ConfigurationError` when both password and sso_token are missing; `validate()`
field-omission reporting; `as_dict()` round-trips `None`-valued fields losslessly.

Property test (`hypothesis`):

- `test_vsphere_credential_roundtrip` — generates `(username, password,
  sso_token)` tuples where `username` is non-empty and at least one of the other
  two is non-empty; builds, serialises, reconstructs, and asserts field-wise
  equality.
