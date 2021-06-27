# TemporaryDirectorySubclassDocumenter and Autosummary based on Sphinx
# https://github.com/sphinx-doc/sphinx
#
# Copyright (c) 2007-2021 by the Sphinx team.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
import re
import sys
from tempfile import TemporaryDirectory
from types import ModuleType
from typing import Any, List, Optional, Tuple

# 3rd party
from docutils import nodes
from docutils.nodes import Node
from docutils.statemachine import StringList
from sphinx import addnodes
from sphinx.application import Sphinx, logger
from sphinx.builders.latex import LaTeXTranslator
from sphinx.errors import PycodeError
from sphinx.ext.autodoc import Documenter, Options
from sphinx.ext.autodoc.directive import DocumenterBridge
from sphinx.ext.autosummary import extract_summary, get_import_prefixes_from_env, mangle_signature
from sphinx.locale import _, __, admonitionlabels
from sphinx.pycode import ModuleAnalyzer
from sphinx.util.docutils import SphinxDirective, SphinxRole, unescape
from sphinx_toolbox import latex
from sphinx_toolbox.more_autodoc.typehints import default_preprocessors, format_annotation
from sphinx_toolbox.more_autosummary import PatchedAutoSummClassDocumenter
from sphinx_toolbox_experimental.autosummary_widths import AutosummaryWidths

# this package
from domdf_python_tools.paths import PathPlus


def replace_emoji(app: Sphinx, exception: Optional[Exception] = None):
	if exception:
		return

	if app.builder.name.lower() != "latex":
		return

	output_file = PathPlus(app.builder.outdir) / f"{app.builder.titles[0][1]}.tex"

	output_content = output_file.read_text()

	# Documentation summary emoji
	output_content = output_content.replace(" 🐍 🛠️", '')
	output_content = output_content.replace('🐍', '')
	output_content = output_content.replace('🛠', '')
	output_content = output_content.replace('️', '')  # Variation Selector-16

	output_content = output_content.replace('≈', r" $\approx$ ")  # coming in sphinx-toolbox 2.12
	output_content = output_content.replace('μ', r"\textmu ")  # fixed in sphinx-toolbox 2.12
	output_content = output_content.replace(r"\textmum", r"\textmu m")  # fixed in sphinx-toolbox 2.12
	output_content = output_content.replace('\u205f', r"\medspace ")  # medium mathematical space

	# in words.py
	output_content = output_content.replace(r'A\sphinxhyphen{}Ω', r"A\sphinxhyphen{}\textOmega")
	output_content = output_content.replace(r'α\sphinxhyphen{}ϖ', r"\textalpha\sphinxhyphen{}\textomega")

	output_file.write_clean(output_content)


class InlineRole(SphinxRole):
	"""
	Sphinx role for showing inline code (monospaced) which contains backticks.
	"""

	def run(self):
		return [nodes.literal('', unescape(self.text))], []


class TemporaryDirectorySubclassDocumenter(PatchedAutoSummClassDocumenter):
	"""
	Modified class documenter for documenting :class:`domdf_python_tools.paths.TemporaryDirectory`.

	Can be removed with sphinx-toolbox 2.12.0
	"""

	priority = PatchedAutoSummClassDocumenter.priority + 2
	objtype = "td-class"
	directivetype = "class"

	@classmethod
	def can_document_member(
			cls,
			member: Any,
			membername: str,
			isattr: bool,
			parent: Any,
			) -> bool:

		if not isinstance(member, type):
			return False
		if not issubclass(member, TemporaryDirectory):
			return False

		return super().can_document_member(member, membername, isattr, parent)

	def add_directive_header(self, sig: str) -> None:
		sourcename = self.get_sourcename()

		if self.doc_as_attr:
			self.directivetype = "attribute"

		Documenter.add_directive_header(self, sig)

		if self.analyzer and '.'.join(self.objpath) in self.analyzer.finals:
			self.add_line("   :final:", sourcename)

		# add inheritance info, if wanted
		if not self.doc_as_attr and self.options.show_inheritance:
			sourcename = self.get_sourcename()
			self.add_line('', sourcename)
			if hasattr(self.object, "__bases__") and len(self.object.__bases__):
				bases = []

				for b in self.object.__bases__:
					if b is TemporaryDirectory:
						bases.append(":py:obj:`~tempfile.TemporaryDirectory`")
					elif b.__module__ in ("__builtin__", "builtins"):
						bases.append(f':class:`{b.__name__}`')
					else:
						bases.append(format_annotation(b))

				self.add_line("   " + _("Bases: %s") % ", ".join(bases), sourcename)


class Autosummary(AutosummaryWidths):
	"""
	Modified autosummary directive which allows the summary of objects to be customised.
	"""

	def get_items(self, names: List[str]) -> List[Tuple[str, str, str, str]]:
		"""Try to import the given names, and return a list of
		``[(name, signature, summary_string, real_name), ...]``.
		"""
		prefixes = get_import_prefixes_from_env(self.env)

		items: List[Tuple[str, str, str, str]] = []

		max_item_chars = 50

		for name in names:

			summary = None

			if ',' in name:
				name, summary = name.split(',')
				name = name.strip().split()[0]
				summary = summary.strip()

			display_name = name

			if name.startswith('~'):
				name = name[1:]
				display_name = name.split('.')[-1]

			try:
				real_name, obj, parent, modname = self.import_by_name(name, prefixes=prefixes)
			except ImportError:
				logger.warning(__("autosummary: failed to import %s"), name, location=self.get_source_info())
				continue

			self.bridge.result = StringList()  # initialize for each documenter
			full_name = real_name
			if not isinstance(obj, ModuleType):
				# give explicitly separated module name, so that members
				# of inner classes can be documented
				full_name = modname + "::" + full_name[len(modname) + 1:]
			# NB. using full_name here is important, since Documenters
			#     handle module prefixes slightly differently
			documenter = self.create_documenter(self.env.app, obj, parent, full_name)
			if not documenter.parse_name():
				logger.warning(__("failed to parse name %s"), real_name, location=self.get_source_info())
				items.append((display_name, '', '', real_name))
				continue
			if not documenter.import_object():
				logger.warning(__("failed to import object %s"), real_name, location=self.get_source_info())
				items.append((display_name, '', '', real_name))
				continue
			if documenter.options.members and not documenter.check_module():
				continue

			# try to also get a source code analyzer for attribute docs
			try:
				documenter.analyzer = ModuleAnalyzer.for_module(documenter.get_real_modname())
				# parse right now, to get PycodeErrors on parsing (results will
				# be cached anyway)
				documenter.analyzer.find_attr_docs()
			except PycodeError as err:
				logger.debug("[autodoc] module analyzer failed: %s", err)
				# no source file -- e.g. for builtin and C modules
				documenter.analyzer = None

			# -- Grab the signature

			try:
				sig = documenter.format_signature(show_annotation=False)
			except TypeError:
				# the documenter does not support ``show_annotation`` option
				sig = documenter.format_signature()

			if not sig:
				sig = ''
			else:
				max_chars = max(10, max_item_chars - len(display_name))
				sig = mangle_signature(sig, max_chars=max_chars)

			# -- Grab the summary

			documenter.add_content(None)

			if summary is None:
				summary = extract_summary(self.bridge.result.data[:], self.state.document)

			items.append((display_name, sig, summary, real_name))

		return items

	def run(self) -> List[Node]:
		self.bridge = DocumenterBridge(self.env, self.state.document.reporter, Options(), self.lineno, self.state)

		names = [x.strip() for x in self.content if x.strip() and re.search(r'^[~a-zA-Z_]', x.strip()[0])]

		items = self.get_items(names)
		nodes = self.get_table(items)

		if "caption" in self.options:
			logger.warning(__("A captioned autosummary requires :toctree: option. ignored."), location=nodes[-1])

		return nodes


class AutoUnitDirective(SphinxDirective):
	required_arguments = 1

	def run(self) -> List[nodes.Node]:
		content = [f".. autoclass:: {self.arguments[0]}", "    :no-autosummary:"]

		content_node = nodes.paragraph(rawsource='\n'.join(content))
		self.state.nested_parse(StringList(content), self.content_offset, content_node)
		return content_node.children


def setup(app: Sphinx):
	app.connect("build-finished", replace_emoji)
	app.connect("build-finished", latex.replace_unknown_unicode, priority=550)

	app.add_autodocumenter(TemporaryDirectorySubclassDocumenter)

	app.add_role("inline-code", InlineRole())
	app.add_directive("autounit", AutoUnitDirective)
	app.add_directive("autosummary2", Autosummary, override=True)


class SysStdout:

	def __repr__(self) -> str:
		return "sys.stdout"


class SysStderr:

	def __repr__(self) -> str:
		return "sys.stderr"


default_preprocessors.append((lambda x: x is sys.stdout, lambda d: SysStdout()))
default_preprocessors.append((lambda x: x is sys.stderr, lambda d: SysStderr()))
