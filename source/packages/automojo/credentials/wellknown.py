
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from threading import RLock

from automojo.foundation.collections.wellknown import ContextSingleton
from automojo.foundation.collections.contextpaths import ContextPaths
from automojo.foundation.configuration.configurationmaps import CONFIGURATION_MAPS

from automojo.credentials.credentialmanager import CredentialManager

CREDENTIAL_MANAGER_SINGLETON = None

SINGLETON_LOCK = RLock()


def CredentialManagerSingleton() -> CredentialManager:
    """
        Instantiates and gets a global instance of the :class:`CredentialManager` class.  The
        :class:`CredentialManager` provides for management of credentials.
    """
    global CREDENTIAL_MANAGER_SINGLETON

    if CREDENTIAL_MANAGER_SINGLETON is None:
        SINGLETON_LOCK.acquire()
        try:

            if CREDENTIAL_MANAGER_SINGLETON is None:
                credential_info = {}
                if CONFIGURATION_MAPS.CREDENTIAL_CONFIGURATION_MAP is not None and \
                    len(CONFIGURATION_MAPS.CREDENTIAL_CONFIGURATION_MAP) > 0:
                    credential_info = CONFIGURATION_MAPS.CREDENTIAL_CONFIGURATION_MAP

                ctx = ContextSingleton()
                credential_uris = ctx.lookup(ContextPaths.CONFIG_CREDENTIAL_URIS, [])

                credmgr = CredentialManager()
                credmgr.load_credentials(credential_info, source_uris=credential_uris)
                CREDENTIAL_MANAGER_SINGLETON = credmgr
                
        finally:
            SINGLETON_LOCK.release()
    
    return CREDENTIAL_MANAGER_SINGLETON
