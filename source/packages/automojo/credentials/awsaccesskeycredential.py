"""
    .. module:: awsaccesskeycredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`AwsAccessKeyCredential` which
                   represents an AWS access key credential.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, List, Optional

import os

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.basecredential import BaseCredential

class AwsAccessKeyCredential(BaseCredential):
    """
        The :class:`AwsAccessKeyCredential` is a container object for an AWS
        access key credential.

        .. code:: yaml
            "identifier": "aws-cred"
            "category": "aws-access-key"
            "keyid": "FETD64DUFYLUFY"
            "secret": "B130909CD9744F1E8679755034F9E70B08519F16C3DE46FCBFE82117F2794BA1"

    """

    def __init__(self, *, identifier: str, categories: List[str], keyid: str, secret: str, role: Optional[str] = "priv"):
        """
            Initializes an :class:`AwsAccessKeyCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential
            :param keyid: The AWS key identifier.
            :param secret: The AWS secret key.
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "aws-access-key" not in categories:
            raise ConfigurationError("The AwsAccessKeyCredential should only be given credentials of category 'aws-access-key'.")
        if len(keyid) == 0:
            raise ConfigurationError("The AwsAccessKeyCredential constructor requires a 'keyid' parameter be provided.")
        if len(secret) == 0:
            raise ConfigurationError("The AwsAccessKeyCredential constructor requires a 'secret' parameter be provided.")
        
        self._keyid = keyid
        self._secret = secret
        return

    @property
    def keyid(self):
        """
            Returns the AWS key identifier associated with this credential.

            :returns: The key identifier string.
        """
        return self._keyid
    
    @property
    def secret(self):
        """
            Returns the AWS secret key.

            :returns: The secret key string.
        """
        return self._secret
    

    @classmethod
    def validate(cls, cred_info):
        """
            Validates the dictionary describing an AWS access key credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: None
        """

        errmsg_lines = []

        if "keyid" not in cred_info:
                errmsg_lines.append("    * missing 'keyid' in aws access key credential.")
        
        if "secret" not in cred_info:
                errmsg_lines.append("    * missing 'secret' in aws access key credential.")

        if len(errmsg_lines) > 0:
            identifier = "????"
            if "identifier" in cred_info:
                identifier = cred_info["identifier"]

            errmsg = "Errors found while validating the '{}' aws access key credential:".format(identifier)
            errmsg_lines.insert(0, errmsg)
            errmsg = os.linesep.join(errmsg_lines)

            raise ConfigurationError(errmsg) from None

        return

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["keyid"] = self._keyid
        rtnval["secret"] = self._secret
        
        return rtnval
