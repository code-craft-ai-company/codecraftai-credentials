"""
    .. module:: azuremanagedidentitycredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`AzureManagedIdentityCredential` which
                   references an Azure managed identity resolved at use time.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.basecredential import BaseCredential


class AzureManagedIdentityCredential(BaseCredential):
    """
        The :class:`AzureManagedIdentityCredential` is a container object that references a
        system-assigned or user-assigned Azure managed identity.  No secret material is
        stored; the credential is resolved at use time against the Azure Instance Metadata
        Service from inside an Azure-hosted runtime.

        .. code:: yaml
            "identifier": "azure-mi"
            "category": "cloud-venue"
            "client_id": ""
            "resource_id": ""

    """

    def __init__(self, *, identifier: str, categories: List[str], client_id: Optional[str] = None,
                 resource_id: Optional[str] = None, role: Optional[str] = "priv") -> None:
        """
            Initializes an :class:`AzureManagedIdentityCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param client_id: The optional client id of a user-assigned managed identity.
            :param resource_id: The optional resource id of a user-assigned managed identity.
            :param role: Identifies the role of the credential.

            :raises: ConfigurationError
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "cloud-venue" not in categories:
            errmsg_lines = [
                "The AzureManagedIdentityCredential should be given credentials of category 'cloud-venue'.",
                "MISSING CATEGORY: cloud-venue",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        if client_id is None and resource_id is None:
            raise ConfigurationError("The AzureManagedIdentityCredential constructor requires at least one of 'client_id' or 'resource_id' be provided.")

        self._client_id = client_id
        self._resource_id = resource_id
        return

    @property
    def client_id(self) -> Optional[str]:
        """
            Returns the client id of the referenced user-assigned managed identity.

            :returns: The client identifier string, or None.
        """
        return self._client_id

    @property
    def resource_id(self) -> Optional[str]:
        """
            Returns the resource id of the referenced user-assigned managed identity.

            :returns: The resource identifier string, or None.
        """
        return self._resource_id

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing an Azure managed identity credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        has_client_id = "client_id" in cred_info
        has_resource_id = "resource_id" in cred_info

        if not has_client_id and not has_resource_id:
            errors.append("at least one of 'client_id' or 'resource_id' must be provided in azure-managed-identity credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["client_id"] = self._client_id
        rtnval["resource_id"] = self._resource_id

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential.

            :returns: A string representation safe for logs.
        """
        rtnval = (
            "AzureManagedIdentityCredential("
            "identifier={!r}, categories={!r}, client_id={!r}, resource_id={!r})"
        ).format(self._identifier, self._categories, self._client_id, self._resource_id)

        return rtnval
