"""
Wikibot main file.
Version: 1.0.0

Copyright (c) 2023-present ElBe Development (under ElBe-Plaq's github profile).

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the 'Software'),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

###########
# IMPORTS #
###########

import argparse

from modules import newsletter  # pylint: disable=E0401

#############
# CONSTANTS #
#############

VERSION = "1.0.0"

########
# MAIN #
########

parser = argparse.ArgumentParser(
    prog="wikibot",
    description="Does stuff",
    epilog="(C) Copyright by ElBe Development 2023.",
)
parser.add_argument("-v", "--version", action="version", version=f"wikibot v{VERSION}")
parser.add_argument(
    "--newsletter", action="store_true", help="Activates the newsletter module"
)
args = parser.parse_args()

if __name__ == "__main__":
    if args.newsletter:
        newsletter.send_newsletter(newsletter.subscribers())
