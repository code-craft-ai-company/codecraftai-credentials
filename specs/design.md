# AutoMojo Credentials Package - Design Document

## Overview

The `automojo-credentials` package provides a comprehensive credential management system for the Automation Mojo testing framework. It implements a flexible, extensible architecture for handling various types of authentication credentials used in automated testing scenarios.

## Architecture

### Core Design Principles

1. **Extensibility**: The system uses inheritance and polymorphism to support multiple credential types
2. **Type Safety**: Leverages Python type hints throughout for better code reliability
3. **Validation**: Each credential type implements validation logic to ensure configuration correctness
4. **Debuggability**: Prioritizes clear error messages and debugging capabilities over performance
5. **Configuration-Driven**: Credentials are loaded from configuration files (YAML/JSON) rather than hardcoded

### Package Structure

```
automojo/credentials/
├── __init__.py                     # Package initialization
├── basecredential.py              # Abstract base class for all credentials
├── credentialmanager.py           # Central manager for credential loading and lookup
├── wellknown.py                   # Singleton pattern implementation
└── [credential_types]/            # Individual credential implementations
    ├── apitokencredential.py
    ├── awsaccesskeycredential.py
    ├── azureclientsecretcredential.py
    ├── basiccredential.py
    ├── githubappcredential.py
    ├── githubtokencredential.py
    ├── personalapitokencredential.py
    ├── publickeycredential.py
    ├── secrettokencredential.py
    ├── sshcredential.py
    └── wifichoicecredential.py
```

## Core Components

### BaseCredential Class

The foundation of the credential system, providing:

- **Common Properties**: `identifier`, `categories`, `role`
- **Validation Framework**: Abstract validation methods
- **Serialization**: `as_dict()` method for configuration export
- **Type Safety**: Enforces required parameters through constructor validation

**Key Design Decisions:**
- Uses composition over inheritance for credential categories
- Supports multiple categories per credential (e.g., basic + ssh + rest-basic)
- Immutable after construction to prevent accidental modification

### CredentialManager Class

Central orchestrator responsible for:

- **Loading**: Parses credential configurations from dictionaries
- **Validation**: Coordinates validation across all credential types
- **Lookup**: Provides fast credential retrieval by identifier
- **Error Handling**: Comprehensive error reporting with source URI tracking

**Key Features:**
- Factory pattern for credential instantiation
- Batch validation with detailed error reporting
- Support for multiple configuration sources
- Thread-safe singleton access pattern

### Credential Type Hierarchy

Each credential type implements:

1. **Constructor Validation**: Ensures required fields are present
2. **Category Enforcement**: Validates credential is used for appropriate authentication types
3. **Static Validation**: Class-level validation for configuration dictionaries
4. **Serialization**: Consistent dictionary representation

## Supported Credential Types

### Authentication Categories

| Category | Description | Use Cases |
|----------|-------------|-----------|
| `basic` | Username/password authentication | HTTP Basic Auth, general login |
| `ssh` | SSH key-based or password authentication | Remote server access, Git operations |
| `rest-basic` | REST API basic authentication | API testing, service integration |
| `api-token` | Simple API token authentication | Service APIs, webhooks |
| `aws-access-key` | AWS access key/secret pairs | AWS service testing |
| `azure-client-secret` | Azure service principal credentials | Azure service testing |
| `github-app` | GitHub application private keys | GitHub API automation |
| `github-token` | GitHub personal access tokens | Git operations, GitHub API |
| `personal-api-token` | Personal API tokens | User-specific API access |
| `public-key` | Public key authentication | Certificate-based auth |
| `secret-token` | Generic secret tokens | Custom authentication schemes |
| `wifi-choice` | WiFi network credentials | Network testing scenarios |

### Multi-Category Support

The system supports credentials that can be used across multiple authentication categories:

```yaml
identifier: "multi-use-cred"
categories: ["basic", "ssh", "rest-basic"]
username: "testuser"
password: "testpass"
```

**Constraints:**
- Only `basic`, `ssh`, and `rest-basic` categories can be combined
- Multi-category credentials must have common attributes (`username` + `password`)

## Configuration Format

### YAML Configuration Example

```yaml
credentials:
  - identifier: "ssh-key-auth"
    category: "ssh"
    username: "ubuntu"
    keyfile: "~/.ssh/id_rsa"
    keypasswd: "optional-key-password"
    allow_agent: false
    primitive: false

  - identifier: "api-access"
    category: "api-token"
    token: "abc123def456"

  - identifier: "aws-testing"
    category: "aws-access-key"
    keyid: "AKIAIOSFODNN7EXAMPLE"
    secret: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

  - identifier: "multi-auth"
    categories: ["basic", "ssh", "rest-basic"]
    username: "testuser"
    password: "testpass"
```

## Error Handling Strategy

### Validation Levels

1. **Constructor Validation**: Immediate validation during object creation
2. **Configuration Validation**: Batch validation during credential loading
3. **Runtime Validation**: Credential lookup and usage validation

### Error Types

- **ConfigurationError**: Invalid credential configuration
- **Missing Credential**: Requested credential not found
- **Category Mismatch**: Credential used for wrong authentication type
- **File Not Found**: SSH key files or certificates missing

### Error Reporting

```python
# Example error output
ConfigurationError: Errors found in credentials.
ERRORS:
    Duplicate identifier found. identifier=ssh-cred
    Missing 'keyfile' in ssh credential when allow_agent is False
WARNINGS:
    Unknown credential category=custom-auth
SOURCE_URIS:
    /path/to/landscape.yaml
    /path/to/credentials.yaml
```

## Singleton Pattern Implementation

### CredentialManagerSingleton

- **Thread-Safe**: Uses RLock for concurrent access protection
- **Lazy Loading**: Credentials loaded on first access
- **Configuration Integration**: Integrates with AutoMojo configuration system
- **Context Awareness**: Supports multiple configuration sources

## Integration Points

### Dependencies

- `automojo-xmodules`: Core utilities and collections
- `automojo-configuration`: Configuration management system
- `automojo-testbase`: Testing framework integration

### Usage Patterns

```python
# Singleton access
from automojo.credentials.wellknown import CredentialManagerSingleton

credmgr = CredentialManagerSingleton()
ssh_cred = credmgr.lookup_credential("ssh-server-access")

# Direct manager usage
from automojo.credentials.credentialmanager import CredentialManager

credmgr = CredentialManager()
credmgr.load_credentials(config_dict, source_uris=["config.yaml"])
api_cred = credmgr.lookup_credential("api-token")
```

## Security Considerations

### Credential Storage

- **No Plaintext Storage**: Credentials stored in memory only during execution
- **Configuration Files**: Credentials loaded from external configuration files
- **Environment Variables**: Support for environment variable expansion in file paths

### Access Control

- **Role-Based**: Optional role assignment for credential categorization
- **Identifier-Based**: Unique identifiers prevent credential conflicts
- **Category Validation**: Prevents credential misuse across authentication types

## Testing Strategy

### Test Organization

Following the testbase framework structure:
```
source/testroots/automojo/tests/singlehost/credentials/
├── test_credentialmanager.py
├── test_basiccredential.py
├── test_sshcredential.py
└── [other credential type tests]
```

### Test Execution

```bash
source .venv/bin/activate
testbase testing run --root source/testroots/automojo --includes=automojo.tests.singlehost --output=test_output
```

## Future Extensibility

### Adding New Credential Types

1. **Inherit from BaseCredential**: Implement required methods
2. **Define Category**: Add new authentication category
3. **Implement Validation**: Static and instance validation methods
4. **Register in Manager**: Add factory logic to CredentialManager
5. **Add Tests**: Follow established testing patterns

### Configuration Evolution

- **Backward Compatibility**: Maintain support for existing configuration formats
- **Schema Versioning**: Support for configuration schema evolution
- **Migration Tools**: Utilities for upgrading credential configurations

## Performance Characteristics

### Design Trade-offs

- **Debuggability over Performance**: Comprehensive error messages and validation
- **Readability over Conciseness**: Clear, maintainable code structure
- **Safety over Speed**: Extensive validation and type checking

### Memory Usage

- **Lazy Loading**: Credentials loaded only when needed
- **Singleton Pattern**: Single instance reduces memory footprint
- **Immutable Objects**: Prevents accidental modification and enables safe sharing

## Documentation Standards

### Sphinx Documentation

- **Module-level**: Comprehensive module documentation
- **Class-level**: Detailed class descriptions with usage examples
- **Method-level**: Parameter and return value documentation
- **Type Hints**: Complete type annotations for all public APIs

### Code Examples

Each credential type includes YAML configuration examples in docstrings, providing clear usage guidance for test automation engineers.