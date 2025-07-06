# Git `rb`

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI Latest Release](https://img.shields.io/pypi/v/git-rb.svg)](https://pypi.org/project/git-rb/)
[![License](https://img.shields.io/pypi/l/git-rb.svg)](https://github.com/geo7/git-rb/blob/main/LICENSE)
[![image](https://img.shields.io/pypi/pyversions/git-rb.svg)](https://pypi.python.org/pypi/git-rb)
[![Actions status](https://github.com/geo7/git-rb/workflows/CI/badge.svg)](https://github.com/geo7/git-rb/actions)

`git-rb` is a command-line tool to simplify interactive rebase workflow in Git,
often I'd find my self copying hashes from `git log` output in order to paste
into `git rebase -i`. This tools only purpose is to simplify that.

Code is self contained within `main.py`, so you could just copy the whole script.

## Usage

Typically I'll have the following in `.gitconfig`:

```
[alias]
  rb = !<<sh command to run this git-rb script>>
```

To provide the alias `git rb`.
