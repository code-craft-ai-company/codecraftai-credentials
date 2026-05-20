# Requirements

## Introduction

The `vsphere-credentials` feature promotes the current ad-hoc
`BasicCredential` usage for VSphere into a typed `VSphereCredential` class.  The
class wraps username + password + an optional SSO token used by the VSphere venue
provisioner (`venues/vsphere/`) and by `automojo-interop-vsphere`'s session-mint
flow.

It inherits from `BaseCredential` and follows the patterns established by
`basiccredential.py` and `awsaccesskeycredential.py`.  VSphere is a VM-shaped
venue, so the credential is registered under the `vm-venue` category (and not
`cloud-venue`).

See Also:
- [`venue-vsphere`](../../../automojo-provisioning/specs/venue-vsphere/requirements.md)
- [`vsphere-client-rest-base`](../../../automojo-interop-vsphere/specs/vsphere-client-rest-base/requirements.md)

---

## Requirements

### Requirement 1: VSphereCredential Construction

**User Story:** As a provisioning author, I want a typed VSphere credential so that
username/password authentication for VSphere is distinguishable from generic
`BasicCredential` usage at the type level.

#### Acceptance Criteria

1. WHEN a caller constructs `VSphereCredential` with `identifier`, `categories`,
   `username`, `password`, and optional `sso_token` THE SYSTEM SHALL initialise
   the instance with read-only property access.
2. THE SYSTEM SHALL require all parameters to be passed by name.
3. IF `categories` does not contain `"vm-venue"` THEN THE SYSTEM SHALL raise
   `ConfigurationError`.
4. IF `username` is the empty string THEN THE SYSTEM SHALL raise
   `ConfigurationError`.
5. IF `password` is empty AND `sso_token` is `None` THEN THE SYSTEM SHALL raise
   `ConfigurationError` instructing the caller to supply one or the other.

---

### Requirement 2: Validation Surface

#### Acceptance Criteria

1. WHEN `validate(cred_info)` is called with a dict missing `username` THE SYSTEM
   SHALL return an `errors` list naming the field.
2. WHEN `validate(cred_info)` is called with neither `password` nor `sso_token`
   THE SYSTEM SHALL return an `errors` list noting one of the two is required.
3. WHEN the input is complete THE SYSTEM SHALL return two empty lists.

---

### Requirement 3: Round-Trip Serialisation

#### Acceptance Criteria

1. WHILE the credential carries any valid field combination THE SYSTEM SHALL ensure
   reconstructing an instance from `as_dict()` yields a value-equal credential.
2. THE SYSTEM SHALL verify this via a `hypothesis` property test that explores
   both the password-only and sso-token-only field states.

---

### Requirement 4: Category Registration

#### Acceptance Criteria

1. THE SYSTEM SHALL register `VSphereCredential` in `wellknown.py` under categories
   `["vm-venue", "vsphere-basic"]`.
