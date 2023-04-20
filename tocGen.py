"""
Copyright (C) 2023 nojasm
A small tool by me for quickly generating a table of content for a markdown file.
"""


import sys
import pyperclip

file = sys.argv[-1]
args = sys.argv[:-1]

if "-h" in sys.argv or "--help" in sys.argv:
	print("Generate table of contents for markdown files.")
	print("Usage: tocGen.py (options) <file.md>")
	print("Where options are:")
	print("  -c			Copies output directly to clipboard")


def genLink(title):
	title = title.replace(" ", "-")
	title = title.lower()
	return title

output = ""
with open(file) as mdFile:
	for line in mdFile.read().split("\n"):
		if line.strip() == "": continue

		if line.startswith("# "):
			title = line[2:]
			output += "- [" + title + "](#" + genLink(title) + ")\n"
		elif line.startswith("## "):
			title = line[3:]
			output += "\t- [" + title + "](#" + genLink(title) + ")\n"
		elif line.startswith("### "):
			title = line[4:]
			output += "\t\t- [" + title + "](#" + genLink(title) + ")\n"


print("-" * 25)
print(output)
print("-" * 25)

if "-c" in args:
	pyperclip.copy(output)
	print("Copied to clipboard.")
