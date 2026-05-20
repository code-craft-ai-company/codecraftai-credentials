# Implementation Plan — coreweave-credentials

- [ ] 1. Create `coreweaveapicredential.py` with `CoreweaveApiCredential(BaseCredential)`,
      keyword-only constructor with `token` and optional `organization_id`.
- [ ] 2. Enforce `hpc-venue` category and non-empty `token` in `__init__`.
- [ ] 3. Expose `token` and `organization_id` as read-only properties.
- [ ] 4. Implement `validate(cred_info)` classmethod.
- [ ] 5. Implement `as_dict()` extending the base mapping with both fields.
- [ ] 6. Explicitly omit any kubeconfig field — note in module docstring that
      kubeconfig issuance is the responsibility of
      `automojo-interop-coreweave` at use time per §7 decision.
- [ ] 7. Register the class in `wellknown.py` under categories
      `["hpc-venue", "coreweave-api-token"]`.
- [ ] 8. Add example-based unit tests covering construction, category enforcement,
      empty-token rejection, `validate()` behaviour, and `as_dict()` content for
      both `organization_id` states.
- [ ] 9. Add a `hypothesis` property test `test_coreweave_credential_roundtrip`
      asserting serialise → reconstruct equality.
- [ ] 10. Cross-link this spec from
       `automojo-provisioning/specs/venue-coreweave/design.md`.
