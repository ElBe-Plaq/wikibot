"""
Wikibot configuration parser.
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

import json
from typing import Any, Dict, Final


#########
# UTILS #
#########

try:
    with open("wikibot/config.json", encoding="utf-8") as config_file:
        CONFIG: Final[Dict[str, Any]] = json.load(config_file)
except FileNotFoundError:
    with open("config.json", encoding="utf-8") as config_file:
        CONFIG: Final[Dict[str, Any]] = json.load(config_file)
try:
    TRANSLATIONS: Final[Dict[str, Any]] = CONFIG["translations"][CONFIG["language"]]
except KeyError:
    print(
        f"Error: The requested language ({CONFIG['language']}) was not found in the `translations` dictionary."
    )

MODULES: Final[Dict[str, Any]] = CONFIG["modules"]
