# stdlib
import json
import re
import sys

# 3rd party
from coincidence.selectors import not_windows, only_windows
from faker import Faker
from faker.providers import bank, company, internet, phone_number, python

# this package
from domdf_python_tools.terminal import Echo, br, clear, interrupt, overtype

fake = Faker()
fake.add_provider(internet)
fake.add_provider(bank)
fake.add_provider(company)
fake.add_provider(phone_number)
fake.add_provider(python)


def test_br(capsys):
	br()

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ['', '']

	br()
	print("foo")

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ['', "foo", '']

	print("foo")
	br()
	print("bar")

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ["foo", '', "bar", '']


@only_windows(reason="Different test used for POSIX")
def test_interrupt_windows(capsys):
	interrupt()

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ["(Press Ctrl-C to quit at any time)", '']


@not_windows(reason="Different test used for Windows")
def test_interrupt_posix(capsys):
	interrupt()

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ["(Press Ctrl-D to quit at any time)", '']


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
	stdout = captured.out.split('\n')
	assert stdout == ["\u001bc"]

	print("Hello World!")
	clear()

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ["Hello World!", "\u001bc"]


def test_overtype(capsys):
	print("Waiting...", end='')
	overtype("foo", "bar")
	sys.stdout.flush()

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ["Waiting...\rfoo bar"]

	print("Waiting...", end='')
	overtype("foo", "bar", sep='')
	sys.stdout.flush()

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ["Waiting...\rfoobar"]

	print("Waiting...", end='')
	overtype("foo", "bar", sep='-', end='\n')
	sys.stdout.flush()

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ["Waiting...\rfoo-bar", '']

	sys.stderr.write("Waiting...")
	overtype("foo", "bar", file=sys.stderr)
	sys.stdout.flush()

	captured = capsys.readouterr()
	stderr = captured.err.split('\n')
	assert stderr == ["Waiting...\rfoo bar"]


def test_echo(capsys):
	with Echo():
		abc = "a variable"
		var = 1234

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')

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
	stdout = captured.out.split('\n')

	assert stdout[0] == "  {{'address': '{}',".format(address.replace('\n', "\\n"))
	assert stdout[1] == f"   'alive': {alive},"
	assert stdout[2] == f"   'employer': '{employer}',"
	assert stdout[3] == f"   'iban': '{iban}',"
	assert stdout[4] == f"   'ip_address': '{ip_address}',"
	assert stdout[5] == f"   'name': '{name}',"
	assert stdout[6] == f"   'telephone': '{telephone}',"
	assert stdout[7].startswith("   'z_other': {")
	assert stdout[7].endswith(',')
	for line in range(8, 13, 1):
		assert re.match(r"^\s*'.*':.*[,}]$", stdout[line])
	assert stdout[-2].endswith('}')
	assert stdout[-1] == ''
