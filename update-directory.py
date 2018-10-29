"""
update-directory.py

The purpose of this script is to generate a PDF file containing all of the
problems for certain topics in order to facilitate content creation.

This script generates the JSON file `src/practice/practice0.json`. You can then
compile the PDF file with `make practice n=0`.

Usage:

    python3 update-directory.py

        This generates a JSON file containing every problem in the repository.
        Be warned: the generated PDF file will be quite long.

    python3 update-directory.py rsa counting combinatorial

        This generates a JSON file containing only the problems for `rsa`,
        `counting`, and `combinatorial`. You can specify as many directories as
        you want.
"""


import glob
import json
import os
import sys


directories = [
    "asymptoticnotation/",
    "divideandconquer/",
]


if len(sys.argv) > 1:
    directories = [d + "/" for d in sys.argv[1:]]
os.chdir("src/problems/")
list_of_problems = []
for d in directories:
    files = [f.replace(".tex", "") for f in glob.glob(d + "*.tex")]
    list_of_problems.extend(files)
practice_json = {"questions": list_of_problems, "title": ""}
os.chdir("../practice/")
with open("practice0.json", "w") as f:
    json.dump(practice_json, f, indent=2, sort_keys=True)
