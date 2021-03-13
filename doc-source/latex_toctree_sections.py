# stdlib
from typing import Any, Dict, List

# 3rd party
import sphinx.directives.other
from docutils import nodes
from sphinx.application import Sphinx

__all__ = ["TocTreePlusDirective", "setup"]


# TODO: The first section in a part has all sub sections nested under it in the sidebar,
#  The numbering is correct, and its correct in the contents

class TocTreePlusDirective(sphinx.directives.other.TocTree):

	def run(self) -> List[nodes.Node]:

		output = []
		caption = self.options.get("caption")

		if (
				caption is not None and self.env.app.builder.name.lower() == "latex"
				and self.env.docname == self.env.config.master_doc
				):

			# TODO: \setcounter{section}{0}
			# https://tex.stackexchange.com/questions/271075/reset-counter-section-in-part
			latex_part_node = nodes.raw(text=f"\\setcounter{{chapter}}{{1}}\n\\setcounter{{section}}{{0}}\n\\\\part{{{caption}}}", format="latex")
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
