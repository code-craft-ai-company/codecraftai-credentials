# Implementation Plan — azure-credentials

- [x] 1. Create `azureserviceprincipalcredential.py` with
      `AzureServicePrincipalCredential(BaseCredential)`, keyword-only constructor,
      `tenant_id` / `client_id` / `client_secret` properties.
- [x] 2. Add `cloud-venue` category enforcement in the constructor; raise
      `ConfigurationError` with descriptive messages for missing fields.
- [x] 3. Implement `validate(cred_info)` classmethod returning
      `(errors, warnings)`.
- [x] 4. Implement `as_dict()` extending the base mapping with the three Azure
      fields.
- [x] 5. Create `azuremanagedidentitycredential.py` with
      `AzureManagedIdentityCredential(BaseCredential)`, keyword-only constructor,
      optional `client_id` / `resource_id` properties.
- [x] 6. Enforce "at least one of `client_id`, `resource_id`" in the constructor.
- [x] 7. Implement `validate(cred_info)` and `as_dict()` for the managed-identity
      class.
- [x] 8. Register both classes in `wellknown.py` under the `cloud-venue` category
      and their respective sub-categories.
- [x] 9. Add example-based unit tests covering construction, category enforcement,
      missing-field validation, and `as_dict()` content.
- [x] 10. Add `hypothesis` property tests `test_service_principal_roundtrip` and
       `test_managed_identity_roundtrip` asserting serialise → reconstruct equality
       over arbitrary valid field combinations.
- [x] 11. Cross-link this spec from `codecraftai-provisioning/specs/venue-azure/design.md`
       under its See Also section.
