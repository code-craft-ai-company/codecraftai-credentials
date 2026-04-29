<<<<<<< Updated upstream
====================
automojo-credentials
====================

Automation Mojo - Credentials Package

Overview
========
automojo-credentials is a core component of the Automation Mojo technology stack. It provides robust, reusable foundation code designed to enable and orchestrate complex software automation tasks.

Installation
============
Using Poetry:

.. code-block:: bash

    poetry add automojo-credentials

Development
===========
This repository provides a standard Poetry environment.

1. Activate virtual environment:
   Run `poetry shell` and `poetry install`
2. Test Execution:
   Run `poetry run pytest`

References
==========
- `User Guide <userguide/userguide.rst>`
- `Coding Standards <userguide/10-00-coding-standards.rst>`
=======
============================
Automation Mojo Credentials
============================

The ``automojo-credentials`` package is the credentials vocabulary for the automojo suite. It defines a small hierarchy of credential classes rooted at ``BaseCredential`` and adds concrete types for the authentication styles the rest of the suite has to talk to. A ``CredentialManager`` loads credentials from configuration and exposes them by name so that protocol and REST clients (for example ``automojo-protocol-ssh``, ``automojo-restclient-github-public``, and ``automojo-gitlab``) can request the credential they need without hard-coding authentication details.

Highlights
==========

- ``BaseCredential`` root and ``CredentialManager`` for declarative credential lookup by name.
- SSH-oriented credential types: ``BasicCredential``, ``PublicKeyCredential``, and ``SshCredential``.
- Token-oriented types: ``ApiTokenCredential``, ``SecretTokenCredential``, ``PersonalApiTokenCredential``.
- Vendor-specific credentials: ``GithubTokenCredential``, ``GithubAppCredential``, ``AwsAccessKeyCredential``, and ``AzureClientSecretCredential``.
- ``WifiChoiceCredential`` for network-selection scenarios.
- Implements the ``IBasicCredential`` interface from ``automojo-interfaces``.

Repository Structure
====================

- ``development/`` - Runtime environment scripts.
- ``repository-setup/`` - Repository homing and setup scripts.
- ``source/packages/`` - Package source code.
- ``source/tests/`` - ``unittest``-based tests.
- ``specs/`` - Requirements, design, and task documentation.
- ``userguide/`` - Standards, conventions, and documentation.

Environment Setup
=================

When working in a Codex container:

.. code-block:: bash

   ./development/setup-agent-container

For local development:

.. code-block:: bash

   ./repository-setup/rehome-repository
   ./development/setup-envrionment

Running Tests
=============

Activate the virtual environment:

.. code-block:: bash

   source .venv/bin/activate

Run ``unittest`` tests:

.. code-block:: bash

   python -m unittest discover -s source/tests -p "test_*.py"

Standards and Conventions
=========================

- Naming conventions: ``userguide/10-02-naming-conventions.rst``
- Code organization: ``userguide/10-01-code-organization.rst``
- Coding standards: ``userguide/10-00-coding-standards.rst``

Additional Resources
====================

- User guide entry point: ``userguide/userguide.rst``
- Design documentation: ``specs/design.md``
- Requirements: ``specs/requirements.md``
>>>>>>> Stashed changes
