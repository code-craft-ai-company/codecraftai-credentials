"""
    .. module:: coreweaveapicredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`CoreweaveApiCredential` which
                   wraps the CoreWeave venue API-token authentication material.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os

from ccai.errors.exceptions import ConfigurationError

from ccai.credentials.basecredential import BaseCredential


class CoreweaveApiCredential(BaseCredential):
    """
        The :class:`CoreweaveApiCredential` is a container object that wraps the
        CoreWeave venue API-token authentication material plus an optional
        organisation scope.  The credential intentionally does not hold a
        kubeconfig; kubeconfig issuance happens inside ``codecraftai-interop-coreweave``
        at use time.

        .. code:: yaml
            "identifier": "coreweave-token"
            "category": "hpc-venue"
            "provider": "coreweave"
            "token": "..."
            "organization_id": null

    """

    def __init__(self, *, identifier: str, categories: List[str], token: str,
                 organization_id: Optional[str] = None,
                 role: Optional[str] = "priv") -> None:
        """
            Initializes a :class:`CoreweaveApiCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param token: The CoreWeave API token value.
            :param organization_id: The optional CoreWeave organisation scope.
            :param role: Identifies the role of the credential.

            :raises: ConfigurationError
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "hpc-venue" not in categories:
            errmsg_lines = [
                "The CoreweaveApiCredential should be given credentials of category 'hpc-venue'.",
                "MISSING CATEGORY: hpc-venue",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        if token is None or len(token) == 0:
            raise ConfigurationError("The CoreweaveApiCredential constructor requires a non-empty 'token' parameter be provided.")

        self._token = token
        self._organization_id = organization_id
        return

    @property
    def token(self) -> str:
        """
            Returns the CoreWeave API token value.

            :returns: The API token string.
        """
        return self._token

    @property
    def organization_id(self) -> Optional[str]:
        """
            Returns the CoreWeave organisation scope.

            :returns: The organisation identifier string, or None.
        """
        return self._organization_id

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a CoreWeave API credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "token" not in cred_info:
            errors.append("missing 'token' in coreweave-api-token credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["token"] = self._token
        rtnval["organization_id"] = self._organization_id

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential with the token redacted.

            :returns: A redacted string representation safe for logs.
        """
        rtnval = (
            "CoreweaveApiCredential("
            "identifier={!r}, categories={!r}, token='***', organization_id={!r})"
        ).format(self._identifier, self._categories, self._organization_id)

        return rtnval
