# Kaye Engine: GitHub Release Builds

`build-github-release` builds the one versioned plugin `.zip` of a consumer project, ready to attach to a GitHub Release. It reaches the archive through the same path as `claude plugin -z`, so the zip opens straight in Claude Desktop's *Plugins > Upload*.

## Run It from a Consumer CLI

A bare `kaye-engine` console script registers no consumer, so it has nothing to export. Run the command through the console script of a consumer project, which registers its consumers first (q.v. [Consumer Requirement](claude-doc.md#consumer-requirement)):

```bash
CONSUMER_CLI build-github-release CONSUMER_PROJ            # dist/CONSUMER_PROJ-claude-VERSION.zip
CONSUMER_CLI build-github-release CONSUMER_PROJ -o FOLDER  # FOLDER/CONSUMER_PROJ-claude-VERSION.zip
CONSUMER_CLI build-github-release CONSUMER_PROJ -n          # print the result line, write nothing
```

- `CONSUMER_PROJ`: required, the canonical name of the consumer to build. One process may hold several consumers (a consumer plus a library it depends on); the name picks one, so only that zip is produced. An unknown name exits 1 and lists the valid names
- `-o`, `--output FOLDER`: destination folder, created when missing; default `dist/`
- `-n`, `--dry-run`: report the zip and write nothing
- render options (`--surface`, `--comment`, `--sparseness`, ~~): the same flags and defaults as `claude plugin`, surface `claude`, comments off, sparseness `0`
- `-v`: more build detail, as `claude plugin -z`

The zip is named `CONSUMER_PROJ-claude-VERSION.zip`, carrying the consumer's version, and has `.claude-plugin/plugin.json` at its root.

## Actions Pattern

A release workflow runs on a version tag, installs the engine and the consumer, builds the zip, and uploads it. The engine and consumer versions come from the consumer's own `pyproject.toml` pins, never from the workflow.

```yaml
on:
  push:
    tags: ["v*"]

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - name: Install engine at the pinned tag, then the consumer
        run: |
          ENGINE_VERSION=$(sed -nE 's/.*kaye-engine==([0-9][^"]*).*/\1/p' pyproject.toml | head -1)
          pip install "git+https://github.com/OWNER/kaye-engine.git@v${ENGINE_VERSION}"
          pip install --no-deps .
      - name: Build the zip
        run: CONSUMER_CLI build-github-release CONSUMER_PROJ -o dist
      - name: Create the release
        env:
          GH_TOKEN: ${{ github.token }}
        run: gh release create "$GITHUB_REF_NAME" dist/*.zip --generate-notes
```

- Pin Read: parse the version out of the `kaye-engine==X` pin, so the installed engine follows the consumer's `pyproject.toml`
- Tag Check: compare the tag with `v` plus the consumer's version before building, so a stray tag fails early
- Pre-releases: add `--prerelease` to `gh release create` for `-alpha` and `-beta` tags
- Token: public repositories need no secret; the built-in `GITHUB_TOKEN` covers checkout and the upload
