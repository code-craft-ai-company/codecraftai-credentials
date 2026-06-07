# Requirements

## Introduction

The `digitalocean-credentials` feature adds a `DigitalOceanApiTokenCredential` class
to `codecraftai-credentials`.  The class wraps a single DigitalOcean personal-access
token used by the DigitalOcean venue provisioner (`venues/digitalocean/`).

The class inherits from `BaseCredential` and follows the patterns established by
`awsaccesskeycredential.py`: keyword-only constructor, category enforcement in
`__init__`, read-only properties, `validate(cred_info)` classmethod, and
`as_dict()` override.

See Also:
[`venue-digitalocean`](../../../codecraftai-provisioning/specs/venue-digitalocean/requirements.md).

---

## Requirements

### Requirement 1: DigitalOceanApiTokenCredential Construction

**User Story:** As a provisioning author, I want a typed DigitalOcean credential so
that API tokens are never passed around as raw strings.

#### Acceptance Criteria

1. WHEN a caller constructs `DigitalOceanApiTokenCredential` with `identifier`,
   `categories`, and `token` THE SYSTEM SHALL initialise the instance with a
   read-only `token` property.
2. THE SYSTEM SHALL require all parameters to be passed by name.
3. IF `categories` does not contain `"cloud-venue"` THEN THE SYSTEM SHALL raise
   `ConfigurationError`.
4. IF `token` is the empty string THEN THE SYSTEM SHALL raise `ConfigurationError`.

---

### Requirement 2: Validation Surface

**User Story:** As the credential manager, I want a `validate(cred_info)` classmethod
so YAML loaders report omissions uniformly.

#### Acceptance Criteria

1. WHEN `validate(cred_info)` is called with a dict missing `token` THE SYSTEM SHALL
   return an `errors` list containing a message naming the missing field.
2. WHEN the input is complete THE SYSTEM SHALL return two empty lists.

---

### Requirement 3: Round-Trip Serialisation

**User Story:** As a downstream consumer, I want lossless `as_dict()` round-tripping
so persistence layers can store and restore credentials.

#### Acceptance Criteria

1. WHILE the credential carries any valid field combination THE SYSTEM SHALL ensure
   reconstructing an instance from `as_dict()` yields a value-equal credential.
2. THE SYSTEM SHALL verify this via a `hypothesis` property test.

---

### Requirement 4: Category Registration

#### Acceptance Criteria

1. THE SYSTEM SHALL register `DigitalOceanApiTokenCredential` in `wellknown.py`
   under categories `["cloud-venue", "digitalocean-api-token"]`.
