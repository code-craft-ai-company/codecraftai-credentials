"""
    .. module:: credentialmanager
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`CredentialManager` which is used to
                   load credentials.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Dict, List, Optional, Union

import logging
import os

from automojo.errors.exceptions import ConfigurationError

from automojo.credentials.apitokencredential import ApiTokenCredential
from automojo.credentials.awsaccesskeycredential import AwsAccessKeyCredential
from automojo.credentials.azureclientsecretcredential import AzureClientSecretCredential
from automojo.credentials.basiccredential import BasicCredential
from automojo.credentials.githubappcredential import GithubAppCredential
from automojo.credentials.personalapitokencredential import PersonalApiTokenCredential
from automojo.credentials.publickeycredential import PublicKeyCredential
from automojo.credentials.secrettokencredential import SecretTokenCredential
from automojo.credentials.sshcredential import SshCredential
from automojo.credentials.wifichoicecredential import WifiChoiceCredential

logger = logging.getLogger()

class CredentialManager:
    """
        The :class:`CredentialManager` provides for loading credential
        definitions and returning credential objects on demand.
    """

    def __init__(self):
        """
            Initializes an instance of the :class:`CredentialManager` class.

            The manager maintains a collection of credential objects loaded from
            configuration sources.
        """

        self._credentials = {}
        self._source_uris = []

        return

    @property
    def credentials(self):
        """
            Returns the dictionary of credentials loaded by the manager.

            :returns: Dictionary mapping credential identifiers to credential objects.
        """
        return self._credentials

    def lookup_credential(self, credkey: str) -> Union[ApiTokenCredential,
                                                      AzureClientSecretCredential,
                                                      BasicCredential,
                                                      GithubAppCredential,
                                                      PersonalApiTokenCredential,
                                                      PublicKeyCredential,
                                                      SecretTokenCredential,
                                                      SshCredential,
                                                      WifiChoiceCredential]:
        """
            Lookup a credential by key.
        """
        
        if credkey not in self._credentials:

            errmsg_lines = [
                f"Error missing credential '{credkey}'."
            ]
        
            if len(self._source_uris) > 0:
                errmsg_lines.append("CREDENTIAL URIS:")

                for cfile in self._source_uris:
                    errmsg_lines.append(f"    {cfile}")

            errmsg = os.linesep.join(errmsg_lines)

            raise ConfigurationError(errmsg)
        
        cred = self._credentials[credkey]
        
        return cred

    def load_credentials(self, credential_info: dict, source_uris: Optional[List[str]] = None):
        """
            Loads credentials from a dictionary object.

            :param credential_info: Dictionary containing credential definitions.
            :param source_uris: Optional list of source URIs for the credentials.
        """

        if source_uris != None:
            self._source_uris.extend(source_uris)

        if credential_info is not None and len(credential_info) > 0:
            try:
                credentials_list = credential_info["credentials"]
                errors, warnings = self._validate_credentials(credentials_list)

                if len(errors) == 0:
                    for credential in credentials_list:
                        # Copy the credential so if we modify it, we dont modify the
                        # original declaration.
                        credential = credential.copy()

                        if "identifier" not in credential:
                            errmsg = "Credential items in 'environment/credentials' must have an 'identifier' member."
                            raise ConfigurationError(errmsg)
                        ident = credential["identifier"]

                        if "category" not in credential and "categories" not in credential:
                            errmsg = "Credential items in 'environment/credentials' must have an 'category' or categories member."
                            raise ConfigurationError(errmsg)

                        # If we find a 'category' or 'categories' parameter we need to pass the categories along as a single
                        # list parameter 
                        categories = []
                        if "category" in credential:
                            category = credential["category"]
                            del credential["category"]

                            if isinstance(category, list):
                                categories = category
                            else:
                                categories = [ category]

                            credential["categories"] = categories
                        
                        elif "categories" in credential:
                            categories = credential["categories"]

                            if isinstance(categories, str):
                                categories = [ categories ]


                        # If the credential has more than one category, we create a simple `BasicCredential` which has a common set of
                        # attributes.  The only credential we support with common attributes is a simple 'username' and 'password' credetial 
                        if len(categories) > 1:

                            for category in categories:
                                if category not in ['basic', 'ssh', 'rest-basic']:
                                    errmsg = "The only categories of credentials that can be used together are ['basic', 'ssh (with password)', 'rest-basic']"
                                    raise ConfigurationError(errmsg)

                            if "username" in credential and "password" in credential:

                                username = credential["username"]
                                password = credential["password"]

                                credobj = BasicCredential(identifier=ident, categories=categories, username=username, password=password)
                                
                                self._credentials[ident] = credobj
                            
                            else:
                                errmsg = "Multi category credentials must have common attributes. Currently, the only common credential supporte is a 'username' and 'password' credential."
                                raise ConfigurationError(errmsg)

                        else:
                            category = categories[0]

                            if category == "api-token":
                                credobj = ApiTokenCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "aws-access-key":
                                credobj = AwsAccessKeyCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == 'azure-client-secret':
                                credobj = AzureClientSecretCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "basic" or category == "rest-basic":
                                credobj = BasicCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "github-app":
                                credobj = GithubAppCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "personal-api-token":
                                credobj = PersonalApiTokenCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "public-key":
                                credobj = PublicKeyCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "secret-token":
                                credobj = SecretTokenCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "ssh":
                                credobj = SshCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "wifi-choice":
                                credobj = WifiChoiceCredential(**credential)
                                self._credentials[ident] = credobj
                                
                            else:
                                warnmsg = f"Unknown category '{category}' found in credential '{ident}'"
                                logger.warning(warnmsg)

                else:
                    errmsg_lines = [
                        f"Errors found in credentials.",
                        "ERRORS:"
                    ]
                    for err in errors:
                        errmsg_lines.append(f"    {err}")

                    errmsg_lines.append("WARNINGS:")
                    for warn in warnings:
                        errmsg_lines.append(f"    {warn}")

                    errmsg_lines.append("SOURCE_URIS:")
                    for suri in self._source_uris:
                        errmsg_lines.append(f"    {suri}")

                    errmsg = os.linesep.join(errmsg_lines)
                    raise ConfigurationError(errmsg)

            except KeyError:
                errmsg = f"No 'credentials' field found."
                raise ConfigurationError(errmsg)

        return

    def _validate_credentials(self, cred_list: List[Dict[str, str]]):
        """
            Validates a list of credential dictionaries for correctness.

            :param cred_list: List of credential dictionaries.

            :returns: A tuple containing a list of error strings and warning strings.
        """

        errors = []
        warnings = []

        identifier_set = set()

        for cinfo in cred_list:
            if "identifier" in cinfo:
                identifier = cinfo["identifier"]
                if identifier in identifier_set:
                    errmsg = f"Duplicate identifer found. identifier={identifier}"
                    errors.append(errmsg)
                else:
                    identifier_set.add(identifier)
            else:
                errmsg = f"All credentials must have an identifier field. cinfo={cinfo}"
                errors.append(errmsg)

            if "category" in cinfo or "categories" in cinfo:

                if 'category' in cinfo and 'categories' in cinfo:
                    errmsg = "A credetial should not have both a 'category' and 'categories' field.  The newest method is to just use a 'catagories' field."
                    raise ConfigurationError(errmsg)

                categories = None

                if "category" in cinfo:
                    category = cinfo["category"]

                    if isinstance(category, list):
                        categories = category
                    else:
                        categories = [category]

                elif "categories" in cinfo:
                    categories = cinfo["categories"]
                    if isinstance(categories, str):
                        categories = [categories]

                if len(categories) > 1:
                    for category in categories:
                        if category not in ['basic', 'ssh', 'rest-basic']:
                            errmsg = "The only categories of credentials that can be used together are ['basic', 'ssh (with password)', 'rest-basic']"
                            raise ConfigurationError(errmsg)
                    
                    if "username" not in cinfo or "password" not in cinfo:
                        errmsg = "Multi category credentials must have common attributes. Currently, the only common credential supporte is a 'username' and 'password' credential."
                        raise ConfigurationError(errmsg)

                else:
                    category = categories[0]

                    if category == "basic" or category == "rest-basic":
                        child_errors, child_warnings = BasicCredential.validate(cinfo)
                    elif category == "ssh":
                        child_errors, child_warnings = SshCredential.validate(cinfo)
                    elif category == "api-token":
                        child_errors, child_warnings = ApiTokenCredential.validate(cinfo)
                    elif category == "aws-access-key":
                        child_errors, child_warnings = AwsAccessKeyCredential.validate(cinfo)
                    elif category == "azure-client-secret":
                        child_errors, child_warnings = AzureClientSecretCredential.validate(cinfo)
                    elif category == "github-app":
                        child_errors, child_warnings = GithubAppCredential.validate(cinfo)
                    elif category == "personal-api-token":
                        child_errors, child_warnings = PersonalApiTokenCredential.validate(cinfo)
                    elif category == "public-key":
                        child_errors, child_warnings = PublicKeyCredential.validate(cinfo)
                    elif category == "secret-token":
                        child_errors, child_warnings = SecretTokenCredential.validate(cinfo)
                    elif category == "wifi-choice":
                        child_errors, child_warnings = WifiChoiceCredential.validate(cinfo)
                    else:
                        child_errors = []
                        child_warnings = [f"Unknown credential category={category}. info={cinfo}"]

                    errors.extend(child_errors)
                    warnings.extend(child_warnings)

            else:
                errmsg = "Credential info has no category. info=%r" % cinfo
                errors.append(errmsg)

        return errors, warnings

