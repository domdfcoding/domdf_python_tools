# stdlib
import random
import string

# 3rd party
import pytest

# this package
from domdf_python_tools.words import DOUBLESTRUCK_LETTERS, alpha_sort, get_random_word, get_words_list


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


def test_font():
	assert DOUBLESTRUCK_LETTERS("Hello World") == "ℍ𝕖𝕝𝕝𝕠 𝕎𝕠𝕣𝕝𝕕"
	assert DOUBLESTRUCK_LETTERS["A"] == "𝔸"
	assert DOUBLESTRUCK_LETTERS.get("A") == "𝔸"

	assert DOUBLESTRUCK_LETTERS["-"] == "-"
	assert DOUBLESTRUCK_LETTERS.get("-") == '-'
	assert DOUBLESTRUCK_LETTERS.get("-", "Default") == 'Default'


def test_alpha_sort():
	alphabet = f"_{string.ascii_uppercase}{string.ascii_lowercase}0123456789"

	assert alpha_sort(["_hello", "apple", "world"], alphabet) == ["_hello", "apple", "world"]
	assert alpha_sort(["apple", "_hello", "world"], alphabet) == ["_hello", "apple", "world"]
	assert alpha_sort(["apple", "_hello", "world"], alphabet, reverse=True) == ["world", "apple", "_hello"]

	with pytest.raises(ValueError, match="The character '☃' was not found in the alphabet."):
		alpha_sort(["apple", "_hello", "world", "☃"], alphabet)

	assert alpha_sort(["apple", "_hello", "world", "☃"], alphabet + "☃") == ["_hello", "apple", "world", "☃"]
