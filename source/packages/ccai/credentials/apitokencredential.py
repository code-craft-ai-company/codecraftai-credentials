"""
    .. module:: apitokencredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`ApiTokenCredential` which is a simple
                   container used to hold an API token.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

from ccai.errors.exceptions import ConfigurationError

from ccai.credentials.basecredential import BaseCredential

class ApiTokenCredential(BaseCredential):
    """
        The :class:`ApiTokenCredential` is a container object for an api token credential.

        .. code:: yaml
            "identifier": "jira-token"
            "category": "api-token"
            "token": "B130909CD9744F1E8679755034F9E70B08519F16C3DE46FCBFE82117F2794BA1"

    """

    def __init__(self, *, identifier: str, categories: List[str], token: str, role: Optional[str] = "priv"):
        """
            Initializes an :class:`ApiTokenCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential
            :param token: A token that serves as an identity credential used to authenticate
                            access to specific APIs.
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "api-token" not in categories:
            raise ConfigurationError("The ApiTokenCredential should only be given credentials of category 'api-token'.")
        if token is None or len(token) == 0:
            raise ConfigurationError("The ApiTokenCredential constructor requires a 'token' parameter be provided.")
        
        self._token = token
        return

    @property
    def token(self) -> str:
        """
            Returns the API token string.

            :returns: The API token value.
        """
        return self._token

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing an API token credential.

            :param cred_info: The credential information dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "token" not in cred_info:
            errors.append("missing 'token' in api token credential.")

        return errors, warnings
    
    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["token"] = self._token
        
        return rtnval
