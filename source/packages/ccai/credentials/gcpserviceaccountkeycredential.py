"""
    .. module:: gcpserviceaccountkeycredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`GcpServiceAccountKeyCredential` which
                   wraps the contents of a GCP service-account JSON key.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os

from ccai.errors.exceptions import ConfigurationError

from ccai.credentials.basecredential import BaseCredential


class GcpServiceAccountKeyCredential(BaseCredential):
    """
        The :class:`GcpServiceAccountKeyCredential` is a container object that wraps the
        contents of a Google Cloud Platform service-account JSON key.

        .. code:: yaml
            "identifier": "gcp-sa"
            "category": "cloud-venue"
            "provider": "gcp-service-account"
            "project_id": "my-project"
            "client_email": "svc@my-project.iam.gserviceaccount.com"
            "private_key_id": "abcdef0123456789"
            "private_key": "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
            "token_uri": "https://oauth2.googleapis.com/token"

    """

    DEFAULT_TOKEN_URI = "https://oauth2.googleapis.com/token"

    def __init__(self, *, identifier: str, categories: List[str], project_id: str, client_email: str,
                 private_key_id: str, private_key: str, token_uri: Optional[str] = None,
                 role: Optional[str] = "priv") -> None:
        """
            Initializes a :class:`GcpServiceAccountKeyCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param project_id: The GCP project id the service account belongs to.
            :param client_email: The service account client email address.
            :param private_key_id: The identifier of the service account private key.
            :param private_key: The PEM body of the service account private key.
            :param token_uri: The OAuth2 token endpoint; defaults to :data:`DEFAULT_TOKEN_URI`.
            :param role: Identifies the role of the credential.

            :raises: ConfigurationError
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "cloud-venue" not in categories:
            errmsg_lines = [
                "The GcpServiceAccountKeyCredential should be given credentials of category 'cloud-venue'.",
                "MISSING CATEGORY: cloud-venue",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        if project_id is None or len(project_id) == 0:
            raise ConfigurationError("The GcpServiceAccountKeyCredential constructor requires a non-empty 'project_id' parameter be provided.")
        if client_email is None or len(client_email) == 0:
            raise ConfigurationError("The GcpServiceAccountKeyCredential constructor requires a non-empty 'client_email' parameter be provided.")
        if private_key_id is None or len(private_key_id) == 0:
            raise ConfigurationError("The GcpServiceAccountKeyCredential constructor requires a non-empty 'private_key_id' parameter be provided.")
        if private_key is None or len(private_key) == 0:
            raise ConfigurationError("The GcpServiceAccountKeyCredential constructor requires a non-empty 'private_key' parameter be provided.")

        effective_token_uri = token_uri
        if effective_token_uri is None or len(effective_token_uri) == 0:
            effective_token_uri = self.DEFAULT_TOKEN_URI

        self._project_id = project_id
        self._client_email = client_email
        self._private_key_id = private_key_id
        self._private_key = private_key
        self._token_uri = effective_token_uri
        return

    @property
    def project_id(self) -> str:
        """
            Returns the GCP project id.

            :returns: The project id string.
        """
        return self._project_id

    @property
    def client_email(self) -> str:
        """
            Returns the service account client email address.

            :returns: The client email string.
        """
        return self._client_email

    @property
    def private_key_id(self) -> str:
        """
            Returns the identifier of the service account private key.

            :returns: The private key id string.
        """
        return self._private_key_id

    @property
    def private_key(self) -> str:
        """
            Returns the PEM body of the service account private key.

            :returns: The private key string.
        """
        return self._private_key

    @property
    def token_uri(self) -> str:
        """
            Returns the OAuth2 token endpoint URI.

            :returns: The token URI string.
        """
        return self._token_uri

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a GCP service account key credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "project_id" not in cred_info:
            errors.append("missing 'project_id' in gcp-service-account-key credential.")

        if "client_email" not in cred_info:
            errors.append("missing 'client_email' in gcp-service-account-key credential.")

        if "private_key_id" not in cred_info:
            errors.append("missing 'private_key_id' in gcp-service-account-key credential.")

        if "private_key" not in cred_info:
            errors.append("missing 'private_key' in gcp-service-account-key credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["project_id"] = self._project_id
        rtnval["client_email"] = self._client_email
        rtnval["private_key_id"] = self._private_key_id
        rtnval["private_key"] = self._private_key
        rtnval["token_uri"] = self._token_uri

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential with private key material redacted.

            :returns: A redacted string representation safe for logs.
        """
        rtnval = (
            "GcpServiceAccountKeyCredential("
            "identifier={!r}, categories={!r}, project_id={!r}, client_email={!r}, "
            "private_key_id='***', private_key='***', token_uri={!r})"
        ).format(self._identifier, self._categories, self._project_id, self._client_email, self._token_uri)

        return rtnval
