"""
    .. module:: tailscaleauthkeycredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`TailscaleAuthKeyCredential` which
                   represents a pre-minted Tailscale auth key credential.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.basecredential import BaseCredential


class TailscaleAuthKeyCredential(BaseCredential):
    """
        The :class:`TailscaleAuthKeyCredential` is a container object for a pre-minted
        Tailscale auth key used to join nodes to a tailnet.

        .. code:: yaml
            "identifier": "ts-lab-key"
            "category": "tailscale-authkey"
            "authkey": "tskey-auth-XXXX-YYYY"
            "reusable": false
            "ephemeral": true
            "preauthorized": true

    """

    def __init__(self, *, identifier: str, categories: List[str], authkey: str,
                 reusable: bool = False, ephemeral: bool = True, preauthorized: bool = True,
                 role: Optional[str] = "priv"):
        """
            Initializes a :class:`TailscaleAuthKeyCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param authkey: The pre-minted Tailscale auth key value.
            :param reusable: Indicates whether the key may be used to join more than one node.
            :param ephemeral: Indicates whether nodes joined with this key are ephemeral.
            :param preauthorized: Indicates whether nodes joined with this key are pre-authorized.
            :param role: Identifies the role of the credential.
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "tailscale-authkey" not in categories:
            raise ConfigurationError("The TailscaleAuthKeyCredential should only be given credentials of category 'tailscale-authkey'.")
        if authkey is None or len(authkey) == 0:
            raise ConfigurationError("The TailscaleAuthKeyCredential constructor requires a non-empty 'authkey' parameter be provided.")

        self._authkey = authkey
        self._reusable = reusable
        self._ephemeral = ephemeral
        self._preauthorized = preauthorized
        return

    @property
    def authkey(self) -> str:
        """
            Returns the Tailscale auth key string.

            :returns: The auth key value.
        """
        return self._authkey

    @property
    def reusable(self) -> bool:
        """
            Indicates whether the auth key is reusable.

            :returns: True if the key is reusable, False otherwise.
        """
        return self._reusable

    @property
    def ephemeral(self) -> bool:
        """
            Indicates whether nodes joined with this key are ephemeral.

            :returns: True if joined nodes are ephemeral, False otherwise.
        """
        return self._ephemeral

    @property
    def preauthorized(self) -> bool:
        """
            Indicates whether nodes joined with this key are pre-authorized.

            :returns: True if joined nodes are pre-authorized, False otherwise.
        """
        return self._preauthorized

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a Tailscale auth key credential.

            :param cred_info: The credential information dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "authkey" not in cred_info:
            errors.append("missing 'authkey' in tailscale-authkey credential.")

        warnings.append("TailscaleAuthKeyCredential is recommended for lab use only; prefer 'TailscaleOAuthCredential' for production provisioning.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["authkey"] = self._authkey
        rtnval["reusable"] = self._reusable
        rtnval["ephemeral"] = self._ephemeral
        rtnval["preauthorized"] = self._preauthorized

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential with the auth key redacted.

            :returns: A redacted string representation safe for logs.
        """
        rtnval = (
            "TailscaleAuthKeyCredential("
            "identifier={!r}, categories={!r}, authkey='***', "
            "reusable={!r}, ephemeral={!r}, preauthorized={!r})"
        ).format(self._identifier, self._categories, self._reusable, self._ephemeral, self._preauthorized)

        return rtnval
