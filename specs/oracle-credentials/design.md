# Design

## Overview

`OracleCloudApiKeyCredential` is a `BaseCredential` subclass wrapping the four-field
OCI API-key credential (tenancy OCID, user OCID, PEM private key body, key
fingerprint) plus an optional `passphrase` for encrypted keys.  The Oracle venue
provisioner consumes it via the `cloud-venue` category filter.

See Also:
- `automojo-provisioning/specs/venue-oracle/design.md`
- `automojo-credentials/source/packages/automojo/credentials/awsaccesskeycredential.py`

---

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│        automojo-provisioning venue-oracle                  │
│   builds an oci.Signer from the credential's four fields   │
└────────────────────────────┬───────────────────────────────┘
                             ▼
                    CredentialManager
                             │
                             ▼
   ┌─────────────────────────────────────────────────────┐
   │   OracleCloudApiKeyCredential                       │
   │   identifier / categories /                         │
   │   tenancy_ocid / user_ocid / private_key /          │
   │   fingerprint / passphrase?                         │
   └─────────────────────────────────────────────────────┘
                             │
                             ▼
                       BaseCredential
```

---

## Data Model

```python
class OracleCloudApiKeyCredential(BaseCredential):

    TENANCY_OCID_PREFIX = "ocid1.tenancy."
    USER_OCID_PREFIX    = "ocid1.user."

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        tenancy_ocid: str,
        user_ocid: str,
        private_key: str,
        fingerprint: str,
        passphrase: Optional[str] = None,
        role: Optional[str] = "priv",
    ) -> None: ...

    @property
    def tenancy_ocid(self) -> str: ...
    @property
    def user_ocid(self) -> str: ...
    @property
    def private_key(self) -> str: ...
    @property
    def fingerprint(self) -> str: ...
    @property
    def passphrase(self) -> Optional[str]: ...

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]: ...

    def as_dict(self) -> Dict[str, Any]: ...
```

Required category: `"cloud-venue"`.

---

## Module Layout

```
source/packages/automojo/credentials/
├── oraclecloudapikeycredential.py
└── wellknown.py

source/testroots/testbase/automojo/tests/credentials/
├── test_oraclecloudapikeycredential.py
└── test_oracle_credentials_properties.py
```

---

## Testing Strategy

Example-based tests cover: successful construction; `ConfigurationError` when
`categories` lacks `"cloud-venue"`; `ConfigurationError` on empty required fields;
`ConfigurationError` on OCID-prefix mismatches; `validate()` reports the right
missing fields; `as_dict()` round-trips `passphrase=None` and a non-empty
passphrase identically.

Property test (`hypothesis`):

- `test_oracle_credential_roundtrip` — generates `(tenancy_ocid, user_ocid,
  private_key, fingerprint, passphrase)` tuples where the OCIDs carry the required
  prefixes and other strings are non-empty; builds, serialises, reconstructs, and
  asserts field-wise equality.
