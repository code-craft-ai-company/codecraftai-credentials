# Requirements

## Introduction

The `proxmox-credentials` feature adds a `ProxmoxApiTokenCredential` class to
`automojo-credentials`.  The class wraps the two-field Proxmox API token
(token id + secret) used by the Proxmox venue provisioner (`venues/proxmox/`)
against the Proxmox REST API on port 8006.

It inherits from `BaseCredential` and follows the patterns established by
`awsaccesskeycredential.py`.  Proxmox is a VM-shaped venue, so the credential is
registered under the `vm-venue` category.

See Also:
[`venue-proxmox`](../../../automojo-provisioning/specs/venue-proxmox/requirements.md).

---

## Requirements

### Requirement 1: ProxmoxApiTokenCredential Construction

**User Story:** As a provisioning author, I want a typed Proxmox credential so the
(token id, secret) pair is never threaded through code as separate raw strings.

#### Acceptance Criteria

1. WHEN a caller constructs `ProxmoxApiTokenCredential` with `identifier`,
   `categories`, `token_id`, and `secret` THE SYSTEM SHALL initialise the
   instance with read-only `token_id` and `secret` properties.
2. THE SYSTEM SHALL require all parameters to be passed by name.
3. IF `categories` does not contain `"vm-venue"` THEN THE SYSTEM SHALL raise
   `ConfigurationError`.
4. IF `token_id` or `secret` is the empty string THEN THE SYSTEM SHALL raise
   `ConfigurationError` naming the offending field.
5. IF `token_id` does not match the form `<user>@<realm>!<tokenname>` THEN THE
   SYSTEM SHALL raise `ConfigurationError` with a message describing the expected
   form.

---

### Requirement 2: Validation Surface

#### Acceptance Criteria

1. WHEN `validate(cred_info)` is called with a dict missing `token_id` or
   `secret` THE SYSTEM SHALL return an `errors` list naming each missing field.
2. WHEN the input is complete THE SYSTEM SHALL return two empty lists.

---

### Requirement 3: Round-Trip Serialisation

#### Acceptance Criteria

1. WHILE the credential carries any valid field combination THE SYSTEM SHALL
   ensure reconstructing an instance from `as_dict()` yields a value-equal
   credential.
2. THE SYSTEM SHALL verify this via a `hypothesis` property test that generates
   syntactically-valid token-id strings.

---

### Requirement 4: Category Registration

#### Acceptance Criteria

1. THE SYSTEM SHALL register `ProxmoxApiTokenCredential` in `wellknown.py` under
   categories `["vm-venue", "proxmox-api-token"]`.
