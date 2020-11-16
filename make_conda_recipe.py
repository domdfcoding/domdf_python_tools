#!/usr/bin/python3

# This file is managed by 'repo_helper'. Don't edit it directly.

# stdlib
import pathlib

# this package
from __pkginfo__ import __version__

description_block = """Helpful functions for Python 🐍 🛠️



Before installing please ensure you have added the following channels: domdfcoding, conda-forge
""".replace('"', '\\"')


repo_root = pathlib.Path(__file__).parent
recipe_dir = repo_root / "conda"

if not recipe_dir.exists():
	recipe_dir.mkdir()

all_requirements = (repo_root / "requirements.txt").read_text(encoding="utf-8").split('\n')

# TODO: entry_points, manifest

for requires in {'dates': ['pytz>=2019.1'], 'testing': ['pytest>=6.0.0', 'pytest-regressions>=2.0.2'], 'all': ['pytest-regressions>=2.0.2', 'pytest>=6.0.0', 'pytz>=2019.1']}.values():
	all_requirements += requires

all_requirements = {x.replace(" ", '') for x in set(all_requirements)}
requirements_block = "\n".join(f"    - {req}" for req in all_requirements if req)

(recipe_dir / "meta.yaml").write_text(
		encoding="UTF-8",
		data=f"""\
package:
  name: "domdf_python_tools"
  version: "{__version__}"

source:
  url: "https://pypi.io/packages/source/d/domdf_python_tools/domdf_python_tools-{__version__}.tar.gz"

build:
  noarch: python
  script: "{{{{ PYTHON }}}} -m pip install . -vv"

requirements:
  build:
    - python
    - setuptools
    - wheel
  host:
    - pip
    - python
{requirements_block}
  run:
    - python
{requirements_block}

test:
  imports:
    - domdf_python_tools

about:
  home: "https://github.com/domdfcoding/domdf_python_tools"
  license: "GNU Lesser General Public License v3 or later (LGPLv3+)"
  # license_family: LGPL
  # license_file: LICENSE
  summary: "Helpful functions for Python 🐍 🛠️"
  description: "{description_block}"
  doc_url: https://domdf_python_tools.readthedocs.io
  dev_url: https://github.com/domdfcoding/domdf_python_tools

extra:
  maintainers:
    - Dominic Davis-Foster
    - github.com/domdfcoding

""")

print(f"Wrote recipe to {recipe_dir / 'meta.yaml'}")
