"""
    .. module:: vspherecredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`VSphereCredential` which
                   wraps VSphere username/password and/or SSO-token credential
                   material for the VSphere venue provisioner.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os

from ccai.errors.exceptions import ConfigurationError

from ccai.credentials.basecredential import BaseCredential


class VSphereCredential(BaseCredential):
    """
        The :class:`VSphereCredential` is a container object that wraps the
        VSphere/vCenter SSO authentication material.  It carries a username
        plus either a password, an SSO token, or both.  VSphere is a
        VM-shaped venue, so the credential is registered under the
        ``vm-venue`` category.

        .. code:: yaml
            "identifier": "vsphere-cred"
            "category": "vm-venue"
            "provider": "vsphere"
            "username": "administrator@vsphere.local"
            "password": "@@&_@@&_LetMeComeIn"
            "sso_token": null

    """

    REQUIRED_CATEGORY = "vm-venue"

    def __init__(self, *, identifier: str, categories: List[str], username: str,
                 password: Optional[str] = None, sso_token: Optional[str] = None,
                 role: Optional[str] = "priv") -> None:
        """
            Initializes a :class:`VSphereCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param username: The VSphere SSO username associated with this credential.
            :param password: The optional VSphere SSO password.
            :param sso_token: The optional pre-minted VSphere SSO session token.
            :param role: Identifies the role of the credential.

            :raises: ConfigurationError
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if self.REQUIRED_CATEGORY not in categories:
            errmsg_lines = [
                "The VSphereCredential should be given credentials of category 'vm-venue'.",
                "MISSING CATEGORY: {}".format(self.REQUIRED_CATEGORY),
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        if username is None or len(username) == 0:
            raise ConfigurationError("The VSphereCredential constructor requires a non-empty 'username' parameter be provided.")

        password_present = password is not None and len(password) > 0
        sso_token_present = sso_token is not None and len(sso_token) > 0

        if not password_present and not sso_token_present:
            errmsg_lines = [
                "The VSphereCredential constructor requires one of 'password' or 'sso_token' to be provided.",
                "PROVIDE: a non-empty 'password' or a non-empty 'sso_token'.",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        self._username = username
        self._password = password
        self._sso_token = sso_token
        return

    @property
    def username(self) -> str:
        """
            Returns the VSphere SSO username associated with this credential.

            :returns: The username string.
        """
        return self._username

    @property
    def password(self) -> Optional[str]:
        """
            Returns the VSphere SSO password associated with this credential.

            :returns: The password string, or None.
        """
        return self._password

    @property
    def sso_token(self) -> Optional[str]:
        """
            Returns the pre-minted VSphere SSO session token.

            :returns: The SSO token string, or None.
        """
        return self._sso_token

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a VSphere credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors: List[str] = []
        warnings: List[str] = []

        if "username" not in cred_info:
            errors.append("missing 'username' in vsphere credential.")

        has_password = "password" in cred_info and cred_info.get("password") not in (None, "")
        has_sso_token = "sso_token" in cred_info and cred_info.get("sso_token") not in (None, "")

        if not has_password and not has_sso_token:
            errors.append("one of 'password' or 'sso_token' is required in vsphere credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.

            :returns: A dictionary representation of the credential.
        """
        rtnval = super().as_dict()

        rtnval["username"] = self._username
        rtnval["password"] = self._password
        rtnval["sso_token"] = self._sso_token

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential with secret
            material redacted.

            :returns: A redacted string representation safe for logs.
        """
        password_repr = "None"
        if self._password is not None:
            password_repr = "'***'"

        sso_token_repr = "None"
        if self._sso_token is not None:
            sso_token_repr = "'***'"

        rtnval = (
            "VSphereCredential("
            "identifier={!r}, categories={!r}, username={!r}, "
            "password={}, sso_token={})"
        ).format(
            self._identifier, self._categories, self._username,
            password_repr, sso_token_repr,
        )

        return rtnval
