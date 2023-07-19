# Bake a Py

This project provides a template from which you can create your own Python packages and projects.
It uses modern tools and conventions to ensure a good development experience.

- [Package Structure](#package-structure)
- [GitHub Features](#github-features)
- [Tooling](#tooling)

## Package Structure

Package structure was inspired by various templates and recommended best practices, such as:

- https://github.com/TezRomacH/python-package-template
- https://github.com/pyscaffold/pyscaffold
- https://github.com/f4str/python-package-template
- https://github.com/audreyfeldroy/cookiecutter-pypackage
- https://github.com/ionelmc/python-nameless

It provides a `src` directory, under which your own packages sit. Example files for `__init__.py`, `__main__.py` and `cli.py` are already provided.

Tests are placed under the `tests` directory, and documentation under the `docs` directory.

To start your new project, you should change its name, URL and metadata details at:

1. `README.md`
2. `CHANGELOG.md`
3. `setup.py`
4. `tests/*.py`
5. `src/*`

## GitHub Features

The `.github` directory comes with a number of files to configure certain GitHub features.

- Various Issue templates can be found under `ISSUE_TEMPLATE`.
- A Pull Request template can be found at `PULL_REQUEST_TEMPLATE.md`.
- Automatically mark issues as stale after a period of inactivity. The configuration file can be found at `.stale.yml`.
- Keep package dependencies up to date with Dependabot. The configuration file can be found at `dependabot.yml`.
- Keep Release Drafts automatically up to date with Pull Requests, using the [Release Drafter GitHub Action](https://github.com/marketplace/actions/release-drafter). The configuration file can be found at `release-drafter.yml` and the workflow at `workflows/release-drafter.yml`.
- Automatic package building and publishing when pushing a new version tag to `main`. The workflow can be found at `workflows/publish-package.yml`.
- Code quality and security analysis with CodeQL. The workflow can be found at `workflows/codeql-analysis.yml`.

## Tooling

This package sets up various `tox` environments for static checks, testing, building and publishing.
It is also configured with `pre-commit` hooks to perform static checks and automatic formatting.

If you do not use `tox`, you can build the package with `build` and install a development version with `pip`.

Assume `cd` into the repository's root.

To install the `pre-commit` hooks:

```bash
pre-commit install
```

To run type checking:

```bash
tox -e typecheck
```

To run linting tools:

```bash
tox -e lint
```

To run automatic formatting:

```bash
tox -e format
```

To run tests:

```bash
tox
```

To build the package:

```bash
tox -e build
```

To build the package (with `build`):

```bash
python -m build
```

To clean the previous build files:

```bash
tox -e clean
```

To test package publication (publish to *Test PyPI*):

```bash
tox -e publish
```

To publish the package to PyPI:

```bash
tox -e publish -- --repository pypi
```

To install an editable version:

```bash
pip install -e .
```
