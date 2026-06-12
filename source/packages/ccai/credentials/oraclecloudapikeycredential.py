"""
    .. module:: oraclecloudapikeycredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`OracleCloudApiKeyCredential` which
                   wraps the four-field OCI API-key credential material.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

import os

from ccai.errors.exceptions import ConfigurationError

from ccai.credentials.basecredential import BaseCredential


class OracleCloudApiKeyCredential(BaseCredential):
    """
        The :class:`OracleCloudApiKeyCredential` is a container object that wraps the
        four-field Oracle Cloud Infrastructure API-key credential material plus an
        optional passphrase for encrypted keys.

        .. code:: yaml
            "identifier": "oci-key"
            "category": "cloud-venue"
            "provider": "oracle-cloud"
            "tenancy_ocid": "ocid1.tenancy.oc1..aaaa"
            "user_ocid": "ocid1.user.oc1..bbbb"
            "private_key": "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
            "fingerprint": "aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99"
            "passphrase": null

    """

    TENANCY_OCID_PREFIX = "ocid1.tenancy."
    USER_OCID_PREFIX = "ocid1.user."

    def __init__(self, *, identifier: str, categories: List[str], tenancy_ocid: str, user_ocid: str,
                 private_key: str, fingerprint: str, passphrase: Optional[str] = None,
                 role: Optional[str] = "priv") -> None:
        """
            Initializes an :class:`OracleCloudApiKeyCredential` instance.

            :param identifier: The identifier that is used to reference this credential.  (required)
            :param categories: The categories of authentication that are supported by the credential.
            :param tenancy_ocid: The OCI tenancy OCID.
            :param user_ocid: The OCI user OCID.
            :param private_key: The PEM body of the OCI API signing key.
            :param fingerprint: The fingerprint of the OCI API signing key.
            :param passphrase: The optional passphrase for an encrypted private key.
            :param role: Identifies the role of the credential.

            :raises: ConfigurationError
        """
        super().__init__(identifier=identifier, categories=categories, role=role)

        if "cloud-venue" not in categories:
            errmsg_lines = [
                "The OracleCloudApiKeyCredential should be given credentials of category 'cloud-venue'.",
                "MISSING CATEGORY: cloud-venue",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        if tenancy_ocid is None or len(tenancy_ocid) == 0:
            raise ConfigurationError("The OracleCloudApiKeyCredential constructor requires a non-empty 'tenancy_ocid' parameter be provided.")
        if user_ocid is None or len(user_ocid) == 0:
            raise ConfigurationError("The OracleCloudApiKeyCredential constructor requires a non-empty 'user_ocid' parameter be provided.")
        if private_key is None or len(private_key) == 0:
            raise ConfigurationError("The OracleCloudApiKeyCredential constructor requires a non-empty 'private_key' parameter be provided.")
        if fingerprint is None or len(fingerprint) == 0:
            raise ConfigurationError("The OracleCloudApiKeyCredential constructor requires a non-empty 'fingerprint' parameter be provided.")

        if not tenancy_ocid.startswith(self.TENANCY_OCID_PREFIX):
            errmsg_lines = [
                "The OracleCloudApiKeyCredential 'tenancy_ocid' parameter has an invalid OCID prefix.",
                "EXPECTED PREFIX: {}".format(self.TENANCY_OCID_PREFIX),
                "PROVIDED VALUE: {}".format(tenancy_ocid),
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        if not user_ocid.startswith(self.USER_OCID_PREFIX):
            errmsg_lines = [
                "The OracleCloudApiKeyCredential 'user_ocid' parameter has an invalid OCID prefix.",
                "EXPECTED PREFIX: {}".format(self.USER_OCID_PREFIX),
                "PROVIDED VALUE: {}".format(user_ocid),
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        self._tenancy_ocid = tenancy_ocid
        self._user_ocid = user_ocid
        self._private_key = private_key
        self._fingerprint = fingerprint
        self._passphrase = passphrase
        return

    @property
    def tenancy_ocid(self) -> str:
        """
            Returns the OCI tenancy OCID.

            :returns: The tenancy OCID string.
        """
        return self._tenancy_ocid

    @property
    def user_ocid(self) -> str:
        """
            Returns the OCI user OCID.

            :returns: The user OCID string.
        """
        return self._user_ocid

    @property
    def private_key(self) -> str:
        """
            Returns the PEM body of the OCI API signing key.

            :returns: The private key string.
        """
        return self._private_key

    @property
    def fingerprint(self) -> str:
        """
            Returns the fingerprint of the OCI API signing key.

            :returns: The fingerprint string.
        """
        return self._fingerprint

    @property
    def passphrase(self) -> Optional[str]:
        """
            Returns the passphrase for an encrypted private key.

            :returns: The passphrase string, or None.
        """
        return self._passphrase

    @classmethod
    def validate(cls, cred_info: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
            Validates the dictionary describing an Oracle Cloud API-key credential.

            :param cred_info: Credential definition dictionary to validate.

            :returns: A tuple of lists containing errors and warnings.
        """

        errors = []
        warnings = []

        if "tenancy_ocid" not in cred_info:
            errors.append("missing 'tenancy_ocid' in oracle-api-key credential.")

        if "user_ocid" not in cred_info:
            errors.append("missing 'user_ocid' in oracle-api-key credential.")

        if "private_key" not in cred_info:
            errors.append("missing 'private_key' in oracle-api-key credential.")

        if "fingerprint" not in cred_info:
            errors.append("missing 'fingerprint' in oracle-api-key credential.")

        return errors, warnings

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of this credential object.
        """
        rtnval = super().as_dict()

        rtnval["tenancy_ocid"] = self._tenancy_ocid
        rtnval["user_ocid"] = self._user_ocid
        rtnval["private_key"] = self._private_key
        rtnval["fingerprint"] = self._fingerprint
        rtnval["passphrase"] = self._passphrase

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a debug representation of this credential with key material redacted.

            :returns: A redacted string representation safe for logs.
        """
        passphrase_repr = "None"
        if self._passphrase is not None:
            passphrase_repr = "'***'"

        rtnval = (
            "OracleCloudApiKeyCredential("
            "identifier={!r}, categories={!r}, tenancy_ocid={!r}, user_ocid={!r}, "
            "private_key='***', fingerprint={!r}, passphrase={})"
        ).format(
            self._identifier, self._categories, self._tenancy_ocid, self._user_ocid,
            self._fingerprint, passphrase_repr,
        )

        return rtnval
