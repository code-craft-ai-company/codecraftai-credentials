# Design

## Overview

Two new `BaseCredential` subclasses model Azure cloud-venue authentication:

- `AzureServicePrincipalCredential` — app-style auth with a client secret.
- `AzureManagedIdentityCredential` — assertion that the runtime hosts a managed
  identity; resolved at use time.

Both follow the patterns established by `awsaccesskeycredential.py` and
`azureclientsecretcredential.py`: keyword-only constructor, category validation in
`__init__`, read-only properties, `validate(cred_info)` classmethod, and `as_dict()`
override that extends the base mapping.

See Also:
- `automojo-provisioning/specs/venue-azure/design.md`
- `automojo-credentials/source/packages/automojo/credentials/azureclientsecretcredential.py`

---

## Architecture

```
┌───────────────────────────────────────────────────────────────┐
│              automojo-provisioning venue-azure                │
│   resolves credential by identifier from CredentialManager    │
└───────────────────────────┬───────────────────────────────────┘
                            │ get_credential_by_identifier(...)
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                  CredentialManager                            │
│   load_credentials(...) dispatches by category                │
└───────────────────────────┬───────────────────────────────────┘
                            │ instantiate
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌─────────────────────────┐   ┌────────────────────────────────┐
│ AzureServicePrincipal-  │   │ AzureManagedIdentityCredential │
│   Credential            │   │                                │
│ tenant_id / client_id / │   │ client_id? / resource_id?      │
│ client_secret           │   │ (no secret material stored)    │
└─────────────────────────┘   └────────────────────────────────┘
            │                               │
            └───────────────┬───────────────┘
                            ▼
                     BaseCredential
                  identifier / categories / role
```

---

## Data Model

### `AzureServicePrincipalCredential`

```python
class AzureServicePrincipalCredential(BaseCredential):

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        tenant_id: str,
        client_id: str,
        client_secret: str,
        role: Optional[str] = "priv",
    ) -> None: ...

    @property
    def tenant_id(self) -> str: ...
    @property
    def client_id(self) -> str: ...
    @property
    def client_secret(self) -> str: ...

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]: ...

    def as_dict(self) -> Dict[str, Any]: ...
```

Required category: `"cloud-venue"`.  The class also accepts the legacy
`"azure-service-principal"` discriminator alongside `"cloud-venue"`.

### `AzureManagedIdentityCredential`

```python
class AzureManagedIdentityCredential(BaseCredential):

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        client_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        role: Optional[str] = "priv",
    ) -> None: ...

    @property
    def client_id(self) -> Optional[str]: ...
    @property
    def resource_id(self) -> Optional[str]: ...

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]: ...

    def as_dict(self) -> Dict[str, Any]: ...
```

At least one of `client_id` / `resource_id` MUST be provided; both may be set when a
user-assigned identity is being referenced by both selectors.

---

## Module Layout

```
source/packages/automojo/credentials/
├── azureserviceprincipalcredential.py    ← AzureServicePrincipalCredential
├── azuremanagedidentitycredential.py     ← AzureManagedIdentityCredential
└── wellknown.py                          ← category map registration

source/testroots/testbase/automojo/tests/credentials/
├── test_azureserviceprincipalcredential.py
├── test_azuremanagedidentitycredential.py
└── test_azure_credentials_properties.py  ← hypothesis property tests
```

File names follow the project standard: lowercase, no underscores, named after the
class.

---

## Testing Strategy

Example-based tests cover:

- Constructor success on a known-good field set.
- `ConfigurationError` when `categories` lacks `cloud-venue`.
- `ConfigurationError` on empty mandatory strings (service principal).
- `ConfigurationError` when both selectors are `None` (managed identity).
- `as_dict()` includes every declared field.
- `validate(cred_info)` returns `(errors, warnings)` with the right message set for
  each missing-field permutation.

Property tests (`hypothesis`) cover Requirement 4:

- `test_service_principal_roundtrip` — generate non-empty strings for `tenant_id`,
  `client_id`, `client_secret`, build a credential, serialise, reconstruct, assert
  equality of all fields.
- `test_managed_identity_roundtrip` — generate `(client_id, resource_id)` pairs where
  at least one is non-`None`; serialise / reconstruct; assert equality.

Equality for tests is defined via a small `_fields_equal(a, b)` helper that compares
the public properties — credential classes themselves do not override `__eq__` to
avoid changing identity semantics elsewhere.
