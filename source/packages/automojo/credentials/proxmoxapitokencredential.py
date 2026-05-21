"""
    .. module:: proxmoxapitokencredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`ProxmoxApiTokenCredential` which
                   wraps the Proxmox venue API-token authentication material.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os
import re

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.basecredential import BaseCredential


class ProxmoxApiTokenCredential(BaseCredential):
    """
        The :class:`ProxmoxApiTokenCredential` is a container object that wraps the
        Proxmox venue API-token authentication material.  The ``token_id`` carries
        the ``<user>@<realm>!<tokenname>`` form that Proxmox requires.

        .. code:: yaml
            "identifier": "proxmox-token"
            "category": "vm-venue"
            "token_id": "root@pam!automation"
            "secret": "..."

    """

    TOKEN_ID_PATTERN = r"^[^@!]+@[^@!]+![^@!]+$"

    def __init__(self, *, identifier: str, categories: List[str], token_id: str,
                 secret: str, role: Optional[str] = "priv") -> None:
        """
            Initializes a :class:`ProxmoxApiTokenCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param token_id: The Proxmox API token id in ``<user>@<realm>!<tokenname>`` form.
            :param secret: The Proxmox API token secret value.
            :param role: Identifies the role of the credential.

            :raises: ConfigurationError
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "vm-venue" not in categories:
            errmsg_lines = [
                "The ProxmoxApiTokenCredential should be given credentials of category 'vm-venue'.",
                "MISSING CATEGORY: vm-venue",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        if token_id is None or len(token_id) == 0:
            raise ConfigurationError("The ProxmoxApiTokenCredential constructor requires a non-empty 'token_id' parameter be provided.")
        if secret is None or len(secret) == 0:
            raise ConfigurationError("The ProxmoxApiTokenCredential constructor requires a non-empty 'secret' parameter be provided.")

        matched = re.match(self.TOKEN_ID_PATTERN, token_id)
        if matched is None:
            errmsg_lines = [
                "The ProxmoxApiTokenCredential 'token_id' parameter has an invalid format.",
                "EXPECTED FORMAT: <user>@<realm>!<tokenname>",
                "PROVIDED VALUE: {}".format(token_id),
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        self._token_id = token_id
        self._secret = secret
        return

    @property
    def token_id(self) -> str:
        """
            Returns the Proxmox API token id.

            :returns: The token id string.
        """
        return self._token_id

    @property
    def secret(self) -> str:
        """
            Returns the Proxmox API token secret value.

            :returns: The token secret string.
        """
        return self._secret

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a Proxmox API-token credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "token_id" not in cred_info:
            errors.append("missing 'token_id' in proxmox-api-token credential.")

        if "secret" not in cred_info:
            errors.append("missing 'secret' in proxmox-api-token credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["token_id"] = self._token_id
        rtnval["secret"] = self._secret

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential with the secret redacted.

            :returns: A redacted string representation safe for logs.
        """
        rtnval = (
            "ProxmoxApiTokenCredential("
            "identifier={!r}, categories={!r}, token_id={!r}, secret='***')"
        ).format(self._identifier, self._categories, self._token_id)

        return rtnval
