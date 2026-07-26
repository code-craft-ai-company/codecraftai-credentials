"""
    .. module:: digitaloceanapitokencredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`DigitalOceanApiTokenCredential` which
                   wraps the DigitalOcean venue personal-access-token authentication material.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os

from ccai.errors.exceptions import ConfigurationError

from ccai.credentials.basecredential import BaseCredential


class DigitalOceanApiTokenCredential(BaseCredential):
    """
        The :class:`DigitalOceanApiTokenCredential` is a container object that wraps the
        DigitalOcean venue personal-access-token authentication material.

        .. code:: yaml
            "identifier": "digitalocean-token"
            "category": "cloud-venue"
            "provider": "digitalocean"
            "token": "dop_v1_..."
            "spaces_access_key": "DO00..."
            "spaces_secret_key": "..."

        The Spaces keys are optional and separate from the API token because
        DigitalOcean issues them separately: Spaces is an S3-compatible object
        store authenticated with its own access-key pair, and the
        personal-access token has no authority there.  A credential that
        never touches buckets does not need them.
    """

    def __init__(self, *, identifier: str, categories: List[str], token: str,
                 spaces_access_key: Optional[str] = None,
                 spaces_secret_key: Optional[str] = None,
                 role: Optional[str] = "priv") -> None:
        """
            Initializes a :class:`DigitalOceanApiTokenCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param token: The DigitalOcean personal-access-token value.
            :param spaces_access_key: The S3-compatible Spaces access key, required
                                      only for bucket operations.
            :param spaces_secret_key: The S3-compatible Spaces secret key, required
                                      only for bucket operations.
            :param role: Identifies the role of the credential.

            :raises: ConfigurationError
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "cloud-venue" not in categories:
            errmsg_lines = [
                "The DigitalOceanApiTokenCredential should be given credentials of category 'cloud-venue'.",
                "MISSING CATEGORY: cloud-venue",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        if token is None or len(token) == 0:
            raise ConfigurationError("The DigitalOceanApiTokenCredential constructor requires a non-empty 'token' parameter be provided.")

        one_spaces_key_missing = (
            (spaces_access_key is None) != (spaces_secret_key is None)
        )
        if one_spaces_key_missing:
            errmsg_lines = [
                "The DigitalOceanApiTokenCredential Spaces keys must be supplied as a pair.",
                "Half a key pair cannot authenticate a bucket operation, and accepting it",
                "here would defer the failure to the first bucket call.",
                f"    spaces_access_key: {'set' if spaces_access_key is not None else 'missing'}",
                f"    spaces_secret_key: {'set' if spaces_secret_key is not None else 'missing'}",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        self._token = token
        self._spaces_access_key = spaces_access_key
        self._spaces_secret_key = spaces_secret_key
        return

    @property
    def token(self) -> str:
        """
            Returns the DigitalOcean personal-access-token value.

            :returns: The API token string.
        """
        return self._token

    @property
    def spaces_access_key(self) -> Optional[str]:
        """
            Returns the S3-compatible Spaces access key.

            :returns: The Spaces access key, or None when the credential carries
                      no bucket authority.
        """
        return self._spaces_access_key

    @property
    def spaces_secret_key(self) -> Optional[str]:
        """
            Returns the S3-compatible Spaces secret key.

            :returns: The Spaces secret key, or None when the credential carries
                      no bucket authority.
        """
        return self._spaces_secret_key

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a DigitalOcean API-token credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "token" not in cred_info:
            errors.append("missing 'token' in digitalocean-api-token credential.")

        has_access_key = "spaces_access_key" in cred_info
        has_secret_key = "spaces_secret_key" in cred_info
        if has_access_key != has_secret_key:
            present = "spaces_access_key" if has_access_key else "spaces_secret_key"
            absent = "spaces_secret_key" if has_access_key else "spaces_access_key"
            errors.append(
                f"digitalocean-api-token credential declares '{present}' without "
                f"'{absent}'; Spaces keys must be supplied as a pair."
            )

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["token"] = self._token

        if self._spaces_access_key is not None:
            rtnval["spaces_access_key"] = self._spaces_access_key
        if self._spaces_secret_key is not None:
            rtnval["spaces_secret_key"] = self._spaces_secret_key

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential with the secrets redacted.

            :returns: A redacted string representation safe for logs.
        """
        spaces = "absent"
        if self._spaces_access_key is not None:
            spaces = "'***'"

        rtnval = (
            "DigitalOceanApiTokenCredential("
            "identifier={!r}, categories={!r}, token='***', spaces_keys={})"
        ).format(self._identifier, self._categories, spaces)

        return rtnval
