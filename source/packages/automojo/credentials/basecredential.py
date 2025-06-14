"""
    .. module:: basecredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`BaseCredential` object which is the
                   common base class that all other credential objects inherit from.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, List, Optional

from automojo.errors.exceptions import ConfigurationError

class BaseCredential:
    """
        The :class:`BaseCredential` is the base container object for credentials passed in the landscape
        configuration file.

        .. code:: yaml
            "identifier": "player-ssh"
            "category": "(category)"
    """
    def __init__(self, *, identifier: str, categories: List[str], role: Optional[str]="priv"):
        """
            Initializes a :class:`BaseCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that the credential can
                               be used for.
            :param role: Identifies the role of the credential
        """
        if len(identifier) == 0:
            raise ConfigurationError("The BaseCredential constructor requires a 'identifier' parameter be provided.")
        if len(categories) == 0:
            raise ConfigurationError("The BaseCredential constructor requires a 'categories' parameter be provided.")

        self._identifier = identifier
        self._categories = categories
        self._role = role
        return

    @property
    def categories(self):
        """
            Gets the authentication categories associated with this credential.

            :returns: A list of category names.
        """
        return self._categories

    @property
    def identifier(self):
        """
            Gets the identifier of this credential.

            :returns: The identifier string for the credential.
        """
        return self._identifier

    @property
    def role(self):
        """
            Gets the role assigned to this credential.

            :returns: The role name associated with this credential.
        """
        return self._role
    
    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """

        rtnval = {
            "identifier": self._identifier,
            "categories": self._categories,
            "role": self._role
        }
        
        return rtnval
