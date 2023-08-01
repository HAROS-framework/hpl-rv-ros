# HPL RV for ROS

This project provides tools to create and deploy runtime monitors for your Robot Operating System applications.

- [Installing](#installing)
- [Usage](#usage)
- [GitHub Features](#github-features)
- [Tooling](#tooling)

## Installing

This package can be installed with `pip`:

```bash
pip install hpl-rv-ros
```

## Usage

You can use this project to generate code both as a library and as a standalone tool.

First, you will need a mapping of ROS topic types to message types.
This can be specified in YAML or JSON formats, when provided as a file.
For example:

```yaml
%YAML 1.2
# file: topics.yaml
---
/a: std_msgs/Int64
/b: std_msgs/Int64
/p: std_msgs/Bool
/q: std_msgs/Bool
```

Then, you will also need to provide a HPL specification. This can be either a list of properties, or a `.hpl` file, depending on how you want to use this package.

### As a Standalone Tool

This package provides the `hpl-rv-ros` CLI script.

#### Required Arguments

1. a path to the topic type mapping file
2. either a list of properties or a list of `.hpl` files, depending on flags

#### Optional Arguments

- flag `--rospy`: generate ROS1 code instead of ROS2 code
- flag `-f` or `--files`: treat positional arguments as a list of paths to `.hpl` files instead of a list of properties
- argument `-o` or `--output`: pass a path to an output file for the generated code (default: print to screen)

#### Example

To generate ROS2 code:

```bash
hpl-rv-ros -f -o rclpy_node.py topics.yaml properties.hpl
```

To generate ROS1 code:

```bash
hpl-rv-ros --rospy -f -o rospy_node.py topics.yaml properties.hpl
```

### As a Library

This repository provides the `hplrv_ros` Python package.

#### Example

```py
from typing import Dict, List
from pathlib import Path
from hpl.ast import HplProperty
from hpl.parser import property_parser
from hplrv_ros.rclpy import generate_node as generate_rclpy
from hplrv_ros.rospy import generate_node as generate_rospy

parser = property_parser()

topic_types: Dict[str, str] = { '/a': 'std_msgs/Int32' }
properties: List[HplProperty] = [parser.parse('globally: no /a {data > 0}')]

rclpy_code: str = generate_rclpy(properties, topic_types)
rospy_code: str = generate_rospy(properties, topic_types)

path: Path = Path('rclpy_node.py')
path.write_text(rclpy_code, encoding='utf-8')
path = Path('rospy_node.py')
path.write_text(rospy_code, encoding='utf-8')
```


## GitHub Features

The `.github` directory comes with a number of files to configure certain GitHub features.

- Various Issue templates can be found under `ISSUE_TEMPLATE`.
- A Pull Request template can be found at `PULL_REQUEST_TEMPLATE.md`.
- Automatically mark issues as stale after a period of inactivity. The configuration file can be found at `.stale.yml`.
- Keep package dependencies up to date with Dependabot. The configuration file can be found at `dependabot.yml`.
- Keep Release Drafts automatically up to date with Pull Requests, using the [Release Drafter GitHub Action](https://github.com/marketplace/actions/release-drafter). The configuration file can be found at `release-drafter.yml` and the workflow at `workflows/release-drafter.yml`.
- Automatic package building and publishing when pushing a new version tag to `main`. The workflow can be found at `workflows/publish-package.yml`.

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
