# Implementation Plan — gcp-credentials

- [x] 1. Create `gcpserviceaccountkeycredential.py` with
      `GcpServiceAccountKeyCredential(BaseCredential)`, keyword-only constructor,
      properties for project / client email / private key id / private key / token
      uri.
- [x] 2. Enforce `cloud-venue` category and non-empty required strings.
- [x] 3. Default `token_uri` to `https://oauth2.googleapis.com/token` when omitted.
- [x] 4. Implement `validate(cred_info)` and `as_dict()` for the SA-key class.
- [x] 5. Create `gcpworkloadidentitycredential.py` with
      `GcpWorkloadIdentityCredential(BaseCredential)`, keyword-only constructor,
      properties for audience / subject token type / service account email / token
      url.
- [x] 6. Enforce `cloud-venue` category and non-empty required strings.
- [x] 7. Default `token_url` to the GCP STS endpoint when omitted.
- [x] 8. Implement `validate(cred_info)` and `as_dict()` for the WIF class.
- [x] 9. Register both classes in `wellknown.py` under the listed categories.
- [x] 10. Add example-based unit tests covering construction, category enforcement,
       defaults, missing-field validation, and `as_dict()` content.
- [x] 11. Add `hypothesis` property tests `test_gcp_service_account_key_roundtrip`
       and `test_gcp_workload_identity_roundtrip` asserting serialise → reconstruct
       equality over arbitrary valid inputs.
- [x] 12. Cross-link this spec from
       `codecraftai-provisioning/specs/venue-gcp/design.md`.
