# Design

## Overview

Two new `BaseCredential` subclasses model GCP venue authentication:

- `GcpServiceAccountKeyCredential` — wraps the contents of a service-account JSON
  key (project, client email, private key id, private key, token uri).
- `GcpWorkloadIdentityCredential` — wraps a Workload Identity Federation assertion
  (audience, subject token type, target service account).

Both follow `awsaccesskeycredential.py` conventions: keyword-only constructor,
category enforcement in `__init__`, read-only properties, `validate()` classmethod,
and `as_dict()` override.

See Also:
- `codecraftai-provisioning/specs/venue-gcp/design.md`
- `codecraftai-credentials/source/packages/ccai/credentials/awsaccesskeycredential.py`

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│            codecraftai-provisioning venue-gcp                  │
│   resolves credential by identifier + cloud-venue filter    │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                    CredentialManager
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌──────────────────────────┐   ┌──────────────────────────────┐
│ GcpServiceAccountKey-    │   │ GcpWorkloadIdentityCredential│
│   Credential             │   │                              │
│ project_id, client_email,│   │ audience,                    │
│ private_key_id,          │   │ subject_token_type,          │
│ private_key, token_uri   │   │ service_account_email,       │
│                          │   │ token_url                    │
└──────────────────────────┘   └──────────────────────────────┘
            │                                 │
            └────────────────┬────────────────┘
                             ▼
                       BaseCredential
```

---

## Data Model

### `GcpServiceAccountKeyCredential`

```python
class GcpServiceAccountKeyCredential(BaseCredential):

    DEFAULT_TOKEN_URI = "https://oauth2.googleapis.com/token"

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        project_id: str,
        client_email: str,
        private_key_id: str,
        private_key: str,
        token_uri: Optional[str] = None,
        role: Optional[str] = "priv",
    ) -> None: ...

    @property
    def project_id(self) -> str: ...
    @property
    def client_email(self) -> str: ...
    @property
    def private_key_id(self) -> str: ...
    @property
    def private_key(self) -> str: ...
    @property
    def token_uri(self) -> str: ...
```

### `GcpWorkloadIdentityCredential`

```python
class GcpWorkloadIdentityCredential(BaseCredential):

    DEFAULT_TOKEN_URL = "https://sts.googleapis.com/v1/token"

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        audience: str,
        subject_token_type: str,
        service_account_email: str,
        token_url: Optional[str] = None,
        role: Optional[str] = "priv",
    ) -> None: ...
```

Both classes override `validate(cls, cred_info)` and `as_dict()`.

---

## Module Layout

```
source/packages/ccai/credentials/
├── gcpserviceaccountkeycredential.py
├── gcpworkloadidentitycredential.py
└── wellknown.py

source/testroots/testbase/ccai/tests/credentials/
├── test_gcpserviceaccountkeycredential.py
├── test_gcpworkloadidentitycredential.py
└── test_gcp_credentials_properties.py
```

---

## Testing Strategy

Example-based tests cover:

- Constructor success on a known-good field set per class.
- `ConfigurationError` when `categories` lacks `"cloud-venue"`.
- `ConfigurationError` on empty required strings.
- `token_uri` / `token_url` default population when omitted.
- `validate()` error-list correctness.
- `as_dict()` completeness.

Property tests (`hypothesis`) for Requirement 4:

- `test_gcp_service_account_key_roundtrip` — generate field tuples, build, serialise,
  reconstruct, compare via a `_fields_equal` helper.
- `test_gcp_workload_identity_roundtrip` — same shape for the WIF credential.
