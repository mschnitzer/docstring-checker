# imports
import sys
import json
from collections import OrderedDict

def func_reader(content):
	"""
	Parses the content of a file
	:param str content: Content of a file
	:return list: [functions_with_docstrings,functions_without_docstrings]
	"""

	# variables
	currfunc = None
	search_for_docstring = False
	with_docstring = []
	without_docstring = []

	for line in content.split("\n"):
		# remove whitespaces from the line
		line = line.rstrip()
		line = line.lstrip()

		# split the line by whitespaces
		parts = line.split(" ")

		if not search_for_docstring:
			# search for 'def' at the beginning of the line
			if parts[0] == 'def':
				# the list 'parts' must have at least 2 elements (def and the name of the function)
				if len(parts) >= 2:
					# save the name of the current function
					currfunc = parts[1]

					# if there is a '(' after the function name (for the parameter list) just delete
					# that shit
					idx = currfunc.find("(")
					if idx != -1:
						currfunc = currfunc[:idx]

					# jump into the 'search_for_docstring' state
					search_for_docstring = True
		else:
			# check if this line is a docstring
			# possibilities: """ or '''
			if parts[0][:3] == '"""' or parts[0][:3] == "'''":
				with_docstring.append(currfunc)
			else:
				without_docstring.append(currfunc)

			# reset our variables -> we'll search for a new function
			currfunc = None
			search_for_docstring = False

	return [with_docstring, without_docstring]

if __name__ == '__main__':
	# check for arguments
	if len(sys.argv) < 2:
		print("Usage: ./docstring-checker.py [Files]")
		sys.exit(1)
	else:
		# collect all items in an OrderedDict
		out = OrderedDict()

		# iter through all files
		for i in sys.argv[1:]:
			try:
				with open(i, 'r') as f:
					# get the content of the file
					content = f.read()

					# search for all function and its DocStrings
					with_docstring, without_docstring = func_reader(content)

					# append an entry to our OrderedDict if the found at least
					# one function with a DocString or one without a DocString
					if with_docstring or with_docstring:
						out[i] = OrderedDict()
						out[i]['with_docstring'] = with_docstring
						out[i]['without_docstring'] = without_docstring
			except (IsADirectoryError, FileNotFoundError, PermissionError):
				pass

		# print the output as JSON
		print(json.dumps(out))