# Design

## Overview

Two new credential classes are added under
`automojo-credentials/source/packages/automojo/credentials/`:

- `tailscaleauthkeycredential.py` — `TailscaleAuthKeyCredential`
- `tailscaleoauthcredential.py` — `TailscaleOAuthCredential`

Both subclass `BaseCredential` and follow the pattern established by
`awsaccesskeycredential.py`: keyword-only constructor with
`ConfigurationError`-based validation, typed read-only properties, a
`validate` classmethod returning `(errors, warnings)`, a YAML sample
in the class docstring, and a `__repr__` that redacts secret material.

The classes are registered with the well-known categories `vpn` and
`mesh` so the credential manager can hand back the right credential
to an `IVPNControlPlane` implementation by category lookup.

**See Also:** [vpn-control-plane-protocol](../../../automojo-interfaces/specs/vpn-control-plane-protocol/design.md),
[well-known-vpn-and-venue-categories](../well-known-vpn-and-venue-categories/design.md).

---

## Architecture

```
+---------------------------------+
| BaseCredential                  |
|  identifier / categories / role |
+----------------+----------------+
                 ^
        +--------+--------+
        |                 |
+-------+--------+ +------+-------------+
| TailscaleAuth- | | TailscaleOAuth-    |
| KeyCredential  | | Credential         |
|  authkey       | |  client_id         |
|  reusable      | |  client_secret     |
|  ephemeral     | |  default_tags      |
|  preauthorized | |                    |
+-------+--------+ +------+-------------+
        |                 |
        | category        | category
        | "tailscale-     | "tailscale-
        |  authkey"       |  oauth"
        v                 v
+--------------------------------------+
| CredentialManager (wellknown.py)     |
| categories: vpn, mesh                |
+--------------------------------------+
        |
        v
+--------------------------------------+
| IVPNControlPlane implementation      |
|  TailscaleControlPlane(credential)   |
+--------------------------------------+
```

---

## Data Model

```python
class TailscaleAuthKeyCredential(BaseCredential):
    """
        Container for a pre-minted Tailscale auth key.

        .. code:: yaml
            "identifier": "ts-lab-key"
            "category": "tailscale-authkey"
            "authkey": "tskey-auth-XXXX-YYYY"
            "reusable": false
            "ephemeral": true
            "preauthorized": true
    """

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        authkey: str,
        reusable: bool = False,
        ephemeral: bool = True,
        preauthorized: bool = True,
        role: Optional[str] = "priv",
    ) -> None:
        super().__init__(identifier=identifier, categories=categories, role=role)
        if "tailscale-authkey" not in categories:
            raise ConfigurationError(
                "TailscaleAuthKeyCredential requires category 'tailscale-authkey'."
            )
        if len(authkey) == 0:
            raise ConfigurationError(
                "TailscaleAuthKeyCredential requires a non-empty 'authkey'."
            )
        self._authkey = authkey
        self._reusable = reusable
        self._ephemeral = ephemeral
        self._preauthorized = preauthorized
        return


class TailscaleOAuthCredential(BaseCredential):
    """
        Container for a Tailscale OAuth client used to mint ephemeral keys.

        .. code:: yaml
            "identifier": "ts-prov-oauth"
            "category": "tailscale-oauth"
            "client_id": "ksXXXX"
            "client_secret": "tskey-client-secret-XXXX"
            "default_tags": ["tag:lab"]
    """

    def __init__(
        self,
        *,
        identifier: str,
        categories: List[str],
        client_id: str,
        client_secret: str,
        default_tags: Optional[List[str]] = None,
        role: Optional[str] = "priv",
    ) -> None:
        super().__init__(identifier=identifier, categories=categories, role=role)
        if "tailscale-oauth" not in categories:
            raise ConfigurationError(
                "TailscaleOAuthCredential requires category 'tailscale-oauth'."
            )
        if len(client_id) == 0:
            raise ConfigurationError(
                "TailscaleOAuthCredential requires a non-empty 'client_id'."
            )
        if len(client_secret) == 0:
            raise ConfigurationError(
                "TailscaleOAuthCredential requires a non-empty 'client_secret'."
            )
        tags = default_tags
        if tags is None:
            tags = []
        self._client_id = client_id
        self._client_secret = client_secret
        self._default_tags = tags
        return
```

Properties return the stored value; no computation. `__repr__` redacts
`authkey` and `client_secret` to `"***"`.

---

## Module Layout

```
automojo-credentials/source/packages/automojo/credentials/
  tailscaleauthkeycredential.py
  tailscaleoauthcredential.py
  wellknown.py            (extended — see sibling spec)
  basecredential.py       (existing)
  awsaccesskeycredential.py  (existing — template pattern)
```

---

## See Also

- [vpn-control-plane-protocol](../../../automojo-interfaces/specs/vpn-control-plane-protocol/design.md)
  — `TailscaleOAuthCredential` is the canonical credential consumed by
  `IVPNControlPlane.mint_authkey`.
- [twingate-credentials](../twingate-credentials/design.md) — peer
  credential spec for the other supported mesh-VPN provider.
- [well-known-vpn-and-venue-categories](../well-known-vpn-and-venue-categories/design.md)
  — registers the `vpn` / `mesh` categories.

---

## Testing Strategy

- **Construction tests.** Both classes construct successfully with
  the YAML-sample values; `ConfigurationError` is raised on missing
  category, empty `authkey`, empty `client_id`, empty `client_secret`.
- **Property accessor tests.** Each property returns the stored
  value verbatim; mutating returned lists does not affect future
  reads (defensive copy is *not* a requirement — read-only contract
  is documented).
- **`validate` tests.** Returns empty `errors` and (for
  `TailscaleAuthKeyCredential`) a warning recommending
  `TailscaleOAuthCredential` for production use.
- **`__repr__` redaction tests.** Assert that the string form contains
  the identifier and class name but never the raw `authkey` or
  `client_secret`.
- **No property tests required** — credential classes carry no
  non-trivial computation; validation is straightforward boolean
  checks.
