# The config.json file

The `config.json` file contains configuration for not only the bot's modules but also the bot in general and the translations.

| Name           | Type       | Default                            | Description                                                                                                                                             |
| :------------- | :--------- | :--------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `wiki`         | String     | `wikipedia`                        | Wiki the bot should be used on. Has to be one of the [supported wikis](supported_wikis.md). Currently custom wikis are not supported.                   |
| `language`     | String     | `en`                               | Language for both the bot's translation and the language version of the wiki to use. has to be one of the [supported langauges](supported_languages.md) |
| `modules`      | Dictionary | empty                              | See [`modules.md`](modules.md).                                                                                                                         |
| `translations` | Dictionary | See [translations](#translations). | Translations for different texts.                                                                                                                       |

## Translations

The `translations` dictionary contains dictionaries of langauges. This may look something like this:

```json

"translations": {
    "en": {
        "editMessagePrefix": "Bot: ",
        "MODULE NAME": {
            "CONFIGURATION": "Hello World!"
        }
    }
}

```

| Name                | Type   | Default | Description                   |
| :------------------ | :----- | :------ | :---------------------------- |
| `editMessagePrefix` | String | `Bot: ` | Prefix for the edit messages. |

See [`modules.md`](modules.md) for a list of modules and a link to their respective configuration options.
