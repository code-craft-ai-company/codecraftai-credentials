"""
    .. module:: nutanixprismcredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`NutanixPrismCredential` which
                   wraps the Nutanix Prism Central authentication material.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.basecredential import BaseCredential


class NutanixPrismCredential(BaseCredential):
    """
        The :class:`NutanixPrismCredential` is a container object that wraps the
        Nutanix Prism Central authentication material: username + password plus
        the Prism Central endpoint URL.

        .. code:: yaml
            "identifier": "nutanix-prism"
            "category": "vm-venue"
            "username": "admin"
            "password": "..."
            "endpoint": "https://prism.example.com:9440"

    """

    ALLOWED_ENDPOINT_PREFIXES = ("http://", "https://")

    def __init__(self, *, identifier: str, categories: List[str], username: str,
                 password: str, endpoint: str, role: Optional[str] = "priv") -> None:
        """
            Initializes a :class:`NutanixPrismCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param username: The Nutanix Prism Central username.
            :param password: The Nutanix Prism Central password.
            :param endpoint: The Nutanix Prism Central endpoint URL.
            :param role: Identifies the role of the credential.

            :raises: ConfigurationError
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "vm-venue" not in categories:
            errmsg_lines = [
                "The NutanixPrismCredential should be given credentials of category 'vm-venue'.",
                "MISSING CATEGORY: vm-venue",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        if username is None or len(username) == 0:
            raise ConfigurationError("The NutanixPrismCredential constructor requires a non-empty 'username' parameter be provided.")
        if password is None or len(password) == 0:
            raise ConfigurationError("The NutanixPrismCredential constructor requires a non-empty 'password' parameter be provided.")
        if endpoint is None or len(endpoint) == 0:
            raise ConfigurationError("The NutanixPrismCredential constructor requires a non-empty 'endpoint' parameter be provided.")

        if not endpoint.startswith(self.ALLOWED_ENDPOINT_PREFIXES):
            errmsg_lines = [
                "The NutanixPrismCredential 'endpoint' parameter has an invalid scheme.",
                "EXPECTED PREFIXES: {}".format(", ".join(self.ALLOWED_ENDPOINT_PREFIXES)),
                "PROVIDED VALUE: {}".format(endpoint),
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        self._username = username
        self._password = password
        self._endpoint = endpoint
        return

    @property
    def username(self) -> str:
        """
            Returns the Nutanix Prism Central username.

            :returns: The username string.
        """
        return self._username

    @property
    def password(self) -> str:
        """
            Returns the Nutanix Prism Central password.

            :returns: The password string.
        """
        return self._password

    @property
    def endpoint(self) -> str:
        """
            Returns the Nutanix Prism Central endpoint URL.

            :returns: The endpoint URL string.
        """
        return self._endpoint

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a Nutanix Prism credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "username" not in cred_info:
            errors.append("missing 'username' in nutanix-prism credential.")

        if "password" not in cred_info:
            errors.append("missing 'password' in nutanix-prism credential.")

        if "endpoint" not in cred_info:
            errors.append("missing 'endpoint' in nutanix-prism credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["username"] = self._username
        rtnval["password"] = self._password
        rtnval["endpoint"] = self._endpoint

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential with the password redacted.

            :returns: A redacted string representation safe for logs.
        """
        rtnval = (
            "NutanixPrismCredential("
            "identifier={!r}, categories={!r}, username={!r}, password='***', endpoint={!r})"
        ).format(self._identifier, self._categories, self._username, self._endpoint)

        return rtnval
