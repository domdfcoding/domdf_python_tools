# stdlib
import random

# 3rd party
import pytest

# this package
from domdf_python_tools.words import get_random_word, get_words_list


@pytest.mark.parametrize(
		"seed, expected_values",
		[
				(1, ["element", "rebound", "stop", "underground", "buyer"]),
				(5, ["vacations", "tail", "maui", "features", "bundle"]),
				(100, ["stats", "seafood", "creativity", "outdoors", "sacred"]),
				(250, ["arranged", "volumes", "korea", "basename", "islands"]),
				(500, ["tuning", "knowledgestorm", "backing", "motivation", "calculated"]),
				]
		)
def test_get_random_word(seed, expected_values):
	random.seed(seed)

	for i in range(5):
		assert get_random_word() == expected_values.pop(0)


def test_get_words_list():
	assert isinstance(get_words_list(), list)
	assert isinstance(get_words_list()[0], str)

	assert isinstance(get_words_list(3), list)
	assert isinstance(get_words_list(3)[0], str)

	assert isinstance(get_words_list(17), list)
	assert isinstance(get_words_list(17)[0], str)

	assert isinstance(get_words_list(17000), list)
	assert get_words_list(17000) == []

	assert isinstance(get_words_list(min_length=3), list)
	assert isinstance(get_words_list(min_length=3)[0], str)

	assert isinstance(get_words_list(min_length=17), list)
	assert isinstance(get_words_list(min_length=17)[0], str)

	assert isinstance(get_words_list(min_length=17000), list)
	assert get_words_list(min_length=17000) == []

	assert isinstance(get_words_list(max_length=3), list)
	assert isinstance(get_words_list(max_length=3)[0], str)

	assert isinstance(get_words_list(max_length=17), list)
	assert isinstance(get_words_list(max_length=17)[0], str)

	assert isinstance(get_words_list(max_length=17000), list)
	assert isinstance(get_words_list(max_length=17000)[0], str)

	assert isinstance(get_words_list(min_length=3, max_length=17), list)
	assert isinstance(get_words_list(min_length=3, max_length=17)[0], str)

	assert isinstance(get_words_list(min_length=3, max_length=17000), list)
	assert isinstance(get_words_list(min_length=3, max_length=17000)[0], str)
