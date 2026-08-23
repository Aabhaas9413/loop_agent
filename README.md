# Dummy Loop Agent

This is a small project for experimenting with a dummy loop agent. The agent logic will be added as the project grows.

## What is UV?

[UV](https://docs.astral.sh/uv/) is a fast Python package and project manager. It can create a virtual environment, install dependencies, manage Python versions, run commands inside the project environment, and generate a lockfile.

Using UV keeps the project setup reproducible without manually creating or activating a virtual environment.

## Getting started with UV

Install UV on Windows with PowerShell:

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Check the installation:

```powershell
uv --version
```

Initialize this project as a Python project:

```powershell
uv init
```

Create a virtual environment and install the project dependencies:

```powershell
uv sync
```

Add a dependency:

```powershell
uv add <package-name>
```

For example:

```powershell
uv add python-dotenv
```

Add a development dependency:

```powershell
uv add --dev pytest
```

Run the dummy agent without manually activating the virtual environment:

```powershell
uv run python main.py
```

Run tests:

```powershell
uv run pytest
```

Update dependencies and the lockfile:

```powershell
uv lock --upgrade
uv sync
```

## Useful UV commands

```powershell
# List installed project packages
uv tree

# Run any command in the project environment
uv run <command>

# Remove a dependency
uv remove <package-name>

# Install the Python version declared by the project
uv python install
```

UV stores the project configuration in `pyproject.toml` and records exact dependency versions in `uv.lock`. Commit both files so another developer can recreate the same environment with:

```powershell
uv sync
```

## Anaconda and UV equivalents

Anaconda uses named environments and commonly stores dependencies in `environment.yml`. UV uses a project virtual environment in `.venv`, stores direct dependencies in `pyproject.toml`, and locks exact versions in `uv.lock`.

| Task | Anaconda | UV |
| --- | --- | --- |
| Create an environment | `conda create -n loop-agent python=3.12` | `uv venv --python 3.12` |
| Activate the environment | `conda activate loop-agent` | Not required; use `uv run ...` |
| Install a package | `conda install requests` | `uv add requests` |
| Install from PyPI | `pip install requests` | `uv add requests` |
| Install development tools | `conda install pytest` | `uv add --dev pytest` |
| List packages | `conda list` | `uv tree` |
| Remove a package | `conda remove requests` | `uv remove requests` |
| Update packages | `conda update --all` | `uv lock --upgrade` then `uv sync` |
| Run Python | `python` after activation | `uv run python` |
| Leave the environment | `conda deactivate` | No action required |

### Maintaining dependencies with UV

For this project, the recommended workflow is:

```powershell
# Add or remove dependencies. These update pyproject.toml and uv.lock.
uv add requests
uv add --dev pytest
uv remove requests

# Recreate or synchronize the environment from the lockfile.
uv sync

# Upgrade packages within the declared version ranges.
uv lock --upgrade
uv sync
```

The UV equivalents of Anaconda's `environment.yml` are `pyproject.toml` and `uv.lock`. Commit both files to source control. A new developer can set up the project with:

```powershell
uv sync
uv run python main.py
```

### Using requirements.txt with UV

If a deployment platform or existing tool requires `requirements.txt`, export it from the UV lockfile rather than maintaining a second list by hand:

```powershell
uv export --format requirements.txt --output-file requirements.txt
```

To start a UV project from an existing requirements file:

```powershell
uv init
uv add -r requirements.txt
uv sync
```

After changing dependencies with `uv add` or `uv remove`, export the compatibility file again. The source of truth should remain `pyproject.toml` and `uv.lock`.

### Maintaining dependencies with Anaconda

The equivalent Anaconda workflow uses an `environment.yml` file:

```powershell
# Create and activate the environment from the file.
conda env create -f environment.yml
conda activate loop-agent

# Add a package and save the environment definition.
conda install requests
conda env export --no-builds > environment.yml

# Recreate or update the environment later.
conda env update -f environment.yml --prune
```

Do not use `conda` and UV to manage the same environment. Choose one tool for the project environment; for this repository, use UV.

> Replace `main.py` with the actual entry-point file when the loop agent is implemented.
