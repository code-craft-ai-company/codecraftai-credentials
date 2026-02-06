"""
    .. module:: azureclientsecretcredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`AzureClientSecretCredential` which is used
            for application access to Azure.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.basecredential import BaseCredential

class AzureClientSecretCredential(BaseCredential):
    """
        The :class:`AzureClientSecretCredential` is a container object for the parameters for a Microsoft Azure 'ClientSecretCredential'.

        .. code:: yaml
            "identifier": "azure-client"
            "category": "azure-client-secret"
            "tenant_id": ""
            "client_id": ""
            "client_secret": "@@&_@@&_LetMeComeIn"

    """

    def __init__(self, *, identifier: str, categories: List[str], tenant_id: str, client_id: str,
                 client_secret: str, role: Optional[str] = "priv"):
        """
            Initializes an :class:`AzureClientSecretCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential
            :param tenant_id: The Microsoft Azure tenant id.
            :param client_id: The Microsoft Azure client id.
            :param client_secret: The Microsoft Azure client secret.
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "azure-client-secret" not in categories:
            raise ConfigurationError("The AzureClientSecretCredential should only be given credentials of category 'azure-client-secret'.")

        self._tenant_id = tenant_id
        self._client_id = client_id
        self._client_secret = client_secret
        return

    @property
    def client_id(self):
        """
            Returns the Azure client identifier for this credential.

            :returns: Azure client identifier.
        """
        return self._client_id
    
    @property
    def client_secret(self):
        """
            Returns the Azure client secret.

            :returns: The client secret string.
        """
        return self._client_secret

    @property
    def tenant_id(self):
        """
            Returns the Azure tenant identifier.

            :returns: The tenant identifier string.
        """
        return self._tenant_id

    @classmethod
    def validate(cls, cred_info) -> Tuple[List[str], List[str]]:
        """
            Validates a dictionary describing an Azure client secret credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "client_id" not in cred_info or cred_info["client_id"] is None:
            errors.append("missing 'client_id' in azure-client-secret credential.")

        if "client_secret" not in cred_info or cred_info["client_secret"] is None:
            errors.append("missing 'client_secret' in azure-client-secret credential.")

        if "tenant_id" not in cred_info or cred_info["tenant_id"] is None:
            errors.append("missing 'tenant_id' in azure-client-secret credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["client_id"] = self._client_id
        rtnval["client_secret"] = self._client_secret
        rtnval["tenant_id"] = self._tenant_id
        
        return rtnval
