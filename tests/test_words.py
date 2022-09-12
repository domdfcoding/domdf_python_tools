# stdlib
import decimal
import pathlib
import random
import string
from typing import List

# 3rd party
import pytest

# this package
from domdf_python_tools import words
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.words import (
		DOUBLESTRUCK_LETTERS,
		Plural,
		PluralPhrase,
		alpha_sort,
		get_random_word,
		get_words_list,
		truncate_string
		)


@pytest.mark.parametrize(
		"seed, expected_values",
		[
				(1, ["element", "rebound", "stop", "underground", "buyer"]),
				(5, ["vacations", "tail", "maui", "features", "bundle"]),
				(100, ["stats", "seafood", "creativity", "outdoors", "sacred"]),
				(250, ["arranged", "volumes", "korea", "basename", "islands"]),
				(500, ["tuning", "knowledgestorm", "backing", "motivation", "calculated"]),
				],
		)
def test_get_random_word(seed: int, expected_values: List[str]):
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
	assert DOUBLESTRUCK_LETTERS['A'] == '𝔸'
	assert DOUBLESTRUCK_LETTERS.get('A') == '𝔸'

	assert DOUBLESTRUCK_LETTERS['-'] == '-'
	assert DOUBLESTRUCK_LETTERS.get('-') == '-'
	assert DOUBLESTRUCK_LETTERS.get('-', "Default") == "Default"


def test_alpha_sort():
	alphabet = f"_{string.ascii_uppercase}{string.ascii_lowercase}0123456789"

	assert alpha_sort(["_hello", "apple", "world"], alphabet) == ["_hello", "apple", "world"]
	assert alpha_sort(["apple", "_hello", "world"], alphabet) == ["_hello", "apple", "world"]
	assert alpha_sort(["apple", "_hello", "world"], alphabet, reverse=True) == ["world", "apple", "_hello"]

	with pytest.raises(ValueError, match="The character '☃' was not found in the alphabet."):
		alpha_sort(["apple", "_hello", "world", '☃'], alphabet)

	assert alpha_sort(["apple", "_hello", "world", '☃'], alphabet + '☃') == ["_hello", "apple", "world", '☃']


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
				],
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
				((["bob", "alice", "fred"], ), {"use_repr": True, "oxford": True, "connective": "or"},
					"'bob', 'alice', or 'fred'"),
				((["bob", "alice"], ), {"connective": "or"}, "bob or alice"),
				((("bob", ), ), {"use_repr": True, "oxford": True}, "'bob'"),
				((("bob", "alice"), ), {"use_repr": True, "oxford": True}, "'bob' and 'alice'"),
				((("bob", "alice", "fred"), ), {"use_repr": True, "oxford": True}, "'bob', 'alice', and 'fred'"),
				],
		)
def test_word_join(args, kwargs, expects):
	assert words.word_join(*args, **kwargs) == expects


def test_plural():
	cow = Plural("cow", "cows")
	glass = Plural("glass", "glasses")

	n = 1
	assert f"The farmer has {n} {cow(n)}." == "The farmer has 1 cow."
	assert f"The bar has {n} {glass(n)}." == "The bar has 1 glass."

	n = 2
	assert f"The farmer has {n} {cow(n)}." == "The farmer has 2 cows."
	assert f"The bar has {n} {glass(n)}." == "The bar has 2 glasses."

	n = 3
	assert f"The farmer has {n} {cow(n)}." == "The farmer has 3 cows."
	assert f"The bar has {n} {glass(n)}." == "The bar has 3 glasses."

	assert repr(cow) == "Plural('cow', 'cows')"
	assert repr(glass) == "Plural('glass', 'glasses')"


def test_pluralphrase():
	phrase1 = PluralPhrase("The proposed {} {} to ...", (Plural("change", "changes"), Plural("is", "are")))
	phrase2 = PluralPhrase("The farmer has {n} {0}.", (Plural("cow", "cows"), ))
	phrase3 = PluralPhrase("The proposed {1} {0} to ...", (Plural("is", "are"), Plural("change", "changes")))
	phrase4 = PluralPhrase(
			"The farmer has {n} {0}. The {0} {1} brown.", (Plural("cow", "cows"), Plural("is", "are"))
			)
	n = 1
	assert phrase1(n) == "The proposed change is to ..."
	assert phrase2(n) == "The farmer has 1 cow."
	assert phrase3(n) == "The proposed change is to ..."
	assert phrase4(n) == "The farmer has 1 cow. The cow is brown."

	n = 2
	assert phrase1(n) == "The proposed changes are to ..."
	assert phrase2(n) == "The farmer has 2 cows."
	assert phrase3(n) == "The proposed changes are to ..."
	assert phrase4(n) == "The farmer has 2 cows. The cows are brown."

	n = 3
	assert phrase1(n) == "The proposed changes are to ..."
	assert phrase2(n) == "The farmer has 3 cows."
	assert phrase3(n) == "The proposed changes are to ..."
	assert phrase4(n) == "The farmer has 3 cows. The cows are brown."

	phrase1_repr = "PluralPhrase(template='The proposed {} {} to ...', words=(Plural('change', 'changes'), Plural('is', 'are')))"
	assert repr(phrase1) == phrase1_repr
	assert repr(phrase2) == "PluralPhrase(template='The farmer has {n} {0}.', words=(Plural('cow', 'cows'),))"
	phrase3_repr = "PluralPhrase(template='The proposed {1} {0} to ...', words=(Plural('is', 'are'), Plural('change', 'changes')))"
	assert repr(phrase3) == phrase3_repr
	phrase4_repr = "PluralPhrase(template='The farmer has {n} {0}. The {0} {1} brown.', words=(Plural('cow', 'cows'), Plural('is', 'are')))"
	assert repr(phrase4) == phrase4_repr


def test_truncate():
	message = "hello world this is a very long sentance with no point"
	assert truncate_string(message, 20) == "hello world this ..."
	assert truncate_string(message, 30) == "hello world this is a very ..."
	assert truncate_string(message, 30, '…') == "hello world this is a very lo…"
	assert truncate_string(message, 200, '…') == message
