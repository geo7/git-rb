import os
import subprocess
import sys
from io import StringIO
from pathlib import Path

import pytest


@pytest.fixture
def git_repo(tmp_path: Path):
    """
    Pytest fixture to create a temporary Git repository.

    Yields the path to the temporary repository.
    """
    original_cwd = Path.cwd()
    os.chdir(tmp_path)  # Change to the temporary directory

    # Initialize a Git repository
    subprocess.run(["git", "init", "-b", "main"], check=True, capture_output=True)

    # Configure Git user for commits
    subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], check=True)

    # Create a dummy editor script that just exits successfully
    editor_script = tmp_path / "git_editor.sh"
    editor_script.write_text("#!/bin/bash\nexit 0")
    editor_script.chmod(0o755)  # Make it executable

    # Set GIT_EDITOR to the path of the dummy editor script
    os.environ["GIT_EDITOR"] = str(editor_script)

    # Create some initial commits
    (tmp_path / "file1.txt").write_text("initial content")
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "feat: Initial commit"], check=True)

    (tmp_path / "file2.txt").write_text("second file")
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "feat: Add second file"], check=True)

    (tmp_path / "file1.txt").write_text("updated content")
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "fix: Update file1"], check=True)

    # Yield the path to the temporary repository
    yield tmp_path

    # Teardown: Change back to the original working directory and unset GIT_EDITOR
    os.chdir(original_cwd)
    del os.environ["GIT_EDITOR"]


@pytest.fixture
def run_git_rb():
    """
    Fixture to run the git-rb command.

    It returns a callable that takes arguments for git-rb and an optional cwd.
    """

    def _runner(*args, cwd: Path = None):
        from git_rb.main import main

        original_cwd = Path.cwd()
        if cwd:
            os.chdir(cwd)

        original_argv = sys.argv
        sys.argv = ["git-rb", *args]

        # Capture stdout/stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        # Capture stdout/stderr as StringIO objects,
        # captured_stdout/captured_stderr ensure stable references to these
        # values.
        sys.stdout = captured_stdout = StringIO()
        sys.stderr = captured_stderr = StringIO()

        exit_code = 0

        try:
            main()
        except SystemExit as e:
            exit_code = e.code if e.code is not None else 1
        except Exception as e:
            raise e
        finally:
            sys.argv = original_argv
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            if cwd:
                os.chdir(original_cwd)

        return exit_code, captured_stdout.getvalue(), captured_stderr.getvalue()

    return _runner
