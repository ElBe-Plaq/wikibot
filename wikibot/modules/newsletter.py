"""
Wikibot newsletter module.
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

from typing import List, Optional

import pywikibot

from config import CONFIG, TRANSLATIONS
from module import Module


#####################
# NEWSLETTER MODULE #
#####################


class Newsletter(Module):
    """Newsletter module class.

    Base:
        Module: Module base class for easier access of configuration values.
    """

    def __init__(
        self, language: str = CONFIG["language"], wiki: str = CONFIG["wiki"]
    ) -> None:
        """Newsletter module initializer.

        Args:
            language (str, optional): Language version of the wiki to use. Defaults to config value `language`.
            wiki (str, optional): Wiki to use. Defaults to config value `wiki`.

        Returns:
            None
        """

        self.subscriber_list: Optional[List[pywikibot.Page]] = None

        super().__init__(language, wiki)

    def subscribers(
        self,
        subscriber_list_page_name: Optional[str] = None,
        subscriber_list_splitter: Optional[str] = None,
    ) -> List[pywikibot.Page]:
        """Gets a list of newsletter subscribers.

        Args:
            subscriber_list_page_name (str): Page name containing the list of subscribers. See
                                             formatting rules in the documentation. Defaults to
                                             config value `subscriber list`.
            subscriber_list_splitter (str): String used to split the list of subscribers from the
                                            header. Defaults to config value `subscriber splitter`.

        Returns:
            List[pywikibot.Page]: List of subscriber pages.
        """

        if subscriber_list_page_name is None:
            subscriber_list_page_name: str = self.config["subscriberList"]

        if subscriber_list_splitter is None:
            subscriber_list_splitter: str = self.config["subscriberSplitter"]

        page: pywikibot.Page = pywikibot.Page(self.site, subscriber_list_page_name)

        self.subscriber_list: List[pywikibot.Page] = [
            pywikibot.Page(
                self.site, user.replace("# [[", "").replace("]]", "")
            )  # TODO (ElBe): Make configurable
            for user in page.text.split(subscriber_list_splitter)[1].splitlines()[:-2]
        ]

        return self.subscriber_list

    def send_newsletter(
        self,
        subscriber_list: Optional[List[pywikibot.Page]] = None,
        newsletter_page_name: Optional[str] = None,
    ) -> None:
        """Sends the newsletter to the given subscribers.

        Args:
            subscriber_list (List[pywikibot.Page]): List of subscribers. Pages must be editable by
                                                    the bot. Defaults to `self.subscriber_list`
            newsletter_page_name (str): Page name of the newsletter. Defaults to config value
                                        `newsletter template`.

        Returns:
            None
        """

        if subscriber_list is None:
            if not self.subscriber_list:
                raise ValueError("`subscriber_list` must not be empty.")

            subscriber_list: List[pywikibot.Page] = self.subscriber_list

        if newsletter_page_name is None:
            newsletter_page_name: str = self.config["newsletterTemplate"]

        for subscriber in subscriber_list:
            if not subscriber.botMayEdit():
                raise PermissionError(f"Bot can not edit page {subscriber.title()}.")

            if not subscriber.exists():
                raise ValueError(f"Subscriber {subscriber.title()} does not exist.")

            subscriber.text += (
                subscriber.text + "\n\n{{subst:%s}}" % newsletter_page_name
            )  # pylint: disable=C0209
            subscriber.save(
                TRANSLATIONS["editMessagePrefix"]
                + self.translations["pageEdited"] % { "newsletter": newsletter_page_name },
                botflag=True,
                asynchronous=True,
                quiet=True,
            )
