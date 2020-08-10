# 3rd party
import pytest

# this package
from domdf_python_tools.secrets import Secret
from domdf_python_tools.words import get_words_list


@pytest.mark.parametrize("value", get_words_list())
def test_secret(value):
	the_secret = Secret(value)
	assert isinstance(the_secret, str)
	assert isinstance(the_secret.value, str)
	assert the_secret.value == value
	assert the_secret == value
	assert str(the_secret) == "<SECRET>"
	assert repr(the_secret) == "'<SECRET>'"
	assert str([the_secret]) == "['<SECRET>']"
	assert str((the_secret, )) == "('<SECRET>',)"
	assert str({the_secret}) == "{'<SECRET>'}"
	assert str({"token": the_secret}) == "{'token': '<SECRET>'}"
	assert repr([the_secret]) == "['<SECRET>']"
	assert repr((the_secret, )) == "('<SECRET>',)"
	assert repr({the_secret}) == "{'<SECRET>'}"
	assert repr({"token": the_secret}) == "{'token': '<SECRET>'}"
	assert hash(the_secret) == hash(value)
