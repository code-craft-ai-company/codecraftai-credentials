# Design

## Overview

`TwingateServiceAccountCredential` is added under
`automojo-credentials/source/packages/automojo/credentials/twingateserviceaccountcredential.py`.
It follows the `AwsAccessKeyCredential` / `TailscaleAuthKeyCredential`
pattern: keyword-only constructor with
`ConfigurationError`-based validation, typed read-only properties, a
`validate` classmethod returning `(errors, warnings)`, a YAML sample
in the docstring, and a `__repr__` that redacts the API token.

The asymmetry between Tailscale and Twingate (§3 of the design plan)
shows up here: Twingate has no flat key-minting story, so there is no
sibling `TwingateOAuthCredential`. Connector tokens are issued
through the control-plane API itself and are not credentials.

**See Also:** [tailscale-credentials](../tailscale-credentials/design.md),
[vpn-control-plane-protocol](../../../automojo-interfaces/specs/vpn-control-plane-protocol/design.md),
[well-known-vpn-and-venue-categories](../well-known-vpn-and-venue-categories/design.md).

---

## Architecture

```
+---------------------------------+
| BaseCredential                  |
+----------------+----------------+
                 ^
                 |
+----------------+----------------+
| TwingateServiceAccountCredential|
|  api_token (redacted in repr)   |
|  network_slug                   |
+----------------+----------------+
                 |
                 | category "twingate-service-account"
                 v
+---------------------------------+
| CredentialManager (wellknown.py)|
| categories: vpn, mesh           |
+---------------------------------+
                 |
                 v
+---------------------------------+
| TwingateControlPlane            |
|  (automojo-interop/vpn/twingate)|
|  GraphQL on /api/graphql/       |
+---------------------------------+
```

---

## Data Model

```python
class TwingateServiceAccountCredential(BaseCredential):
    """
        Container for a Twingate service-account API token and the network slug.

        .. code:: yaml
            "identifier": "tg-prod"
            "category": "twingate-service-account"
            "api_token": "tg-svc-XXXX"
            "network_slug": "acme"
    """

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        api_token: str,
        network_slug: str,
        role: Optional[str] = "priv",
    ) -> None:
        super().__init__(identifier=identifier, categories=categories, role=role)
        if "twingate-service-account" not in categories:
            raise ConfigurationError(
                "TwingateServiceAccountCredential requires category "
                "'twingate-service-account'."
            )
        if len(api_token) == 0:
            raise ConfigurationError(
                "TwingateServiceAccountCredential requires non-empty 'api_token'."
            )
        if len(network_slug) == 0:
            raise ConfigurationError(
                "TwingateServiceAccountCredential requires non-empty 'network_slug'."
            )
        if any(ch.isspace() for ch in network_slug):
            raise ConfigurationError(
                "TwingateServiceAccountCredential 'network_slug' must contain "
                "no whitespace."
            )
        self._api_token = api_token
        self._network_slug = network_slug
        return

    @property
    def api_token(self) -> str:
        return self._api_token

    @property
    def network_slug(self) -> str:
        return self._network_slug

    @classmethod
    def validate(cls, cred_info: dict) -> Tuple[List[str], List[str]]:
        errors: List[str] = []
        warnings: List[str] = []
        # ... mirror of AwsAccessKeyCredential.validate shape ...
        return (errors, warnings)
```

---

## Module Layout

```
automojo-credentials/source/packages/automojo/credentials/
  twingateserviceaccountcredential.py
  wellknown.py            (extended — see sibling spec)
  basecredential.py       (existing)
```

---

## See Also

- [tailscale-credentials](../tailscale-credentials/design.md) — peer
  credential classes for the other supported provider.
- [vpn-control-plane-protocol](../../../automojo-interfaces/specs/vpn-control-plane-protocol/design.md)
  — `TwingateControlPlane` consumes this credential.
- [well-known-vpn-and-venue-categories](../well-known-vpn-and-venue-categories/design.md).

---

## Testing Strategy

- **Construction tests.** Class constructs with the YAML-sample
  values. `ConfigurationError` raised on missing category, empty
  `api_token`, empty `network_slug`, whitespace-containing
  `network_slug`.
- **Property accessor tests.** `api_token` and `network_slug`
  return stored values verbatim.
- **`validate` tests.** Returns expected errors for missing /
  invalid fields.
- **`__repr__` redaction tests.** Asserts `api_token` does not appear
  in the string form; `identifier`, class name, and `network_slug`
  do appear.
- **No property tests required** — pure data-validation class with
  small input space and no algebraic invariants.
