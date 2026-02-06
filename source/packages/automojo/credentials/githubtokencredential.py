"""
    .. module:: githubtokencredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`GithubTokenCredential` which represents
                   a GitHub personal access token credential.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.basecredential import BaseCredential


class GithubTokenCredential(BaseCredential):
    """
        The :class:`GithubTokenCredential` is a container object for a GitHub personal
        access token.  This credential can be used to authenticate GitHub REST API
        requests by placing the token value in the ``Authorization`` header.

        .. code:: yaml
            "identifier": "gh-token"
            "category": "github-token"
            "token": "ghp_xxxxxxxxxxxxxxxxxxxxx"
            "username": "git"

    """

    def __init__(self, *, identifier: str, categories: List[str], token: str,
                 username: str = "git", role: Optional[str] = "priv"):
        """
            Initializes a :class:`GithubTokenCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param token: A GitHub personal access token used to authenticate REST API requests.
            :param username: Optional username for logging and tracking purposes.  GitHub does not
                             verify the username for personal access tokens.  Defaults to ``'git'``.
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "github-token" not in categories:
            raise ConfigurationError(
                "The GithubTokenCredential should only be given credentials of category 'github-token'."
            )
        if token is None or len(token) == 0:
            raise ConfigurationError("The GithubTokenCredential constructor requires a 'token' parameter be provided.")

        self._token = token
        self._username = username
        return

    @property
    def token(self) -> str:
        """
            Returns the GitHub personal access token.

            :returns: The token string.
        """
        return self._token

    @property
    def username(self) -> str:
        """
            Returns the username associated with this credential.

            :returns: The username string.
        """
        return self._username

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a GitHub token credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors: List[str] = []
        warnings: List[str] = []

        if "token" not in cred_info or cred_info["token"] is None:
            errors.append("missing 'token' in github token credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["token"] = self._token
        rtnval["username"] = self._username

        return rtnval

