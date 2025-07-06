# Git rb

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI Latest Release](https://img.shields.io/pypi/v/mypy-clean-slate.svg)](https://pypi.org/project/mypy-clean-slate/)
[![License](https://img.shields.io/pypi/l/mypy-clean-slate.svg)](https://github.com/geo7/mypy_clean_slate/blob/main/LICENSE)
[![image](https://img.shields.io/pypi/pyversions/mypy-clean-slate.svg)](https://pypi.python.org/pypi/mypy-clean-slate)
[![Actions status](https://github.com/geo7/mypy_clean_slate/workflows/CI/badge.svg)](https://github.com/geo7/mypy_clean_slate/actions)

`git-rb` is a command-line tool to simplify interactive rebase workflow in Git,
often I'd find my self copying hashes from `git log` output in order to paste
into `git rebase -i`. This tools only purpose is to simplify that.

## Installation

Install using  `uvx`:

```bash
uvx git-rb
```

Code is self contained within `main.py`, so you might like to simply copy the whole thing.

## Usage

Typically I'll have the following in `.gitconfig`:

```
[alias]
  rb = !uvx git-rb
```

To provide the alias `git rb`.

TODO: I should add an example output here.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
