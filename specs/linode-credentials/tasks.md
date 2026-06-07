# Implementation Plan — linode-credentials

- [x] 1. Create `linodeapitokencredential.py` with `LinodeApiTokenCredential(BaseCredential)`, keyword-only
      constructor.
- [x] 2. Enforce `cloud-venue` category and non-empty token in `__init__`.
- [x] 3. Expose `token` as a read-only property.
- [x] 4. Implement `validate(cred_info)` classmethod returning
      `(errors, warnings)`.
- [x] 5. Implement `as_dict()` extending the base mapping with `token`.
- [x] 6. Register the class in `wellknown.py` under categories
      `["cloud-venue", "linode-api-token"]`.
- [x] 7. Add example-based unit tests for construction, category enforcement,
      empty-token rejection, `validate()` behaviour, and `as_dict()` content.
- [x] 8. Add a `hypothesis` property test `test_linode_token_roundtrip` asserting
      serialise → reconstruct equality over arbitrary valid tokens.
- [x] 9. Cross-link this spec from
      `codecraftai-provisioning/specs/venue-linode/design.md`.
