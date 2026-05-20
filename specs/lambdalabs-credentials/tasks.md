# Implementation Plan — lambdalabs-credentials

- [ ] 1. Create `lambdalabsapikeycredential.py` with `LambdalabsApiKeyCredential(BaseCredential)`, keyword-only
      constructor.
- [ ] 2. Enforce `hpc-venue` category and non-empty token in `__init__`.
- [ ] 3. Expose `token` as a read-only property.
- [ ] 4. Implement `validate(cred_info)` classmethod returning
      `(errors, warnings)`.
- [ ] 5. Implement `as_dict()` extending the base mapping with `token`.
- [ ] 6. Register the class in `wellknown.py` under categories
      `["hpc-venue", "lambdalabs-api-key"]`.
- [ ] 7. Add example-based unit tests for construction, category enforcement,
      empty-token rejection, `validate()` behaviour, and `as_dict()` content.
- [ ] 8. Add a `hypothesis` property test `test_lambdalabs_token_roundtrip` asserting
      serialise → reconstruct equality over arbitrary valid tokens.
- [ ] 9. Cross-link this spec from
      `automojo-provisioning/specs/venue-lambdalabs/design.md`.
