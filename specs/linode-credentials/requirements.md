# Requirements

## Introduction

The `linode-credentials` feature adds a `LinodeApiTokenCredential` class to `codecraftai-credentials`.
The class wraps the authentication material used by the linode venue provisioner
(`venues/linode/`) against the linode_api4 SDK.

It inherits from `BaseCredential` and follows the patterns in
`awsaccesskeycredential.py`.

See Also:
[`venue-linode`](../../../codecraftai-provisioning/specs/venue-linode/requirements.md).

---

## Requirements

### Requirement 1: LinodeApiTokenCredential Construction

**User Story:** As a provisioning author, I want a typed linode credential so that
API tokens are never passed around as raw strings.

#### Acceptance Criteria

1. WHEN a caller constructs `LinodeApiTokenCredential` with `identifier`, `categories`, and the token
   field THE SYSTEM SHALL initialise the instance with a read-only property
   exposing that token.
2. THE SYSTEM SHALL require all parameters to be passed by name.
3. IF `categories` does not contain `"cloud-venue"` THEN THE SYSTEM SHALL raise
   `ConfigurationError`.
4. IF the token is the empty string THEN THE SYSTEM SHALL raise
   `ConfigurationError`.

---

### Requirement 2: Validation Surface

#### Acceptance Criteria

1. WHEN `validate(cred_info)` is called with a dict missing the token field THE
   SYSTEM SHALL return an `errors` list naming the missing field.
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

1. THE SYSTEM SHALL register `LinodeApiTokenCredential` in `wellknown.py` under categories
   `["cloud-venue", "linode-api-token"]`.
