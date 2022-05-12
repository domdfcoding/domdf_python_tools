==================================
:mod:`~domdf_python_tools.bases`
==================================

.. autosummary-widths:: 5/16

.. automodule:: domdf_python_tools.bases
	:autosummary-members:
	:no-members:

Type Variables
------------------

.. autotypevar:: domdf_python_tools.bases._F
.. autotypevar:: domdf_python_tools.bases._LU
.. autotypevar:: domdf_python_tools.bases._S

.. raw:: latex

	\begin{multicols}{2}

.. autotypevar:: domdf_python_tools.bases._T
.. autotypevar:: domdf_python_tools.bases._V

.. raw:: latex

	\end{multicols}


Dictable
---------

.. autoclass:: domdf_python_tools.bases.Dictable
	:inherited-members:
	:special-members:


UserList
---------

.. autoclass:: domdf_python_tools.bases.UserList
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

This avoids any potential issues with :github:repo:`mypy <python/mypy>`.

.. autoclass:: domdf_python_tools.bases.NamedList
	:no-autosummary:
	:exclude-members: __repr__,__str__

.. autofunction:: domdf_python_tools.bases.namedlist


UserFloat
------------

.. autoclass:: domdf_python_tools.bases.UserFloat
	:inherited-members:
	:special-members:
	:exclude-members: __ceil__,__floor__,conjugate,imag,real

.. latex:clearpage::

Lineup
---------

.. autoclass:: domdf_python_tools.bases.Lineup
