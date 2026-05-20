# Implementation Plan — oracle-credentials

- [x] 1. Create `oraclecloudapikeycredential.py` with
      `OracleCloudApiKeyCredential(BaseCredential)`, keyword-only constructor and
      the five field parameters plus optional `passphrase`.
- [x] 2. Enforce `cloud-venue` category and non-empty required fields in
      `__init__`.
- [x] 3. Validate OCID prefixes for `tenancy_ocid` and `user_ocid` in `__init__`.
- [x] 4. Expose `tenancy_ocid`, `user_ocid`, `private_key`, `fingerprint`,
      `passphrase` as read-only properties.
- [x] 5. Implement `validate(cred_info)` classmethod returning
      `(errors, warnings)`.
- [x] 6. Implement `as_dict()` extending the base mapping with the five fields.
- [x] 7. Register the class in `wellknown.py` under categories
      `["cloud-venue", "oracle-api-key"]`.
- [x] 8. Add example-based unit tests covering construction success, category
      enforcement, empty-field rejection, OCID-prefix rejection, `validate()`
      reporting, and `as_dict()` completeness for both passphrase states.
- [x] 9. Add a `hypothesis` property test `test_oracle_credential_roundtrip`
      asserting serialise → reconstruct equality over arbitrary valid OCID-prefixed
      inputs.
- [x] 10. Cross-link this spec from
       `automojo-provisioning/specs/venue-oracle/design.md`.
