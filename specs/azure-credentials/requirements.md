# Requirements

## Introduction

The `azure-credentials` feature adds two new credential classes to `codecraftai-credentials`
for authenticating against Microsoft Azure cloud venues from the provisioning,
landscaping, and interop layers:

- `AzureServicePrincipalCredential` — tenant id, client id, and client secret for
  application-based access (the same shape as the existing
  `AzureClientSecretCredential` but exposed under the `cloud-venue` category so that
  cloud venue consumers can discover it without overloading the legacy
  `azure-client-secret` category).
- `AzureManagedIdentityCredential` — references a system-assigned or user-assigned
  managed identity by client id (optional) and resource id (optional).  No secret is
  stored; the credential is resolved at use time against the Azure Instance Metadata
  Service from inside an Azure-hosted runtime.

Both classes inherit from `BaseCredential` and follow the per-credential naming and
file-layout conventions used by `awsaccesskeycredential.py` and
`azureclientsecretcredential.py`.  The Azure venue provisioner consumes these
credentials via the `cloud-venue` category filter.

See Also: [`venue-azure`](../../../codecraftai-provisioning/specs/venue-azure/requirements.md).

---

## Requirements

### Requirement 1: AzureServicePrincipalCredential Construction

**User Story:** As a provisioning author, I want a typed Azure service principal
credential so that Azure venue calls are authenticated without passing raw strings.

#### Acceptance Criteria

1. WHEN a caller constructs `AzureServicePrincipalCredential` with all of
   `identifier`, `categories`, `tenant_id`, `client_id`, `client_secret` THE SYSTEM
   SHALL initialise an instance exposing those values via read-only properties.
2. THE SYSTEM SHALL accept only named keyword arguments to the constructor.
3. IF `categories` does not contain `"cloud-venue"` THEN THE SYSTEM SHALL raise
   `ConfigurationError` with a message naming the credential class and the missing
   category.
4. IF any of `tenant_id`, `client_id`, `client_secret` is the empty string THEN THE
   SYSTEM SHALL raise `ConfigurationError` naming the offending parameter.
5. WHEN `as_dict()` is invoked THE SYSTEM SHALL return a dictionary containing every
   constructor field including the inherited `identifier`, `categories`, `role`.

---

### Requirement 2: AzureManagedIdentityCredential Construction

**User Story:** As a provisioning author running inside Azure, I want a managed-identity
credential type so that no secret material is stored in spec files.

#### Acceptance Criteria

1. WHEN a caller constructs `AzureManagedIdentityCredential` with `identifier`,
   `categories`, and at least one of `client_id` or `resource_id` THE SYSTEM SHALL
   initialise an instance.
2. THE SYSTEM SHALL accept only named keyword arguments to the constructor.
3. IF both `client_id` and `resource_id` are `None` THEN THE SYSTEM SHALL raise
   `ConfigurationError` instructing the caller to supply at least one selector.
4. IF `categories` does not contain `"cloud-venue"` THEN THE SYSTEM SHALL raise
   `ConfigurationError`.
5. WHEN `as_dict()` is invoked THE SYSTEM SHALL include `client_id` and `resource_id`
   (each may be `None`) plus the inherited base-credential fields.

---

### Requirement 3: Validation Surface

**User Story:** As the credential manager, I want a `validate(cred_info)` class method
on each new class so that YAML loading reports field omissions uniformly.

#### Acceptance Criteria

1. WHEN `AzureServicePrincipalCredential.validate(cred_info)` is called with a dict
   missing any of `tenant_id`, `client_id`, `client_secret` THE SYSTEM SHALL return an
   `errors` list naming each missing field and an empty `warnings` list.
2. WHEN `AzureManagedIdentityCredential.validate(cred_info)` is called with a dict
   missing both `client_id` and `resource_id` THE SYSTEM SHALL return an `errors` list
   with a message indicating at least one of the two must be provided.
3. WHEN the input is fully populated THE SYSTEM SHALL return two empty lists.

---

### Requirement 4: Round-Trip Serialisation

**User Story:** As a downstream consumer, I want every credential to round-trip through
`as_dict()` and a constructor reconstruction so that persistence layers can store and
restore credentials losslessly.

#### Acceptance Criteria

1. WHILE the credential carries any valid field combination THE SYSTEM SHALL guarantee
   that constructing a new instance from `as_dict()` (minus the `categories` filter)
   produces an equal credential by value.
2. THE SYSTEM SHALL be verified by a `hypothesis` property test that generates
   arbitrary valid field combinations and asserts `from_dict(c.as_dict()) == c` for
   every Azure credential class added by this spec.

---

### Requirement 5: Category Registration

**User Story:** As a credential-consumer-by-category, I want both classes registered
under the `cloud-venue` category and the Azure-specific sub-categories.

#### Acceptance Criteria

1. THE SYSTEM SHALL register `AzureServicePrincipalCredential` under categories
   `["cloud-venue", "azure-service-principal"]` in `wellknown.py`'s category map.
2. THE SYSTEM SHALL register `AzureManagedIdentityCredential` under categories
   `["cloud-venue", "azure-managed-identity"]`.
3. WHERE a caller filters credentials by category `"cloud-venue"` THE SYSTEM SHALL
   surface both new classes.
