"""
Wikibot discussion header module.
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

import re
from typing import List, Optional

import pywikibot
import pywikibot.textlib

from config import CONFIG, TRANSLATIONS
from module import Module


############################
# DISCUSSION HEADER MODULE #
############################


class DiscussionHeader(Module):
    """Discussion header module class.

    Base:
        Module: Module base class for easier access of configuration values.
    """

    def __init__(
        self, language: str = CONFIG["language"], wiki: str = CONFIG["wiki"]
    ) -> None:
        """Discussion header module initializer.

        Args:
            language (str, optional): Language version of the wiki to use. Defaults to config
                                      value `language`.
            wiki (str, optional): Wiki to use. Defaults to config value `wiki`.

        Returns:
            None
        """

        self.sections: Optional[List[str]] = None

        super().__init__(language, wiki)

    def get_sections(self, page_name: Optional[str] = None) -> List[str]:
        """Returns the sections on the given page.

        Args:
            page_name (str): Page name to get sections from. Defaults to config value `headerPage`.

        Returns:
            List[str]: List containing the stripped section headings.
        """

        if page_name is None:
            page_name: str = self.config["discussionPage"]

        page: pywikibot.Page = pywikibot.Page(self.site, page_name)
        self.sections: List[str] = []

        for section in pywikibot.textlib.extract_sections(
            page.text, self.site
        ).sections:
            heading = section.heading
            heading = re.sub(r"\[\[.*\|", "", heading)
            heading = heading.replace("]]", "")
            self.sections.append(heading)

        return self.sections

    def replace_header(
        self, sections: Optional[List[str]] = None, page_name: Optional[str] = None
    ) -> None:
        """_summary_

        Args:
            sections (Optional[List[str]], optional): _description_. Defaults to None.
            page_name (Optional[str], optional): _description_. Defaults to None.
        """

        if sections is None:
            if not self.sections:
                raise ValueError("`sections` must not be empty.")

            sections: List[str] = self.sections

        if page_name is None:
            page_name: str = self.config["headerPage"]

        page = pywikibot.Page(self.site, self.config["headerPage"])
        formatted_sections: str = "&nbsp;&bull;&nbsp;\n".join(
            [
                self.config["sectionFormat"]
                % {
                    "link": self.config["discussionPage"] + "#" + section,
                    "sectionName": section,
                }
                for section in sections
            ]
        )

        page.text = self.config["headerFormat"] % {"sections": formatted_sections}
        page.text = page.text.replace("<!-- DOUBLE QUOTE -->", '"')
        page.text = page.text.replace("<!-- PERCENT -->", "%")

        page.save(
            TRANSLATIONS["editMessagePrefix"] + self.translations["pageEdited"],
            botflag=True,
            asynchronous=True,
            quiet=True,
        )
