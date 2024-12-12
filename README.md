# ghexplain

A Python library that provides AI-powered explanations for GitHub issues using LangChain.

## Installation

from repository
```bash
git clone git@github.com:Stell0/ghexplain.git
cd ghexplain
pip install -e .
```

from PyPI (not yet released)

```bash
pip install ghexplain
```

## Usage

### Python API

```python
import ghexplain

# Get a summary of a GitHub issue
summary = ghexplain.issue("https://github.com/owner/repo/issues/123")

# Get a summary in a specific language
summary_es = ghexplain.issue("https://github.com/owner/repo/issues/123", language="spanish")
```

### Command Line Interface

The package provides a CLI tool that can be used directly from your terminal:

```bash
# Export github token as environment
export GITHUB_TOKEN=$(gh auth token)

# Basic usage
ghexplain https://github.com/owner/repo/issues/123

# Get summary in a different language
ghexplain https://github.com/owner/repo/issues/123 -l spanish

# Show help
ghexplain --help
```

You can also use it with python -m:
```bash
python -m ghexplain.cli https://github.com/owner/repo/issues/123
```
