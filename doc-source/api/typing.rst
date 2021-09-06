=================================
:mod:`~domdf_python_tools.typing`
=================================

Various type annotation aids.

.. module:: domdf_python_tools.typing

Type Hints
------------

.. autosummary2::

	~domdf_python_tools.typing.PathLike
	~domdf_python_tools.typing.PathType
	~domdf_python_tools.typing.AnyNumber
	~domdf_python_tools.typing.WrapperDescriptorType, The type of methods of some built-in data types and base classes.
	~domdf_python_tools.typing.MethodWrapperType, The type of *bound* methods of some built-in data types and base classes.
	~domdf_python_tools.typing.MethodDescriptorType, The type of methods of some built-in data types.
	~domdf_python_tools.typing.ClassMethodDescriptorType, The type of *unbound* class methods of some built-in data types.

.. autogenericalias:: PathLike
.. autotypevar:: PathType
.. autogenericalias:: AnyNumber


.. data:: WrapperDescriptorType

	The type of methods of some built-in data types and base classes, such as
	:meth:`object.__init__` or :meth:`object.__lt__`.

	.. versionadded:: 0.8.0


.. data:: MethodWrapperType

	The type of *bound* methods of some built-in data types and base classes.
	For example, it is the type of :code:`object().__str__`.

	.. versionadded:: 0.8.0


.. data:: MethodDescriptorType

	The type of methods of some built-in data types, such as :meth:`str.join`.

	.. versionadded:: 0.8.0


.. data:: ClassMethodDescriptorType

	The type of *unbound* class methods of some built-in data types, such as
	``dict.__dict__['fromkeys']``.

	.. versionadded:: 0.8.0


Protocols
------------

.. autosummary::

	~domdf_python_tools.typing.JsonLibrary
	~domdf_python_tools.typing.HasHead
	~domdf_python_tools.typing.String
	~domdf_python_tools.typing.FrameOrSeries
	~domdf_python_tools.typing.SupportsIndex
	~domdf_python_tools.typing.SupportsLessThan
	~domdf_python_tools.typing.SupportsLessEqual
	~domdf_python_tools.typing.SupportsGreaterThan
	~domdf_python_tools.typing.SupportsGreaterEqual

.. autoprotocol:: JsonLibrary
.. autoprotocol:: HasHead
.. autoprotocol:: String
.. autoprotocol:: FrameOrSeries
.. autoprotocol:: SupportsIndex
.. autoprotocol:: SupportsLessThan
.. autoprotocol:: SupportsLessEqual
.. autoprotocol:: SupportsGreaterThan
.. autoprotocol:: SupportsGreaterEqual


Utility Functions
---------------------

.. autofunction:: check_membership
