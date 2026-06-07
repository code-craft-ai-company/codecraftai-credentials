# Design

## Overview

`CoreweaveApiCredential` is a `BaseCredential` subclass wrapping a CoreWeave API
token plus optional organisation scope.  The credential intentionally does **not**
hold a kubeconfig — kubeconfig issuance happens inside
`codecraftai-interop-coreweave` at use time, and the resulting kubeconfig is handed
to `codecraftai-interop-kubernetes` for all subsequent calls.  This keeps the
"one transport per interop package" invariant from §8 of the design plan.

See Also:
- `codecraftai-provisioning/specs/venue-coreweave/design.md`
- `PLAN-VPN-AND-CLOUD-PROVISIONING.md` §7.6 (CoreWeave auth decision)
- `codecraftai-credentials/source/packages/ccai/credentials/awsaccesskeycredential.py`

---

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│      codecraftai-provisioning venue-coreweave                 │
│   selects credential by identifier (hpc-venue category)    │
└────────────────────────────┬───────────────────────────────┘
                             ▼
                    CredentialManager
                             │
                             ▼
   ┌─────────────────────────────────────────────────────┐
   │   CoreweaveApiCredential                            │
   │   identifier / categories /                         │
   │   token / organization_id?                          │
   └────────────────────────┬────────────────────────────┘
                             │ used by
                             ▼
   ┌─────────────────────────────────────────────────────┐
   │   codecraftai-interop-coreweave                        │
   │   exchanges (token, org) → kubeconfig at use time   │
   └────────────────────────┬────────────────────────────┘
                             ▼
   ┌─────────────────────────────────────────────────────┐
   │   codecraftai-interop-kubernetes (all K8s calls)       │
   └─────────────────────────────────────────────────────┘
```

---

## Data Model

```python
class CoreweaveApiCredential(BaseCredential):

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        token: str,
        organization_id: Optional[str] = None,
        role: Optional[str] = "priv",
    ) -> None: ...

    @property
    def token(self) -> str: ...
    @property
    def organization_id(self) -> Optional[str]: ...

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]: ...

    def as_dict(self) -> Dict[str, Any]: ...
```

Required category: `"hpc-venue"`.

---

## Module Layout

```
source/packages/ccai/credentials/
├── coreweaveapicredential.py
└── wellknown.py

source/testroots/testbase/ccai/tests/credentials/
├── test_coreweaveapicredential.py
└── test_coreweave_credentials_properties.py
```

---

## Testing Strategy

Example-based tests cover: successful construction with and without
`organization_id`; `ConfigurationError` when `categories` lacks `"hpc-venue"`;
`ConfigurationError` on empty `token`; `validate()` reports the missing `token`
field; `as_dict()` round-trips both `organization_id=None` and a non-empty value.

Property test (`hypothesis`):

- `test_coreweave_credential_roundtrip` — generates `(token, organization_id)`
  tuples where `token` is non-empty and `organization_id` is either `None` or a
  non-empty string; builds, serialises, reconstructs, and asserts field-wise
  equality.
