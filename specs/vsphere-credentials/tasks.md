# Implementation Plan — vsphere-credentials

- [x] 1. Create `vspherecredential.py` with `VSphereCredential(BaseCredential)`,
      keyword-only constructor with `username`, optional `password`, optional
      `sso_token`.
- [x] 2. Enforce `vm-venue` category, non-empty `username`, and the "one of
      password / sso_token" rule in `__init__`.
- [x] 3. Expose `username`, `password`, `sso_token` as read-only properties.
- [x] 4. Implement `validate(cred_info)` classmethod reporting missing `username`
      and missing-credentials states.
- [x] 5. Implement `as_dict()` extending the base mapping with all three fields.
- [x] 6. Register the class in `wellknown.py` under categories
      `["vm-venue", "vsphere-basic"]`.
- [x] 7. Add example-based unit tests covering the three field-state combinations,
      category enforcement, validation surface, and `as_dict()` content.
- [x] 8. Add a `hypothesis` property test `test_vsphere_credential_roundtrip`
      asserting serialise → reconstruct equality.
- [x] 9. Cross-link this spec from
      `automojo-provisioning/specs/venue-vsphere/design.md` and from
      `automojo-interop-vsphere/specs/vsphere-client-rest-base/design.md`.
