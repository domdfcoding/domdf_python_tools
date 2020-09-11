=================================
:mod:`domdf_python_tools.typing`
=================================

.. automodule:: domdf_python_tools.typing
	:autosummary-sections: Functions ;; Classes

.. data:: WrapperDescriptorType

	The type of methods of some built-in data types and base classes such as
	:meth:`object.__init__` or :meth:`object.__lt__`.

	.. versionadded:: 0.8.0

.. data:: MethodWrapperType

	The type of *bound* methods of some built-in data types and base classes.
	For example it is the type of :code:`object().__str__`.

	.. versionadded:: 0.8.0


.. data:: MethodDescriptorType

	The type of methods of some built-in data types such as :meth:`str.join`.

	.. versionadded:: 0.8.0


.. data:: ClassMethodDescriptorType

	The type of *unbound* class methods of some built-in data types such as
	``dict.__dict__['fromkeys']``.

	.. versionadded:: 0.8.0
