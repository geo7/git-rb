# Git `rb`

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI Latest Release](https://img.shields.io/pypi/v/git-rb.svg)](https://pypi.org/project/git-rb/)
[![License](https://img.shields.io/pypi/l/git-rb.svg)](https://github.com/geo7/git-rb/blob/main/LICENSE)
[![image](https://img.shields.io/pypi/pyversions/git-rb.svg)](https://pypi.python.org/pypi/git-rb)
[![Actions status](https://github.com/geo7/git-rb/workflows/CI/badge.svg)](https://github.com/geo7/git-rb/actions)

`git-rb` is a simple command-line tool to simplify interactive rebase workflow
in Git, often I'd find my self copying hashes from `git log` output in order to
paste into `git rebase -i`. This tools only purpose is to simplify that.

Code is self contained within `main.py`, so you could just copy the whole script.

> **Note**: _I had this a form of this script kicking around for a while and
> figured I'd try using [Gemini
> CLI](https://github.com/google-gemini/gemini-cli) to do the rest. Results
> were mixed, I wasn't able to '_set and forget_', but it was still useful._

## Usage

### `.gitconfig`

Typically I'll have the following in `.gitconfig`:
```
[alias]
  rb = !uvx git-rb
```

To provide alias `git rb`.

### Example

Running this from sklearn gives:

![Screenshot of git-rb's help message](imgs/img3.png)

Entering '6' in the prompt just runs `git rebase -i <hash on line 6>`, nothing fancy!

![Screenshot of git-rb in action](imgs/img1.png)

## Simple

A simpler approach would be to just use:

```sh
git rebase -i HEAD~{{ N }}
```

That would mean no messing about with `rich` though.
