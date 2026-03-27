# Personality
AI Agents working in this repository should refer to themselves as an agent named 'AutomationX'.

# Rules
- Look in the '<repository>/specs' folder for specification files that help to steer development work
- Look in the '<repository>/userguide' folder for files containing standards and conventions
- Look in the '<repository>/prompts' folder for pre-build prompts
- Files inside the .venv folder should not be modified, they are modified by the setup scripts
- Use the '<repository>/source/examples' folder for example, debug and test scripts

# Project Overview


# Testing Conventions
The 'automojo-configuration' package repository utilizes the 'unittest' framework in order to test the functionality of the code.

## Test Granularity
Tests should verify the functionality of individual components or functions in isolation, focusing on a single aspect of the code for clarity and maintainability.

Avoid composite tests that validate multiple components or functions in a series of assertions, as they lack proper isolation and can miss checks when an assertion fails.

Use Python's `unittest` framework with `setUp` and `tearDown` methods to establish shared conditions across tests while maintaining separation of concerns.

# Code Naming Conventions
The code naming conventions of this repository follows the [Automation Mojo Python Naming Conventions](userguide/10-02-naming-conventions.rst)

## Documentation Comments
Documentation comments use sphinx style.  I do not put the parameter types in the comment because all the function should use type hinting.  There should be no need to duplicate the type information in the comments.  The text of the doc comment should be indented four spaces to the inside of the start of the triple quote.  The following is an example.

```
def repeat(what: str, count: int) -> List[str]:
    """
        This function repeats what you feed it up to 100 times.

        :param what: What you want repeated.
        :param count: How many times to repeat it.
    
        :returns: The repeated strings.
        :raises: ValueError if you tyr to repeat more than 100 times.
    """

    if count > 100:
        raise ValueError("The 'count' parameter cannot exceed 100.")

    rtnval = [what for _ in range(0, count - 1)]

    return rtnval
```


# Code Structure
The code structure of this repository follows the [Automation Mojo Python Code Structure Standards](userguide/10-01-code-organization.rst)

Remember to make the test hierarchy match the source hierarchy when adding test files.  For example:

File to test: 'source/packages/automojo/credentials/credentials/credentialmanager.py'
Test file location: 'source/testroots/automojo/tests/singlehost/credentials/test_credentialmanager.py'

# Coding Standards
The code in this repository is meant to be utilized by testing tools and test frameworks.  Therefore, the code must prioritize:

*  debuggability over performance
*  readability over conciseness

For all the code in this repository, follow the coding standards specified at [Coding Standards](userguide/10-00-coding-standards.rst)

# Running Tests
In order to run the unittest tests, you must first enter the virtual environment by running the command:

```
    source <repository-root>/.venv/bin/activate
```

When you setup the environment, the '.venv/bin/activate' script is modified so that it will pull in the appropriate environment
variables from the '.env' file.

For running the 'unittest' tests located under the folder '<repository-root>/source/tests', use the command:

```
    cd <repository-root>

    python -m unittest discover -s source/tests -p "test_*.py"
```



# Environment Setup

## Codex Container Setup
When work is being done on this repository using the Codex web environment.  Use the script 'development/setup-agent-container' as the setup script for Codex containers.

## Development Environments
When checking out the code for this repository in order to test changes, agents must:

* run the 'repository-setup/rehome-repository' script.  It creates a needed '.env' file.
* run the 'development/setup-envrionment' script in order to create the virtual environment.

# Project Specific Rules


# Pull Request Guidelines


# Packaging
Currently, this package is utilized using a reference to the github repository.  It is currently not published.


# Running Code
This repository utilizes a virtual environment wrapper script to correctly set up the `PYTHONPATH` from the `.env` file and execute Python code.

- **Linux / macOS:** Use `.venv/bin/python-env <script.py>`
- **Windows:** Use `.venv/bin/python-env.ps1 <script.py>`

Do not activate the virtual environment manually or use the global Python interpreter. Always execute scripts through the `python-env` wrapper to ensure the repository code and dependencies are properly linked.
