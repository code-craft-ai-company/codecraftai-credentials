"""
    .. module:: githubappcredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`GithubAppCredential` which represents
                   a GitHub application private key credential.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Any, Dict, List, Optional, Tuple

import os

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.basecredential import BaseCredential


class GithubAppCredential(BaseCredential):
    """
        The :class:`GithubAppCredential` is a container object for GitHub application
        credentials.

        .. code:: yaml
            "identifier": "github-app"
            "category": "github-app"
            "keyfiles": ["~/.config/github/app.pem"]
            "keys": ["-----BEGIN PRIVATE KEY-----..."]
            "keypasswd": ["password1"]
    """

    def __init__(self, *, identifier: str, categories: List[str],
                 keyfiles: Optional[List[str]] = None,
                 keys: Optional[List[str]] = None,
                 keypasswd: Optional[List[Optional[str]]] = None,
                 role: Optional[str] = "priv"):
        """
            Initializes a :class:`GithubAppCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential
            :param keyfiles: A list of private key files that can be used to authenticate with GitHub as an app
            :param keys: A list of raw private keys that can be used to authenticate with GitHub
            :param keypasswd: Optional list of passwords for the key files.
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "github-app" not in categories:
            raise ConfigurationError("The GithubAppCredential should only be given credentials of category 'github-app'.")

        if (not keyfiles or len(keyfiles) == 0) and (not keys or len(keys) == 0):
            raise ConfigurationError("The GithubAppCredential constructor requires either 'keyfiles' or 'keys' parameter be provided.")

        self._keyfiles = keyfiles or []
        self._keys = list(keys) if keys else []
        self._keypasswd = keypasswd

        if keyfiles:
            for kfile in keyfiles:
                abs_kfile = os.path.abspath(os.path.expandvars(os.path.expanduser(kfile)))
                if not os.path.exists(abs_kfile):
                    errmsg = f"GithubAppCredential keyfile '{abs_kfile}' does not exist."
                    raise ConfigurationError(errmsg)
                with open(abs_kfile, "r") as rpf:
                    kdata = rpf.read()
                self._keys.append(kdata)

        return

    @property
    def keyfiles(self) -> List[str]:
        """
            Returns the list of key file paths used by this credential.

            :returns: List of key file paths.
        """
        return self._keyfiles

    @property
    def keys(self) -> List[str]:
        """
            Returns the list of private keys associated with this credential.

            :returns: List of private key strings.
        """
        return self._keys

    @property
    def keypasswd(self) -> Optional[List[Optional[str]]]:
        """
            Returns the list of passwords associated with the key files if provided.

            :returns: List of key file passwords or ``None``.
        """
        return self._keypasswd

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a GitHub application credential.

            :param cred_info: The credential information dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """
        errors: List[str] = []
        warnings: List[str] = []

        has_keyfiles = False
        if "keyfiles" in cred_info:
            keyfiles = cred_info["keyfiles"]
            if not isinstance(keyfiles, list):
                errors.append("'keyfiles' must be a list in github-app credential.")
            else:
                has_keyfiles = len(keyfiles) > 0
                for kfile in keyfiles:
                    path = os.path.abspath(os.path.expandvars(os.path.expanduser(kfile)))
                    if not os.path.exists(path):
                        errors.append(f"specified keyfile '{path}' not found.")

        has_keys = False
        if "keys" in cred_info:
            keys = cred_info["keys"]
            if not isinstance(keys, list):
                errors.append("'keys' must be a list in github-app credential.")
            else:
                has_keys = len(keys) > 0

        if not has_keyfiles and not has_keys:
            errors.append("either 'keyfiles' or 'keys' must be provided in github-app credential.")

        if has_keyfiles and "keypasswd" in cred_info:
            keypasswd = cred_info["keypasswd"]
            if not isinstance(keypasswd, list):
                errors.append("'keypasswd' must be a list when 'keyfiles' are specified in github-app credential.")
            elif len(keypasswd) != len(cred_info["keyfiles"]):
                warnings.append("'keypasswd' length does not match 'keyfiles' length in github-app credential.")
        elif has_keyfiles is False and "keypasswd" in cred_info:
            warnings.append("'keypasswd' provided without 'keyfiles' in github-app credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        if len(self._keyfiles) > 0:
            rtnval["keyfiles"] = self._keyfiles

        rtnval["keys"] = self._keys

        if self._keypasswd is not None:
            rtnval["keypasswd"] = self._keypasswd

        return rtnval
