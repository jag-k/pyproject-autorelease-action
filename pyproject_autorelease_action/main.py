import json

import requests
from github_action_utils import append_job_summary, error, get_env, get_user_input, set_output, warning

from .changelog import Changelog
from .constants import (
    ERROR_NO_CHANGELOG,
    ERROR_ON_EXIST,
    GITHUB_TOKEN,
    IS_DRAFT,
    IS_PRERELASE,
    PACKAGE_VERSION,
)

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}
releases_url = f"{get_env('GITHUB_API_URL')}/repos/{get_env('GITHUB_REPOSITORY')}/releases"

print(releases_url)


def main():
    changelog = Changelog.parse_changelog()

    set_output("version", PACKAGE_VERSION)

    if not changelog:
        if ERROR_NO_CHANGELOG:
            error("No changelog found!")
            return exit(1)
        warning("No changelog found!")
        return exit(0)
    releases_data = requests.get(  # noqa: S113
        releases_url,
        headers=headers,
    )
    releases: list[dict] = releases_data.json()

    if releases_data.status_code != 200:
        error(json.dumps(releases, indent=2, ensure_ascii=False))
        return exit(1)

    if any(i["tag_name"].lstrip("v") == PACKAGE_VERSION for i in releases):
        set_output("release_exist", "true")
        if ERROR_ON_EXIST:
            error("Release already exists!")
            return exit(1)
        warning("Release already exists!")
        return exit(0)
    set_output("release_exist", "true")

    name = "v" + PACKAGE_VERSION
    body = (
        str(get_user_input("body") or "")
        or "\n\n".join(
            [
                str(get_user_input("body_prefix") or ""),
                changelog.changes,
                str(get_user_input("body_suffix") or ""),
            ]
        ).strip()
    )
    result = requests.post(  # noqa: S113
        releases_url,
        headers=headers,
        json={
            "tag_name": name,
            "target_commitish": get_env("GITHUB_SHA") or get_env("GITHUB_REF_NAME") or "main",
            "name": changelog.name,
            "body": body,
            "draft": IS_DRAFT,
            "prerelease": IS_PRERELASE,
            "generate_release_notes": False,
        },
    )
    if result.status_code != 201:
        error(json.dumps(result.json(), indent=2, ensure_ascii=False))
        return exit(1)
    set_output("release_result", result.text)
    append_job_summary(f'# Release "{changelog.name}" ({name})\n\n{changelog.changes}')


if __name__ == "__main__":
    main()
