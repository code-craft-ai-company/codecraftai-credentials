# Implementation Plan — nutanix-credentials

- [x] 1. Create `nutanixprismcredential.py` with
      `NutanixPrismCredential(BaseCredential)`, keyword-only constructor.
- [x] 2. Enforce `vm-venue` category, non-empty fields, and http(s) endpoint
      prefix in `__init__`.
- [x] 3. Expose `username`, `password`, `endpoint` as read-only properties.
- [x] 4. Implement `validate(cred_info)` classmethod.
- [x] 5. Implement `as_dict()` extending the base mapping with all three fields.
- [x] 6. Register the class in `wellknown.py` under categories
      `["vm-venue", "nutanix-prism"]`.
- [x] 7. Add example-based unit tests for construction, category enforcement,
      empty-field rejection, endpoint-prefix rejection, validation surface, and
      `as_dict()` content.
- [x] 8. Add a `hypothesis` property test `test_nutanix_credential_roundtrip`
      asserting serialise → reconstruct equality over arbitrary valid inputs.
- [x] 9. Cross-link this spec from
      `codecraftai-provisioning/specs/venue-nutanix/design.md`.
