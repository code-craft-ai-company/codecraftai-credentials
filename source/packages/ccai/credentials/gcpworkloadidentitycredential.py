"""
    .. module:: gcpworkloadidentitycredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`GcpWorkloadIdentityCredential` which
                   wraps a GCP Workload Identity Federation assertion.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os

from ccai.errors.exceptions import ConfigurationError

from ccai.credentials.basecredential import BaseCredential


class GcpWorkloadIdentityCredential(BaseCredential):
    """
        The :class:`GcpWorkloadIdentityCredential` is a container object that wraps a
        Google Cloud Platform Workload Identity Federation assertion.

        .. code:: yaml
            "identifier": "gcp-wif"
            "category": "cloud-venue"
            "provider": "gcp-workload-identity"
            "audience": "//iam.googleapis.com/projects/123/locations/global/workloadIdentityPools/pool/providers/provider"
            "subject_token_type": "urn:ietf:params:oauth:token-type:jwt"
            "service_account_email": "svc@my-project.iam.gserviceaccount.com"
            "token_url": "https://sts.googleapis.com/v1/token"

    """

    DEFAULT_TOKEN_URL = "https://sts.googleapis.com/v1/token"

    def __init__(self, *, identifier: str, categories: List[str], audience: str, subject_token_type: str,
                 service_account_email: str, token_url: Optional[str] = None,
                 role: Optional[str] = "priv") -> None:
        """
            Initializes a :class:`GcpWorkloadIdentityCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param audience: The workload identity pool provider audience string.
            :param subject_token_type: The subject token type for the federated assertion.
            :param service_account_email: The target service account email to impersonate.
            :param token_url: The security token service endpoint; defaults to :data:`DEFAULT_TOKEN_URL`.
            :param role: Identifies the role of the credential.

            :raises: ConfigurationError
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "cloud-venue" not in categories:
            errmsg_lines = [
                "The GcpWorkloadIdentityCredential should be given credentials of category 'cloud-venue'.",
                "MISSING CATEGORY: cloud-venue",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        if audience is None or len(audience) == 0:
            raise ConfigurationError("The GcpWorkloadIdentityCredential constructor requires a non-empty 'audience' parameter be provided.")
        if subject_token_type is None or len(subject_token_type) == 0:
            raise ConfigurationError("The GcpWorkloadIdentityCredential constructor requires a non-empty 'subject_token_type' parameter be provided.")
        if service_account_email is None or len(service_account_email) == 0:
            raise ConfigurationError("The GcpWorkloadIdentityCredential constructor requires a non-empty 'service_account_email' parameter be provided.")

        effective_token_url = token_url
        if effective_token_url is None or len(effective_token_url) == 0:
            effective_token_url = self.DEFAULT_TOKEN_URL

        self._audience = audience
        self._subject_token_type = subject_token_type
        self._service_account_email = service_account_email
        self._token_url = effective_token_url
        return

    @property
    def audience(self) -> str:
        """
            Returns the workload identity pool provider audience.

            :returns: The audience string.
        """
        return self._audience

    @property
    def subject_token_type(self) -> str:
        """
            Returns the subject token type for the federated assertion.

            :returns: The subject token type string.
        """
        return self._subject_token_type

    @property
    def service_account_email(self) -> str:
        """
            Returns the target service account email.

            :returns: The service account email string.
        """
        return self._service_account_email

    @property
    def token_url(self) -> str:
        """
            Returns the security token service endpoint URL.

            :returns: The token URL string.
        """
        return self._token_url

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a GCP workload identity credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "audience" not in cred_info:
            errors.append("missing 'audience' in gcp-workload-identity credential.")

        if "subject_token_type" not in cred_info:
            errors.append("missing 'subject_token_type' in gcp-workload-identity credential.")

        if "service_account_email" not in cred_info:
            errors.append("missing 'service_account_email' in gcp-workload-identity credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["audience"] = self._audience
        rtnval["subject_token_type"] = self._subject_token_type
        rtnval["service_account_email"] = self._service_account_email
        rtnval["token_url"] = self._token_url

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential.

            :returns: A string representation safe for logs.
        """
        rtnval = (
            "GcpWorkloadIdentityCredential("
            "identifier={!r}, categories={!r}, audience={!r}, subject_token_type={!r}, "
            "service_account_email={!r}, token_url={!r})"
        ).format(
            self._identifier, self._categories, self._audience, self._subject_token_type,
            self._service_account_email, self._token_url,
        )

        return rtnval
