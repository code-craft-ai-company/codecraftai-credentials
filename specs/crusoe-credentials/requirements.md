# Requirements

## Introduction

The `crusoe-credentials` feature adds a `CrusoeApiKeyCredential` class to
`automojo-credentials`.  The class wraps the two-field Crusoe Cloud API credential
(access key id + secret) used by the Crusoe venue provisioner (`venues/crusoe/`)
against `api.crusoecloud.com`.

It inherits from `BaseCredential` and follows the patterns established by
`awsaccesskeycredential.py`.  Because Crusoe is an HPC/AI cloud venue, the
credential is registered under both `cloud-venue` and `hpc-venue` so consumers can
discover it through either path.

See Also:
[`venue-crusoe`](../../../automojo-provisioning/specs/venue-crusoe/requirements.md).

---

## Requirements

### Requirement 1: CrusoeApiKeyCredential Construction

**User Story:** As a provisioning author, I want a typed Crusoe credential so the
(access key id, secret) pair is never threaded through code as separate raw
strings.

#### Acceptance Criteria

1. WHEN a caller constructs `CrusoeApiKeyCredential` with `identifier`,
   `categories`, `access_key_id`, and `secret` THE SYSTEM SHALL initialise the
   instance with read-only `access_key_id` and `secret` properties.
2. THE SYSTEM SHALL require all parameters to be passed by name.
3. IF `categories` contains neither `"cloud-venue"` nor `"hpc-venue"` THEN THE
   SYSTEM SHALL raise `ConfigurationError`.
4. IF `access_key_id` or `secret` is the empty string THEN THE SYSTEM SHALL raise
   `ConfigurationError` naming the offending field.

---

### Requirement 2: Validation Surface

#### Acceptance Criteria

1. WHEN `validate(cred_info)` is called with a dict missing either `access_key_id`
   or `secret` THE SYSTEM SHALL return an `errors` list naming each missing field.
2. WHEN the input is complete THE SYSTEM SHALL return two empty lists.

---

### Requirement 3: Round-Trip Serialisation

#### Acceptance Criteria

1. WHILE the credential carries any valid field combination THE SYSTEM SHALL ensure
   reconstructing an instance from `as_dict()` yields a value-equal credential.
2. THE SYSTEM SHALL verify this via a `hypothesis` property test.

---

### Requirement 4: Category Registration

#### Acceptance Criteria

1. THE SYSTEM SHALL register `CrusoeApiKeyCredential` in `wellknown.py` under
   categories `["cloud-venue", "hpc-venue", "crusoe-api-key"]`.
