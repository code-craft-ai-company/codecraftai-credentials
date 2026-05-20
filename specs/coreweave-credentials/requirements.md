# Requirements

## Introduction

The `coreweave-credentials` feature adds a `CoreweaveApiCredential` class to
`automojo-credentials`.  Per the §7 decision in
`PLAN-VPN-AND-CLOUD-PROVISIONING.md`, this credential is a CoreWeave-issued API
token that the CoreWeave interop client exchanges for a Kubernetes `kubeconfig` at
use time; the resulting kubeconfig is handed to `automojo-interop-kubernetes` and
no double-auth occurs.

The class inherits from `BaseCredential` and follows the patterns in
`awsaccesskeycredential.py`.  Because CoreWeave is a workload-shaped (Kubernetes)
venue used primarily for HPC/AI workloads, the credential is registered under the
`hpc-venue` category (and not `cloud-venue`).

See Also:
[`venue-coreweave`](../../../automojo-provisioning/specs/venue-coreweave/requirements.md).

---

## Requirements

### Requirement 1: CoreweaveApiCredential Construction

**User Story:** As a provisioning author, I want a typed CoreWeave credential that
holds only the API token (not a kubeconfig) so that the exchange-for-kubeconfig
step happens exactly once at use time and is owned by the CoreWeave interop client.

#### Acceptance Criteria

1. WHEN a caller constructs `CoreweaveApiCredential` with `identifier`,
   `categories`, `token`, and optional `organization_id` THE SYSTEM SHALL
   initialise the instance with read-only property access.
2. THE SYSTEM SHALL require all parameters to be passed by name.
3. IF `categories` does not contain `"hpc-venue"` THEN THE SYSTEM SHALL raise
   `ConfigurationError`.
4. IF `token` is the empty string THEN THE SYSTEM SHALL raise
   `ConfigurationError`.
5. THE SYSTEM SHALL NOT store a kubeconfig field on the credential — the kubeconfig
   is materialised by the interop layer at use time.

---

### Requirement 2: Validation Surface

#### Acceptance Criteria

1. WHEN `validate(cred_info)` is called with a dict missing `token` THE SYSTEM
   SHALL return an `errors` list naming the missing field.
2. WHEN the input is complete THE SYSTEM SHALL return two empty lists.

---

### Requirement 3: Round-Trip Serialisation

#### Acceptance Criteria

1. WHILE the credential carries any valid field combination THE SYSTEM SHALL ensure
   reconstructing an instance from `as_dict()` yields a value-equal credential.
2. THE SYSTEM SHALL verify this via a `hypothesis` property test that varies both
   `token` and the optional `organization_id`.

---

### Requirement 4: Category Registration

#### Acceptance Criteria

1. THE SYSTEM SHALL register `CoreweaveApiCredential` in `wellknown.py` under
   categories `["hpc-venue", "coreweave-api-token"]`.
