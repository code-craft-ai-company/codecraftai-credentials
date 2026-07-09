"""
    .. module:: basecredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`BaseCredential` object which is the
                   common base class that all other credential objects inherit from.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Any, Dict, List, Optional, Tuple

from ccai.errors.exceptions import ConfigurationError


# Substrings (case-insensitive) used to identify secret-bearing fields in a
# credential's as_dict() output so they can be masked for safe display/logging.
SENSITIVE_FIELD_SUBSTRINGS = (
    "password",
    "passwd",
    "passphrase",
    "token",
    "secret",
    "private",
    "api_key",
    "apikey",
    "access_key",
    "authkey",
    "auth_key",
    "client_secret",
)

REDACTED_PLACEHOLDER = "***REDACTED***"


def is_sensitive_field(field_name: str) -> bool:
    """
        Indicates whether a credential field name denotes secret material.

        :param field_name: The credential dictionary key to test.

        :returns: ``True`` if the field should be redacted for display/logging.
    """
    lowered = field_name.lower()
    rtnval = False
    for marker in SENSITIVE_FIELD_SUBSTRINGS:
        if marker in lowered:
            rtnval = True
            break
    return rtnval


class BaseCredential:
    """
        The :class:`BaseCredential` is the base container object for credentials passed in the landscape
        configuration file.

        .. code:: yaml
            "identifier": "player-ssh"
            "category": "(category)"
    """

    # Names of this class's ``as_dict`` fields that carry secret material but are
    # NOT matched by the SENSITIVE_FIELD_SUBSTRINGS name heuristic (e.g. "keyraw",
    # "keys", "networks"). Subclasses declare their own; the values are aggregated
    # across the MRO in as_redacted_dict, so a subclass's declaration never drops a
    # base class's. Redaction is name-based only, so a declared field is masked
    # wholesale (safe for nested list/dict values whose leaves hold secrets).
    SECRET_FIELDS: Tuple[str, ...] = ()

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
            Returns a full dictionary representation of this credential object,
            suitable for round-tripping back through the constructor.

            .. warning::
                The returned dictionary includes raw secret material (passwords,
                tokens, keys, ...) for secret-bearing credential subclasses. Do
                NOT log or persist it as-is. Use :meth:`as_redacted_dict` for any
                display, logging, or diagnostic output.
        """

        rtnval = {
            "identifier": self._identifier,
            "categories": self._categories,
            "role": self._role
        }

        return rtnval

    def as_redacted_dict(self) -> Dict[str, Any]:
        """
            Returns a display/logging-safe dictionary representation of this
            credential with all secret-bearing fields masked.

            This is derived from :meth:`as_dict` (so it automatically covers every
            subclass's fields) with any sensitive field value replaced by a
            redaction placeholder. Use this anywhere credential data may be logged
            or persisted.

            :returns: A dictionary with secret fields masked.
        """
        full = self.as_dict()

        declared_secret_fields = set()
        for klass in type(self).__mro__:
            declared_secret_fields.update(getattr(klass, "SECRET_FIELDS", ()))

        rtnval = {}
        for key, value in full.items():
            if is_sensitive_field(key) or key in declared_secret_fields:
                rtnval[key] = REDACTED_PLACEHOLDER
            else:
                rtnval[key] = value

        return rtnval

    def __repr__(self) -> str:
        """
            Returns a secret-safe debug representation of this credential.

            The representation is built from :meth:`as_redacted_dict`, so secret
            fields are masked. Subclasses may override with their own redacted
            representation; this default guarantees no credential class falls back
            to a representation that could leak secret material.

            :returns: A redacted string representation safe for logs.
        """
        redacted = self.as_redacted_dict()

        field_parts = []
        for key, value in redacted.items():
            field_parts.append(f"{key}={value!r}")

        field_str = ", ".join(field_parts)
        rtnval = f"{type(self).__name__}({field_str})"
        return rtnval
