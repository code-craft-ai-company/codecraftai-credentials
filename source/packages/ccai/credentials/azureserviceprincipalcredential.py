"""
    .. module:: azureserviceprincipalcredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`AzureServicePrincipalCredential` which
                   represents an Azure service principal credential for cloud-venue access.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os

from ccai.errors.exceptions import ConfigurationError

from ccai.credentials.basecredential import BaseCredential


class AzureServicePrincipalCredential(BaseCredential):
    """
        The :class:`AzureServicePrincipalCredential` is a container object for an Azure
        service principal credential used for application-based access to Azure cloud venues.

        .. code:: yaml
            "identifier": "azure-sp"
            "category": "cloud-venue"
            "provider": "azure-service-principal"
            "tenant_id": ""
            "client_id": ""
            "client_secret": "@@&_@@&_LetMeComeIn"

    """

    def __init__(self, *, identifier: str, categories: List[str], tenant_id: str, client_id: str,
                 client_secret: str, role: Optional[str] = "priv") -> None:
        """
            Initializes an :class:`AzureServicePrincipalCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param tenant_id: The Microsoft Azure tenant id.
            :param client_id: The Microsoft Azure client (application) id.
            :param client_secret: The Microsoft Azure client secret.
            :param role: Identifies the role of the credential.

            :raises: ConfigurationError
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "cloud-venue" not in categories:
            errmsg_lines = [
                "The AzureServicePrincipalCredential should be given credentials of category 'cloud-venue'.",
                "MISSING CATEGORY: cloud-venue",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        if tenant_id is None or len(tenant_id) == 0:
            raise ConfigurationError("The AzureServicePrincipalCredential constructor requires a non-empty 'tenant_id' parameter be provided.")
        if client_id is None or len(client_id) == 0:
            raise ConfigurationError("The AzureServicePrincipalCredential constructor requires a non-empty 'client_id' parameter be provided.")
        if client_secret is None or len(client_secret) == 0:
            raise ConfigurationError("The AzureServicePrincipalCredential constructor requires a non-empty 'client_secret' parameter be provided.")

        self._tenant_id = tenant_id
        self._client_id = client_id
        self._client_secret = client_secret
        return

    @property
    def client_id(self) -> str:
        """
            Returns the Azure client (application) identifier for this credential.

            :returns: The Azure client identifier string.
        """
        return self._client_id

    @property
    def client_secret(self) -> str:
        """
            Returns the Azure client secret.

            :returns: The client secret string.
        """
        return self._client_secret

    @property
    def tenant_id(self) -> str:
        """
            Returns the Azure tenant identifier.

            :returns: The tenant identifier string.
        """
        return self._tenant_id

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing an Azure service principal credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "tenant_id" not in cred_info:
            errors.append("missing 'tenant_id' in azure-service-principal credential.")

        if "client_id" not in cred_info:
            errors.append("missing 'client_id' in azure-service-principal credential.")

        if "client_secret" not in cred_info:
            errors.append("missing 'client_secret' in azure-service-principal credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["tenant_id"] = self._tenant_id
        rtnval["client_id"] = self._client_id
        rtnval["client_secret"] = self._client_secret

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential with the client secret redacted.

            :returns: A redacted string representation safe for logs.
        """
        rtnval = (
            "AzureServicePrincipalCredential("
            "identifier={!r}, categories={!r}, tenant_id={!r}, client_id={!r}, "
            "client_secret='***')"
        ).format(self._identifier, self._categories, self._tenant_id, self._client_id)

        return rtnval
