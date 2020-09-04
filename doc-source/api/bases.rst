==================================
:mod:`domdf_python_tools.bases`
==================================

.. automodule:: domdf_python_tools.bases
	:no-members:

Dictable
---------

.. autoclass:: domdf_python_tools.bases.Dictable
	:inherited-members:
	:special-members:


NamedList
----------

Both :class:`~.NamedList` and :func:`~.namedlist` can be used to create a named list.

:func:`~.namedlist` can be used as follows:

.. code-block:: python

	>>> ShoppingList = namedlist("ShoppingList")
	>>> shopping_list = ShoppingList(["egg and bacon", "egg sausage and bacon", "egg and spam", "egg bacon and spam"])
	>>>

If you wish to create a subclass with additional features it is recommended to subclass
from :class:`NamedList` rather than from :func:`~.namedlist`. For example, do this:


.. code-block:: python

	>>> class ShoppingList(NamedList):
	...     pass
	>>>

and not this:

.. code-block:: python

	>>> class ShoppingList(namedlist())
	...     pass
	>>>

This avoids any potential issues with `mypy <http://mypy-lang.org/>`_

.. autoclass:: domdf_python_tools.bases.NamedList
	:inherited-members:
	:special-members:

.. autofunction:: domdf_python_tools.bases.namedlist
