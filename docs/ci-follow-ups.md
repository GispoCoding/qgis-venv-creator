# CI follow-ups

These CI improvements were left out of the changelog and workflow hardening work so they can be done later.
Snippets pin actions to commit SHAs, like the workflows do. Check for newer releases before using them.

## 1. Lint workflows with zizmor

[zizmor](https://docs.zizmor.sh/) finds security issues in GitHub Actions workflows. With all the hardening in
place, `uvx zizmor --offline .github/workflows` reports only one informational finding (see item 4).
Running it as a prek hook catches regressions when workflows are edited. The hook also checks
`.github/dependabot.yml`.

Add to `prek.toml`:

```toml
[[repos]]
repo = "https://github.com/zizmorcore/zizmor-pre-commit"
rev = "v1.30.1"
hooks = [{ id = "zizmor", args = ["--offline"] }]
```

`--offline` skips the audits that call the GitHub API, so the hook needs no token. To also run it in CI, add a
`uvx zizmor .github/workflows` step to the lint job, with `GH_TOKEN` set for the online audits.

## 2. Group Dependabot updates and add a cooldown

Dependabot opens one PR per dependency and replaces it with every new upstream release. ruff, ty and prek PRs
(#36–#51) kept superseding each other before anyone could merge them. Grouping makes one PR per ecosystem a
week. A cooldown waits a few days before proposing a new release, which avoids picking up a compromised release
before it is pulled.

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    cooldown:
      default-days: 7
    groups:
      github-actions:
        patterns: ["*"]
  - package-ecosystem: "uv"
    directory: "/"
    schedule:
      interval: "weekly"
    cooldown:
      default-days: 7
    groups:
      python-dependencies:
        patterns: ["*"]
```

The ruff and ty hook revisions in `prek.toml` still have to be bumped by hand to match `uv.lock`.

## 3. Attest build provenance

PyPI already gets [PEP 740](https://peps.python.org/pep-0740/) attestations through trusted publishing. The
files attached to the GitHub release (wheel, sdist and the standalone `create_qgis_venv.py`) don't. With a
provenance attestation, users can check where a downloaded file was built:
`gh attestation verify create_qgis_venv.py --repo GispoCoding/qgis-venv-creator`.

In the `build` job of `release.yml`:

```yaml
    permissions:
      contents: read
      id-token: write
      attestations: write
    steps:
      # ... after "Build distribution":
      - name: Attest build provenance
        uses: actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6 # v4.2.2
        with:
          subject-path: |
            dist/*
            src/qgis_venv_creator/create_qgis_venv.py
```

## 4. Create the GitHub release with `gh` instead of a third-party action

zizmor's `superfluous-actions` audit points out that the runner's `gh` CLI can create the release. Dropping
`softprops/action-gh-release` removes third-party code from the job that has `contents: write`:

```yaml
      - name: Create release
        env:
          GH_TOKEN: ${{ github.token }}
          VERSION: ${{ needs.build.outputs.version }}
          TARGET: ${{ github.event.pull_request.merge_commit_sha }}
        run: >-
          gh release create "v$VERSION"
          --repo "$GITHUB_REPOSITORY"
          --title "Release $VERSION"
          --target "$TARGET"
          --notes-file release-notes.md
          dist/* src/qgis_venv_creator/create_qgis_venv.py
```

## 5. Open release PRs with a GitHub App token

The Prepare a Release workflow opens the release PR with `GITHUB_TOKEN`. GitHub doesn't run workflows
automatically for events created with that token. On the 0.2.1 release PR, the first test run ended as
`action_required` and had to be started by hand. The changelog check behaves the same way.

A GitHub App token makes the release PR behave like any other PR. Install an app on the repository with contents
and pull request write access, store its client ID and private key as secrets, and in `release_pr.yml`:

```yaml
      - name: Create a GitHub App token
        id: app-token
        uses: actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1 # v3.2.0
        with:
          client-id: ${{ secrets.RELEASE_APP_CLIENT_ID }}
          private-key: ${{ secrets.RELEASE_APP_PRIVATE_KEY }}

      - name: Create pull request
        uses: peter-evans/create-pull-request@...
        with:
          token: ${{ steps.app-token.outputs.token }}
          # ...
```

## 6. Protect publishing and `main`

- Add a required reviewer to the `pypi` deployment environment (Settings → Environments). Publishing then waits
  for a manual approval, which is a last check before anything reaches PyPI.
- Branch protection on `main` has no required status checks. Requiring the test jobs and the changelog check
  stops a PR from being merged while they fail. Item 5 is needed first, otherwise release PRs can't satisfy
  required checks without manual runs.
