# stdlib
from typing import Any, Dict, List

# 3rd party
import sphinx.directives.other
import sphinx.writers.latex
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.config import Config

__all__ = ["LaTeXTranslator", "LatexTocTreeDirective", "setup"]

use_bookmark = r"\usepackage{bookmark}"
nest_bookmark_level_part = "\\bookmarksetupnext{{level=part}}\n"


class LaTeXTranslator(sphinx.writers.latex.LaTeXTranslator):

	def generate_indices(self) -> str:

		return '\n'.join([
				nest_bookmark_level_part,
				*super().generate_indices().splitlines(),
				'',
				nest_bookmark_level_part,
				])


class LatexTocTreeDirective(sphinx.directives.other.TocTree):

	def run(self) -> List[nodes.Node]:

		output = []
		caption = self.options.get("caption")

		if (
				caption is not None and self.env.app.builder.name.lower() == "latex"
				and self.env.docname == self.env.config.master_doc
				):

			latex_part_node = nodes.raw(
					text=f"\\setcounter{{section}}{{0}}\n\\part{{{caption}}}\n\\setcounter{{chapter}}{{1}}",
					format="latex"
					)
			output.append(latex_part_node)

		output.extend(super().run())

		return output


def configure(app: Sphinx, config: Config):
	"""
	Configure the Sphinx extension.

	:param app:
	:param config:
	"""

	if not hasattr(config, "latex_elements"):
		config.latex_elements = {}

	latex_preamble = (config.latex_elements or {}).get("preamble", '')

	if use_bookmark not in latex_preamble:
		config.latex_elements["preamble"] = f"{latex_preamble}\n{use_bookmark}"


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup Sphinx extension.

	:param app:
	"""

	app.connect("config-inited", configure)
	app.add_directive("toctree", LatexTocTreeDirective, override=True)
	app.set_translator("latex", LaTeXTranslator, override=True)

	return {
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}
