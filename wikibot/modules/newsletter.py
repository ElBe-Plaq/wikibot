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

from typing import List

import pywikibot

from config import CONFIG, TRANSLATIONS, MODULES


###################
# GET SUBSCRIBERS #
###################


def subscribers(
    subscriber_list: str = MODULES["newsletter"]["subscriber list"],
    subscriber_list_splitter: str = MODULES["newsletter"]["subscriber splitter"],
    language: str = CONFIG["language"],
    wiki: str = CONFIG["wiki"],
) -> List[pywikibot.Page]:
    """Gets a list of newsletter subscribers.

    Args:
        subscriber_list (str): Page name containing the list of subscribers. See formatting rules
                               in the documentation. Defaults to config value `subscriber list`.  # TODO (ElBe): Add docs
        subscriber_list_splitter (str): String used to split the list of subscribers from the
                                        header. Defaults to config value `subscriber splitter`.
        language (str, optional): Language of the wiki to use. Defaults to config value `language`.
        wiki (str, optional): Wiki type to use. Defaults to config value `wiki`.

    Returns:
        List[pywikibot.Page]: List of subscriber pages.
    """

    site = pywikibot.Site(language, wiki)
    page = pywikibot.Page(site, subscriber_list)
    userlist = page.text.split(subscriber_list_splitter)[1]

    return [
        pywikibot.Page(site, user.replace("# [[", "").replace("]]", ""))
        for user in userlist.split("\n")[:-2]
    ]


###################
# SEND NEWSLETTER #
###################


def send_newsletter(
    subscriber_list: List[pywikibot.Page],
    newsletter_page: str = MODULES["newsletter"]["newsletter template"],
) -> None:
    """Sends the newsletter to the given subscribers.

    Args:
        subscriber_list (List[pywikibot.Page]): List of subscribers. Pages must be editable by the bot.
        newsletter_page (str): Page of the newsletter. Defaults to config value `newsletter template`.

    Returns:
        None
    """

    for subscriber in subscriber_list:
        if not subscriber.botMayEdit():
            raise PermissionError(f"Bot can not edit page {subscriber.title()}.")

        if not subscriber.exists():
            raise ValueError(f"Subscriber {subscriber.title()} does not exist.")

        subscriber.text = (
            subscriber.text + "\n\n{{subst:%s}}" % newsletter_page
        )  # pylint: disable=C0209
        subscriber.save(
            CONFIG["edit message prefix"]
            + TRANSLATIONS["newsletter"]["page edited"] % newsletter_page,
            botflag=True,
            asynchronous=True,
            quiet=True,
        )
