import subprocess
from pathlib import Path
from unittest.mock import patch

from git_rb import __version__

# Import Prompt for mocking
from git_rb.main import Prompt


def test_version() -> None:
    # Ensure toml version is in sync with package version.
    with open("pyproject.toml") as f:
        pyproject_version = [line for line in f if line.startswith("version = ")]
    assert len(pyproject_version) == 1
    assert pyproject_version[0].strip().split(" = ")[-1].replace('"', "") == __version__


def test_git_rb_help(git_repo: Path, run_git_rb):
    """Test that --help displays correctly."""
    exit_code, stdout, stderr = run_git_rb("--help", cwd=git_repo)
    assert exit_code == 0
    assert "usage: git-rb [-h]" in stdout  # rich prints to stdout for help
    assert "Git rebase workflow tool." in stdout
    assert not stderr


@patch.object(Prompt, "ask")
def test_git_rb_successful_rebase(mock_prompt_ask, git_repo: Path, run_git_rb):
    """Test a successful interactive rebase scenario."""
    # Simulate user selecting the second commit (index 2, which is "feat: Add second file")
    # The commits in git_repo are:
    # 1: feat: Initial commit
    # 2: feat: Add second file
    # 3: fix: Update file1
    mock_prompt_ask.return_value = "2"

    # Run the git-rb tool
    exit_code, stdout, stderr = run_git_rb(cwd=git_repo)

    # Assertions
    assert exit_code == 0
    assert "Fetching the last 15 commits..." in stdout
    assert "Recent Commits" in stdout
    assert "Running command: git rebase -i" in stdout
    assert "Successfully rebased and updated refs/heads/main." in stderr  # Output from git rebase
    assert not stderr.replace(
        "Successfully rebased and updated refs/heads/main.", ""
    ).strip()  # Only rebase success message

    # Verify the rebase actually happened (e.g., by checking git log)
    # Get the hash of the "feat: Add second file" commit
    log_output = subprocess.run(
        ["git", "log", "--pretty=format:%h", "--grep=Add second file"],
        cwd=git_repo,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    rebase_hash = log_output.splitlines()[0]  # Get the first hash

    # Check if the rebase command was correctly formed and executed
    assert f"git rebase -i {rebase_hash}^" in stdout

    # Verify the commit order after rebase
    # The commits should now be: fix: Update file1, feat: Add second file, feat: Initial commit
    rebased_log = (
        subprocess.run(
            ["git", "log", "--pretty=format:%s"],
            cwd=git_repo,
            capture_output=True,
            text=True,
            check=True,
        )
        .stdout.strip()
        .splitlines()
    )
    assert rebased_log[0] == "fix: Update file1"
    assert rebased_log[1] == "feat: Add second file"
    assert rebased_log[2] == "feat: Initial commit"


@patch.object(Prompt, "ask")
def test_git_rb_abort(mock_prompt_ask, git_repo: Path, run_git_rb):
    """Test user aborting the rebase."""
    mock_prompt_ask.return_value = "q"  # Simulate user aborting

    exit_code, stdout, stderr = run_git_rb(cwd=git_repo)

    assert exit_code == 0
    assert "Aborting." in stdout
    assert "Running command: git rebase -i" not in stdout  # Ensure rebase was not called
    assert not stderr


@patch.object(Prompt, "ask")
def test_git_rb_invalid_input(mock_prompt_ask, git_repo: Path, run_git_rb):
    """Test invalid user input for selection."""
    mock_prompt_ask.return_value = "abc"  # Simulate invalid input

    exit_code, stdout, stderr = run_git_rb(cwd=git_repo)

    assert exit_code == 1  # Expect SystemExit(1)
    assert "Error: Invalid input. Please enter a number." in stderr
    assert "Fetching the last 15 commits..." in stdout  # Initial output should still be there
    assert "Recent Commits" in stdout  # Initial output should still be there


@patch.object(Prompt, "ask")
def test_git_rb_out_of_range_input(mock_prompt_ask, git_repo: Path, run_git_rb):
    """Test user inputting a number out of range."""
    mock_prompt_ask.return_value = "99"  # Simulate out of range

    exit_code, stdout, stderr = run_git_rb(cwd=git_repo)

    assert exit_code == 1  # Expect SystemExit(1)
    assert "Error: Number out of range." in stderr
    assert "Fetching the last 15 commits..." in stdout  # Initial output should still be there
    assert "Recent Commits" in stdout  # Initial output should still be there


@patch.object(Prompt, "ask")
def test_git_rb_not_in_git_repo(mock_prompt_ask, tmp_path: Path, run_git_rb):
    """Test running git-rb outside a Git repository."""
    exit_code, stdout, stderr = run_git_rb(cwd=tmp_path)

    assert exit_code == 1  # Expect SystemExit(1)
    assert "Error:" in stderr  # Or similar git error message
    assert not stdout


@patch.object(Prompt, "ask")
def test_git_rb_no_commits(mock_prompt_ask, git_repo_no_commits, run_git_rb):
    """Test a successful interactive rebase scenario."""
    mock_prompt_ask.return_value = "2"
    exit_code, _, stderr = run_git_rb(cwd=git_repo_no_commits)
    assert exit_code == 1
    assert "Error: fatal: your current branch 'main' does not have any commits yet" in stderr
