# Implementation Plan — Twingate Credentials

## Module and Models

- [x] 1. Create `codecraftai-credentials/source/packages/ccai/credentials/twingateserviceaccountcredential.py`.
- [x] 2. Mirror the file/module conventions from
  `awsaccesskeycredential.py` (header, copyright, Sphinx docstring).

## TwingateServiceAccountCredential — To Implement

- [x] 3. Subclass `BaseCredential` with keyword-only constructor.
- [x] 4. Enforce `"twingate-service-account" in categories`,
  non-empty `api_token`, non-empty `network_slug`, whitespace-free
  `network_slug`; raise `ConfigurationError` on violation.
- [x] 5. Store `_api_token` and `_network_slug` in `__init__`.
- [x] 6. Expose `api_token` and `network_slug` as read-only properties.
- [x] 7. Implement `classmethod validate(cls, cred_info)` returning
  `(errors, warnings)` and reporting each validation failure with a
  descriptive message.
- [x] 8. Implement `__repr__` redacting `api_token` as `"***"`.
- [x] 9. Include YAML sample in class docstring.

## Testing

- [x] 10. `test_twingate_construction_succeeds`.
- [x] 11. `test_twingate_missing_category_raises`.
- [x] 12. `test_twingate_empty_api_token_raises`.
- [x] 13. `test_twingate_empty_network_slug_raises`.
- [x] 14. `test_twingate_network_slug_with_whitespace_raises`.
- [x] 15. `test_twingate_repr_redacts_token`.
- [x] 16. `test_twingate_validate_reports_each_failure`.
