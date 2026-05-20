# Implementation Plan — proxmox-credentials

- [ ] 1. Create `proxmoxapitokencredential.py` with
      `ProxmoxApiTokenCredential(BaseCredential)`, keyword-only constructor.
- [ ] 2. Enforce `vm-venue` category, non-empty fields, and the
      `<user>@<realm>!<tokenname>` form for `token_id` in `__init__`.
- [ ] 3. Expose `token_id` and `secret` as read-only properties.
- [ ] 4. Implement `validate(cred_info)` classmethod.
- [ ] 5. Implement `as_dict()` extending the base mapping with both fields.
- [ ] 6. Register the class in `wellknown.py` under categories
      `["vm-venue", "proxmox-api-token"]`.
- [ ] 7. Add example-based unit tests covering construction, category enforcement,
      empty-field rejection, malformed-token-id rejection, validation, and
      `as_dict()` content.
- [ ] 8. Add a `hypothesis` property test `test_proxmox_credential_roundtrip`
      asserting serialise → reconstruct equality over arbitrary syntactically-valid
      token-id strings.
- [ ] 9. Cross-link this spec from
      `automojo-provisioning/specs/venue-proxmox/design.md`.
