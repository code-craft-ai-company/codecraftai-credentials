"""
    .. module:: publickeycredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`PublicKeyCredential` which represents
                   a public and private key pair.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, List, Optional

import os

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.basecredential import BaseCredential

class PublicKeyCredential(BaseCredential):
    """
        The :class:`PublicKeyCredential` is a container object for a public and private key pair.

        .. code:: yaml
            "identifier": "somename"
            "category": "public-key"
            "public": "FETD64DUFYLUFY"
            "private": "B130909CD9744F1E8679755034F9E70B08519F16C3DE46FCBFE82117F2794BA1"

    """

    def __init__(self, *, identifier: str, categories: List[str], public: str, private: str, role: Optional[str] = "priv"):
        """
            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential
            :param public: The public key value.
            :param private: The private key value.
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "public-key" not in categories:
            raise ConfigurationError("The PublicKeyCredential should only be given credentials of category 'public-key'.")
        if len(public) == 0:
            raise ConfigurationError("The PublicKeyCredential constructor requires a 'public' parameter be provided.")
        if len(private) == 0:
            raise ConfigurationError("The PublicKeyCredential constructor requires a 'private' parameter be provided.")
        
        self._public = public
        self._private = private
        return

    @property
    def public(self):
        """
            Returns the public key value.

            :returns: The public key string.
        """
        return self._public
    
    @property
    def private(self):
        """
            Returns the private key value.

            :returns: The private key string.
        """
        return self._private
    

    @classmethod
    def validate(cls, cred_info):
        """
            Validates the dictionary describing a public/private key credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: None
        """

        errmsg_lines = []

        if "public" not in cred_info:
                errmsg_lines.append("    * missing 'public' in a public key credential.")
        
        if "private" not in cred_info:
                errmsg_lines.append("    * missing 'private' in a public key credential.")

        if len(errmsg_lines) > 0:
            identifier = "????"
            if "identifier" in cred_info:
                identifier = cred_info["identifier"]

            errmsg = "Errors found while validating the '{}' public key credential:".format(identifier)
            errmsg_lines.insert(0, errmsg)
            errmsg = os.linesep.join(errmsg_lines)

            raise ConfigurationError(errmsg) from None

        return
    
    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["public"] = self._public
        rtnval["private"] = self._private

        return rtnval
