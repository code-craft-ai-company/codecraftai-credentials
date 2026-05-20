# Implementation Plan — crusoe-credentials

- [ ] 1. Create `crusoeapikeycredential.py` with
      `CrusoeApiKeyCredential(BaseCredential)`, keyword-only constructor.
- [ ] 2. Enforce that `categories` contains either `cloud-venue` or `hpc-venue`,
      and that `access_key_id` and `secret` are non-empty in `__init__`.
- [ ] 3. Expose `access_key_id` and `secret` as read-only properties.
- [ ] 4. Implement `validate(cred_info)` classmethod returning
      `(errors, warnings)`.
- [ ] 5. Implement `as_dict()` extending the base mapping with both fields.
- [ ] 6. Register the class in `wellknown.py` under categories
      `["cloud-venue", "hpc-venue", "crusoe-api-key"]`.
- [ ] 7. Add example-based unit tests covering construction, category enforcement,
      empty-field rejection, `validate()` reporting, and `as_dict()` content.
- [ ] 8. Add a `hypothesis` property test `test_crusoe_credential_roundtrip`
      asserting serialise → reconstruct equality.
- [ ] 9. Cross-link this spec from
      `automojo-provisioning/specs/venue-crusoe/design.md`.
