"""
    .. module:: basiccredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`BasicCredential` which is a simple
                   username and password based credential.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

from ccai.errors.exceptions import ConfigurationError

from ccai.credentials.basecredential import BaseCredential

class BasicCredential(BaseCredential):
    """
        The :class:`BasicCredential` is a container object for a basic username and password based credential.

        .. code:: yaml
            "identifier": "basic-login"
            "category": "basic"
            "username": "ubuntu"
            "password": "@@&_@@&_LetMeComeIn"

    """

    def __init__(self, *, identifier: str, categories: List[str], username: str, password: str,
                 role: Optional[str] = "priv"):
        """
            Initializes a :class:`BasicCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential
            :param username: The username associated with this credential.
            :param password: The password associated with this credential.
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "basic" not in categories and "rest-basic" not in categories:
            raise ConfigurationError("The BasicCredential should only be given credentials of category 'basic'.")
        if len(username) == 0:
            raise ConfigurationError("The BasicCredential constructor requires a 'username' parameter be provided.")
        if password is None or len(password) == 0:
            raise ConfigurationError("The BasicCredential constructor requires a 'password' parameter be provided.")

        self._username = username
        self._password = password
        return

    @property
    def password(self):
        """
            Returns the password associated with this credential.

            :returns: The password string.
        """
        return self._password

    @property
    def username(self):
        """
            Returns the username associated with this credential.

            :returns: The username string.
        """
        return self._username

    @classmethod
    def validate(cls, cred_info) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a basic credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "password" not in cred_info:
            errors.append("missing 'password' in basic credential.")

        if "username" not in cred_info:
            errors.append("missing 'username' in basic credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["username"] = self._username
        rtnval["password"] = self._password

        return rtnval
