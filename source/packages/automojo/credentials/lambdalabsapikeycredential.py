"""
    .. module:: lambdalabsapikeycredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`LambdalabsApiKeyCredential` which
                   wraps the Lambda Labs venue API-key authentication material.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.basecredential import BaseCredential


class LambdalabsApiKeyCredential(BaseCredential):
    """
        The :class:`LambdalabsApiKeyCredential` is a container object that wraps the
        Lambda Labs venue API-key authentication material.

        .. code:: yaml
            "identifier": "lambdalabs-key"
            "category": "hpc-venue"
            "token": "secret_..."

    """

    def __init__(self, *, identifier: str, categories: List[str], token: str,
                 role: Optional[str] = "priv") -> None:
        """
            Initializes a :class:`LambdalabsApiKeyCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param token: The Lambda Labs API key value.
            :param role: Identifies the role of the credential.

            :raises: ConfigurationError
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "hpc-venue" not in categories:
            errmsg_lines = [
                "The LambdalabsApiKeyCredential should be given credentials of category 'hpc-venue'.",
                "MISSING CATEGORY: hpc-venue",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        if token is None or len(token) == 0:
            raise ConfigurationError("The LambdalabsApiKeyCredential constructor requires a non-empty 'token' parameter be provided.")

        self._token = token
        return

    @property
    def token(self) -> str:
        """
            Returns the Lambda Labs API key value.

            :returns: The API key token string.
        """
        return self._token

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a Lambda Labs API-key credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "token" not in cred_info:
            errors.append("missing 'token' in lambdalabs-api-key credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["token"] = self._token

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential with the token redacted.

            :returns: A redacted string representation safe for logs.
        """
        rtnval = (
            "LambdalabsApiKeyCredential("
            "identifier={!r}, categories={!r}, token='***')"
        ).format(self._identifier, self._categories)

        return rtnval
