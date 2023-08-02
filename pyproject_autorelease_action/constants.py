from pathlib import Path
from tomllib import load

from github_action_utils import get_env, get_user_input

GITHUB_TOKEN: str = get_env("GITHUB_TOKEN")
PROJECT_PATH = Path(get_user_input("project_path") or get_env("GITHUB_WORKSPACE") or Path.cwd())
PYPROJECT_PATH = Path(get_user_input("pyproject_path") or PROJECT_PATH / "pyproject.toml")
CHANGELOG_PATH = Path(get_user_input("changelog_path") or PROJECT_PATH / "CHANGELOG.md")

ERROR_NO_CHANGELOG: bool = str(get_user_input("error_no_changelog") or "false").lower() == "true"
ERROR_ON_EXIST: bool = str(get_user_input("error_on_release_exist") or "false").lower() == "true"
IS_DRAFT: bool = str(get_user_input("is_draft") or "false").lower() == "true"
IS_PRERELASE: bool = str(get_user_input("is_prerelease") or "false").lower() == "true"

with PYPROJECT_PATH.open("rb") as f:
    POETRY_DATA: dict = load(f)["tool"]["poetry"]

PACKAGE_VERSION: str = POETRY_DATA["version"]
