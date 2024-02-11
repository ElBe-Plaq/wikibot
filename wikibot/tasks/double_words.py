import re

import pywikibot
import pywikibot.pagegenerators

def main():
    pattern = re.compile(r"(?P<template>\{\{[Gg]nis.+\}\}) \(englisch\)")
    def change_content(page: pywikibot.Page) -> None:
        try:
            page = page.getRedirectTarget()
        except Exception:
            pass
        
        if re.search(pattern, page.text):
            page.text = re.sub(pattern, lambda m: str(m.group("template")), page.text)
    
            page.save("Bot: [[Wikipedia:Bots/Anfragen#Wortdoppelungen entfernen|Wortdopplung]] entfernt", botflag=True)
    
    site = pywikibot.Site("de", "wikipedia")

    # page = pywikibot.Page(site, "Benutzer:ElBe Bot/Spielwiese/Wortdopplungen entfernen")
    
    for page in [x for x in pywikibot.pagegenerators.SearchPageGenerator("insource:/\{\{[Gg]nis.+\}\} \(englisch\)/", 27, [0], site)]:
        change_content(page)
