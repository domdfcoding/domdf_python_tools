# stdlib
from typing import Any, Dict, List

# 3rd party
import sphinx.directives.other
from docutils import nodes
from sphinx.application import Sphinx

__all__ = ["TocTreePlusDirective", "setup"]


class TocTreePlusDirective(sphinx.directives.other.TocTree):

	def run(self) -> List[nodes.Node]:

		output = []
		caption = self.options.get("caption")

		if (
				caption is not None and self.env.app.builder.name.lower() == "latex"
				and self.env.docname == self.env.config.master_doc
				):

			latex_part_node = nodes.raw(text=f"\\part{{{caption}}}", format="latex")
			output.append(latex_part_node)
			# self.state.nested_parse(StringList(), self.content_offset, latex_part_node)

		output.extend(super().run())
		return output


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup Sphinx Extension.

	:param app:
	"""

	app.add_directive("toctree", TocTreePlusDirective, override=True)

	return {
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}
