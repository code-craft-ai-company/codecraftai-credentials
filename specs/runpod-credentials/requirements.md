# Requirements

## Introduction

The `runpod-credentials` feature adds a `RunpodApiKeyCredential` class to `automojo-credentials`.
The class wraps the authentication material used by the runpod venue provisioner
(`venues/runpod/`) against the RunPod REST API.

It inherits from `BaseCredential` and follows the patterns in
`awsaccesskeycredential.py`.

See Also:
[`venue-runpod`](../../../automojo-provisioning/specs/venue-runpod/requirements.md).

---

## Requirements

### Requirement 1: RunpodApiKeyCredential Construction

**User Story:** As a provisioning author, I want a typed runpod credential so that
API tokens are never passed around as raw strings.

#### Acceptance Criteria

1. WHEN a caller constructs `RunpodApiKeyCredential` with `identifier`, `categories`, and the token
   field THE SYSTEM SHALL initialise the instance with a read-only property
   exposing that token.
2. THE SYSTEM SHALL require all parameters to be passed by name.
3. IF `categories` does not contain `"hpc-venue"` THEN THE SYSTEM SHALL raise
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

1. THE SYSTEM SHALL register `RunpodApiKeyCredential` in `wellknown.py` under categories
   `["hpc-venue", "runpod-api-key"]`.
