# HEADER

###########
# IMPORTS #
###########

import json
from typing import Any, Dict, Final


#########
# UTILS #
#########

with open("wikibot/config.json", encoding="utf-8") as config_file:
    CONFIG: Final[Dict[str, Any]] = json.load(config_file)

TRANSLATIONS: Final[Dict[str, Any]] = CONFIG["translations"][CONFIG["language"]]
MODULES: Final[Dict[str, Any]] = CONFIG["modules"]
