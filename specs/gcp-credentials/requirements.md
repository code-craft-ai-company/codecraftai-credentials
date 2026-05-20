# Requirements

## Introduction

The `gcp-credentials` feature adds two new `BaseCredential` subclasses for Google
Cloud Platform venue authentication:

- `GcpServiceAccountKeyCredential` — a service-account JSON key file's contents
  (project id, client email, private key id, private key, token uri).
- `GcpWorkloadIdentityCredential` — federated identity assertion (audience, subject
  token type, service account email) for keyless authentication.

Both follow the patterns established by `awsaccesskeycredential.py`.  Consumers in
`automojo-provisioning/venues/google` select credentials by the `cloud-venue`
category.

See Also: [`venue-gcp`](../../../automojo-provisioning/specs/venue-gcp/requirements.md).

---

## Requirements

### Requirement 1: GcpServiceAccountKeyCredential Construction

**User Story:** As a provisioning author, I want a typed credential class wrapping a
GCP service-account key so that key material is never passed around as a raw dict.

#### Acceptance Criteria

1. WHEN a caller constructs `GcpServiceAccountKeyCredential` with `identifier`,
   `categories`, `project_id`, `client_email`, `private_key_id`, `private_key`, and
   optional `token_uri` THE SYSTEM SHALL initialise the instance with read-only
   property access.
2. THE SYSTEM SHALL require all parameters to be passed by name.
3. IF `categories` does not contain `"cloud-venue"` THEN THE SYSTEM SHALL raise
   `ConfigurationError`.
4. IF any required string is empty THEN THE SYSTEM SHALL raise `ConfigurationError`
   naming the field.
5. WHEN `token_uri` is omitted THE SYSTEM SHALL default it to
   `"https://oauth2.googleapis.com/token"`.

---

### Requirement 2: GcpWorkloadIdentityCredential Construction

**User Story:** As a provisioning author using Workload Identity Federation, I want a
keyless credential type so that no private key material is stored in spec files.

#### Acceptance Criteria

1. WHEN a caller constructs `GcpWorkloadIdentityCredential` with `identifier`,
   `categories`, `audience`, `subject_token_type`, `service_account_email`, and
   optional `token_url` THE SYSTEM SHALL initialise the instance.
2. THE SYSTEM SHALL require all parameters to be passed by name.
3. IF `categories` does not contain `"cloud-venue"` THEN THE SYSTEM SHALL raise
   `ConfigurationError`.
4. IF `audience`, `subject_token_type`, or `service_account_email` is empty THEN THE
   SYSTEM SHALL raise `ConfigurationError`.

---

### Requirement 3: Validation Surface

**User Story:** As the credential manager, I want a `validate(cred_info)` classmethod
on each class so YAML loaders report omissions uniformly.

#### Acceptance Criteria

1. WHEN `validate(cred_info)` is called on each class with a dict missing required
   fields THE SYSTEM SHALL return an `errors` list naming each missing field.
2. WHEN the input is complete THE SYSTEM SHALL return two empty lists.

---

### Requirement 4: Round-Trip Serialisation

**User Story:** As a downstream consumer, I want lossless `as_dict()` round-tripping
so persistence layers can store and restore GCP credentials.

#### Acceptance Criteria

1. WHILE the credential carries any valid field combination THE SYSTEM SHALL ensure
   that reconstructing an instance from `as_dict()` yields a value-equal credential.
2. THE SYSTEM SHALL verify this via `hypothesis` property tests covering both
   classes.

---

### Requirement 5: Category Registration

#### Acceptance Criteria

1. THE SYSTEM SHALL register `GcpServiceAccountKeyCredential` under categories
   `["cloud-venue", "gcp-service-account-key"]`.
2. THE SYSTEM SHALL register `GcpWorkloadIdentityCredential` under categories
   `["cloud-venue", "gcp-workload-identity"]`.
