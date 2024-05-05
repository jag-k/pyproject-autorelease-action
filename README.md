# pyproject-autorelease-action

Auto release the python project based on changes version in pyproject.toml

## Usage

```yaml
on:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Autorelease
        uses: jag-k/pyproject-autorelease-action@latest
        id: release
        env:
          GITHUB_TOKEN: ${{ github.token }}
      - name: Release result
        run: |
          echo "${{ steps.release.outputs.release_result }}"

```

## Note
You need set a permission `contents: write`
