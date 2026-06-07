# Requirements

## Introduction

The `twingate-credentials` feature adds
`TwingateServiceAccountCredential` to `codecraftai-credentials` — a typed
container for the Twingate API token plus the network slug needed by
the Twingate GraphQL control plane. The class mirrors the
`TailscaleAuthKeyCredential` pattern (subclass `BaseCredential`,
validate in `__init__`, typed properties, redacted `__repr__`,
`validate` classmethod).

Twingate's auth model is asymmetric to Tailscale's — there is no flat
auth-key minting (§3 of the design plan). The class therefore exposes
only the API-token + network-slug pair; connector tokens are issued
through the control plane API itself at use time and are not
credentials by themselves.

**See Also:** [vpn-control-plane-protocol](../../../codecraftai-interfaces/specs/vpn-control-plane-protocol/design.md),
[well-known-vpn-and-venue-categories](../well-known-vpn-and-venue-categories/design.md),
[tailscale-credentials](../tailscale-credentials/design.md).

---

## Requirements

### Requirement 1: Twingate Service Account Credential

**User Story:** As a Twingate control-plane consumer, I want a typed
container for my API token + network slug so I can hand it to interop
code without parsing strings.

#### Acceptance Criteria

1. THE SYSTEM SHALL define
   `TwingateServiceAccountCredential(BaseCredential)` with
   constructor parameters `identifier`, `categories`, `api_token`,
   `network_slug`, and `role="priv"`.
2. THE SYSTEM SHALL enforce that
   `"twingate-service-account"` appears in `categories`; otherwise
   raise `ConfigurationError`.
3. THE SYSTEM SHALL enforce that `api_token` is a non-empty string.
4. THE SYSTEM SHALL enforce that `network_slug` is a non-empty
   string and contains no whitespace (Twingate slugs are
   hostname-shaped).
5. THE SYSTEM SHALL expose `api_token`, `network_slug` as read-only
   properties.

---

### Requirement 2: Validation Classmethod

**User Story:** As a config loader, I want a `validate` classmethod
returning `(errors, warnings)` so loads can report all problems
rather than aborting on the first.

#### Acceptance Criteria

1. THE SYSTEM SHALL implement `classmethod validate(cls, cred_info)`
   returning `Tuple[List[str], List[str]]`.
2. WHEN `api_token` or `network_slug` is missing or empty THE
   SYSTEM SHALL include a descriptive error in the returned errors
   list.
3. WHEN `network_slug` contains whitespace THE SYSTEM SHALL include
   a descriptive error.

---

### Requirement 3: Category Registration

**User Story:** As a credential manager consumer, I want to query
credentials by `vpn` / `mesh` category without knowing the per-
provider class name.

#### Acceptance Criteria

1. THE SYSTEM SHALL register `twingate-service-account` under the
   `vpn` and `mesh` well-known categories in
   `well-known-vpn-and-venue-categories`.

---

### Requirement 4: YAML Sample in Docstring

**User Story:** As an operator writing a credentials file, I want a
copy-paste YAML sample.

#### Acceptance Criteria

1. THE SYSTEM SHALL include a YAML code block in the class
   docstring matching the `AwsAccessKeyCredential.__doc__` pattern.

---

### Requirement 5: Redacted `__repr__`

**User Story:** As a debugger, I want safe `repr()` so logs do not
leak the API token.

#### Acceptance Criteria

1. THE SYSTEM SHALL implement `__repr__` such that `api_token`
   appears as `"***"`.
2. THE SYSTEM SHALL include `identifier`, class name, `categories`,
   and `network_slug` in `__repr__` for diagnosability.
   (`network_slug` is not secret — it is the public network
   identifier on the Twingate dashboard URL.)
