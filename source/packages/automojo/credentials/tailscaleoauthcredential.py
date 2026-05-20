"""
    .. module:: tailscaleoauthcredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`TailscaleOAuthCredential` which
                   represents a Tailscale OAuth client used to mint ephemeral auth keys.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.basecredential import BaseCredential


class TailscaleOAuthCredential(BaseCredential):
    """
        The :class:`TailscaleOAuthCredential` is a container object for a Tailscale
        OAuth client used by the control plane to mint short-lived ephemeral auth keys.

        .. code:: yaml
            "identifier": "ts-prov-oauth"
            "category": "tailscale-oauth"
            "client_id": "ksXXXX"
            "client_secret": "tskey-client-secret-XXXX"
            "default_tags": ["tag:lab"]

    """

    def __init__(self, *, identifier: str, categories: List[str], client_id: str,
                 client_secret: str, default_tags: Optional[List[str]] = None,
                 role: Optional[str] = "priv"):
        """
            Initializes a :class:`TailscaleOAuthCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param client_id: The Tailscale OAuth client identifier.
            :param client_secret: The Tailscale OAuth client secret.
            :param default_tags: Optional list of tags applied by default to keys minted from this client.
            :param role: Identifies the role of the credential.
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "tailscale-oauth" not in categories:
            raise ConfigurationError("The TailscaleOAuthCredential should only be given credentials of category 'tailscale-oauth'.")
        if client_id is None or len(client_id) == 0:
            raise ConfigurationError("The TailscaleOAuthCredential constructor requires a non-empty 'client_id' parameter be provided.")
        if client_secret is None or len(client_secret) == 0:
            raise ConfigurationError("The TailscaleOAuthCredential constructor requires a non-empty 'client_secret' parameter be provided.")

        tags = default_tags
        if tags is None:
            tags = []

        self._client_id = client_id
        self._client_secret = client_secret
        self._default_tags = tags
        return

    @property
    def client_id(self) -> str:
        """
            Returns the Tailscale OAuth client identifier.

            :returns: The OAuth client id string.
        """
        return self._client_id

    @property
    def client_secret(self) -> str:
        """
            Returns the Tailscale OAuth client secret.

            :returns: The OAuth client secret string.
        """
        return self._client_secret

    @property
    def default_tags(self) -> List[str]:
        """
            Returns the default tag list applied to keys minted from this client.

            :returns: The list of default tag strings.
        """
        return self._default_tags

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a Tailscale OAuth credential.

            :param cred_info: The credential information dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "client_id" not in cred_info:
            errors.append("missing 'client_id' in tailscale-oauth credential.")

        if "client_secret" not in cred_info:
            errors.append("missing 'client_secret' in tailscale-oauth credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["client_id"] = self._client_id
        rtnval["client_secret"] = self._client_secret
        rtnval["default_tags"] = self._default_tags

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential with the client secret redacted.

            :returns: A redacted string representation safe for logs.
        """
        rtnval = (
            "TailscaleOAuthCredential("
            "identifier={!r}, categories={!r}, client_id={!r}, "
            "client_secret='***', default_tags={!r})"
        ).format(self._identifier, self._categories, self._client_id, self._default_tags)

        return rtnval
