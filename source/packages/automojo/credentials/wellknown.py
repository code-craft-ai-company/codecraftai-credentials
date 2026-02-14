
"""
    .. module:: wellknown
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that provides a singleton for the :class:`CredentialManager`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import List, Optional

from threading import RLock

from automojo.errors.exceptions import SemanticError

from automojo.credentials.credentialmanager import CredentialManager

CREDENTIAL_MANAGER_SINGLETON = None
CREDENTIAL_CONFIGURATION_MAP = None

SINGLETON_LOCK = RLock()


def CredentialManagerSingleton(credential_info: Optional[dict] = None, credential_uris: Optional[List[str]] = None) -> CredentialManager:
    """
        Instantiates and gets a global instance of the :class:`CredentialManager` class.  The
        :class:`CredentialManager` provides for management of credentials.
    """
    global CREDENTIAL_MANAGER_SINGLETON

    if CREDENTIAL_MANAGER_SINGLETON is None:

        if credential_info is None or credential_uris is None:
             errmsg = "The first call to create the CredentialManagerSingleton must include the credential_info and credential_uris parameters."
             raise SemanticError(errmsg)

        SINGLETON_LOCK.acquire()
        try:

                credmgr = CredentialManager()
                credmgr.load_credentials(credential_info, source_uris=credential_uris)
                CREDENTIAL_MANAGER_SINGLETON = credmgr
                
        finally:
            SINGLETON_LOCK.release()
    
    return CREDENTIAL_MANAGER_SINGLETON
