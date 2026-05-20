# Requirements

## Introduction

The `tailscale-credentials` feature adds two new credential classes to
`automojo-credentials` for Tailscale: `TailscaleAuthKeyCredential`
(static, pre-minted auth key) and `TailscaleOAuthCredential` (OAuth
client id + secret used by `IVPNControlPlane` to mint short-lived
ephemeral keys). Both follow the established
`AwsAccessKeyCredential` pattern: subclass `BaseCredential`, validate
in `__init__`, expose typed property accessors, register categories
with `wellknown.py`.

Per the §5 decision in `PLAN-VPN-AND-CLOUD-PROVISIONING.md`, the
canonical provisioning flow uses `TailscaleOAuthCredential` to mint
ephemeral, preauthorized, single-use keys per instance.
`TailscaleAuthKeyCredential` is supported as the documented "lab-only"
path. The credential classes themselves do not enforce that policy —
that lives in the provisioning engine — but the design documents
the preferred usage.

**See Also:** [vpn-control-plane-protocol](../../../automojo-interfaces/specs/vpn-control-plane-protocol/design.md),
[well-known-vpn-and-venue-categories](../well-known-vpn-and-venue-categories/design.md).

---

## Requirements

### Requirement 1: Tailscale Auth Key Credential

**User Story:** As a lab user, I want a typed container for a
pre-minted Tailscale auth key with its `reusable`, `ephemeral`, and
`preauthorized` flags, so I can hand it to interop / sysman /
provisioning code without parsing strings.

#### Acceptance Criteria

1. THE SYSTEM SHALL define `TailscaleAuthKeyCredential(BaseCredential)`
   with constructor parameters `identifier`, `categories`, `authkey`,
   `reusable`, `ephemeral`, `preauthorized`, and `role="priv"`.
2. THE SYSTEM SHALL enforce that `"tailscale-authkey"` appears in
   `categories`; otherwise raise `ConfigurationError`.
3. THE SYSTEM SHALL enforce that `authkey` is a non-empty string;
   otherwise raise `ConfigurationError`.
4. THE SYSTEM SHALL expose `authkey`, `reusable`, `ephemeral`,
   `preauthorized` as read-only properties.
5. THE SYSTEM SHALL implement `classmethod validate(cls, cred_info)`
   returning `(errors, warnings)` following the
   `AwsAccessKeyCredential.validate` pattern.

---

### Requirement 2: Tailscale OAuth Credential

**User Story:** As the provisioning engine, I want a typed container
for a Tailscale OAuth client id + secret pair so I can mint ephemeral
auth keys at apply time without ever embedding a long-lived key in a
cloud-init payload.

#### Acceptance Criteria

1. THE SYSTEM SHALL define `TailscaleOAuthCredential(BaseCredential)`
   with constructor parameters `identifier`, `categories`,
   `client_id`, `client_secret`, optional `default_tags: List[str]`,
   and `role="priv"`.
2. THE SYSTEM SHALL enforce that `"tailscale-oauth"` appears in
   `categories`; otherwise raise `ConfigurationError`.
3. THE SYSTEM SHALL enforce that `client_id` and `client_secret` are
   non-empty strings.
4. THE SYSTEM SHALL expose `client_id`, `client_secret`,
   `default_tags` as read-only properties.
5. THE SYSTEM SHALL implement `classmethod validate(cls, cred_info)`
   returning `(errors, warnings)`.

---

### Requirement 3: Category Registration

**User Story:** As a credential manager consumer, I want to query
credentials by category (`vpn`, `mesh`) without knowing the per-
provider class names.

#### Acceptance Criteria

1. THE SYSTEM SHALL list `tailscale-authkey` and `tailscale-oauth`
   under the `vpn` and `mesh` well-known categories registered in
   `well-known-vpn-and-venue-categories`.
2. THE SYSTEM SHALL document that the per-category lookup is the
   intended consumption path for `IVPNControlPlane` implementations.

---

### Requirement 4: YAML Sample in Docstrings

**User Story:** As an operator writing a credentials file, I want a
copy-paste YAML sample in each credential class's docstring.

#### Acceptance Criteria

1. THE SYSTEM SHALL include a YAML code block in each class's
   docstring matching the
   `AwsAccessKeyCredential.__doc__` pattern (identifier, category,
   key fields).
2. WHEN the field set changes THE SYSTEM SHALL update the YAML
   sample in the same commit.

---

### Requirement 5: No Secret Material in `__repr__`

**User Story:** As a debugger, I want safe `repr()` of credential
objects so logs do not leak secret material.

#### Acceptance Criteria

1. THE SYSTEM SHALL implement `__repr__` on both classes such that
   `authkey`, `client_secret`, and any other secret-bearing field
   appear as `"***"`.
2. THE SYSTEM SHALL include `identifier`, class name, and
   `categories` in `__repr__` for diagnosability.

---

### Requirement 6: Validation Returns Both Errors and Warnings

**User Story:** As a config loader, I want non-fatal warnings
surfaced separately from errors so I can log them without rejecting
the load.

#### Acceptance Criteria

1. THE SYSTEM SHALL have `validate` return `Tuple[List[str], List[str]]`
   where the first list is errors and the second is warnings.
2. WHEN the credential set uses `TailscaleAuthKeyCredential` THE
   SYSTEM SHALL emit a warning recommending `TailscaleOAuthCredential`
   for production provisioning use.
