import re
from dataclasses import dataclass
from typing import Self

from github_action_utils import get_user_input

from .constants import CHANGELOG_PATH, PACKAGE_VERSION

_NAME_RE = re.compile(r"\[(?P<name>.+)] - v?(?P<version>.+)")


@dataclass
class Changelog:
    changes: str
    name: str

    def __bool__(self):
        return bool(self.changes)

    @classmethod
    def parse_changelog(cls) -> Self | None:
        """Parse the changelog file and return the latest version."""
        name: str = get_user_input("release_name") or f"v{PACKAGE_VERSION}"
        changes: str = get_user_input("release_changes") or ""

        if not name or not changes:
            if not CHANGELOG_PATH.exists():
                return None

            with CHANGELOG_PATH.open("r") as f:
                changelog = f.read().split("## ")[1:]

            changes_dict = {}

            for i in changelog:
                version, new_changes = i.split("\n", 1)

                if m := _NAME_RE.match(version.split("\n")[0]):
                    changes_dict[m.group("version")] = cls(
                        changes=new_changes.split("\n", 1)[-1].strip() or changes,
                        name=m.group("name") or name,
                    )
                else:
                    changes_dict[version] = cls(changes=changes, name=name)
            return changes_dict.get(PACKAGE_VERSION, None)

        return cls(changes, name)
