# Implementation Plan — Well-Known VPN and Venue Categories

## Module and Models

- [x] 1. Open `codecraftai-credentials/source/packages/ccai/credentials/wellknown.py`
  for in-place extension.
- [x] 2. Add the five category constants: `CATEGORY_VPN`,
  `CATEGORY_MESH`, `CATEGORY_CLOUD_VENUE`, `CATEGORY_VM_VENUE`,
  `CATEGORY_HPC_VENUE`.
- [x] 3. Add `WELL_KNOWN_CATEGORY_MEMBERSHIP` dict with the seed
  entries listed in the design (VPN seeded; venue umbrellas seeded
  with the categories already present in the codebase).
- [x] 4. Confirm `CredentialManager.get_credentials_by_categories(
  categories=...)` exists; add it if missing.

## Helpers — To Implement

- [x] 5. Implement `_require_initialised_singleton()` raising
  `SemanticError` with a clear message when the singleton is `None`.
- [x] 6. Implement `get_credentials_by_category(category)` that
  expands umbrella categories via `WELL_KNOWN_CATEGORY_MEMBERSHIP`
  and delegates to `CredentialManager.get_credentials_by_categories`.
- [x] 7. Update module `__all__` to export all new symbols.
- [x] 8. Add Sphinx-style docstrings on every new public symbol.

## Testing

- [x] 9. `test_category_constants_exported`.
- [x] 10. `test_membership_seed_for_vpn`.
- [x] 11. `test_get_credentials_by_category_umbrella_expansion_vpn`.
- [x] 12. `test_get_credentials_by_category_umbrella_expansion_cloud_venue`.
- [x] 13. `test_get_credentials_by_category_per_provider_lookup`.
- [x] 14. `test_get_credentials_by_category_raises_when_singleton_uninitialised`.
- [x] 15. `test_existing_credentialmanagersingleton_signature_unchanged`.
