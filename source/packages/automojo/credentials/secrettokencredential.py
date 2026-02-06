
"""
    .. module:: secrettokencredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`SecretTokenCredential` used for third party verifications such as hCaptcha.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.basecredential import BaseCredential

class SecretTokenCredential(BaseCredential):
    """
        The :class:`SecretTokenCredential` is a container object for a secret token credential.

        .. code:: yaml
            "identifier": "hcaptcha"
            "category": "secret-token"
            "endpoint": "https://hcaptcha.com/siteverify"
            "token": "B130909CD9744F1E8679755034F9E70B08519F16C3DE46FCBFE82117F2794BA1"

    """

    def __init__(self, *, identifier: str, categories: List[str], endpoint: str, token: str, role: Optional[str] = "priv"):
        """
            Initializes a :class:`SecretTokenCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential
            :param endpoint: The endpoint of a service that has knowledge of the secret token.
            :param token: A token that services as a secret token.
            
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "secret-token" not in categories:
            raise ConfigurationError("The SecretTokenCredential should only be given credentials of category 'secret-token'.")
        if len(token) == 0:
            raise ConfigurationError("The SecretTokenCredential constructor requires a 'token' parameter be provided.")

        self._endpoint = endpoint
        self._token = token
        
        return

    @property
    def endpoint(self):
        """
            Returns the endpoint of the service that shares the secret token.

            :returns: The endpoint string.
        """
        return self._endpoint

    @property
    def token(self):
        """
            Returns the secret token.

            :returns: The token string.
        """
        return self._token

    @classmethod
    def validate(cls, cred_info) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a secret token credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "endpoint" not in cred_info or cred_info["endpoint"] is None:
            errors.append("missing 'endpoint' in secret token credential.")

        if "token" not in cred_info or cred_info["token"] is None:
            errors.append("missing 'token' in secret token credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["endpoint"] = self._endpoint
        rtnval["token"] = self._token
        
        return rtnval
