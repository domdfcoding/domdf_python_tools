# stdlib
from typing import Any, Dict, List, Tuple

# 3rd party
import sphinx.directives.other
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.domains import IndexEntry
from sphinx.writers.latex import LaTeXTranslator

__all__ = ["TocTreePlusDirective", "setup"]


def generate_indices(translator) -> str:
	def generate(content: List[Tuple[str, List[IndexEntry]]], collapsed: bool) -> None:
		ret.append("\\bookmarksetupnext{{level=part}}\n")
		ret.append('\\begin{sphinxtheindex}\n')
		ret.append('\\let\\bigletter\\sphinxstyleindexlettergroup\n')
		for i, (letter, entries) in enumerate(content):
			if i > 0:
				ret.append('\\indexspace\n')
			ret.append('\\bigletter{%s}\n' % translator.escape(letter))
			for entry in entries:
				if not entry[3]:
					continue
				ret.append('\\item\\relax\\sphinxstyleindexentry{%s}' %
						   translator.encode(entry[0]))
				if entry[4]:
					# add "extra" info
					ret.append('\\sphinxstyleindexextra{%s}' % translator.encode(entry[4]))
				ret.append('\\sphinxstyleindexpageref{%s:%s}\n' %
						   (entry[2], translator.idescape(entry[3])))
		ret.append('\\end{sphinxtheindex}\n')

	ret = []
	# latex_domain_indices can be False/True or a list of index names
	indices_config = translator.builder.config.latex_domain_indices
	if indices_config:
		for domain in translator.builder.env.domains.values():
			for indexcls in domain.indices:
				indexname = '%s-%s' % (domain.name, indexcls.name)
				if isinstance(indices_config, list):
					if indexname not in indices_config:
						continue
				content, collapsed = indexcls(domain).generate(
						translator.builder.docnames)
				if not content:
					continue
				ret.append('\\renewcommand{\\indexname}{%s}\n' %
						   indexcls.localname)
				generate(content, collapsed)

	return ''.join(ret)

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
			latex_part_node = nodes.raw(text=f"\\setcounter{{section}}{{0}}\n\\bookmarksetupnext{{level=part}}\n\\part{{{caption}}}\n\\setcounter{{chapter}}{{1}}", format="latex")
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
	LaTeXTranslator.generate_indices = generate_indices

	return {
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}
