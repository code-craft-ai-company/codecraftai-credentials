"""
    .. module:: crusoeapikeycredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`CrusoeApiKeyCredential` which
                   wraps the two-field Crusoe Cloud API credential material.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.basecredential import BaseCredential


class CrusoeApiKeyCredential(BaseCredential):
    """
        The :class:`CrusoeApiKeyCredential` is a container object that wraps the
        two-field Crusoe Cloud API credential material.

        .. code:: yaml
            "identifier": "crusoe-key"
            "category": "hpc-venue"
            "access_key_id": "..."
            "secret": "..."

    """

    def __init__(self, *, identifier: str, categories: List[str], access_key_id: str,
                 secret: str, role: Optional[str] = "priv") -> None:
        """
            Initializes a :class:`CrusoeApiKeyCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param access_key_id: The Crusoe Cloud API access key identifier.
            :param secret: The Crusoe Cloud API secret value.
            :param role: Identifies the role of the credential.

            :raises: ConfigurationError
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "cloud-venue" not in categories and "hpc-venue" not in categories:
            errmsg_lines = [
                "The CrusoeApiKeyCredential should be given credentials of category 'cloud-venue' or 'hpc-venue'.",
                "MISSING CATEGORY: at least one of 'cloud-venue' or 'hpc-venue'",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        if access_key_id is None or len(access_key_id) == 0:
            raise ConfigurationError("The CrusoeApiKeyCredential constructor requires a non-empty 'access_key_id' parameter be provided.")
        if secret is None or len(secret) == 0:
            raise ConfigurationError("The CrusoeApiKeyCredential constructor requires a non-empty 'secret' parameter be provided.")

        self._access_key_id = access_key_id
        self._secret = secret
        return

    @property
    def access_key_id(self) -> str:
        """
            Returns the Crusoe Cloud API access key identifier.

            :returns: The access key identifier string.
        """
        return self._access_key_id

    @property
    def secret(self) -> str:
        """
            Returns the Crusoe Cloud API secret value.

            :returns: The secret string.
        """
        return self._secret

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a Crusoe Cloud API-key credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "access_key_id" not in cred_info:
            errors.append("missing 'access_key_id' in crusoe-api-key credential.")

        if "secret" not in cred_info:
            errors.append("missing 'secret' in crusoe-api-key credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["access_key_id"] = self._access_key_id
        rtnval["secret"] = self._secret

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential with the secret redacted.

            :returns: A redacted string representation safe for logs.
        """
        rtnval = (
            "CrusoeApiKeyCredential("
            "identifier={!r}, categories={!r}, access_key_id={!r}, secret='***')"
        ).format(self._identifier, self._categories, self._access_key_id)

        return rtnval
