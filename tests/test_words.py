# stdlib
import decimal
import pathlib
import random
import string

# 3rd party
import pytest

# this package
from domdf_python_tools import words
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
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
	assert DOUBLESTRUCK_LETTERS.get("-", "Default") == "Default"


def test_alpha_sort():
	alphabet = f"_{string.ascii_uppercase}{string.ascii_lowercase}0123456789"

	assert alpha_sort(["_hello", "apple", "world"], alphabet) == ["_hello", "apple", "world"]
	assert alpha_sort(["apple", "_hello", "world"], alphabet) == ["_hello", "apple", "world"]
	assert alpha_sort(["apple", "_hello", "world"], alphabet, reverse=True) == ["world", "apple", "_hello"]

	with pytest.raises(ValueError, match="The character '☃' was not found in the alphabet."):
		alpha_sort(["apple", "_hello", "world", "☃"], alphabet)

	assert alpha_sort(["apple", "_hello", "world", "☃"], alphabet + "☃") == ["_hello", "apple", "world", "☃"]


@pytest.mark.parametrize(
		"value, expects",
		[
				(12345, "12345"),
				(123.45, "123.45"),
				([123.45], "[123.45]"),
				({123.45}, "{123.45}"),
				((123.45, ), "(123.45,)"),
				(None, ''),
				(pathlib.Path('.'), '.'),
				(PathPlus('.'), '.'),
				(StringList(["Hello", "World"]), "Hello\nWorld"),
				(decimal.Decimal("1234"), "1234"),
				]
		)
def test_as_text(value, expects):
	assert words.as_text(value) == expects


@pytest.mark.parametrize(
		"args, kwargs, expects",
		[
				(([], ), {}, ''),
				(((), ), {}, ''),
				((["bob"], ), {}, "bob"),
				((["bob", "alice"], ), {}, "bob and alice"),
				((["bob", "alice", "fred"], ), {}, "bob, alice and fred"),
				((("bob", ), ), {}, "bob"),
				((("bob", "alice"), ), {}, "bob and alice"),
				((("bob", "alice", "fred"), ), {}, "bob, alice and fred"),
				((("bob", ), ), {"delimiter": ';'}, "bob"),
				((("bob", "alice"), ), {"delimiter": ';'}, "bob and alice"),
				((("bob", "alice", "fred"), ), {"delimiter": ';'}, "bob; alice and fred"),
				((["bob"], ), {"use_repr": True}, "'bob'"),
				((["bob", "alice"], ), {"use_repr": True}, "'bob' and 'alice'"),
				((["bob", "alice", "fred"], ), {"use_repr": True}, "'bob', 'alice' and 'fred'"),
				((("bob", ), ), {"use_repr": True}, "'bob'"),
				((("bob", "alice"), ), {"use_repr": True}, "'bob' and 'alice'"),
				((("bob", "alice", "fred"), ), {"use_repr": True}, "'bob', 'alice' and 'fred'"),
				((["bob"], ), {"use_repr": True, "oxford": True}, "'bob'"),
				((["bob", "alice"], ), {"use_repr": True, "oxford": True}, "'bob' and 'alice'"),
				((["bob", "alice", "fred"], ), {"use_repr": True, "oxford": True}, "'bob', 'alice', and 'fred'"),
				((["bob", "alice", "fred"], ), {"use_repr": True, "oxford": True, "delimiter": ';'},
					"'bob'; 'alice'; and 'fred'"),
				((["bob", "alice", "fred"], ), {"use_repr": True, "oxford": True, "connective": 'or'},
					"'bob', 'alice', or 'fred'"),
				((("bob", ), ), {"use_repr": True, "oxford": True}, "'bob'"),
				((("bob", "alice"), ), {"use_repr": True, "oxford": True}, "'bob' and 'alice'"),
				((("bob", "alice", "fred"), ), {"use_repr": True, "oxford": True}, "'bob', 'alice', and 'fred'"),
				]
		)
def test_word_join(args, kwargs, expects):
	assert words.word_join(*args, **kwargs) == expects
