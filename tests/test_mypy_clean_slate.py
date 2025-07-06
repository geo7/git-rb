
from git_rb import __version__

def test_version() -> None:
    # Ensure toml version is in sync with package version.
    with open("pyproject.toml") as f:
        pyproject_version = [line for line in f if line.startswith("version = ")]
    assert len(pyproject_version) == 1
    assert pyproject_version[0].strip().split(" = ")[-1].replace('"', "") == __version__
