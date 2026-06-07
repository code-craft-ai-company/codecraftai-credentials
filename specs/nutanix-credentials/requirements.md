# Requirements

## Introduction

The `nutanix-credentials` feature adds a `NutanixPrismCredential` class to
`codecraftai-credentials`.  The class wraps Nutanix Prism Central authentication —
username, password, and the Prism Central endpoint URL — used by the Nutanix venue
provisioner (`venues/nutanix/`).

It inherits from `BaseCredential` and follows the patterns established by
`basiccredential.py` and `awsaccesskeycredential.py`.  Nutanix AHV is a VM-shaped
venue, so the credential is registered under the `vm-venue` category.

See Also:
[`venue-nutanix`](../../../codecraftai-provisioning/specs/venue-nutanix/requirements.md).

---

## Requirements

### Requirement 1: NutanixPrismCredential Construction

**User Story:** As a provisioning author, I want a typed Nutanix Prism Central
credential that carries the endpoint alongside the username/password so consumers
don't need to thread the endpoint as a separate parameter.

#### Acceptance Criteria

1. WHEN a caller constructs `NutanixPrismCredential` with `identifier`,
   `categories`, `username`, `password`, and `endpoint` THE SYSTEM SHALL
   initialise the instance with read-only property access.
2. THE SYSTEM SHALL require all parameters to be passed by name.
3. IF `categories` does not contain `"vm-venue"` THEN THE SYSTEM SHALL raise
   `ConfigurationError`.
4. IF any of `username`, `password`, `endpoint` is the empty string THEN THE
   SYSTEM SHALL raise `ConfigurationError` naming the offending field.
5. IF `endpoint` does not start with `"http://"` or `"https://"` THEN THE SYSTEM
   SHALL raise `ConfigurationError` describing the expected form.

---

### Requirement 2: Validation Surface

#### Acceptance Criteria

1. WHEN `validate(cred_info)` is called with a dict missing any of `username`,
   `password`, `endpoint` THE SYSTEM SHALL return an `errors` list naming each
   missing field.
2. WHEN the input is complete THE SYSTEM SHALL return two empty lists.

---

### Requirement 3: Round-Trip Serialisation

#### Acceptance Criteria

1. WHILE the credential carries any valid field combination THE SYSTEM SHALL
   ensure reconstructing an instance from `as_dict()` yields a value-equal
   credential.
2. THE SYSTEM SHALL verify this via a `hypothesis` property test.

---

### Requirement 4: Category Registration

#### Acceptance Criteria

1. THE SYSTEM SHALL register `NutanixPrismCredential` in `wellknown.py` under
   categories `["vm-venue", "nutanix-prism"]`.
