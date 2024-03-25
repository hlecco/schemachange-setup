# Snowflake setup

This repository is a mock for a Snowflake setup using CI/CD routines and schemachange.


## Developing

### Setting up the environment

 - Create a virtual environment (recommended) and install the requirements from `requirements-dev.txt`;
 - Run `pre-commit install`

### Creating new scripts

Always branch out from the `main` branch.
Scripts must be created inside the `scripts/` directory.
Never edit the `deploy` directory.
