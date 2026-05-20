# Implementation Plan — Tailscale Credentials

## Module and Models

- [x] 1. Create `automojo-credentials/source/packages/automojo/credentials/tailscaleauthkeycredential.py`.
- [x] 2. Create `automojo-credentials/source/packages/automojo/credentials/tailscaleoauthcredential.py`.
- [x] 3. Mirror the file/module conventions from
  `awsaccesskeycredential.py` (header, copyright, Sphinx docstring).

## TailscaleAuthKeyCredential — To Implement

- [x] 4. Subclass `BaseCredential` with keyword-only constructor.
- [x] 5. Enforce `"tailscale-authkey" in categories` and non-empty
  `authkey`; raise `ConfigurationError` on violation.
- [x] 6. Store `_authkey`, `_reusable`, `_ephemeral`, `_preauthorized`
  in `__init__`.
- [x] 7. Expose `authkey`, `reusable`, `ephemeral`, `preauthorized`
  as read-only properties.
- [x] 8. Implement `classmethod validate(cls, cred_info)` returning
  `(errors, warnings)`; emit warning recommending OAuth for production.
- [x] 9. Implement `__repr__` redacting `authkey` as `"***"`.
- [x] 10. Include YAML sample in class docstring.

## TailscaleOAuthCredential — To Implement

- [x] 11. Subclass `BaseCredential` with keyword-only constructor.
- [x] 12. Enforce `"tailscale-oauth" in categories`, non-empty
  `client_id`, non-empty `client_secret`.
- [x] 13. Store `_client_id`, `_client_secret`, `_default_tags`.
- [x] 14. Expose `client_id`, `client_secret`, `default_tags` as
  read-only properties.
- [x] 15. Implement `classmethod validate(cls, cred_info)` returning
  `(errors, warnings)`.
- [x] 16. Implement `__repr__` redacting `client_secret` as `"***"`.
- [x] 17. Include YAML sample in class docstring.

## Testing

- [x] 18. `test_tailscaleauthkey_construction_succeeds`.
- [x] 19. `test_tailscaleauthkey_missing_category_raises`.
- [x] 20. `test_tailscaleauthkey_empty_authkey_raises`.
- [x] 21. `test_tailscaleauthkey_repr_redacts_secret`.
- [x] 22. `test_tailscaleauthkey_validate_emits_production_warning`.
- [x] 23. `test_tailscaleoauth_construction_succeeds`.
- [x] 24. `test_tailscaleoauth_missing_category_raises`.
- [x] 25. `test_tailscaleoauth_empty_client_id_raises`.
- [x] 26. `test_tailscaleoauth_empty_client_secret_raises`.
- [x] 27. `test_tailscaleoauth_repr_redacts_secret`.
- [x] 28. `test_tailscaleoauth_default_tags_optional`.
