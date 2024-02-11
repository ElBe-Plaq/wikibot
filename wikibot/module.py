"""
Wikibot module class.
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

from typing import Any, Dict

import pywikibot

from config import CONFIG, MODULES


################
# MODULE CLASS #
################


class Module:
    """Base Module class for all modules to inherit from."""

    def __init__(
        self, language: str = CONFIG["language"], wiki: str = CONFIG["wiki"]
    ) -> None:
        """Module initializer.

        Args:
            language (str, optional): _description_. Defaults to CONFIG["language"].
            wiki (str, optional): _description_. Defaults to CONFIG["wiki"].

        Returns (as self values):
            self.config: Module configuration from the `config.json` file.
            self.site: Pywikibot site object for all edits to use one consistent site.
            self.translations: Translations dictionary for the current language and the current
                               module.
        """

        name = type(self).__name__[0].lower() + type(self).__name__[1:]
        self.config: Dict[str, Any] = MODULES[name]
        self.site: pywikibot.BaseSite = pywikibot.Site(language, wiki)
        self.translations: Dict[str, str] = CONFIG["translations"][language][name]
