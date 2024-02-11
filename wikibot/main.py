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

import pywikibot

from config import CONFIG
from modules import newsletter as newsletter_module
from modules import discussion_header as discussion_header_module


#############
# CONSTANTS #
#############

VERSION = "1.1.0"


########
# MAIN #
########

parser = argparse.ArgumentParser(
    prog="wikibot",
    description="Wikibot is a simple mediawiki bot currently supporting newsletters and discussion headers. You can use it like a module to implement your own features.",
    epilog="(C) Copyright by ElBe Development 2023.",
    add_help=False,
)
parser.add_argument(
    "-h",
    "--help",
    action="help",
    default=argparse.SUPPRESS,
    help="Show this help message and exit.",
)
parser.add_argument(
    "-v",
    "--version",
    action="version",
    version=f"wikibot v{VERSION}",
    help="Show program's version number and exit.",
)
parser.add_argument(
    "--newsletter", action="store_true", help="Activates the newsletter module"
)
parser.add_argument(
    "--discussion-header",
    action="store_true",
    help="Activates the discussion header module",
)
args = parser.parse_args()

if __name__ == "__main__":
    try:
        site = pywikibot.Site(CONFIG["language"], CONFIG["site"])
        run_page = pywikibot.Page(site, f"User:{pywikibot._config.usernames[CONFIG['wiki']][CONFIG['language']]}/Run")
        
        if run_page.text.strip().lower() != "true":
            raise PermissionError(f"The bot was disabled on the whole wiki by [[User:{run_page.lastNonBotUser()}]]")
        
        if args.newsletter:
            newsletter = newsletter_module.Newsletter()
            newsletter.subscribers()
            newsletter.send_newsletter()
        if args.discussion_header:
            discussion_header = discussion_header_module.DiscussionHeader()
            discussion_header.get_sections()
            discussion_header.replace_header()
    except pywikibot.exceptions.UnknownFamilyError:
        print(
            f"Error: The wiki set in `config.json` ({CONFIG['wiki']}) is not supported."
        )
    except pywikibot.exceptions.UnknownSiteError:
        print(
            f"Error: The language version set in `config.json` ({CONFIG['language']}) was not found in wiki {CONFIG['wiki']}."
        )
