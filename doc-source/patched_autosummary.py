# stdlib
import re
from typing import Any, Dict, List, Tuple

# 3rd party
import sphinx
from sphinx.application import Sphinx
from sphinx.ext.autosummary import Autosummary


class PatchedAutosummary(Autosummary):
	"""
	Pretty table containing short signatures and summaries of functions etc.

	Patched version of :class:`sphinx.ext.autosummary.Autosummary` to fix issue where
	the module name is sometimes duplicated.

	I.e. ``foo.bar.baz()`` became ``foo.bar.foo.bar.baz()``, which of course doesn't exist
	and so resulted in a broken link.
	"""

	def import_by_name(self, name: str, prefixes: List[str]) -> Tuple[str, Any, Any, str]:
		real_name, obj, parent, modname = super().import_by_name(name=name, prefixes=prefixes)
		real_name = re.sub(rf"((?:{modname}\.)+)", f"{modname}.", real_name)
		return real_name, obj, parent, modname


def setup(app: Sphinx) -> Dict[str, Any]:
	app.setup_extension("sphinx.ext.autosummary")
	app.add_directive("autosummary", PatchedAutosummary, override=True)

	return {
			"version": f"{sphinx.__display_version__}-patched-autosummary-0",
			"parallel_read_safe": True,
			}
