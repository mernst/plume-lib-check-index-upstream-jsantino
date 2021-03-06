#!/usr/bin/python

# This script reformats each file supplied on the command line according
# to the Google Java style (by calling out to the google-java-format program),
# but with improvements to the formatting of annotations in comments.

import os
import re
import sys
import tempfile
import filecmp
import subprocess
import urllib

debug = False

script_dir = os.path.dirname(os.path.abspath(__file__))
# Rather than calling out to the shell, it would be better to
# call directly in Python.
fixup_py = os.path.join(script_dir, "fixup-google-java-format.py")

gjf_jar_name = "google-java-format-1.0-all-deps.jar"
# Set gjf_jar_path
if os.path.isfile(os.path.join(script_dir, gjf_jar_name)):
    gjf_jar_path = os.path.join(script_dir, gjf_jar_name)
elif os.path.isfile(os.path.join(os.path.dirname(script_dir), "lib", gjf_jar_name)):
    gjf_jar_path = os.path.join(os.path.dirname(script_dir), "lib", gjf_jar_name)
else:
    gjf_jar_path = os.path.join(script_dir, gjf_jar_name)
    urllib.urlretrieve("https://github.com/google/google-java-format/releases/download/google-java-format-1.0/google-java-format-1.0-all-deps.jar", gjf_jar_path)

if not os.path.isfile(fixup_py):
    urllib.urlretrieve("https://raw.githubusercontent.com/mernst/plume-lib/master/bin/fixup-google-java-format.py", fixup_py)

if debug:
    print("script_dir:", script_dir)
    print("fixup_py: ", fixup_py)
    print("gjf_jar_path: ", gjf_jar_path)

files = sys.argv[1:]
if len(files) == 0:
    print("run-google-java-format.py expects 1 or more filenames as arguments")
    sys.exit(1)

result = subprocess.call(["java", "-jar", gjf_jar_path, "--replace", "--sort-imports=also"] + files)
if result != 0:
    sys.exit(result)
if files == ["--help"]:
    sys.exit(0)
result = subprocess.call([fixup_py] + files)
if result != 0:
    sys.exit(result)


###########################################################################
### end of script
###

# If you reformat your codebase, then that may be disruptive to people who
# have changes in their own branches/clones/forks.  (But, once you settle
# on consistent formatting, that will never be a problem again.)

# Here are some notes about a possible way to deal with upstream
# reformatting, which have not yet been tested by fire:

# For the person doing the reformatting:
#  * Tag the commit before the whitespace change as "before reformatting".
#  * Run "ant reformat" or the equivalent command.
#  * Run a tool that seaches the diffs for hunks that are *shorter* than
#    they were before.  These are possibly places where an if/for/while whose
#    body was a single statement that has gotten sucked up onto the if/for/while
#    loop.  Or, just run a tool that searches the diffs for if/for/while with
#    body on the same line.  Add curly braces to get the body back on its own
#    line. 
#  * Tag the commit that does the whitespace change as "reformatting".
# 
# For a client to merge the massive upstream changes:
#  * Merge in the commit before the reformatting into your branch.
#  * Merge in the reformatting commit, preferring all your own changes.
#  * Run "ant reformat" or the equivalent command.
#  * Commit your changes.
