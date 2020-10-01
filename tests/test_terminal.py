# stdlib
import json
import os
import re
import sys

# 3rd party
import pytest
from faker import Faker  # type: ignore
from faker.providers import bank, company, internet, phone_number, python  # type: ignore

# this package
from domdf_python_tools import terminal_colours
from domdf_python_tools.terminal import Echo, br, clear, interrupt, overtype
from domdf_python_tools.testing import not_windows, only_windows

fake = Faker()
fake.add_provider(internet)
fake.add_provider(bank)
fake.add_provider(company)
fake.add_provider(phone_number)
fake.add_provider(python)


def test_br(capsys):
	br()

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout == ['', '']

	br()
	print("foo")

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout == ['', "foo", '']

	print("foo")
	br()
	print("bar")

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout == ["foo", '', "bar", '']


@only_windows(reason="Different test used for POSIX")
def test_interrupt_windows(capsys):
	interrupt()

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout == ["(Press Ctrl-C to quit at any time.)", '']


@not_windows(reason="Different test used for Windows")
def test_interrupt_posix(capsys):
	interrupt()

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout == ["(Press Ctrl-D to quit at any time.)", '']


# @only_windows(reason="Different test used for POSIX")
# def test_clear_windows(capsys):
# 	clear()
#
# 	captured = capsys.readouterr()
# 	stdout = captured.out.split("\n")
# 	assert stdout == ['(Press Ctrl-C to quit at any time.)', '']
#


@not_windows(reason="Different test used for Windows")
def test_clear_posix(capsys):
	clear()

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout == ["\033c"]

	print("Hello World!")
	clear()

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout == ["Hello World!", "\033c"]


def test_overtype(capsys):
	print("Waiting...", end='')
	overtype("foo", "bar")
	sys.stdout.flush()

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout == ["Waiting...\rfoo bar"]

	print("Waiting...", end='')
	overtype("foo", "bar", sep='')
	sys.stdout.flush()

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout == ["Waiting...\rfoobar"]

	print("Waiting...", end='')
	overtype("foo", "bar", sep='-', end="\n")
	sys.stdout.flush()

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout == ["Waiting...\rfoo-bar", '']

	sys.stderr.write("Waiting...")
	overtype("foo", "bar", file=sys.stderr)
	sys.stdout.flush()

	captured = capsys.readouterr()
	stderr = captured.err.split("\n")
	assert stderr == ["Waiting...\rfoo bar"]


def test_echo(capsys):
	with Echo():
		abc = "a variable"
		var = 1234

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")

	data = {
			"abc": "a variable",
			"var": 1234,
			}
	dictionary = json.dumps(data).replace('"', "'")
	assert stdout == [f"  {dictionary}", '']

	# def test_echo_pprint(capsys):

	# Lots of variables, which should be pretty printed
	with Echo():
		name = fake.name()
		address = fake.address()
		ip_address = fake.ipv4_private()
		iban = fake.iban()
		employer = fake.company()
		telephone = fake.phone_number()
		alive = fake.pybool()
		z_other = fake.pydict()

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")

	assert stdout[0] == "  {{'address': '{}',".format(address.replace("\n", "\\n"))
	assert stdout[1] == f"   'alive': {alive},"
	assert stdout[2] == f"   'employer': '{employer}',"
	assert stdout[3] == f"   'iban': '{iban}',"
	assert stdout[4] == f"   'ip_address': '{ip_address}',"
	assert stdout[5] == f"   'name': '{name}',"
	assert stdout[6] == f"   'telephone': '{telephone}',"
	assert stdout[7].startswith("   'z_other': {")
	assert stdout[7].endswith(",")
	for line in range(8, 13, 1):
		assert re.match(r"^\s*'.*':.*[,}]$", stdout[line])
	assert stdout[-2].endswith("}")
	assert stdout[-1] == ''


def test_terminal_colours_constants():
	assert terminal_colours.CSI == "\033["
	assert terminal_colours.OSC == "\033]"
	assert terminal_colours.BEL == "\a"


def test_terminal_colours_stacks():
	assert terminal_colours.fore_stack == [terminal_colours.Fore.RESET]
	assert terminal_colours.back_stack == [terminal_colours.Back.RESET]
	assert terminal_colours.style_stack == [terminal_colours.Style.NORMAL]


def test_terminal_colours_functions():
	assert terminal_colours.set_title("Foo") == "\033]2;Foo\a"

	assert terminal_colours.clear_screen() == "\033[2J"
	assert terminal_colours.clear_screen(1) == "\033[1J"

	assert terminal_colours.clear_line() == "\033[2K"
	assert terminal_colours.clear_line(1) == "\033[1K"


def test_ansi_cursor():
	assert terminal_colours.Cursor.UP() == "\033[1A"
	assert terminal_colours.Cursor.UP(1) == "\033[1A"
	assert terminal_colours.Cursor.UP(2) == "\033[2A"
	assert terminal_colours.Cursor.UP(3) == "\033[3A"

	assert terminal_colours.Cursor.DOWN() == "\033[1B"
	assert terminal_colours.Cursor.DOWN(1) == "\033[1B"
	assert terminal_colours.Cursor.DOWN(2) == "\033[2B"
	assert terminal_colours.Cursor.DOWN(3) == "\033[3B"

	assert terminal_colours.Cursor.FORWARD() == "\033[1C"
	assert terminal_colours.Cursor.FORWARD(1) == "\033[1C"
	assert terminal_colours.Cursor.FORWARD(2) == "\033[2C"
	assert terminal_colours.Cursor.FORWARD(3) == "\033[3C"

	assert terminal_colours.Cursor.BACK() == "\033[1D"
	assert terminal_colours.Cursor.BACK(1) == "\033[1D"
	assert terminal_colours.Cursor.BACK(2) == "\033[2D"
	assert terminal_colours.Cursor.BACK(3) == "\033[3D"

	assert terminal_colours.Cursor.POS() == "\033[1;1H"
	assert terminal_colours.Cursor.POS(1) == "\033[1;1H"
	assert terminal_colours.Cursor.POS(2) == "\033[1;2H"
	assert terminal_colours.Cursor.POS(3) == "\033[1;3H"
	assert terminal_colours.Cursor.POS(y=1) == "\033[1;1H"
	assert terminal_colours.Cursor.POS(y=2) == "\033[2;1H"
	assert terminal_colours.Cursor.POS(y=3) == "\033[3;1H"
	assert terminal_colours.Cursor.POS(x=1) == "\033[1;1H"
	assert terminal_colours.Cursor.POS(x=2) == "\033[1;2H"
	assert terminal_colours.Cursor.POS(x=3) == "\033[1;3H"
	assert terminal_colours.Cursor.POS(1, 1) == "\033[1;1H"
	assert terminal_colours.Cursor.POS(2, 2) == "\033[2;2H"
	assert terminal_colours.Cursor.POS(3, 3) == "\033[3;3H"
	assert terminal_colours.Cursor.POS(x=2, y=3) == "\033[3;2H"
