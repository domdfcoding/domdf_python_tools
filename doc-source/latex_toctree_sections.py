# stdlib
from typing import Any, Dict, List

# 3rd party
import sphinx.directives.other
import sphinx.writers.latex
from docutils import nodes
from sphinx.application import Sphinx

__all__ = ["TocTreePlusDirective", "setup"]


class LaTeXTranslator(sphinx.writers.latex.LaTeXTranslator):

	def generate_indices(self) -> str:

		lines = super().generate_indices().splitlines()

		return "\n".join([
				"\\bookmarksetupnext{{level=part}}\n",
				*lines,
				'',
				"\\bookmarksetupnext{{level=part}}\n",
				])

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
			latex_part_node = nodes.raw(
					text=
					f"\\setcounter{{section}}{{0}}\n\\part{{{caption}}}\n\\setcounter{{chapter}}{{1}}",
					format="latex"
					)
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
	app.set_translator("latex", LaTeXTranslator, override=True)

	return {
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}
