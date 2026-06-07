# Requirements

## Introduction

The `oracle-credentials` feature adds an `OracleCloudApiKeyCredential` class to
`codecraftai-credentials`.  The class wraps the four-field OCI API-key credential
material — tenancy OCID, user OCID, private key, and key fingerprint — used by the
Oracle Cloud venue provisioner (`venues/oracle/`) through the `oci` SDK.

It inherits from `BaseCredential` and follows the patterns established by
`awsaccesskeycredential.py`.  The region the credential is exercised against is a
runtime parameter on the provisioner, not part of the credential itself.

See Also:
[`venue-oracle`](../../../codecraftai-provisioning/specs/venue-oracle/requirements.md).

---

## Requirements

### Requirement 1: OracleCloudApiKeyCredential Construction

**User Story:** As a provisioning author, I want a typed OCI API-key credential so
that the four-field tuple is never threaded through code as separate raw strings.

#### Acceptance Criteria

1. WHEN a caller constructs `OracleCloudApiKeyCredential` with `identifier`,
   `categories`, `tenancy_ocid`, `user_ocid`, `private_key`, `fingerprint`, and
   optional `passphrase` THE SYSTEM SHALL initialise the instance with read-only
   property access to each field.
2. THE SYSTEM SHALL require all parameters to be passed by name.
3. IF `categories` does not contain `"cloud-venue"` THEN THE SYSTEM SHALL raise
   `ConfigurationError`.
4. IF any of `tenancy_ocid`, `user_ocid`, `private_key`, `fingerprint` is the empty
   string THEN THE SYSTEM SHALL raise `ConfigurationError` naming the offending
   field.
5. WHEN `passphrase` is omitted THE SYSTEM SHALL default it to `None`.

---

### Requirement 2: OCID Shape Validation

**User Story:** As a credential author, I want obvious typos in OCID strings caught
at construction time so misconfigured credentials fail loudly rather than at the
first API call.

#### Acceptance Criteria

1. IF `tenancy_ocid` does not start with the literal `"ocid1.tenancy."` THEN THE
   SYSTEM SHALL raise `ConfigurationError` with a message naming the field.
2. IF `user_ocid` does not start with the literal `"ocid1.user."` THEN THE SYSTEM
   SHALL raise `ConfigurationError` with a message naming the field.

---

### Requirement 3: Validation Surface

#### Acceptance Criteria

1. WHEN `validate(cred_info)` is called with a dict missing any of `tenancy_ocid`,
   `user_ocid`, `private_key`, `fingerprint` THE SYSTEM SHALL return an `errors`
   list naming each missing field.
2. WHEN the input is complete THE SYSTEM SHALL return two empty lists.

---

### Requirement 4: Round-Trip Serialisation

#### Acceptance Criteria

1. WHILE the credential carries any valid field combination THE SYSTEM SHALL ensure
   reconstructing an instance from `as_dict()` yields a value-equal credential.
2. THE SYSTEM SHALL verify this via a `hypothesis` property test that generates
   syntactically-valid OCIDs and arbitrary key/fingerprint strings.

---

### Requirement 5: Category Registration

#### Acceptance Criteria

1. THE SYSTEM SHALL register `OracleCloudApiKeyCredential` in `wellknown.py` under
   categories `["cloud-venue", "oracle-api-key"]`.
