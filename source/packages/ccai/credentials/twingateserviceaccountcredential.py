"""
    .. module:: twingateserviceaccountcredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`TwingateServiceAccountCredential` which
                   represents a Twingate service-account API token and network slug pair.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

from ccai.errors.exceptions import ConfigurationError

from ccai.credentials.basecredential import BaseCredential


class TwingateServiceAccountCredential(BaseCredential):
    """
        The :class:`TwingateServiceAccountCredential` is a container object for a
        Twingate service-account API token plus the network slug used to address the
        Twingate GraphQL control plane.

        .. code:: yaml
            "identifier": "tg-prod"
            "category": "twingate-service-account"
            "api_token": "tg-svc-XXXX"
            "network_slug": "acme"

    """

    def __init__(self, *, identifier: str, categories: List[str], api_token: str,
                 network_slug: str, role: Optional[str] = "priv"):
        """
            Initializes a :class:`TwingateServiceAccountCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param api_token: The Twingate service-account API token value.
            :param network_slug: The Twingate network slug (hostname-shaped, no whitespace).
            :param role: Identifies the role of the credential.
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "twingate-service-account" not in categories:
            raise ConfigurationError("The TwingateServiceAccountCredential should only be given credentials of category 'twingate-service-account'.")
        if api_token is None or len(api_token) == 0:
            raise ConfigurationError("The TwingateServiceAccountCredential constructor requires a non-empty 'api_token' parameter be provided.")
        if network_slug is None or len(network_slug) == 0:
            raise ConfigurationError("The TwingateServiceAccountCredential constructor requires a non-empty 'network_slug' parameter be provided.")

        has_whitespace = False
        for ch in network_slug:
            if ch.isspace():
                has_whitespace = True
                break

        if has_whitespace:
            raise ConfigurationError("The TwingateServiceAccountCredential 'network_slug' must contain no whitespace.")

        self._api_token = api_token
        self._network_slug = network_slug
        return

    @property
    def api_token(self) -> str:
        """
            Returns the Twingate API token string.

            :returns: The API token value.
        """
        return self._api_token

    @property
    def network_slug(self) -> str:
        """
            Returns the Twingate network slug.

            :returns: The network slug string.
        """
        return self._network_slug

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing a Twingate service-account credential.

            :param cred_info: The credential information dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "api_token" not in cred_info:
            errors.append("missing 'api_token' in twingate-service-account credential.")
        else:
            api_token = cred_info["api_token"]
            if api_token is None or len(api_token) == 0:
                errors.append("empty 'api_token' in twingate-service-account credential.")

        if "network_slug" not in cred_info:
            errors.append("missing 'network_slug' in twingate-service-account credential.")
        else:
            network_slug = cred_info["network_slug"]
            if network_slug is None or len(network_slug) == 0:
                errors.append("empty 'network_slug' in twingate-service-account credential.")
            else:
                has_whitespace = False
                for ch in network_slug:
                    if ch.isspace():
                        has_whitespace = True
                        break
                if has_whitespace:
                    errors.append("'network_slug' in twingate-service-account credential must contain no whitespace.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["api_token"] = self._api_token
        rtnval["network_slug"] = self._network_slug

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential with the API token redacted.

            :returns: A redacted string representation safe for logs.
        """
        rtnval = (
            "TwingateServiceAccountCredential("
            "identifier={!r}, categories={!r}, api_token='***', network_slug={!r})"
        ).format(self._identifier, self._categories, self._network_slug)

        return rtnval
